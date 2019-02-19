# main文件中的代码
### 初始化
***
程序首先实例化`Game`类，接下来是一系列初始化工作

    # If loading an existing neural network, copy the config file to root
    if initialise.INITIAL_RUN_NUMBER != None:
        copyfile(run_archive_folder  + env.name + '/run' + str(initialise.INITIAL_RUN_NUMBER).zfill(4) + '/config.py', './config.py')


如注释所说，如果在`initialise`中定义了`run_number`，则从`run_archive_folder`中加载相应的配置。下面的`memory`类和`model`类实例化时也是如此

这里需要注意的是，我搜索了整个框架代码，没有发现在程序里设置`run_archive_folder`的代码，说明这个路径包括`initialse`文件都是需要我们自己手动设置的。具体来说，在某次训练结束后，我们若需要保存训练成果，根据代码我们可以看出，要手工将整个run文件夹存在`run_archive_folder`文件夹，并按照自己设置的版本号改名，如：`run0001`。

加载游戏记忆、过往模型参数不再赘述。

    #copy the config file to the run folder
    copyfile('./config.py', run_folder + 'config.py')
    plot_model(current_NN.model, to_file=run_folder + 'models/model.png', show_shapes = True)
这里首先复制当前`config`文件到`run`文件夹中，目的应是方便手动保存。之后是输出当前神经网络的框图，这里是一个坑点，keras中的`plot_model`方法可能会报错，keras官方文档中也有[提示](https://keras-cn.readthedocs.io/en/latest/other/visualization/)：

> 【Tips】依赖 pydot-ng 和 graphviz，若出现错误，用命令行输入pip install pydot-ng & brew install graphviz

但是有些人即便使用`pip`命令安装成功，错误依旧存在，类似于

    Failed to import pydot. You must install pydot and graphviz for……

可参考[这里](https://stackoverflow.com/questions/36886711/keras-runtimeerror-failed-to-import-pydot-after-installing-graphviz-and-pyd?r=SearchResults)解决

    current_player = Agent('current_player', env.state_size, env.action_size, config.MCTS_SIMS, config.CPUCT, current_NN)
    best_player = Agent('best_player', env.state_size, env.action_size, config.MCTS_SIMS, config.CPUCT, best_NN)

这两行代码实例化了两个`Agent`类，在这里两者是完全一样的，其实都是历史最优网络，但在后面，`current_player`会利用自我博弈的数据进行训练学习，然后和`best_player`比拼。接下来进入自我博弈和模型训练部分。
****
### 自我对弈
***
    ######## SELF PLAY ########
    _, memory, _, _ = playMatches(best_player, best_player, config.EPISODES, lg.logger_main, turns_until_tau0 = config.TURNS_UNTIL_TAU0, memory = memory)
    print('\n')
    memory.clear_stmemory()
开始自我对弈，对弈中的每轮游戏状态，都会存储在`memory`类的`stmemory`列表中，`stmemory`即短时游戏记忆，只存储每一轮的所有游戏状态，一次博弈后，数据会转入`ltmemory`，`memory`会执行`clear_stmemory()`方法清空短时记忆

### replay方法训练模型
****
    if len(memory.ltmemory) >= config.MEMORY_SIZE:

        ######## RETRAINING ########
        print('RETRAINING...')
        current_player.replay(memory.ltmemory)
        print('')
        pickle.dump( memory, open( run_folder + "memory/memory" + str(iteration).zfill(4) + ".p", "wb" ) 
        ......
    else:
        print('MEMORY SIZE: ' + str(len(memory.ltmemory)))

如果`ltmemory`中存储的数据量大于`config`中设置的记忆量，说明存储够了足够的数据，可以开始训练了，`Agent`类的`replay`方法，传入游戏记忆，“重玩”一遍来训练`current_player`。实例化的`pickle`类将`memory`序列化后保存起来。如果数据量不够则继续自我博弈

        lg.logger_memory.info('====================')
        lg.logger_memory.info('NEW MEMORIES')
        lg.logger_memory.info('====================')
        
        memory_samp = random.sample(memory.ltmemory, min(1000, len(memory.ltmemory)))
        
        for s in memory_samp:
            current_value, current_probs, _ = current_player.get_preds(s['state'])
            best_value, best_probs, _ = best_player.get_preds(s['state'])

            lg.logger_memory.info('MCTS VALUE FOR %s: %f', s['playerTurn'], s['value'])
            ......
            model.convertToModelInput(s['state']))

            s['state'].render(lg.logger_memory)
输出memory日志

### 训练后新模型与历史最优模型pk
***
        ######## TOURNAMENT ########
        scores, _, points, sp_scores = playMatches(best_player, current_player, config.EVAL_EPISODES, lg.logger_tourney, turns_until_tau0 = 0, memory = None)
        ......(省略若干print)
            
        if scores['current_player'] > scores['best_player'] * config.SCORING_THRESHOLD:
            best_player_version = best_player_version + 1
            best_NN.model.set_weights(current_NN.model.get_weights())
        best_NN.write(env.name, best_player_version)
            
`Tournament`即`current_player`和b`est_player`进行pk，`congfig`中可以配置pk的次数和`current_player`的获胜阈值，如果训练后的新模型超过阈值分数，则替换掉`best_player`成为历史最优并保存。这里`write`方法原代码在`if`内部，我考虑到自己弱鸡笔记本性能太弱，于是放在if外面，即便没获胜也可以把训练模型保存下来（事实证明，刚开始的几个版本一般是能胜过的）。


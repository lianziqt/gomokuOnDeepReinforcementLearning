# funcs文件的内容
funcs文件实现了两个函数：

- `playMatchesBetweenVersions`：实现两个不同版本模型之间的比赛
- `playMatches`： 实现两个玩家间的比赛，两个玩家既可以实例化`User`类，也可以实例化`Agent`类

## `playMatchesBetweenVersions`函数
***
    if player1version == -1:
        player1 = User('player1', env.state_size, env.action_size)
    else:
        player1_NN = Residual_CNN(config.REG_CONST, config.LEARNING_RATE, env.input_shape,   env.action_size, config.HIDDEN_CNN_LAYERS)

        if player1version > 0:
            player1_network = player1_NN.read(env.name, run_version, player1version)
            player1_NN.model.set_weights(player1_network.get_weights())   
        player1 = Agent('player1', env.state_size, env.action_size, config.MCTS_SIMS, config.CPUCT, player1_NN)
如果`player1version`传入值为-1，则`player1`实例化`User`类，否则载入相应版本的模型参数，实例化`Agent`类。`player2`同理。最后，仍然调用`playMatches`

## `playMatches`函数
***
    env = Game()
    scores = {player1.name:0, "drawn": 0, player2.name:0}
    sp_scores = {'sp':0, "drawn": 0, 'nsp':0}
    points = {player1.name:[], player2.name:[]}
首先是各种初始化，其中`sp_scores`字典分别存储的是：`sp`(start_player)指先手胜利次数,`drawn`指平局次数,`nsp`(non_start_player)指后手胜利次数。

接下来依据传入的EPISODES参数进行多轮对弈：

    if goes_first == 0:
        player1Starts = random.randint(0,1) * 2 - 1
    else:
        player1Starts = goes_first
如果未至定先走方，则随机决定。`goes_fisrt`传入1则代号分配如下：

    players = {1:{"agent": player1, "name":player1.name}
           , -1: {"agent": player2, "name":player2.name}
           }
否则为：

    players = {1:{"agent": player2, "name":player2.name}
            , -1: {"agent": player1, "name":player1.name}
            }
    logger.info(player2.name + ' plays as X')

接下来的循环即为落子过程，知道返回的`done`为1，即游戏结束。

    if turn < turns_until_tau0:
        action, pi, MCTS_value, NN_value = players[state.playerTurn]['agent'].act(state, 1)
    else:
        action, pi, MCTS_value, NN_value = players[state.playerTurn]['agent'].act(state, 0)
游戏过程中，首先调用`agent`类中的`act`方法选择往哪落子。其中，`turn`表示当前这局对弈的回合数，小于阈值则传入`tau`值为1，超过阈值则传入`tau`值为0。`tau`被`act`方法传入`chooseAction`方法来指定不同的落子策略。总的来说，小于阈值的前几回合，`agent`实例会随机选择走法，优先考虑探索值高（被多次搜索）的节点。超过阈值的游戏后期，则必定选择探索度高的节点。

这是个比较稳妥的策略，因为估值高但探索度低的接地，其估值并不可靠。

    if memory != None:
        ####Commit the move to memory
        memory.commit_stmemory(env.identities, state, pi)
    state, value, done, _ = env.step(action)
选择策略后，将走法传入短时游戏记忆并落子，返回新的游戏局面。如果`done`为1，表明游戏结束，需要将短时游戏记忆转入长时游戏记忆，并根据返回值判断赢家进行相应的日志输出。
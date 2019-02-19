
## 简介
[DeepReinforcementLearning](http://link.zhihu.com/?target=https%3A//github.com/AppliedDataSciencePartners/DeepReinforcementLearning)。该项目是作者David Foster基于自己的理解搭建的AlphaZero框架，只要你实现了游戏规则对应的API，可将该框架用于多种双人棋类游戏。我自己也惊叹于AlphaZero学习能力，十分感兴趣，于是找到这个框架，在阅读代码的过程中将自己对代码的理解记录下来，算是个wiki，方便自己以后查阅，也帮助其他和我一样的小白阅读代码。

下文将简单介绍各个文件的作用，每个模块的代码将分章节详细介绍。

### agent.py
agent.py实现了进行游戏的玩家类————Agent，每个玩家都实例化自己的CNN和蒙特卡洛树。
主要有以下两个方法：
* simulate方法模拟蒙特卡洛树的搜索过程；
* act方法多次运行simulate方法，得出在当前局面下应该走哪一步；

### config.py & initialise.py & loggers.py & settings.py
config.py 即框架的配置文件，主要可以设置每轮自我博弈的次数、每次落子时simulateu方法运行的次数、cnn层数以及训练网络时的epoch，学习率等参数

initialise.py 仅仅设置了3个变量，主要是初始化时要用到，分别是CNN模型版本，博弈运行版本和用来训练网络的博弈过程版本，需要手动设置。

settings.py 内设置运行时保存模型文件及log日志的路径，以及手动编码的过去版本的模型文件和运行日志

### funcs.py & utils.py
funcs.py中主要实现了两个函数：
* playMatchesBetweenVersions——即让两个不同训练程度的模型博弈的函数，主要用于比较当前训练版本与历史最强版本孰强孰弱。
* playMatches——实现了两个agent类之间的博弈

## game.py
实现棋类运行规则的API，只要根据目标游戏规则，实现该文件中的各类API，模型即可根据规则在自我博弈中不断学习。主要实现了两个类：
* GameState类表示游戏中的一个状态，根据游戏规则实现了可落子位置、判断输赢等方法，并通过takeAction方法返回执行某个动作后的下一个状态
* Game类中包含当前游戏的各类信息，包括当前游戏状态，棋盘大小，CNN输入格式等。

## model.py & loss.py
实现了训练用的模型类和损失函数
CNN采用 AlphaGo Zero 论文中的神经网络架构，可设置的多个圈基层，接着是一些残留层，然后分解成值端（value head）和策略端（policy head）。
卷积过滤器的深度和数量可以在 config 文件中设置。
Keras 程序库用于搭建神经网络，使用 TensorFlow 后端。

## MCTS.py
它包含节点、边缘和 MCTS 类，它们构成了一个蒙特卡洛搜索树。
MCTS 类包含前面提到的simulate要用到的 moveToLeaf 和 backFill 方法，并且边缘类的实例存储每个可能的move的统计数据。

## memory.py
这是 Memory 类的一个实例，用以存储之前游戏的记忆，该算法会用它们重新训练 current_player 的神经网络。

## main.py

模型运行的主文件，实现了模型、游戏记忆等一系列实例初始化，运行自我博弈和模型训练过程




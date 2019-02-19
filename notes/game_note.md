# game文件中的代码
原文件中的内容均是作者基于`connect4`游戏规则编写的，本文则基于我修改后的五子棋规则（无禁手，就是最基本的五子连珠即胜）来写。

## GameState类
***
GameState类可以实例化当前游戏的一个状态。
### `__init__(self, board, playerTurn)`
init方法初始化了游戏状态的各种属性，需要传入当前棋盘局面和当前玩家

### `_allowedActions(self)`
该方法依据游戏规则，返回可以落子的棋盘坐标

### `_binary(self)`、`_convertStateToId(self)`
`binary`方法中：

    currentplayer_position = np.zeros(len(self.board), dtype=np.int)
    currentplayer_position[self.board==self.playerTurn] = 1
以current_player为例，该变量初始化时为全0的数组，之后将current_player中对应self.playerTurn的位置的值置1。
    other_position = np.zeros(len(self.board), dtype=np.int)
    other_position[self.board==-self.playerTurn] = 1
显而易见，这两句则是将`other_position`中对应另外一位玩家的位置置1。可以看出，`binary`方法分离并以一维数组的形式返回返回两名玩家的落子。

`convertStateToId`方法与`binary`方法类似，不过不再区分当前玩家，并且将棋盘转化成字符串，相当于为当前界面生成一个id。


### `_checkForEndGame(self)`
顾名思义，根据当前游戏规则检查游戏是否结束。显然，五子棋中，出现五子连珠或棋盘下满则游戏结束。这里判断五子连珠的方法是将所有可能连珠的位置全部写进列表里，挨个判断。

### `_getValue(self)`、`_getScore(self)`:
`getValue`方法返回一个三元组表示当前局面的价值（`value`），通过`getScore`方法的返回我们可以看到，三元组的第二个数应该表示本局面对于当前玩家的分数，第三个数表示本局面对于前一个玩家的分数。从`takeAction`方法中可以看出，三元组第一个值仅表示当前局面的价值，有一方赢了即为-1，没赢即为0

### `takeAction(self, action)`
该方法在`Game`类的`step`方法中被调用，传入`Action`参数，即当前玩家落子的坐标。
方法返回落子后的新局面，以及该局面的价值（`value`）和游戏是否结束

### `render(self, logger)`:
在传入的logger中输出当前局面的信息


## Game类
***
### `__init__(self)`、`reset(self)`
`init`方法初始化了各种属性，从名字即可读出各项含义。`reset`方法重置了当前游戏状态和当前玩家。

值得注意的是，为了实现棋类游戏的通用API，游戏状态中将当前局面和棋盘格式分开存储，落子时，坐标是一维的，只有在必要时（如将游戏状态传入神经网络）时，才渲染成张量格式

### `step(self, action)`
    next_state, value, done = self.gameState.takeAction(action)
    self.gameState = next_state
    self.currentPlayer = -self.currentPlayer
    info = None
    return ((next_state, value, done, info))
传入要采取的`action`，即落子的坐标，通过`gameState.takeAction`方法返回落子后的局面，并更换当前玩家

### `identities(self, state, actionValues)`:
由于作者没有注释，起初十分疑惑，在对比阅读了作者提供的connect4和metasquares两个游戏的game文件后才搞懂，由于棋类游戏本身的特性，对当前棋盘旋转90度又是一个新局面，这个方法实际上是利用当前的游戏状态，生成多种游戏状态，丰富训练数据。
- connect4游戏中，棋盘是6*7格式，不对称，所以只实现了镜面反转。
- metasquares游戏棋盘是正方形，故实现了旋转4次，在镜面反转后旋转4次。
五子棋棋盘也是正方形，故实现了和metasquares一样的操作。
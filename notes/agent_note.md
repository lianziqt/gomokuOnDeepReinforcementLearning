# `Agent`文件中的内容

## `User`类
***
该类与 `Agent` 类有所区别，主要是实现了玩家与AI对弈时用的类。只包含几个简单的属性和一个`act`落子方法
#### `act(self, state, tau)`
方法读取玩家输入的落子坐标，将pi数组中的相应位置置1并返回。方法接收的tau参数和返回的另外两个值只是由于要实现和`Agent`类中相同的`act`方法

## `Agent`类
***
### `simulate(self)`
蒙塔卡罗树搜索一次完整的过程包含四个步骤**选择**、**扩展**、**模拟**、**回溯**。
- 由`MCTS`类我们可以知道，`MCTS.moveToLeaf`方法实现了**选择**过程，最终会选择到一个叶节点;
- `evaluateLeaf`方法自然实现了**扩展**和**模拟**两个过程，获得当前页节点的一个价值（value）
- `backFill`方法实现了**回溯**过程

### `get_preds(self, state)`
该方法接收当前局面，并返回神经网络价值端和策略端的结果。具体说来：
    inputToModel = np.array([self.model.`convertToModelInput`(state)])
    preds = self.model.`predict`(inputToModel)
    value_array = preds[0]
    logits_array = preds[1]
    value = value_array[0]
    logits = logits_array[0]
首先由`convertToModelInput`方法将当前局面转换成神经网络可以接受的输入格式，然后由Keras的`predict`方法返回输出结果。

    mask = np.ones(logits.shape,dtype=bool)
    mask[allowed`act`ions] = False
    logits[mask] = -100
    
mask数组相当于一个遮罩，数值类型为布尔值，允许落子处为False，不允许落子为处，从而将`logits`数组中的不允许落子处置为-100。

    #SOFTMAX
    odds = np.exp(logits)
    probs = odds / np.sum(odds) 
然后，手动实现`softmax`激活函数，将策略端输出转换成类概率值，经过mask数组的处理，不允许落子处的值非常小，经过`softmax`后会趋近于0。

### `evaluateLeaf(self, leaf, value, done, breadcrumbs)`
该方法对叶节点实现**扩展**和**模拟**两个过程

    if done == 0:
    ......
    else:
        lg.logger_MCTS.info('GAME VALUE FOR %d: %f', leaf.playerTurn, value)
首先，若传入的参数`done`为1表明该节点以前已经探索过，游戏已经结束，不用再评估。下面是评估过程的代码：

    value, probs, allowedactions = self.get_preds(leaf.state)
    ......
    probs = probs[allowedactions]
评估过程中，首先获得神经网络对当前局面的评估结果和落子策咯（可落子处的概率）。传统的**模拟**过程是在该叶节点拓展一个新节点，执行快速走子策略，并根据结果，给这个新节点评估一个分数，分数的形式通常是该节点的访问总次数（新节点自然为1）和胜利次数（1或者0）。
而此处神经网络取代了这个过程，价值端直接输出该叶节点的value。

    for idx, `act`ion in enumerate(allowed`act`ions):
        newState, _, _ = leaf.state.take`act`ion(`act`ion)
        if newState.id not in self.`MCTS`.tree:
            node = mc.Node(newState)
            self.`MCTS`.addNode(node)
        else:
            node = self.`MCTS`.tree[newState.id]
        newEdge = mc.Edge(leaf, node, probs[idx], `act`ion)
        leaf.edges.append((`act`ion, newEdge))
之后迭代每个可走的步骤，如果这个节点不在蒙特卡洛树中，则将其添加进树中，并向叶节点中添加新的edge。

    return ((value, breadcrumbs))
最后返回对该节点的评估值和选择路径（`breadcrumbs`），供回溯函数使用。

### `buildMCTS(self, state)`
以传入的游戏局面为根节点，创建蒙特卡洛树

### `changeRootMCTS(self, state)`
将蒙特卡洛树的根换为指定局面

### `getAV(self, tau) & choose`act`ion(self, pi, values, tau)`

    for `act`ion, edge in edges:
        pi[`act`ion] = pow(edge.stats['N'], 1/tau) 
        values[`act`ion] = edge.stats['Q']
    pi = pi / (np.sum(pi) * 1.0)
    return pi, values
    #`act`方法调用getAV时传入的tau参数为1

从代码上看，`pi`数组是根节点的各个子节点的探索比例，`values`数组是各个节点的胜率。可以看出，函数返回这些值是供根节点选择路径时使用，这些数据会在`chooseaction`中用到，如下。

    if tau == 0:
        `act`ions = np.argwhere(pi == max(pi))
        `act`ion = random.choice(`act`ions)[0]
    else:
        `act`ion_idx = np.random.multinomial(1, pi)
        `act`ion = np.where(`act`ion_idx==1)[0][0]
可以看出，如果传入的参数`tau`为0，那么将在探索比例最大的几个选择中随机选择一个。否则，则按照`pi`数组中的比例为概率分布，随机选出一个。（`np.random.multinomial`为多项分布随机，具体可以参考[这里](https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.multinomial.html)

### `act(self, state, tau)`
    if self.MCTS == None or state.id not in self.`MCTS`.tree:
        self.build`MCTS`(state)
    else:
        self.changeRoot`MCTS`(state)
如果没建树或当前局面不再现有树中，则重新建树。否则，表明当前局面在树中，那么就将当前局面设为根节点。

    for sim in range(self.MCTSsimulations):
        self.simulate()
按照传入的模拟次数进行蒙特卡洛树搜索。

    pi, values = self.getAV(1)
    `act`ion, value = self.choose`act`ion(pi, values, tau)
    nextState, _, _ = state.takeaction(`act`ion)
搜索结束后，选择子节点，并用`takeaction`方法获取新的局面

    NN_value = -self.get_preds(nextState)[0]
    return (`act`ion, pi, value, NN_value)
给新的局面打分，由于新局面是对手面对的，所以神经网络打分加个负号

###　`replay(self, ltmemory)`

代码逻辑较为清晰，可以看出是从长时游戏记忆中随机选取几盘对模型进行训练。
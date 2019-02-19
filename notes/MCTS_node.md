#MCTS(蒙特卡洛树搜索)文件内容

MCTS的相关知识可以看这一篇[文章](https://zhuanlan.zhihu.com/p/25345778)简要了解

## Node类
***
蒙特卡洛树一个节点表示一个游戏状态，那么自然而然，一个节点的属性当前的游戏状态，状态的id，节点连接的`edge`。`Node`类还实现了一个`isLeaf`方法判断当前节点是否为叶节点（没有edge的点）

## Edge类
***
在了解蒙特卡洛树搜索的过程中，我感觉各类文章里并没出现边这个概念，这里可能是出于编程实现方面的考虑写了这个类。
`edge`对象包含头节点（`inNode`），尾节点（`outNode`），这个边对应的`action`以及`status`。

从`MCTS`类的回溯方法`backFill`里可以看出，`status['N']`表示当前节点探索的总次数，`status['W']`代表所有探索次数中胜出的次数，`status['Q']`则代表胜率。
从MCTS类的实现中可以看出，status中存储的是终止节点的参数



## MCTS类
***
### `__init__(self, root, cpuct)` & `__len__(self)`
初始化了根节点，树字典，树长度

### `moveToLeaf(self)`
MCTS类中的关键方法，从根节点移动到叶子节点。

    breadcrumbs = []
    currentNode = self.root
    done = 0
    value = 0

接下来，只要不是叶节点，就一直循环

    maxQU = -99999
初始化蒙特卡洛树搜索中`selection`环节的节点分数最大值

    if currentNode == self.root:
        epsilon = config.EPSILON
        nu = np.random.dirichlet([config.ALPHA] * len(currentNode.edges))
    else:
        epsilon = 0
        nu = [0] * len(currentNode.edges)
如果当前节点是根节点，则从`config`中读取`epsilon`，若不是根节点，则将`epsilon`置0，这样可以保证后续计算出`maxQU`只是根节点的下一层节点中的`maxQU`

    Nb = 0
    for action, edge in currentNode.edges:
        Nb = Nb + edge.stats['N']
这段代码计算当前节点所有边缘的访问次数，即所有子节点的访问次数，记为`Nb`

    for idx, (action, edge) in enumerate(currentNode.edges):
        U = self.cpuct * \
            ((1-epsilon) * edge.stats['P'] + epsilon * nu[idx] )  * \
            np.sqrt(Nb) / (1 + edge.stats['N'])
        
        Q = edge.stats['Q']
        ......
        if Q + U > maxQU:
            maxQU = Q + U
            simulationAction = action
            simulationEdge = edge
之后继续迭代当前节点所有子节点，计算每个节点的分数`U`，与胜率`Q`相加，选取`QU`最大的节点

        newState, value, done = currentNode.state.takeAction(simulationAction) #the value of the newState from the POV of the new playerTurn

        currentNode = simulationEdge.outNode
        breadcrumbs.append(simulationEdge)
    return currentNode, value, done, breadcrumbs
选择这个节点，采用这个走法，返回心得状态，并将这个子节点替换为当前节点，继续下次循环。这里也可以看出`breadcrumbs`列表中存储的是从根节点到叶节点的路径，用于回溯（面包屑这个名字很形象了）。

### `backFill(self, leaf, value, breadcrumbs)`

    currentPlayer = leaf.state.playerTurn
回溯自然从叶子节点开始

    for edge in breadcrumbs:
        playerTurn = edge.playerTurn
        if playerTurn == currentPlayer:
            direction = 1
        else:
            direction = -1
        edge.stats['N'] = edge.stats['N'] + 1
        edge.stats['W'] = edge.stats['W'] + value * direction
        edge.stats['Q'] = edge.stats['W'] / edge.stats['N']
沿着面包屑中存储的路径信息一路迭代，注意到当前玩家与节点玩家不同时，获胜次数的计算要变成减法。
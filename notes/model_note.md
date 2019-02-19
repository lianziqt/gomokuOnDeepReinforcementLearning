# model文件中的代码
`model`文件中实现了两个类，分别是`Gen_Model`类和`Residual_CNN`类，其中`Residual_CNN`继承自`Gen_Model`类

## Gen_Model类
***
### `__init__`
该类的初始化方法，分别初始化了正则化参数、学习率、输入尺寸和输出尺寸

### `predict`、`fit`、`write`、`read`
四个方法非常直观，直接调用keras的`Model`类的对应方法，实现了模型预测、模型训练、模型参数保存和读取四个功能

### `printWeightAverages(self)`、`viewLayers(self)`
`printWeightAverages`方法首先从`model`的方法中获取网络的所有`layer`，然后迭代输出每一层的权重值和偏置值

`viewLayers`则实现了每一个网络层的可视化

## Residual_CNN类（继承自Gen_Model类）
***
### `__init__`
除了`Gen_Model`类中已经初始化的属性，还初始化了隐藏层的配置（在`config`文件中以字典列表的方式实现）以及神经网络模型实例


### `_build_model(self)`
该方法构建需要的CNN模型

    x = self.conv_layer(main_input, self.hidden_layers[0]['filters'], self.hidden_layers[0]['kernel_size'])

从输入层出来，首先是一层卷积层，参数来自于`config`文件`hidden_layers`的第一组数据

    if len(self.hidden_layers) > 1:
        for h in self.hidden_layers[1:]:
            x = self.residual_layer(x, h['filters'], h['kernel_size'])
从卷积层出来，要经过若干个残差神经网络，参数来自于`config`文件`hidden_layers`的后几组数据

    vh = self.value_head(x)
    h = self.policy_head(x)
    model = Model(inputs=[main_input], outputs=[vh, ph])
经过残差层后，网络直接分裂为价值网络和策咯网络，这也是AlphaZero与之前的Alpha版本一大不同

    model.compile(loss={'value_head': 'mean_squared_error', 'policy_head': softmax_cross_entropy_with_logits},
        optimizer=SGD(lr=self.learning_rate, momentum = config.MOMENTUM),	
        oss_weights={'value_head': 0.5, 'policy_head': 0.5}	
        )
从`compile`函数中可以看出，价值端的损失函数为均方误差，而策略端则是自定义的损失函数，详见loss文件。优化器则为 `sgd`（随机梯度下降）

### `residual_layer(self, input_block, filters, kernel_size)`
该方法实现了一个残差网络块，换句话说，就是将输入部分（`input_block`）经由两层卷积网络和标准化层（`BatchNormalization`）后的输出再与输入相加，然后通过一层`LeakyReLU`激活层输出。

### `value_head` & `policy_head`
- `value_head` 的输出是神经网络对当前局面评分，取代了传统蒙特卡洛树搜索中，使用传统统计学方法对局面进行评分的方法，因此价值端的输出维度为1
- `policy_head` 的输出神经网络针对当前局面给出在各个坐标落子的概率，因此输出维度为2

### `convertToModelInput(self, state)`
容易看出，该方法接受一个游戏状态，并将该状态的binary属性整形为神经网络的输入格式

具体来说，`state`中的`binary`属性是个一维numpy数组，元素有`2*15*15`个，即分离出的两位玩家的落子情况，numpy的`reshape`方法接受3个参数：

    numpy.reshape(a, newshape, order='C')
`a`为待整形数组，`newshape`即目标尺寸，`order`为整形时的读取顺序和向新型数组写入时的顺序，默认为`C`，`C`指的是用类C写的读/索引顺序的元素，横着读，横着写，优先读/写一行。在这里，`reshape`方法将`binary`重整为(2,15,15)格式的数组
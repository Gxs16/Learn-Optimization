'''
@Author: Xinsheng Guo
@Time: 2021年2月16日23:52:17
@File: ANN.py
'''
import pandas as pd
import numpy as np
import scipy.special
from sklearn.model_selection import train_test_split 
class NeuralNetwork:
    '''
    人工神经网络的自写类。\n
    param:\n
    layers: list, 每一层神经元的个数.\n
    learning_rate: float, 学习率.\n
    epoches: int, 训练次数，epoches越大，模型对于训练集拟合效果越好，但是也更容易过拟合；epoches过小会导致欠拟合，或者神经网络各个系数不收敛.
    '''
    def __init__(self, layers: list, learning_rate: float=0.05, epoches: int=1000):
        '''
        param:\n
        layers: list, 每一层神经元的个数.\n
        learning_rate: float, 学习率.\n
        epoches: int, 训练次数，epoches越大，模型对于训练集拟合效果越好，但是也更容易过拟合；epoches过小会导致欠拟合，或者神经网络各个系数不收敛.
        '''
        # 记录每一层神经元的个数
        self.layers = layers
        # 学习率
        self.lr = learning_rate

        # 创建神经元之间的系数矩阵
        self.W = []
        for i in range(len(self.layers)-1):
            self.W.append(np.random.rand(self.layers[i+1], self.layers[i])-0.5)
        # 创建每个神经元的bias向量
        self.b = []
        for j in self.layers[1:]:
            self.b.append(np.random.rand(j, 1)-0.5)

        # 定义激活函数 此处为sigmoid
        self.act_func = lambda x: scipy.special.expit(x)

        # 记录训练次数
        self.epo = epoches

    def _forward_prop(self, X: np.ndarray):
        '''
        正向传播。\n
        param:\n
        X: np.ndarray, 输入的训练数据，n*k的矩阵，n代表数据的个数，k代表输入的维度。\n
        return:\n
        outputs: list, 神经网络每一层的输出值，第0个输出值即为输入的数据。\n
        '''
        # 记录每一层的输出，第0层的输出即为数据集的输入
        outputs = [X]
        result = X.view()

        # 依次计算每一层的输入输出
        for W, b in zip(self.W, self.b):
            result = np.matmul(W, result) + b
            result = self.act_func(result)
            # 将输出添加至list中
            outputs.append(result)
        return outputs

    def _backprop(self, Y: np.ndarray, outputs: list):
        '''
        反向传播\n
        param:\n
        Y: np.ndarray, 输入训练数据所对应的结果，n*m的矩阵，代表n结果的个数，m代表每个结果的维度。\n
        outputs: list, 神经网络每一层的输出值，第0个输出值即为输入的数据。\n
        '''
        # 计算输出层到目标输出的误差
        g = Y - outputs[-1]
        # 反向传播，从后向前依次更新每一层的参数
        for i in range(1, len(outputs)):
            # 获取当前层的输出
            a = outputs[-i]
            # 获取上一层的输出，即当前层的输入
            h = outputs[-i-1]
            # 将误差与激活函数的导数相乘
            g = g*(a)*(1-a)
            # 计算梯度并与学习率相乘，获得W与b的更新量
            b_delta = self.lr*g
            W_delta = self.lr*np.matmul(g, h.T)
            # 计算上一层的误差
            g = np.matmul(self.W[-i].T, g)
            # 更新当前层的参数
            self.b[-i] += b_delta
            self.W[-i] += W_delta

    def train(self, X: np.ndarray, Y: np.ndarray):
        '''
        训练过程。\n
        param:\n
        X: np.ndarray, 训练集的输入，n*k的矩阵，n代表数据的个数，k代表输入的维度。\n
        Y: np.ndarray, 训练集的目标输出，n*m的矩阵，代表n结果的个数，m代表每个结果的维度。\n
        '''
        for i in range(self.epo):
            for x, y in zip(X, Y):
                # 将输入输出都变为二维矩阵
                x = np.array(x, ndmin=2).T
                y = np.array(y, ndmin=2).T
                # 前向传播
                outputs = self._forward_prop(x)
                # 反向传播
                self._backprop(y, outputs)

    def predict(self, X):
        '''
        预测过程。\n
        param:\n
        X: 输入的数据，n*k的矩阵，n代表数据的个数，k代表输入的维度。
        return:
        result: 输出的结果，m*n的矩阵，代表m结果的个数，n代表每个结果的维度。
        '''
        # 对输入进行转置
        result = X.view().T

        # 依次计算每一层的输入输出
        for W, b in zip(self.W, self.b):
            result = np.matmul(W, result) + b
            result = self.act_func(result)
        return result

if __name__=='__main__':
    # 读取数据集
    data = pd.read_csv('Iris.csv')
    # 数据预处理
    data.set_index('Id', inplace=True)
    X = data[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']].values
    Y = pd.get_dummies(data['Species']).values
    X = (X-np.min(X, axis=0))/(np.max(X, axis=0)-np.min(X, axis=0))
    # 切分训练集合测试集
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

    # 定义人工神经网络
    classifier = NeuralNetwork(layers=[4,3], learning_rate=0.1, epoches=500)
    # 训练
    classifier.train(X_train, y_train)

    # 查看测试集准确度
    y_train_predict = classifier.predict(X_train)
    label_predict = np.argmax(y_train_predict, axis=0)
    label_train = np.argmax(y_train.T, axis=0)
    print(label_predict-label_train)

    # 查看测试集准确度
    Y_predict = classifier.predict(X_test)
    label_predict = np.argmax(Y_predict, axis=0)
    label_test = np.argmax(y_test.T, axis=0)
    print(label_predict-label_test)

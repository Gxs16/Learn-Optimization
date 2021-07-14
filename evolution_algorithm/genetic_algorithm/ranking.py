'''
@Author: Xinsheng Guo
@Time: 2021年7月13日17:16:32
@File: ranking.py
@Reference: <https://github.com/guofei9987/scikit-opt>
@Description: Basic Genetic Algorithm template
'''
import numpy as np

__all__ = ['normal', 'linear']

def normal(self):
    # GA select the biggest one, but we want to minimize func, so we put a negative here
    self.FitV = -self.Y


def linear(self):
    '''
    For more details see [Baker1985]_.

    :param self:
    :return:

    .. [Baker1985] Baker J E, "Adaptive selection methods for genetic
    algorithms, 1985.
    '''
    self.FitV = np.argsort(np.argsort(-self.Y))
    return self.FitV

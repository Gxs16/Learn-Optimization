'''
@Author: Xinsheng Guo
@Time: 2021年7月13日17:16:32
@File: ga_real.py
@Reference: <https://github.com/guofei9987/scikit-opt>
@Description: Genetic Algorithm based on real code
'''

import numpy as np
from genetic_algorithm import GeneticAlgorithm

class GaReal(GeneticAlgorithm):
    '''
    基于实数编码的遗传算法
    '''
    def chrom2x(self):
        self.X = self.lb + (self.ub - self.lb) * self.Chrom

    def crtbp(self):
        self.Chrom = np.random.random([self.size_pop, self.n_dim])

if __name__ == '__main__':

    # min f(x1, x2, x3) = x1^2 + (x2-0.05)^2 + (x3-0.5)^2
    # s.t.
    #     x1*x2 >= 1
    #     x1*x2 <= 5
    #     x2 + x3 = 1
    #     0 <= x1 <=2
    #     -10 <= x2 <= 10
    #     -5 <= x3 <= 2

    def demo_func_real(x):
        return x[0] ** 2 + (x[1] - 0.05) ** 2 + (x[2] - 0.5) ** 2

    constraint_eq = [
        lambda x: 1 - x[1] - x[2]
    ]

    constraint_ueq = [
        lambda x: 1 - x[0] * x[1],
        lambda x: x[0] * x[1] - 5
    ]

    ga_real = GaReal(func=demo_func_real, n_dim=3, size_pop=200, max_iter=1000, prob_mut=0.3,
                lb=np.array([-1, -10, -5]), ub=np.array([2, 10, 2]),
                constraint_eq=constraint_eq, constraint_ueq=constraint_ueq
                )

    best_x, best_y = ga_real.run()
    print('best_x:', best_x, '\n', 'best_y:', best_y)

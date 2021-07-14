'''
@Author: Xinsheng Guo
@Time: 2021年7月7日14:36:25
@File: genetic_algorithm.py
@Reference: <https://github.com/guofei9987/scikit-opt>
@Description: Basic Genetic Algorithm template
'''

import types
import sys
from multiprocessing import Pool
from abc import abstractmethod
import numpy as np
import mutation
import crossover
import ranking
import selection

class GeneticAlgorithm:
    def __init__(self, func: types.FunctionType, n_dim: int,
                 lb: np.ndarray, ub: np.ndarray, 
                 parallel: bool=False,
                 ranking_method: str='normal',
                 crossover_method: str='one_point',
                 mutation_method: str='poly',
                 selection_method: str='tournament_faster',
                 size_pop: int=50, max_iter: int=200, prob_mut: float=0.001, prob_cross: float=0.5,
                 constraint_eq: list=[], constraint_ueq: list=[],
                 print_interval: int=10) -> None:
        '''
        param:
        parallel: bool, 是否并行计算，此功能暂时废弃
        ranking_method: ['normal', 'linear']
        crossover_method: ['sbx', 'one_point', 'two_point', 'two_point_bit', 'pmx', 'two_point_prob']
        mutation_method: ['poly', 'normal', 'TSP_1', 'swap', 'reverse']
        selection_method: ['tournament', 'tournament_faster', 'roulette_1', 'roulette_2']
        size_pop: int, 种群个数
        max_iter: int, 最大迭代次数
        prob_mut: float, 发生变异的概率
        prob_cross: float, 发生交叉的概率
        constraint_eq: list, 等号约束
        constraint_ueq: list, 不等号约束
        print_interval: int, 日志打印代数的间隔
        '''
        self.parallel = parallel
        self.func = func
        assert size_pop % 2 == 0, 'size_pop must be even integer'
        self.size_pop = size_pop  # size of population
        self.max_iter = max_iter # the maximum number of iteration
        self.prob_mut = prob_mut  # probability of mutation
        self.prob_cross = prob_cross # probability of crossover
        self.n_dim = n_dim

        self.print_interval = print_interval

        # constraint:
        self.has_constraint = constraint_eq or constraint_ueq
        self.constraint_eq = constraint_eq # a list of equal functions with ceq[i] = 0
        self.constraint_ueq = constraint_ueq  # a list of unequal constraint functions with c[i] <= 0

        self.lb = lb
        self.ub = ub
        self.Chrom = None
        self.X = None  # shape = (size_pop, n_dim)
        self.Y_raw = None  # shape = (size_pop,) , value is f(x)
        self.Y = None  # shape = (size_pop,) , value is f(x) + penalty for constraint
        self.FitV = None  # shape = (size_pop,)

        self.generation_best_X = []
        self.generation_best_Y = []

        self.all_history_Y = []
        self.all_history_FitV = []

        self.best_x, self.best_y = None, None

        try:
            rank = getattr(ranking, ranking_method)
            setattr(self, 'ranking', types.MethodType(rank, self))
        except AttributeError:
            print('ranking_method should be chosen from {method_set}'\
                        .format(method_set=ranking.__all__))
            sys.exit()

        try:
            select = getattr(selection, selection_method)
            setattr(self, 'selection', types.MethodType(select, self))
        except AttributeError:
            print('selection_method should be chosen from {method_set}'\
                        .format(method_set=selection.__all__))
            sys.exit()

        try:
            cross = getattr(crossover, crossover_method)
            setattr(self, 'crossover', types.MethodType(cross, self))
        except AttributeError:
            print('crossover_method should be chosen from {method_set}'\
                        .format(method_set=crossover.__all__))
            sys.exit()

        try:
            mut = getattr(mutation, mutation_method)
            setattr(self, 'mutation', types.MethodType(mut, self))
        except AttributeError:
            print('mutation_method should be chosen from {method_set}'\
                        .format(method_set=mutation.__all__))
            sys.exit()

        self.crtbp()

    def func_transformed(self, x):
        '''
        将目标方程和约束条件合并
        '''
        if not self.has_constraint:
            return self.func(x)
        else:
            penalty_eq = np.sum(np.abs([c_i(x) for c_i in self.constraint_eq]))
            penalty_ueq = np.sum(np.abs([max(0, c_i(x)) for c_i in self.constraint_ueq]))
            return self.func(x) + 1e5 * penalty_eq + 1e5 * penalty_ueq
            
    @abstractmethod
    def chrom2x(self):
        pass

    @abstractmethod
    def crtbp(self):
        pass

    def cal_y(self) -> np.ndarray:
        '''
        计算Y值
        '''
        if self.parallel:
            # TODO 并行设计有问题，此功能暂时废弃
            pool = Pool(8)
            self.Y = np.array(pool.map(self.func_transformed, self.X))
        else:
            self.Y = np.apply_along_axis(self.func_transformed, 1, self.X)

    def run(self, max_iter=None) -> tuple:
        self.max_iter = max_iter or self.max_iter
        for i in range(self.max_iter):
            self.chrom2x()
            self.cal_y()
            self.ranking()
            self.selection()
            self.crossover()
            self.mutation()

            # record the best ones
            generation_best_index = self.FitV.argmax()
            self.generation_best_X.append(self.X[generation_best_index, :])
            self.generation_best_Y.append(self.Y[generation_best_index])
            self.all_history_Y.append(self.Y)
            self.all_history_FitV.append(self.FitV)
            if i%self.print_interval == 0:
                print('当前为第{t}代，当前最好个体适应度为{obj}'.format(t=i, obj=self.FitV[generation_best_index]))

        global_best_index = np.array(self.generation_best_Y).argmin()
        self.best_x = self.generation_best_X[int(global_best_index)]
        self.best_y = self.func(self.best_x)
        return self.best_x, self.best_y
        
'''
@Author: Xinsheng Guo
@Time: 2021年7月7日14:36:25
@File: GeneticAlgorithm.py
@Reference: <https://github.com/guofei9987/scikit-opt>
@Description: Basic Genetic Algorithm template
'''

import types
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
                 crossover_method: str='1point',
                 mutation_method: str='poly',
                 selection_method: str='tournament_faster',
                 size_pop: int=50, max_iter: int=200, prob_mut: float=0.001, prob_cross: float=0.5,
                 constraint_eq=tuple(), constraint_ueq=tuple(),
                 print_interval=10) -> None:
        '''
        param:
        parallel: 是否并行计算
        ranking_method: ['normal', 'linear']
        crossover_method: ['sbx', '1point', '2point', '2point_bit', 'pmx', '2point_prob']
        mutation_method: ['poly', 'normal', 'TSP_1', 'swap', 'reverse']
        selection_method: ['tournament', 'tournament_faster', ]
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
        self.has_constraint = len(constraint_eq) > 0 or len(constraint_ueq) > 0
        self.constraint_eq = list(constraint_eq)  # a list of equal functions with ceq[i] = 0
        self.constraint_ueq = list(constraint_ueq)  # a list of unequal constraint functions with c[i] <= 0

        self.lb = lb
        self.ub = ub
        self.Chrom = None
        self.X = None  # shape = (size_pop, n_dim)
        self.Y_raw = None  # shape = (size_pop,) , value is f(x)
        self.Y = None  # shape = (size_pop,) , value is f(x) + penalty for constraint
        self.FitV = None  # shape = (size_pop,)

        # self.FitV_history = []
        self.generation_best_X = []
        self.generation_best_Y = []

        self.all_history_Y = []
        self.all_history_FitV = []

        self.best_x, self.best_y = None, None

        try:
            rank = getattr(ranking, 'ranking_{method}'.format(method=ranking_method))
            setattr(self, 'ranking', types.MethodType(rank, self))
        except AttributeError:
            print('ranking_method should be chosen from {method_set}'.format(method_set=ranking.__all__))
            raise

        try:
            select = getattr(selection, 'selection_{method}'.format(method=selection_method))
            setattr(self, 'selection', types.MethodType(select, self))
        except AttributeError:
            print('selection_method should be chosen from {method_set}'.format(method_set=selection.__all__))
            raise

        try:
            cross = getattr(crossover, 'crossover_{method}'.format(method=crossover_method))
            setattr(self, 'crossover', types.MethodType(cross, self))
        except AttributeError:
            print('crossover_method should be chosen from {method_set}'.format(method_set=crossover.__all__))
            raise

        try:
            mut = getattr(mutation, 'mutation_{method}'.format(method=mutation_method))
            setattr(self, 'mutation', types.MethodType(mut, self))
        except AttributeError:
            print('mutation_method should be chosen from {method_set}'.format(method_set=mutation.__all__))
            raise

        self.crtbp()

    def func_transformed(self, x):
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
        if self.parallel:
            self.pool = Pool(8)
            self.Y = np.array(self.pool.map(self.func_transformed, self.X))
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
                print('当前为第{t}代，当前最好个体目标函数为{obj}'.format(t=i, obj=self.Y[generation_best_index]))

        global_best_index = np.array(self.generation_best_Y).argmin()
        self.best_x = self.generation_best_X[global_best_index]
        self.best_y = self.func(self.best_x)
        return self.best_x, self.best_y
        
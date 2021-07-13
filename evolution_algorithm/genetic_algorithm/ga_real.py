'''
@Author: Xinsheng Guo
@Time: 2021年7月13日17:16:32
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
from genetic_algorithm import GeneticAlgorithm

class GaReal(GeneticAlgorithm):
    def chrom2x(self):
        self.X = self.lb + (self.ub - self.lb) * self.Chrom

    def crtbp(self):
        self.Chrom = np.random.random([self.size_pop, self.n_dim])

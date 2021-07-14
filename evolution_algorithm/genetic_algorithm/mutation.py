'''
@Author: Xinsheng Guo
@Time: 2021年7月13日17:16:32
@File: mutation.py
@Reference: <https://github.com/guofei9987/scikit-opt>
@Description: Basic Genetic Algorithm template
'''
import numpy as np

__all__=['poly', 'normal', 'TSP_1', 'swap', 'reverse']

def normal(self):
    '''
    mutation of 0/1 type chromosome
    faster than `self.Chrom = (mask + self.Chrom) % 2`
    :param self:
    :return:
    '''
    mask = (np.random.rand(self.size_pop, self.len_chrom) < self.prob_mut)
    self.Chrom ^= mask

def poly(self):
    '''
    Routine for real polynomial mutation of an individual
    '''
    size_pop, n_dim, Chrom= self.size_pop, self.n_dim, self.Chrom
    for i in range(size_pop):
        for j in range(n_dim):
            r = np.random.random()
            if r <= self.prob_mut:
                y = Chrom[i][j]
                r = np.random.random()
                mut_pow = 0.5
                if r <= 0.5:
                    val = 2.0 * r + (1.0 - 2.0 * r) * ((1.0 - y) ** 2.0)
                    deltaq = val ** mut_pow - 1.0
                else:
                    val = 2.0 * (1.0 - r) + 2.0 * (r - 0.5) * (y ** 2.0)
                    deltaq = 1.0 - val ** mut_pow
                y = y + deltaq
                y = min(1, max(y, 0))
                Chrom[i][j] = y
    return Chrom

def TSP_1(self):
    '''
    every gene in every chromosome mutate
    :param self:
    :return:
    '''
    Chrom = self.Chrom
    for i in range(self.size_pop):
        for j in range(self.n_dim):
            if np.random.rand() < self.prob_mut:
                n = np.random.randint(0, self.len_chrom, 1)
                Chrom[i, j], Chrom[i, n] = Chrom[i, n], Chrom[i, j]
    self.Chrom = Chrom


def _swap(individual):
    n1, n2 = np.random.randint(0, individual.shape[0] - 1, 2)
    if n1 >= n2:
        n1, n2 = n2, n1 + 1
    individual[n1], individual[n2] = individual[n2], individual[n1]
    return individual


def _reverse(individual):
    '''
    Reverse n1 to n2
    Also called `2-Opt`: removes two random edges, reconnecting them so they cross
    Karan Bhatia, "Genetic Algorithms and the Traveling Salesman Problem", 1994
    https://pdfs.semanticscholar.org/c5dd/3d8e97202f07f2e337a791c3bf81cd0bbb13.pdf
    '''
    n1, n2 = np.random.randint(0, individual.shape[0] - 1, 2)
    if n1 >= n2:
        n1, n2 = n2, n1 + 1
    individual[n1:n2] = individual[n1:n2][::-1]
    return individual


def transpose(individual):
    # randomly generate n1 < n2 < n3. Notice: not equal
    n1, n2, n3 = sorted(np.random.randint(0, individual.shape[0] - 2, 3))
    n2 += 1
    n3 += 2
    slice1, slice2, slice3, slice4 = individual[0:n1], individual[n1:n2], individual[n2:n3 + 1], individual[n3 + 1:]
    individual = np.concatenate([slice1, slice3, slice2, slice4])
    return individual


def reverse(self):
    '''
    Reverse
    :param self:
    :return:
    '''
    Chrom = self.Chrom
    for i in range(self.size_pop):
        if np.random.rand() < self.prob_mut:
            Chrom[i] = _reverse(Chrom[i])
    self.Chrom = Chrom


def swap(self):
    Chrom = self.Chrom
    for i in range(self.size_pop):
        if np.random.rand() < self.prob_mut:
            Chrom[i] = _swap(Chrom[i])
    self.Chrom = Chrom

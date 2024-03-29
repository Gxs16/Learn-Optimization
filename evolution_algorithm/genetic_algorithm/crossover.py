import numpy as np

__all__ = ['sbx', 'one_point', 'two_point', 'two_point_bit', 'two_point_prob', 'pmx']


def sbx(self):
    '''
    模拟二进制交叉
    '''
    Chrom, size_pop, len_chrom, prob_cross= self.Chrom, self.size_pop, len(self.Chrom[0]), self.FitV, self.prob_cross
    for i in range(0, size_pop, 2):
        if np.random.random() <= prob_cross:
            for j in range(len_chrom):
                y1 = Chrom[i][j]
                y2 = Chrom[i + 1][j]
                r = np.random.random()
                if r <= 0.5:
                    betaq = (2 * r) ** (1.0 / (1 + 1.0))
                else:
                    betaq = (0.5 / (1.0 - r)) ** (1.0 / (1 + 1.0))

                child1 = 0.5 * ((1 + betaq) * y1 + (1 - betaq) * y2)
                child2 = 0.5 * ((1 - betaq) * y1 + (1 + betaq) * y2)

                child1 = min(max(child1, 0), 1)
                child2 = min(max(child2, 0), 1)

                Chrom[i][j] = child1
                Chrom[i + 1][j] = child2
    self.Chrom = Chrom

def one_point(self):
    '''
    单点交叉
    '''
    Chrom, size_pop, len_chrom = self.Chrom, self.size_pop, len(self.Chrom[0])
    for i in range(0, size_pop, 2):
        n = np.random.randint(0, len_chrom)
        # crossover at the point n
        seg1, seg2 = Chrom[i, n:].copy(), Chrom[i + 1, n:].copy()
        Chrom[i, n:], Chrom[i + 1, n:] = seg2, seg1
    self.Chrom = Chrom


def two_point(self):
    '''
    两点交叉
    '''
    Chrom, size_pop, len_chrom = self.Chrom, self.size_pop, len(self.Chrom[0])
    for i in range(0, size_pop, 2):
        n1, n2 = np.random.randint(0, len_chrom, 2)
        if n1 > n2:
            n1, n2 = n2, n1
        # crossover at the points n1 to n2
        seg1, seg2 = Chrom[i, n1:n2].copy(), Chrom[i + 1, n1:n2].copy()
        Chrom[i, n1:n2], Chrom[i + 1, n1:n2] = seg2, seg1
    self.Chrom = Chrom


def two_point_bit(self):
    '''
    3 times faster than `crossover_2point`, but only use for 0/1 type of Chrom
    :param self:
    :return:
    '''
    Chrom, size_pop, len_chrom = self.Chrom, self.size_pop, len(self.Chrom[0])
    half_size_pop = int(size_pop / 2)
    Chrom1, Chrom2 = Chrom[:half_size_pop], Chrom[half_size_pop:]
    mask = np.zeros(shape=(half_size_pop, len_chrom), dtype=int)
    for i in range(half_size_pop):
        n1, n2 = np.random.randint(0, len_chrom, 2)
        if n1 > n2:
            n1, n2 = n2, n1
        mask[i, n1:n2] = 1
    mask2 = (Chrom1 ^ Chrom2) & mask
    Chrom1 ^= mask2
    Chrom2 ^= mask2
    return self.Chrom


def two_point_prob(self, crossover_prob):
    '''
    2 points crossover with probability
    '''
    Chrom, size_pop, len_chrom = self.Chrom, self.size_pop, len(self.Chrom[0])
    for i in range(0, size_pop, 2):
        if np.random.rand() < crossover_prob:
            n1, n2 = np.random.randint(0, len_chrom, 2)
            if n1 > n2:
                n1, n2 = n2, n1
            seg1, seg2 = Chrom[i, n1:n2].copy(), Chrom[i + 1, n1:n2].copy()
            Chrom[i, n1:n2], Chrom[i + 1, n1:n2] = seg2, seg1
    self.Chrom = Chrom

def pmx(self):
    '''
    Executes a partially matched crossover (PMX) on Chrom.
    For more details see [Goldberg1985]_.

    :param self:
    :return:

    .. [Goldberg1985] Goldberg and Lingel, "Alleles, loci, and the traveling
   salesman problem", 1985.
    '''
    Chrom, size_pop, len_chrom = self.Chrom, self.size_pop, len(self.Chrom[0])
    for i in range(0, size_pop, 2):
        Chrom1, Chrom2 = Chrom[i], Chrom[i + 1]
        cxpoint1, cxpoint2 = np.random.randint(0, len_chrom - 1, 2)
        if cxpoint1 >= cxpoint2:
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1 + 1
        # crossover at the point cxpoint1 to cxpoint2
        pos1_recorder = {value: idx for idx, value in enumerate(Chrom1)}
        pos2_recorder = {value: idx for idx, value in enumerate(Chrom2)}
        for j in range(cxpoint1, cxpoint2):
            value1, value2 = Chrom1[j], Chrom2[j]
            pos1, pos2 = pos1_recorder[value2], pos2_recorder[value1]
            Chrom1[j], Chrom1[pos1] = Chrom1[pos1], Chrom1[j]
            Chrom2[j], Chrom2[pos2] = Chrom2[pos2], Chrom2[j]
            pos1_recorder[value1], pos1_recorder[value2] = pos1, j
            pos2_recorder[value1], pos2_recorder[value2] = j, pos2

        Chrom[i], Chrom[i + 1] = Chrom1, Chrom2
    self.Chrom = Chrom

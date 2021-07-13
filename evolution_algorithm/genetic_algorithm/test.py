import numpy as np
from ga_real import GaReal


demo_func = lambda x: x[0] ** 2 + (x[1] - 0.05) ** 2 + (x[2] - 0.5) ** 2
ga = GaReal(func=demo_func, n_dim=3, size_pop=100, max_iter=1000, prob_mut=0.2, parallel=True,
        lb=np.array([-1, -10, -5]), ub=np.array([2, 10, 2]))
best_x, best_y = ga.run()
print('best_x:', best_x, '\n', 'best_y:', best_y)
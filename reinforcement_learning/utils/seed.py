import random

import numpy as np
import paddle


def all_seed(env, seed=1):
    """
    omnipotent seed for RL, attention the position of seed function, you'd better put it just following the env create function
    Args:
        env (_type_):
        seed (int, optional): _description_. Defaults to 1.
    """
    print(f"seed = {seed}")
    env.seed(seed)  # env config
    np.random.seed(seed)
    random.seed(seed)
    paddle.seed(seed)

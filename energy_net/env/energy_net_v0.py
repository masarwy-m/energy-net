import sys
import os

# Add the project's root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from env.EnergyNetEnv import EnergyNetEnv
from wrappers.order_enforcing_parallel import  OrderEnforcingParallelWrapper


def parallel_env(*args, **kwargs):
    p_env = EnergyNetEnv(*args, **kwargs)
    p_env = OrderEnforcingParallelWrapper(p_env)
    return p_env
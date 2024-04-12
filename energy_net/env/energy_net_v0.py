
from .EnergyNetEnv import EnergyNetEnv
from ..wrappers.order_enforcing_parallel import  OrderEnforcingParallelWrapper


def parallel_env(*args, **kwargs):
    p_env = EnergyNetEnv(*args, **kwargs)
    p_env = OrderEnforcingParallelWrapper(p_env)
    return p_env

import numpy as np
from typing import List, Mapping, Any, Union

from ..config import DEFAULT_EFFICIENCY
from ..entities.params import StorageParams, ProductionParams, ConsumptionParams
from ..network_entity import NetworkEntity
from ..entities.local_storage import Battery
from ..dynamics.storage_dynamics import BatteryDynamics
from ..entities.private_producer import PrivateProducer
from ..dynamics.production_dynmaics import PVDynamics
from ..entities.local_consumer import ConsumerDevice
from ..dynamics.consumption_dynamic import ElectricHeaterDynamics
from ..entities.household import Household
from ..reward_function import RewardFunction


def observation_seperator(observation:dict[str, np.ndarray]):
    """
    Seperates the observation into the agent's observation.

    Parameters:
    observation (dict): The observation of all agents.
    agent (str): The agent to get the observation for.

    Returns:
    dict: The observation of the agent.
    """

    return [observation[name] for name in observation.keys()]


def default_household():
    """Create a default household with a battery, pv, and load."""
    battery = Battery(StorageParams(energy_capacity = 100, power_capacity = 200,
                    inital_charge = 50, charging_efficiency = 1,
                    discharging_efficiency = 1, lifetime_constant = 15, energy_dynamics=BatteryDynamics(), name='test_battery'))
    pv = PrivateProducer(ProductionParams(max_production=100, efficiency=0.9, energy_dynamics=PVDynamics(), name='test_pv'))
    load = ConsumerDevice(ConsumptionParams(max_electric_power=100, efficiency=DEFAULT_EFFICIENCY, energy_dynamics=ElectricHeaterDynamics(), name='test_heater'))
    return Household(name='test_household', sub_entities=[battery, pv, load])


def default_network_entities() -> List[NetworkEntity]:
        household = default_household()
        return [household]


class DefaultRewardFunction(RewardFunction):
    r"""Dummy reward function class.

    Parameters
    ----------
    env_metadata: Mapping[str, Any]:
        General static information about the environment.
    **kwargs : dict
        Other keyword arguments for custom reward calculation.
    """

    def __init__(self, env_metadata: Mapping[str, Any], **kwargs):
        super().__init__(env_metadata, **kwargs)

    def calculate(self, observations: List[Mapping[str, Union[int, float]]]) -> List[float]:
        return 0

def default_reward(meta_data: dict[str, str])-> RewardFunction:
    return DefaultRewardFunction(env_metadata=meta_data)




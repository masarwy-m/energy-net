
import numpy as np
from typing import List, Mapping, Any, Union

from ..config import DEFAULT_EFFICIENCY, DEFAULT_LIFETIME_CONSTANT
from ..entities.params import StorageParams, ProductionParams, ConsumptionParams
from ..network_entity import NetworkEntity
from ..entities.local_storage import Battery
from ..dynamics.storage_dynamics import BatteryDynamics
from ..entities.local_producer import PrivateProducer
from ..dynamics.production_dynamics import PVDynamics
from ..entities.consumer_device import ConsumerDevice
from ..dynamics.consumption_dynamics import HouseholdConsumptionDynamics
from ..entities.household import Household
from ..model.reward import RewardFunction


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


# def default_household():
#     """Create a default household with a battery, pv, and load."""
#     battery = Battery(storage_params=StorageParams(energy_capacity = 100, power_capacity = 200,
#                     inital_charge = 50, charging_efficiency = 1,
#                     discharging_efficiency = 1, lifetime_constant = 15, energy_dynamics=BatteryDynamics(), name='test_battery'))
#     pv = PrivateProducer(ProductionParams(max_production=100, efficiency=0.9, energy_dynamics=PVDynamics(), name='test_pv'))
#     load = ConsumerDevice(ConsumptionParams(max_electric_power=100, efficiency=DEFAULT_EFFICIENCY, energy_dynamics=ElectricHeaterDynamics(), name='test_heater'))
#     return Household(name='test_household', sub_entities=[battery, pv, load])


def default_household():
    # initialize consumer devices
        consumption_params_arr=[]
        consumption_params = ConsumptionParams(name='household_consumption', energy_dynamics=HouseholdConsumptionDynamics(), lifetime_constant=DEFAULT_LIFETIME_CONSTANT)
        consumption_params_arr.append(consumption_params)
        consumption_params_dict = {'household_consumption': consumption_params}

        # initialize storage devices
        storage_params_arr=[]
        storage_params = StorageParams(name = 'test_battery', energy_capacity = 100, power_capacity = 200,inital_charge = 50, charging_efficiency = 1,discharging_efficiency = 1, lifetime_constant = 15, energy_dynamics = BatteryDynamics())
        storage_params_arr.append(storage_params)
        storage_params_dict = {'test_battery': storage_params}

        # initialize production devices
        production_params_arr=[]
        production_params = ProductionParams(name='test_pv', max_production=100, efficiency=0.9, energy_dynamics=PVDynamics())
        production_params_arr.append(production_params)
        production_params_dict = {'test_pv': production_params}

        # initilaize household
        return Household(name="test_household", consumption_params_dict=consumption_params_dict, storage_params_dict=storage_params_dict, production_params_dict=production_params_dict, agg_func= None)


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




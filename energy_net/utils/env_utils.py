
import numpy as np
import importlib
from typing import List
from network_entity import NetworkEntity
from entities.local_storage import Battery
from dynamics.storage_dynamics import BatteryDynamics
from entities.private_producer import PrivateProducer
from dynamics.production_dynmaics import PVDynamics
from entities.local_consumer import ConsumerDevice
from dynamics.consumption_dynamic import ElectricHeaterDynamics
from entities.household import Household
from reward_function import HouseholdDummyRewardFunction, RewardFunction


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
    battery = Battery(energy_capacity = 100, power_capacity = 200,
                    inital_charge = 50, charging_efficiency = 1,
                    discharging_efficiency = 1, lifetime_constant = 15, energy_dynamics=BatteryDynamics(), name='test_battery')
    pv = PrivateProducer(max_produce=100, efficiency=0.9, energy_dynamics=PVDynamics(), name='test_pv')
    load = ConsumerDevice(max_electric_power=100, energy_dynamics=ElectricHeaterDynamics(), name='test_heater')
    return Household(name='test_household', sub_entities=[battery, pv, load])


def default_network_entities() -> List[NetworkEntity]:
        household = default_household()
        return [household]


def default_reward(meta_data: dict[str, str])-> RewardFunction:
    return HouseholdDummyRewardFunction(env_metadata=meta_data)





import numpy as np
from gymnasium.spaces import Box
from typing import List, Mapping, Any, Union

from ..defs import Bounds
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


def bounds_to_gym_box(bounds: Bounds) -> Box:
    """
    Converts a Bounds object to a gym.Box object.

    Args:
        bounds (Bounds): The Bounds object to be converted.

    Returns:
        gym.Box: The corresponding gym.Box object.
    """
    return Box(
        low=bounds['low'],
        high=bounds['high'],
        shape=bounds['shape'],
        dtype=bounds['dtype']
    )





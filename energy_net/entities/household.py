from typing import Any, Union
from gymnasium.spaces import Dict
import numpy as np
from numpy.typing import ArrayLike

from ..config import INITIAL_TIME
from ..model.action import EnergyAction
from ..model.state import State
from ..dynamics.energy_dynamcis import ConsumptionDynamics
from ..network_entity import NetworkEntity, CompositeNetworkEntity, ElementaryNetworkEntity
from ..entities.device import StorageDevice
from ..utils.utils import AggFunc, get_value_by_type
from ..dynamics.consumption_dynamics import ElectricHeaterDynamics
from ..dynamics.production_dynamics import PVDynamics
from ..dynamics.storage_dynamics import BatteryDynamics
from ..entities.consumer_device import ConsumerDevice
from ..entities.local_storage import Battery
from ..entities.params import StorageParams, ProductionParams, ConsumptionParams
from ..entities.local_producer import PrivateProducer


class Household(CompositeNetworkEntity):
    """ A household entity that contains a list of sub-entities. The sub-entities are the devices and the household itself is the composite entity.
    The household entity is responsible for managing the sub-entities and aggregating the reward.
    """

    def __init__(self, name: str, sub_entities: list[NetworkEntity] = None, consumption_params_dict:dict[str,ConsumptionParams]=None, storage_params_dict:dict[str,StorageParams]=None, production_params_dict:dict[str,ProductionParams]=None, agg_func=None):

        if sub_entities is None:
            # initialize consumer devices (non-shiftable loads)
            self.consumption_array = []
            for consumption_params in consumption_params_dict:
                householdConsumption = HouseholdConsumption(consumption_params)
                self.consumption_array.append(householdConsumption)

            # initialize storage devices
            self.storage_array = []
            for storage_params in storage_params_dict:
                device = Battery(init_time=INITIAL_TIME, storage_params=storage_params)
                self.storage_array.append(device)

            # initialize production devices
            self.production_array = []
            for production_params in production_params_dict:
                device = PrivateProducer(production_params)
                self.production_array.append(device)

            sub_entities = self.consumption_array+ self.storage_array+ self.production_array

        super().__init__(name=name,sub_entities=sub_entities, agg_func=agg_func)

    def step(self, actions: dict[str, EnergyAction]):

        super().step(actions)

    def predict(self, actions: Union[np.ndarray, dict[str, Any]]):
        pass

    def get_current_state(self):
        return self.apply_func_to_sub_entities(lambda entity: entity.get_current_state())

    def update_state(self, state: State):
        for entity in self.sub_entities:
            entity.update_state(state[entity.name])

    def get_observation_space(self):
        return Dict(self.apply_func_to_sub_entities(lambda entity: entity.get_observation_space()))

    def get_action_space(self):
        conditions = lambda entity: isinstance(entity, StorageDevice)
        # print(self.apply_func_to_sub_entities(lambda entity: entity.get_action_space(), conditions), "Action Space")
        return Dict(self.apply_func_to_sub_entities(lambda entity: entity.get_action_space(), conditions))

    def reset(self):
        return self.apply_func_to_sub_entities(lambda entity: entity.reset())

    @property
    def current_storge_state(self):
        return sum([s.current_state['state_of_charge'] for s in self.storage_units])

    def apply_func_to_sub_entities(self, func, condition=lambda x: True):
        results = {}
        for name, entity in self.sub_entities.items():
            if condition(entity):
                results[name] = func(entity)
        return results


class HouseholdConsumption(ElementaryNetworkEntity):
    def __init__(self, consumption_params:ConsumptionParams):
        super().__init__(name=consumption_params["name"],energy_dynamics=consumption_params["energy_dynamics"])



class HouseholdIS(CompositeNetworkEntity):
    """ A household entity that contains a list of sub-entities. The sub-entities are the devices and the household itself is the composite entity.
    The household entity is responsible for managing the sub-entities and aggregating the reward.
    """

    def __init__(self, name: str = None, sub_entities: list[NetworkEntity] = None):
        super().__init__(name, sub_entities)

    def step(self, actions: Union[np.ndarray, dict[str, Any]]):
        pass

    def get_current_state(self):
        return self.apply_func_to_sub_entities(lambda entity: entity.get_current_state())

    def update_state(self, state: State):
        for entity in self.sub_entities:
            entity.update_state(state[entity.name])

    def get_observation_space(self):
        return Dict(self.apply_func_to_sub_entities(lambda entity: entity.get_observation_space()))

    def get_action_space(self):
        conditions = lambda entity: isinstance(entity, StorageDevice)
        # print(self.apply_func_to_sub_entities(lambda entity: entity.get_action_space(), conditions), "Action Space")
        return Dict(self.apply_func_to_sub_entities(lambda entity: entity.get_action_space(), conditions))

    def reset(self):
        return self.apply_func_to_sub_entities(lambda entity: entity.reset())

    @property
    def current_storge_state(self):
        return sum([s.current_state['state_of_charge'] for s in self.storage_units])

    def apply_func_to_sub_entities(self, func, condition=lambda x: True):
        results = {}
        for name, entity in self.sub_entities.items():
            if condition(entity):
                results[name] = func(entity)
        return results




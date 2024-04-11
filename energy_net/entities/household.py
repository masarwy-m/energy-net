from typing import Any, Union
from gymnasium.spaces import Dict
import numpy as np
from numpy.typing import ArrayLike

from ..defs import EnergyAction, State
from ..network_entity import NetworkEntity, CompositeNetworkEntity
from ..entities.device import StorageDevice
from ..utils.utils import AggFunc, get_value_by_type
from energy_net.dynamics.consumption_dynamic import ElectricHeaterDynamics
from energy_net.dynamics.production_dynmaics import PVDynamics
from energy_net.dynamics.storage_dynamics import BatteryDynamics
from energy_net.entities.local_consumer import ConsumerDevice
from energy_net.entities.local_storage import Battery
from energy_net.entities.params import StorageParams, ProductionParams, LoadParams
from energy_net.entities.private_producer import PrivateProducer

class Household(CompositeNetworkEntity):
    """ A household entity that contains a list of sub-entities. The sub-entities are the devices and the household itself is the composite entity.
    The household entity is responsible for managing the sub-entities and aggregating the reward.
    """

    def __init__(self, name: str, device_params_dict:dict[str,LoadParams], storage_params_dict:dict[str,StorageParams], production_params_dict:dict[str,ProductionParams]):

        # initialize consumer devices (non-shiftable loads)
        self.device_array = []
        for device_params in device_params_dict:
            device = ConsumerDevice(device_params)
            self.device_array.append(device)

        # initialize storage devices
        self.storage_array = []
        for storage_params in storage_params_dict:
            device = Battery(storage_params)
            self.storage_array.append(device)

        # initialize production devices
        self.production_array = []
        for production_params in production_params_dict:
            device = PrivateProducer(production_params)
            self.production_array.append(device)

        super().__init__(name=name, sub_entities=[self.device_array+self.storage_array+self.production_array])

    def step(self, actions: Union[np.ndarray, dict[str, Any]]):
        print('step in household')

    def predict(self, actions: Union[np.ndarray, dict[str, Any]]):
        print('step in household')

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










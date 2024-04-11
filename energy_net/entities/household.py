from typing import Any, Union

from network_entity import NetworkEntity, CompositeNetworkEntity
from entities.device import StorageDevice
from utils.utils import AggFunc, get_value_by_type
from defs import EnergyAction, State
from gymnasium.spaces import Dict
import numpy as np
from numpy.typing import ArrayLike


#return Household(name='test_household',  agg_func=lambda x: x)

class Household(CompositeNetworkEntity):
    """ A household entity that contains a list of sub-entities. The sub-entities are the devices and the household itself is the composite entity.
    The household entity is responsible for managing the sub-entities and aggregating the reward.
    """
    def __init__(self, name: str = None, sub_entities:list[NetworkEntity] = None):
        super().__init__(name, sub_entities)

    def step(self, actions: Union[np.ndarray, dict[str,Any]]):
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
   
   
    








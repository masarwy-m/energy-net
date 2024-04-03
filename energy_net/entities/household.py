
from network_entity import NetworkEntity, CompositeNetworkEntity 
from utils import AggFunc, get_value_by_type
from defs import EnergyAction, State
from gymnasium.spaces import Dict
import numpy as np
from numpy.typing import ArrayLike

class HouseHold(CompositeNetworkEntity):
    def __init__(self, name, sub_entities:list[NetworkEntity], agg_func:AggFunc):
        super().__init__(name, sub_entities, agg_func)
        from entities.device import StorageDevice
        self.storage_units = [s for s in sub_entities if isinstance(s, StorageDevice)]

    def get_current_state(self):
        return self.apply_func_to_sub_entities(lambda entity: entity.get_current_state())
    
    def update_state(self, state: State):
        for entity in self.sub_entities:
            entity.update_state(state[entity.name])
            
    def get_observation_space(self):
        return Dict(self.apply_func_to_sub_entities(lambda entity: entity.get_observation_space()))
    
    def get_action_space(self):
        return Dict(self.apply_func_to_sub_entities(lambda entity: entity.get_action_space()))
    
    def reset(self):
        return self.apply_func_to_sub_entities(lambda entity: entity.reset())
    
    def get_reward(self):
        return sum(self.apply_func_to_sub_entities(lambda entity: entity.get_reward()).values())   
    

    def build_action(self, action: EnergyAction) -> dict[str, ArrayLike]:
        return {name: np.array(get_value_by_type(action, entity.action_type)) for name, entity in self.sub_entities.items()}

    
    @property
    def current_storge_state(self):
        return sum([s.current_state['state_of_charge'] for s in self.storage_units])
    

    def apply_func_to_sub_entities(self, func):
        results = {}
        for name, entity in self.sub_entities.items():
            results[name] = func(entity)
        return results








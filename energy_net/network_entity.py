from abc import abstractmethod
from dynamics.energy_dynamcis import EnergyDynamics
from utils import AggFunc
from defs import EnergyAction, State, Reward

class NetworkEntity:
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def step(self, action: EnergyAction) -> [State, Reward]:
        pass

    @abstractmethod
    def predict(self, action: EnergyAction, state: State) -> [State,Reward]:
        pass
    
    @abstractmethod
    def current_state(self):
        pass


class CompositeNetworkEntity(NetworkEntity):
    def __init__(self, name: str, sub_entities:list[NetworkEntity], agg_func:AggFunc):
        super().__init__(name)
        self.sub_entities = sub_entities
        self.agg_func = agg_func

    def step(self, action: EnergyAction) -> [State, Reward]:
        return self.agg_func([entity.step(action) for entity in self.sub_entities])

    def predict(self, action: EnergyAction, state: State):
        predictions = [entity.predict(action, state) for entity in self.sub_entities]
        return self.agg_func(predictions)


class ElementaryNetworkEntity(NetworkEntity):
    def __init__(self, name, energy_dynamics:EnergyDynamics):
        super().__init__(name)
        self.energy_dynamics = energy_dynamics

    def step(self, action: EnergyAction, state:State) -> [State, Reward]:
        return self.energy_dynamics.do(action, state)

    def predict(self, action: EnergyAction, state: State):
        pass



class HouseHold(CompositeNetworkEntity):
    def __init__(self, name, sub_entities:list[NetworkEntity], agg_func:AggFunc):
        super().__init__(name, sub_entities, agg_func)
        from entities.device import StorageDevice
        self.storage_units = [s for s in sub_entities if isinstance(s, StorageDevice)]

    def step(self, action: EnergyAction):
        if self.illegal_action(action):
            raise ValueError('Illegal action')
        for entity in self.sub_entities:
            entity.step(action, entity.current_state)
            
    
    
    def illegal_action(self, action: EnergyAction) -> bool:
        return action.get('consume') + action.get('charge') < action.get('produce') + self.current_storge_state  
    
    @property
    def current_storge_state(self):
        return sum([s.current_state['state_of_charge'] for s in self.storage_units])

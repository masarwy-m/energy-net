from abc import abstractmethod
from energy_net.dynamics.energy_dynamcis import EnergyDynamics
from energy_net.utils import AggFunc
from energy_net.defs import EnergyAction, State, Reward
class NetworkEntity:
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def step(self, action: EnergyAction) -> [State, Reward]:
        pass

    @abstractmethod
    def predict(self, action: EnergyAction, state: State) -> [State,Reward]:
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

    def step(self, action: EnergyAction) -> [State, Reward]:
        pass

    def predict(self, action: EnergyAction, state: State):
        pass
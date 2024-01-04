from abc import abstractmethod
from energy_net.dynamics.energy_dynamcis import EnergyDynamics, ProductionDynamics
from energy_net.utils import AggFunc

from typing import Callable, Any
EnergyAction = dict[str, Any]
State = dict[str, Any]
Reward = dict[str, float]

class NetworkEntity:
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def step(self, action: EnergyAction) -> [State,Reward]:
        pass

    @abstractmethod
    def predict(self, action: EnergyAction, state) -> [State,Reward]:
        pass


class CompositeNetworkEntity(NetworkEntity):
    def __init__(self, name, sub_entities, agg_func:AggFunc):
        super().__init__(name)
        self.sub_entities = sub_entities
        self.agg_func = agg_func

    def step(self, action: EnergyAction) -> [State, Reward]:
        return self.agg_func([entity.step(action) for entity in self.sub_entities])

    def predict(self, action: EnergyAction, state):
        predictions = [entity.predict(action, state) for entity in self.sub_entities]
        return self.agg_func(predictions)


class ElementaryNetworkEntity(NetworkEntity):
    def __init__(self, name, energy_dynamics):
        super().__init__(name)

        self.energy_dynamics = energy_dynamics

    def step(self, action: EnergyAction) -> [State, Reward]:
        out = {}
        for action, params in action.items():
            out[action] = self.energy_dynamics.do(action, params)

        return out

    def predict(self, action: EnergyAction, state):
        out = {}
        for action, params in action.items():
            out[action] = self.energy_dynamics.predict(action, params, state)

        return out


class MarketProducer(ElementaryNetworkEntity):

    def __init__(self, name, energy_dynamics: ProductionDynamics):
        super().__init__(name, energy_dynamics)

    @abstractmethod
    def production_bid(self, state, consumption_demand):
        pass



from abc import abstractmethod
from energy_net.dynamics.energy_dynamcis import EnergyDynamics, ProductionDynamics

from typing import Any

class NetworkEntity:
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def step(self, action: dict[str, Any]):
        pass

    @abstractmethod
    def predict(self, action: dict[str, Any], state):
        pass


class CompositeNetworkEntity(NetworkEntity):
    def __init__(self, name, sub_entities, aggregator):
        super().__init__(name)

        self.sub_entities = sub_entities
        self.aggregator = aggregator

    def step(self, action):
        return self.aggregator([entity.step(action) for entity in self.sub_entities])

    def predict(self, action: dict[str, Any], state):
        return self.aggregator([entity.predict(action, state) for entity in self.sub_entities])


class ElementaryNetworkEntity(NetworkEntity):
    def __init__(self, name, energy_dynamics):
        super().__init__(name)

        self.energy_dynamics = energy_dynamics

    def step(self, action):
        out = {}
        for action, params in action.items():
            out[action] = self.energy_dynamics.do(action, params)

        return out

    def predict(self, action: dict[str, Any], state):
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

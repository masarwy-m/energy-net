from abc import abstractmethod
from energy_net.defs import State, Bid
from energy_net.dynamics.energy_dynamcis import ProductionDynamics
from energy_net.network_entity import ElementaryNetworkEntity, CompositeNetworkEntity


class MarketEntity(ElementaryNetworkEntity):

    @abstractmethod
    def get_bid(self, bid_type:str, state:State, args)-> Bid:
        pass

class CompositeMarketEntity(CompositeNetworkEntity):

    @abstractmethod
    def get_bid(self, bid_type:str, state:State, args)-> Bid:
        pass


class MarketProducer(MarketEntity):

    def __init__(self, name: str, energy_dynamics: ProductionDynamics):
        super().__init__(name, energy_dynamics)


class MarketConsumer(MarketEntity):

    def __init__(self, name: str, energy_dynamics: ProductionDynamics):
        super().__init__(name, energy_dynamics)


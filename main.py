from energy_net.network_entity import ElementaryNetworkEntity, MarketProducer, CompositeNetworkEntity
from energy_net.dynamics.energy_dynamcis import EnergyDynamics, ProductionDynamics
from energy_net.network_manager import NetworkManager


class DummyStationDynamics(ProductionDynamics):
    def __init__(self, production_capacity):
        self.production_capacity = production_capacity

    def do(self, action, params, cur_state):
        if action == "produce":
            return min(params['amount'], self.production_capacity)
        else:
            raise NotImplemented('stations can only produce')

    def predict(self, action, params, state):
        if action == "produce":
            return min(params['amount'], self.production_capacity)
        else:
            raise NotImplemented('stations can only produce')


class DummyProducer(MarketProducer):
    def __init__(self, name, energy_dynamics: ProductionDynamics, fixed_price):
        super().__init__(name, energy_dynamics)
        self.fixed_price = fixed_price

    def production_bid(self, state, consumption_demand):
        return self.energy_dynamics.production_capacity, self.fixed_price


class DummyConsumerDynamics(EnergyDynamics):
    def __init__(self, fixed_consumption):
        self.consumption = fixed_consumption

    def do(self, action, params, cur_state):
        if action == 'consume':
            return self.consumption
        else:
            raise NotImplemented('consumers can only consume')

    def predict(self, action, params, state):
        if action == "consume":
            return self.consumption
        else:
            raise NotImplemented('consumers can only consume')


def test_elementary_network_market():
    station1 = DummyProducer('station1', DummyStationDynamics(production_capacity=200), fixed_price=10)
    station2 = DummyProducer('station2', DummyStationDynamics(production_capacity=300), fixed_price=2)
    station3 = DummyProducer('station3', DummyStationDynamics(production_capacity=400), fixed_price=4)
    station4 = DummyProducer('station4', DummyStationDynamics(production_capacity=500), fixed_price=100)
    station5 = DummyProducer('station5', DummyStationDynamics(production_capacity=600), fixed_price=42)

    consumer1 = ElementaryNetworkEntity('consumer1', DummyConsumerDynamics(fixed_consumption=2))
    consumer2 = ElementaryNetworkEntity('consumer2', DummyConsumerDynamics(fixed_consumption=4))
    consumer3 = ElementaryNetworkEntity('consumer3', DummyConsumerDynamics(fixed_consumption=6))
    consumer4 = ElementaryNetworkEntity('consumer4', DummyConsumerDynamics(fixed_consumption=8))


    mgr = NetworkManager([station1, station2, station3, station4, station5],
                         [consumer1, consumer2, consumer3, consumer4])

    demand = mgr.collect_demand(None)
    bids = mgr.collect_bids(None, demand)
    workloads, price = mgr.market_clearing(demand, bids)

    print(f'demand was: {demand}')
    print(f'bids were: {bids}')
    print(f'workloads are: {workloads}')
    print(f'final price is: {price}')


def test_composite_network_market():
    station1 = DummyProducer('station1', DummyStationDynamics(production_capacity=200), fixed_price=10)
    station2 = DummyProducer('station2', DummyStationDynamics(production_capacity=300), fixed_price=2)
    station3 = DummyProducer('station3', DummyStationDynamics(production_capacity=400), fixed_price=4)
    station4 = DummyProducer('station4', DummyStationDynamics(production_capacity=500), fixed_price=100)
    station5 = DummyProducer('station5', DummyStationDynamics(production_capacity=600), fixed_price=42)

    consumer1 = ElementaryNetworkEntity('consumer1', DummyConsumerDynamics(fixed_consumption=2))
    consumer2 = ElementaryNetworkEntity('consumer2', DummyConsumerDynamics(fixed_consumption=4))
    consumer3 = ElementaryNetworkEntity('consumer3', DummyConsumerDynamics(fixed_consumption=6))
    consumer4 = ElementaryNetworkEntity('consumer4', DummyConsumerDynamics(fixed_consumption=8))

    # this is the key difference from the elementary implementation
    consumer_aggregator = CompositeNetworkEntity('agg1',[consumer1, consumer2, consumer3, consumer4], sum)
    mgr = NetworkManager([station1, station2, station3, station4, station5],
                         [consumer_aggregator])

    demand = mgr.collect_demand(None)
    bids = mgr.collect_bids(None, demand)
    workloads, price = mgr.market_clearing(demand, bids)

    print(f'demand was: {demand}')
    print(f'bids were: {bids}')
    print(f'workloads are: {workloads}')
    print(f'final price is: {price}')


if __name__ == "__main__":
    test_elementary_network_market()
    #test_composite_network_market()

#############################

#implementing a neighborhood of 5 buildings
# building 1: driven by a data file that determines what happens at each step (like CityLearn)
# building 2: is modeled as a single unit (no sub-entities) that has a solar pannel and a batery
# building 3: a building modeled as 4 appartments (sub-entities), all of which consume energy, and 2 have solar pannels and batteries
# building 4: a building that models 4 appartments, 2 are modeled as a single unit, 1 has several consumer devices, and 1 is data driven.
# building 5: a house with many devices, each device can only consume, but the house has a single battery.


#b1 = ...


#b2 = ...


#b3 = ...


#b4 = ...


#b5 = ...



#my_neighborhood = NetworkEntity(sub_entities=[b1, b2, b3, b4, b5])

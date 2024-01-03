from energy_net.network_entity import CompositeNetworkEntity


class Network(CompositeNetworkEntity):
    def __init__(self, name, sub_entities, aggregator, connections: dict[]):
        super().__init__(name, sub_entities, aggregator)

        if sub_entities:
            self.is_compound = True
        else:
            self.is_compound = False
        self.sub_entities = sub_entities
        self.energy_dynamics = energy_dynamics
        self.aggregate_energy_dynmaics = aggregate_energy_dynmaics


class Node:

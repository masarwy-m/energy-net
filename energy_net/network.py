from .network_entity import CompositeNetworkEntity, NetworkEntity


class Network(CompositeNetworkEntity):
    def __init__(self, network_entities: list[NetworkEntity]):
        self.network_entities = network_entities


class Node:
    pass

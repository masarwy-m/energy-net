from energy_net.dynamics.production_dynmaics import FFProductionDynamics
from energy_net.dynamics.storage_dynamics import StorageUnitDynamics
from energy_net.network_entity import ElementaryNetworkEntity, NetworkEntity

class PrivateProducer(ElementaryNetworkEntity):
    def __init__(self, name, storage_dynamics:StorageUnitDynamics,production_dynamics:FFProductionDynamics):
        self.storage = storage_dynamics
        self.production = production_dynamics

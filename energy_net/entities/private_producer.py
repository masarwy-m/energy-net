from energy_net.dynamics.production_dynmaics import PVDynamics
from energy_net.dynamics.storage_dynamics import PrivateStorageUnitDynamics
from energy_net.network_entity import ElementaryNetworkEntity


class PrivatePVProducer(ElementaryNetworkEntity):
    def __init__(self, name, storage_dynamics:PrivateStorageUnitDynamics,production_dynamics:PVDynamics):
        self.name = name
        self.storage = storage_dynamics
        self.production = production_dynamics






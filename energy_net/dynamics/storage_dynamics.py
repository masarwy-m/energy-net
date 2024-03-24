from energy_net.defs import EnergyAction, State
from energy_net.dynamics.energy_dynamcis import StorageDynamics

class StorageUnitDynamics(StorageDynamics):
    def __init__(self, dc_capacity, net_connection_size, efficiency, capacity):
        pass

class LocalStorageUnitDynamics(StorageDynamics):
    def __init__(self, dc_capacity, net_connection_size, efficiency, capacity):
        pass

    def do(self, action:EnergyAction, params, cur_state:State):
        pass

    def predict(self, action:EnergyAction, params, cur_state:State):
        pass

    def get_current_discharge_capability(self):
        pass

    def predict_discharge_capability(self, state:State):
        pass

    @abstractmethod
    def get_current_charge_capability(self):
        pass

    @abstractmethod
    def predict_charge_capability(self, state:State):
        pass

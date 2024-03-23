from dynamics.energy_dynamcis import StorageDynamics
from defs import EnergyAction, State

class StorageUnitDynamics(StorageDynamics):
    def __init__(self, dc_capacity, net_connection_size, efficiency, capacity):
        pass

    def do(self, action, params):
        pass

    def predict(self, action, params, state):
        pass

    def get_current_discharge_capability(self):
        pass

    def predict_discharge_capability(self, state):
        pass

    def get_current_charge_capability(self):
        pass

    def predict_charge_capability(self, state): 
        pass       



class BatteryDynamics(StorageDynamics):
    def __init__(self) -> None:
        super().__init__()

    def do(self, action:EnergyAction, params:dict):
        if action == 'charge':
            curr_device = params['device']
            new_cpacity =  curr_device.capacity + params['charge_amount']
            curr_device.capacity = new_cpacity
        else:
            raise ValueError('Invalid action')

    def predict(self, action, params, state):
        pass



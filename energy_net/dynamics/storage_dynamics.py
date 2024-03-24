
from dynamics.energy_dynamcis import StorageDynamics
from defs import EnergyAction, BatteryState




class BatteryDynamics(StorageDynamics):
    def __init__(self) -> None:
        super().__init__()

    def do(self, action:EnergyAction, state:BatteryState):
        key, value = next(iter(action.items()))
        if key == 'charge':
            return state['state_of_charge'] + value if state['state_of_charge'] + value <= state['capacity'] else state['capacity']	
        else:
            raise ValueError('Invalid action')

    def predict(self, action, params, state):
        pass


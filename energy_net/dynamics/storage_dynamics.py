
from dynamics.energy_dynamcis import StorageDynamics
from defs import EnergyAction, BatteryState




class BatteryDynamics(StorageDynamics):
    def __init__(self) -> None:
        super().__init__()

    def do(self, action:EnergyAction, state:BatteryState) -> float:
        
        r"""Perform action on battery.
            parameters
            ----------
            action : EnergyAction
                Action to be performed. Must be a dictionary with a single key-value pair.
            state : BatteryState
                Current state of the battery.
            return : float
                New state of charge in [kWh].
        """
        value = action.get('charge')
        if value is not None:
            return state['state_of_charge'] + value if state['state_of_charge'] + value <= state['capacity'] else state['capacity']	
        else:
            raise ValueError('Invalid action')

    def predict(self, action, params, state):
        pass


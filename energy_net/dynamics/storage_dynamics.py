
from dynamics.energy_dynamcis import StorageDynamics
from defs import  BatteryState
from numpy.typing import ArrayLike 
from env.config import MIN_CHARGE


class BatteryDynamics(StorageDynamics):
    def __init__(self) -> None:
        super().__init__()

    def do(self, action: ArrayLike, state:BatteryState) -> BatteryState:
        
        """Perform action on battery.
            parameters
            ----------
            action : Numpy array
                Action to be performed. Must be a numpy array with a single value.
            state : BatteryState
                Current state of the battery.
            return : BatteryState
                New state of charge in [kWh].
        """
        assert action.ndim == 1, 'Only one action is allowed'
        value = action[0]
        if value is not None:
            new_state = state.copy()
            new_state['state_of_charge'] = max(state['state_of_charge'] + value, MIN_CHARGE) 
            return new_state	
        else:
            raise ValueError('Invalid action')

    def predict(self, action, params, state):
        pass


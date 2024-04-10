
from dynamics.energy_dynamcis import StorageDynamics
from defs import  BatteryState
from numpy.typing import ArrayLike 
from functools import partial
from env.config import MIN_CHARGE, MIN_EXPONENT, MAX_EXPONENT
import numpy as np


class BatteryDynamics(StorageDynamics):
    def __init__(self) -> None:
        super().__init__()

    def do(self, action: ArrayLike, state:BatteryState, *args, **kwargs) -> BatteryState:
        
        """Perform action on battery.
            parameters
            ----------
            action : Numpy array
                Action to be performed. Must be a numpy array with a single value.
            state : BatteryState
                Current state of the battery.
            lifetime_constant : float
            return : BatteryState
                New state of charge in [kWh].
        """
        assert action.ndim == 1, 'Only one action is allowed'
        value = action[0]
        lifetime_constant = kwargs.get('lifetime_constant')
        if value is not None:
            new_state = state.copy()
            if value > MIN_CHARGE: # Charge
                new_state.state_of_charge = min(state.state_of_charge + value, state.energy_capacity)
            else: # Discharge
                new_state.state_of_charge = max(state.state_of_charge + value, MIN_CHARGE)

            exp_mult = partial(self.exp_mult, state=state, lifetime_constant=lifetime_constant)
            new_state.energy_capacity = exp_mult(state.energy_capacity)
            new_state.power_capacity =  exp_mult(state.power_capacity)
            new_state.charging_efficiency = exp_mult(state.charging_efficiency)
            new_state.discharging_efficiency =  exp_mult(state.discharging_efficiency)
            new_state.current_time += 1
            return new_state	
        else:
            raise ValueError('Invalid action')

    def predict(self, action, params, state):
        pass
    
    @staticmethod
    def exp_mult(x, state, lifetime_constant):
        if lifetime_constant == 0:
            return x  # or handle the zero division case in another way
        else:
            # Clamp the exponent value to prevent overflow
            exponent = state.current_time / float(lifetime_constant)
            exponent =  max(MIN_EXPONENT, min(MAX_EXPONENT, exponent))
            return x * np.exp(exponent)
        

    


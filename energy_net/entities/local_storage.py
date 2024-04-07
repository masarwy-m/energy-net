'''This code is based on https://github.com/intelligent-environments-lab/CityLearn/blob/master/citylearn/energy_model.py'''

from typing import Any, TypedDict
from defs import BatteryState, ChargeAction
from entities.device import StorageDevice
from gymnasium.spaces import Box
import numpy as np
from env.config import MIN_CHARGE, MIN_EFFICIENCY, MAX_EFFICIENCY


class Battery(StorageDevice):
    """Base electricity storage class.

    Parameters
    ----------
    energy_capacity : float, default: inf
        Maximum amount of energy the storage device can store in [kWh]. Must be >= 0.
    efficiency : float, default: 1.0
        Technical efficiency.
    initial_charge : float, default: 0.0
        Initial state of charge of the storage device.

    
    Other Parameters
    ----------------
    **kwargs : Any
        Other keyword arguments used to initialize super classes.
    """
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.action_type = ChargeAction

    @property
    def current_state(self) -> BatteryState:
        return np.array(energy_capacity = self.energy_capacity, power_capacity = self.power_capacity,
                    state_of_charge = self.state_of_charge, charging_efficiency = self.charging_efficiency,
                    discharging_efficiency = self.discharging_efficiency, lifetime_constant = self.lifetime_constant)
    
    def get_current_state(self) -> BatteryState:
        return self.current_state
    
    def update_state(self, state: BatteryState) -> None:
        self.energy_capacity = state.energy_capacity
        self.power_capacity = state.power_capacity
        self.state_of_charge = state.state_of_charge
        self.charging_efficiency = state.charging_efficiency
        self.discharging_efficiency = state.discharging_efficiency
        self.lifetime_constant = state.lifetime_constant
        self.current_time = state.current_time


    def get_reward(self):
        return 0    
    
    def reset(self) -> BatteryState:
        super().reset()
        return self.get_current_state()
    
    def get_action_space(self) -> Box:
        low = - self.state_of_charge if self.state_of_charge > MIN_CHARGE else MIN_CHARGE
        return Box(low=low, high=(self.capacity - self.state_of_charge), shape=(1,), dtype=float)  

    def get_observation_space(self) -> Box:
        if self.energy_capacity < 0:
            raise ValueError("Energy capacity value must be non-negative.")

        if self.charging_efficiency < 0:
            raise ValueError("Charging efficiency value must be non-negative.")

        if self.discharging_efficiency < 0:
            raise ValueError("Discharging efficiency value must be non-negative.")

        if self.lifetime_constant < 0:
            raise ValueError("Battery lifetime value must be non-negative.")

        return Box(low=np.array([MIN_CHARGE, MIN_EFFICIENCY]), high=np.array([self.capacity, MAX_EFFICIENCY]), dtype=float)
    


        
        




    

        


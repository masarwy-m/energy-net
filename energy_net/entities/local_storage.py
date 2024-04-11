'''This code is based on https://github.com/intelligent-environments-lab/CityLearn/blob/master/citylearn/energy_model.py'''

from typing import Any, TypedDict
from defs import BatteryState, ChargeAction
from entities.device import StorageDevice
from gymnasium.spaces import Box
import numpy as np
from config import MIN_CHARGE, MIN_EFFICIENCY, MAX_EFFICIENCY, MIN_CAPACITY, MAX_CAPACITY, INITIAL_TIME, MAX_TIME
from typing import NamedTuple

from energy_net.dynamics.energy_dynamcis import EnergyDynamics





class Battery(StorageDevice):
    """Base electricity storage class.

    Parameters
    ----------
    energy_capacity : float, default: inf
        Maximum amount of energy the storage device can store in [kWh]. Must be >= 0.
    power_capacity : float, default: inf
        Maximum amount of power the storage device can store in [kW]. Must be >= 0.
    state_of_charge : float, default: 0.0
        Current state of charge of the storage device in [kWh]. Must be >= 0.
    charging_efficiency : float, default: 1.0
        Charging efficiency of the storage device. Must be > 0.
    discharging_efficiency : float, default: 1.0
        Discharging efficiency of the storage device. Must be > 0.
    lifetime_constant : float, default: inf
        Lifetime constant of the storage device in years. Must be > 0.
    energy_dynamics : Dynamics, default: None
        Energy dynamics of the storage device. Must be a subclass of Dynamics.
    name : str, default: None
        Name of the storage device. Must be a string.


    
    Other Parameters
    ----------------
    **kwargs : Any
        Other keyword arguments used to initialize super classes.
    """
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.action_type = ChargeAction
        self.current_time = INITIAL_TIME

    @property
    def current_state(self) -> BatteryState:
        return BatteryState(energy_capacity = self.energy_capacity, power_capacity = self.power_capacity,
                    state_of_charge = self.state_of_charge, charging_efficiency = self.charging_efficiency,
                    discharging_efficiency = self.discharging_efficiency, current_time = self.current_time)
    
    def get_current_state(self) -> BatteryState:
        return self.current_state
    
    def update_state(self, state: BatteryState) -> None:
        self.energy_capacity = state.energy_capacity
        self.power_capacity = state.power_capacity
        self.state_of_charge = state.state_of_charge
        self.charging_efficiency = state.charging_efficiency
        self.discharging_efficiency = state.discharging_efficiency
        self.current_time = state.current_time


    def get_reward(self):
        return 0    
    
    def reset(self) -> BatteryState:
        super().reset()
        return self.get_current_state()
    
    def get_action_space(self) -> Box:
        low = - self.state_of_charge if self.state_of_charge > MIN_CHARGE else MIN_CHARGE
        return Box(low=low, high=(self.energy_capacity - self.state_of_charge), shape=(1,), dtype=np.float32)  

    def get_observation_space(self) -> Box:
        low = np.array([MIN_CAPACITY, MIN_CAPACITY, MIN_CHARGE, MIN_EFFICIENCY, MIN_EFFICIENCY, INITIAL_TIME])
        high = np.array([MAX_CAPACITY, MAX_CAPACITY, self.energy_capacity, MAX_EFFICIENCY, MAX_EFFICIENCY, MAX_TIME])
        return Box(low=low, high=high, dtype=np.float32)


        
        




    

        


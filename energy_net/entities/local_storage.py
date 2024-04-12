'''This code is based on https://github.com/intelligent-environments-lab/CityLearn/blob/master/citylearn/energy_model.py'''

from typing import Any
from gymnasium.spaces import Box
import numpy as np

from .params import StorageParams
from ..defs import BatteryState, ChargeAction
from .device import StorageDevice
from ..config import MIN_CHARGE, MIN_EFFICIENCY, MAX_EFFICIENCY, MIN_CAPACITY, MAX_CAPACITY, INITIAL_TIME, MAX_TIME





class Battery(StorageDevice):
    """Base electricity storage class.
    """
    def __init__(self, storage_params:StorageParams):
        super().__init__(storage_params)
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


        
        




    

        


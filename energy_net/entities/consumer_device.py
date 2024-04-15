from typing import Any
from gymnasium.spaces import Box
import numpy as np


from ..entities.device import Device
from ..model.state import ConsumerState
from ..model.energy_action import ConsumeAction
from ..config import MAX_ELECTRIC_POWER, MIN_POWER, MIN_EFFICIENCY, MAX_EFFICIENCY, NO_CONSUMPTION
from .params import ConsumptionParams

class ConsumerDevice(Device):
    """Base consumer class.
    Parameters
    ----------
    max_electric_power : float, default: None
        Maximum amount of electric power that the electric heater can consume from the power grid.


    Other Parameters
    ----------------
    **kwargs : Any
        Other keyword arguments used to initialize super class.
    """
    
    def __init__(self, consumptionParams:ConsumptionParams):
        super().__init__(consumptionParams)
        self.max_electric_power = MAX_ELECTRIC_POWER if consumptionParams["max_electric_power"] is None else consumptionParams["max_electric_power"]
        self.efficiency = MAX_EFFICIENCY if consumptionParams["efficiency"] is None else consumptionParams["efficiency"]
        self.init_max_electric_power = self.max_electric_power
        self.consumption = NO_CONSUMPTION
        self.action_type = ConsumeAction


    @property
    def max_electric_power(self):
        return self._max_electric_power
    
    @max_electric_power.setter
    def max_electric_power(self, max_electric_power: float):
        assert max_electric_power >= MIN_POWER, 'max_electric_power must be >= MIN_POWER.'
        self._max_electric_power = max_electric_power

    @property
    def current_state(self) -> ConsumerState:
        return ConsumerState(max_electric_power=self.max_electric_power, efficiency=self.efficiency)
    
    @property
    def efficiency(self) -> float:
        return self._efficiency
    
    @efficiency.setter
    def efficiency(self, efficiency: float):
        assert efficiency >= MIN_EFFICIENCY, 'efficiency must be >= MIN_EFFICIENCY.'
        self._efficiency = efficiency
    
    def get_current_state(self) -> ConsumerState:
        return self.current_state
    

    def update_state(self, state: ConsumerState):
        self.max_electric_power = state.max_electric_power
        self.efficiency = state.efficiency
        self.consumption = state.consumption

  
    def reset(self) -> ConsumerState:
        super().reset()
        self.max_electric_power = self.init_max_electric_power
        self.consumption = NO_CONSUMPTION
        return self.get_current_state()


    def get_action_space(self):
        return Box(low=MIN_POWER, high=self.max_electric_power, shape=(1,), dtype=np.float32)
        

    def get_observation_space(self):
        # Define the lower and upper bounds for each dimension of the observation space
        low = np.array([NO_CONSUMPTION, MIN_POWER, MIN_EFFICIENCY])  # Example lower bounds
        high = np.array([self.max_electric_power, MAX_ELECTRIC_POWER, MAX_EFFICIENCY])  # Example upper bounds
        return Box(low=low, high=high, dtype=np.float32)
        
    
   


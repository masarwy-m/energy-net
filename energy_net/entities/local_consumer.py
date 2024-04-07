from entities.device import Device
from typing import Any
from defs import ConsumerState, ConsumeAction
from env.config import MAX_ELECTRIC_POWER, MIN_POWER, MIN_EFFICIENCY, MAX_EFFICIENCY, NO_CONSUMPTION
from gymnasium.spaces import Box
import numpy as np


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
    
    def __init__(self, max_electric_power:float = None, **kwargs: Any):
        super().__init__(**kwargs)
        self.max_electric_power = MAX_ELECTRIC_POWER if max_electric_power is None else max_electric_power
        self.init_max_electric_power = self.max_electric_power
        self.action_type = ConsumeAction
        self.consumption = NO_CONSUMPTION


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
    
    def get_current_state(self) -> ConsumerState:
        return self.current_state
    

    def update_state(self, state: ConsumerState):
        self.max_electric_power = state.max_electric_power
        self.efficiency = state.efficiency
        self.consumption = state.consumption

        

    def get_reward(self):
        return 0
    
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
        
    
   


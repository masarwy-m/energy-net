from typing import Any
import numpy as np
from gymnasium.spaces import Box

from .device import Device
from .params import ProductionParams
from ..model.state import ProducerState
from ..model.action import ProduceAction
from ..config import MIN_POWER, MIN_PRODUCTION, MAX_ELECTRIC_POWER, DEFAULT_SELF_CONSUMPTION

class PrivateProducer(Device):
    """Base producer class.

    Parameters
    ----------
    max_produce : float, default: 0.0
        producer output power in [kW]. Must be >= 0.
    efficiency : float, default: 1.0
    
    Other Parameters
    ----------------
    **kwargs : Any
        Other keyword arguments used to initialize super class.
    """
    
    def __init__(self, production_params:ProductionParams):
        super().__init__(production_params)
        self.max_production = production_params["max_production"]
        self.init_max_production = self.max_production
        self.production = MIN_PRODUCTION
        self.self_consumption = production_params["self_consumption"] if "self_consumption" in production_params  else DEFAULT_SELF_CONSUMPTION  # self consumption
        self.action_type = ProduceAction

    @property
    def current_state(self) -> ProducerState:
        return ProducerState(max_produce=self.max_production, production=self.production)

    @property
    def max_production(self):
        return self._max_production
    
    @max_production.setter
    def max_production(self, max_production: float):
        assert max_production >= MIN_POWER, 'max_production must be >= MIN_POWER.'
        self._max_production = max_production



    @property
    def production(self):
        return self._production
    
    @production.setter
    def production(self, production: float):
        assert MIN_PRODUCTION <= production <= self.max_production, 'production must be in [MIN_PRODUCTION, MAX_PRODUCTION].'
        self._production = production


    def get_current_state(self) -> ProducerState:
        return self.current_state
    
    def update_state(self, state: ProducerState):
        self.max_production = state.max_production
        self.production = state.production
        
    
    def get_reward(self):
        return self.self_consumption
    
    def reset(self):
        super().reset()
        self.max_production = self.init_max_production
        return self.get_current_state()

    def get_action_space(self) -> Box:
        return Box(low=MIN_POWER, high=self.max_production, shape=(1,), dtype=np.float32)

    def get_observation_space(self) -> Box :
        # Define the lower and upper bounds for each dimension of the observation space
        low = np.array([MIN_POWER, MIN_POWER])  # Example lower bounds
        high = np.array([self.max_production, MAX_ELECTRIC_POWER])  # Example upper bounds
        return Box(low=low, high=high, dtype=np.float32)


    
    


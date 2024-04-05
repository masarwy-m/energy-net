from entities.device import Device
from typing import Any
from defs import ProducerState, ProduceAction
from gymnasium.spaces import Box
from env.config import MIN_POWER, MAX_ELECTRIC_POWER, MIN_EFFICIENCY, MAX_EFFICIENCY
import numpy as np

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
    
    def __init__(self, max_produce: float = None, efficiency: float = None, **kwargs: Any):
        super().__init__(efficiency, **kwargs)
        self.max_produce = max_produce
        self.init_max_produce = self.max_produce
        self.action_type = ProduceAction

    @property
    def current_state(self) -> ProducerState:
        return dict(max_produce=self.max_produce, efficiency=self.efficiency)

    @property
    def max_produce(self):
        return self._max_produce
    
    @max_produce.setter
    def max_produce(self, max_produce: float):
        assert max_produce >= MIN_POWER, 'max_produce must be >= MIN_POWER.'
        self._max_produce = max_produce


    def get_current_state(self) -> ProducerState:
        return self.current_state
    
    def update_state(self, state: ProducerState):
        self.max_produce = state['max_produce']
        self.efficiency = state['efficiency']
    
    def get_reward(self):
        return 0
    
    def reset(self):
        super().reset()
        self.max_produce = self.init_max_produce
        return self.get_current_state()

    def get_action_space(self) -> Box:
        return Box(low=MIN_POWER, high=self.max_produce, shape=(1,), dtype=float)

    def get_observation_space(self) -> Box :
        return Box(low=np.array([MIN_POWER, MIN_EFFICIENCY]), high=np.array([MAX_ELECTRIC_POWER, MAX_EFFICIENCY]), dtype=float)


    
    



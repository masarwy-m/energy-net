'''This code is based on https://github.com/intelligent-environments-lab/CityLearn/blob/master/citylearn/energy_model.py'''

from typing import Any, List
from entities.device import StorageDevice


INITAL_CAPACITY = 0.0

class Battery(StorageDevice):
    r"""Base electricity storage class.

    Parameters
    ----------
    capacity : float, default: 0.0
        Maximum amount of energy the storage device can store in [kWh]. Must be >= 0.
    
    Other Parameters
    ----------------
    **kwargs : Any
        Other keyword arguments used to initialize super classes.
    """
    def __init__(self, capacity: float = None, **kwargs: Any):
        self._capacity_history = []
        super().__init__(capacity=capacity, **kwargs)
        self._state_of_charge = INITAL_CAPACITY
        self._capacity_history = [self.capacity]


    @property
    def degraded_capacity(self) -> float:
        r"""Maximum amount of energy the storage device can store after degradation in [kWh]."""

        return self.capacity_history[-1]


    @property
    def capacity_history(self) -> List[float]:
        """Time series of maximum amount of energy the storage device can store in [kWh]."""

        return self._capacity_history
    
    @property
    def state_of_charge(self):
        return self._state_of_charge
    
    @state_of_charge.setter
    def state_of_charge(self, state_of_charge: float):
        assert state_of_charge >= INITAL_CAPACITY, 'state_of_charge must be >= INITAL_CAPACITY.'
        assert state_of_charge <= self.capacity, 'state_of_charge must be <= capacity.'
        self._state_of_charge = state_of_charge

    def update_state_of_charge(self, new_state_of_charge: float):
        r"""Update the state of charge of the battery."""

        self.state_of_charge = new_state_of_charge

    def reset(self):
        r"""Reset `Battery` to initial state."""

        super().reset()
        self._capacity_history = self._capacity_history[0:1]
        self._state_of_charge = INITAL_CAPACITY




    

        


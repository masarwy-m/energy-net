'''This code is based on https://github.com/intelligent-environments-lab/CityLearn/blob/master/citylearn/energy_model.py'''

from typing import Any, List
from entities.device import StorageDevice



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
        self._capacity_history = [self.capacity]


    @property
    def degraded_capacity(self) -> float:
        r"""Maximum amount of energy the storage device can store after degradation in [kWh]."""

        return self.capacity_history[-1]


    @property
    def capacity_history(self) -> List[float]:
        """Time series of maximum amount of energy the storage device can store in [kWh]."""

        return self._capacity_history

    def reset(self):
        r"""Reset `Battery` to initial state."""

        super().reset()
        self._capacity_history = self._capacity_history[0:1]




    

        


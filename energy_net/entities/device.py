'''This code is based on https://github.com/intelligent-environments-lab/CityLearn/blob/master/citylearn/energy_model.py'''
from typing import Any
import numpy as np
import sys
import os
sys.path.append(os.path.abspath('../network_entity.py'))
from defs import State
from network_entity import ElementaryNetworkEntity
from env.config import NO_EFFICIENCY, NO_CHARGE, MAX_CAPACITY, MIN_CHARGE, MIN_EFFICIENCY, MIN_CAPACITY
np.seterr(divide='ignore', invalid='ignore')

class Device(ElementaryNetworkEntity):
    """Base device class.

    Parameters
    ----------
    efficiency : float, default: 1.0
    Technical efficiency. Must be set to > 0.

    Other Parameters
    ----------------
    **kwargs : dict
        Other keyword arguments used to initialize super class.
    """

    def __init__(self, efficiency: float = None, **kwargs):
        super().__init__(**kwargs)
        self.efficiency = efficiency
        self.init_efficiency = efficiency

    @property
    def efficiency(self) -> float:
        """Technical efficiency."""
        return self.__efficiency

    @efficiency.setter
    def efficiency(self, efficiency: float):
        if efficiency is None:
            self.__efficiency = NO_EFFICIENCY 
        else:
            assert efficiency > MIN_EFFICIENCY, 'efficiency must be > 0.'
            self.__efficiency = efficiency

    def reset(self):
        """Reset the device to its initial state."""
        self.efficiency = self.init_efficiency
        

    
class StorageDevice(Device):
    """Base storage device class.

    Parameters
    ----------
    capacity : float, default: inf
        Maximum amount of energy the storage device can store in [kWh]. Must be >= 0.
    efficiency : float, default: 1.0
        Technical efficiency.
    inital_chage : float, default: 0.0
        Initial state of charge of the storage device.
    

    Other Parameters
    ----------------
    **kwargs : Any
        Other keyword arguments used to initialize super class.
    """
    
    def __init__(self, capacity: float = None, efficiency: float = None, inital_charge: float = None, **kwargs: Any):
        super().__init__(efficiency = efficiency, **kwargs)
        self.capacity = capacity if capacity is not None else MAX_CAPACITY
        self.state_of_charge = inital_charge if inital_charge is not None else NO_CHARGE
        self.init_capacity = self.capacity
        self.init_state_of_charge = self.state_of_charge

    @property
    def capacity(self) -> float:
        r"""Maximum amount of energy the storage device can store in [kWh]."""
        return self.__capacity
    
    @capacity.setter
    def capacity(self, capacity: float):
        capacity = MAX_CAPACITY if capacity is None else capacity
        assert capacity >= MIN_CAPACITY, 'capacity must be >= 0.'
        self.__capacity = capacity


    @property
    def state_of_charge(self):
        return self._state_of_charge
    
    @state_of_charge.setter
    def state_of_charge(self, state_of_charge: float):
        assert state_of_charge >= MIN_CHARGE, 'state_of_charge must be >= MIN_CHARGE.'
        assert state_of_charge <= self.capacity, 'state_of_charge must be <= capacity.'
        self._state_of_charge = state_of_charge

    def reset(self):
        """Reset `StorageDevice` to initial state."""
        super().reset()
        self.state_of_charge = self.init_state_of_charge
        self.capacity = self.init_capacity
        

    def get_current_state(self) -> State:
        """Return the current state of the `StorageDevice`."""
        return dict(state_of_charge=self.state_of_charge, capacity=self.capacity)
    
    def update_state(self, state: State):
        """Update the state of the `StorageDevice`."""
        self.state_of_charge = state['state_of_charge']
        self.capacity = state['capacity']
    
    
        



        


'''This code is based on https://github.com/intelligent-environments-lab/CityLearn/blob/master/citylearn/energy_model.py'''
from typing import Any
import numpy as np

from network_entity import ElementaryNetworkEntity
from config import NO_EFFICIENCY, NO_CHARGE, MAX_CAPACITY, MIN_CHARGE, MIN_EFFICIENCY, MIN_CAPACITY, INF
np.seterr(divide='ignore', invalid='ignore')



class Device(ElementaryNetworkEntity):
    """Base device class.

    Parameters
    ----------
    efficiency : float, default: 1.0
    Technical efficiency. Must be set to > 0.
    inital_efficiency : float, default: 1.0

    Other Parameters
    ----------------
    **kwargs : dict
        Other keyword arguments used to initialize super class.
    """

    def __init__(self, lifetime_constant: float = None, **kwargs):
        super().__init__(**kwargs)
        self.__lifetime_constant = lifetime_constant if lifetime_constant is not None else INF
        

    @property
    def lifetime_constant(self) -> float:
        """Technical efficiency."""
        return self.__lifetime_constant

    @lifetime_constant.setter
    def lifetime_constant(self, life_time_constant: float):
        self.__lifetime_constant = life_time_constant

    
    def dynamic_parametrs(self):
        return { 'lifetime_constant': self.lifetime_constant }
        

    
class StorageDevice(Device):
    """Base storage device class.

    Parameters
    ----------
    energy_capacity : float, default: inf
        Maximum amount of energy the storage device can store in [kWh]. Must be >= 0.
    power_capacity : float, default: inf
        Maximum amount of power the storage device can store in [kW]. Must be >= 0.
    charging_efficiency : float, default: 1.0
        Technical efficiency of the charging process. Must be > 0.
    discharging_efficiency : float, default: 1.0
        Technical efficiency of the discharging process. Must be > 0.
    inital_charge : float, default: 0.0
        Initial state of charge of the storage device.

    

    Other Parameters
    ----------------
    **kwargs : Any
        Other keyword arguments used to initialize super class.
    """
    def __init__(self, energy_capacity: float = None, 
                power_capacity: float = None,
                charging_efficiency: float = None,
                discharging_efficiency: float = None,
                inital_charge: float = None,
                **kwargs: Any):
        super().__init__(**kwargs)
        self.power_capacity = energy_capacity if energy_capacity is not None else MAX_CAPACITY
        self.energy_capacity = power_capacity if power_capacity is not None else MAX_CAPACITY
        self.charging_efficiency = charging_efficiency
        self.discharging_efficiency = discharging_efficiency
        self.state_of_charge = inital_charge if inital_charge is not None else NO_CHARGE
        self.init_power_capacity = self.power_capacity
        self.init_energy_capacity = self.energy_capacity
        self.init_state_of_charge = self.state_of_charge
        


    @property
    def power_capacity(self) -> float:
        r"""Maximum amount of power the storage device can store in [kW]."""
        return self.__power_capacity
    
    @power_capacity.setter
    def power_capacity(self, power_capacity: float):
        power_capacity = MAX_CAPACITY if power_capacity is None else power_capacity
        assert power_capacity >= MIN_CAPACITY, 'power_capacity must be >= 0.'
        self.__power_capacity = power_capacity

    @property
    def energy_capacity(self) -> float:
        r"""Maximum amount of energy the storage device can store in [kWh]."""
        return self.__energy_capacity
    
    @energy_capacity.setter
    def energy_capacity(self, energy_capacity: float):
        energy_capacity = MAX_CAPACITY if energy_capacity is None else energy_capacity
        assert energy_capacity >= MIN_CAPACITY, 'energy_capacity must be >= 0.'
        self.__energy_capacity = energy_capacity


    @property
    def charging_efficiency(self) -> float:
        r"""Technical efficiency of the charging process."""
        return self.__charging_efficiency
    
    @charging_efficiency.setter
    def charging_efficiency(self, charging_efficiency: float):
        charging_efficiency = NO_EFFICIENCY if charging_efficiency is None else charging_efficiency
        assert charging_efficiency > MIN_EFFICIENCY, 'charging_efficiency must be > 0.'
        self.__charging_efficiency = charging_efficiency


    @property
    def discharging_efficiency(self) -> float:
        r"""Technical efficiency of the discharging process."""
        return self.__discharging_efficiency
    
    @discharging_efficiency.setter
    def discharging_efficiency(self, discharging_efficiency: float):
        discharging_efficiency = NO_EFFICIENCY if discharging_efficiency is None else discharging_efficiency
        assert discharging_efficiency > MIN_EFFICIENCY, 'discharging_efficiency must be > 0.'
        self.__discharging_efficiency = discharging_efficiency


    @property
    def state_of_charge(self):
        r"""Current state of charge of the storage device."""
        return self._state_of_charge
    
    @state_of_charge.setter
    def state_of_charge(self, state_of_charge: float):
        assert state_of_charge >= MIN_CHARGE, 'state_of_charge must be >= MIN_CHARGE.'
        assert state_of_charge <= self.energy_capacity, 'state_of_charge must be <= capacity.'
        self._state_of_charge = state_of_charge

    def reset(self):
        """Reset `StorageDevice` to initial state."""
        super().reset()
        self.power_capacity = self.init_power_capacity
        self.energy_capacity = self.init_energy_capacity
        self.state_of_charge = self.init_state_of_charge
        

    
    
        



        


'''This code is based on https://github.com/intelligent-environments-lab/CityLearn/blob/master/citylearn/energy_model.py'''
from typing import Any
import numpy as np

from .params import DeviceParams, StorageParams
from ..network_entity import ElementaryNetworkEntity
from ..config import DEFAULT_EFFICIENCY, NO_CHARGE, MAX_CAPACITY, MIN_CHARGE, MIN_EFFICIENCY, MIN_CAPACITY, INF, \
    DEFAULT_LIFETIME_CONSTANT
from ..model.state import State, StorageState

np.seterr(divide='ignore', invalid='ignore')


class Device(ElementaryNetworkEntity):
    """Base device class.
    """

    def __init__(self, device_params:DeviceParams, init_state:State=None):
        super().__init__(device_params["name"], device_params["energy_dynamics"], init_state = init_state)
        self.__lifetime_constant = device_params["lifetime_constant"] if "lifetime_constant" in device_params else DEFAULT_LIFETIME_CONSTANT
        

    @property
    def lifetime_constant(self) -> float:
        """Technical efficiency."""
        return self.__lifetime_constant

    @lifetime_constant.setter
    def lifetime_constant(self, life_time_constant: float):
        self.__lifetime_constant = life_time_constant

    
    def dynamics_parameters(self):
        return {'lifetime_constant': self.__lifetime_constant }
        

    
class StorageDevice(Device):
    """Base storage device class.
    """
    def __init__(self, storage_params:StorageParams, init_state:State=None, init_time=None):
        state_of_charge = storage_params["inital_charge"] if storage_params["inital_charge"] is not None else NO_CHARGE
        charging_efficiency = storage_params["charging_efficiency"] if storage_params["charging_efficiency"] is not None else DEFAULT_EFFICIENCY
        discharging_efficiency =storage_params["discharging_efficiency"] if storage_params["discharging_efficiency"] is not None else DEFAULT_EFFICIENCY
        power_capacity = storage_params["energy_capacity"] if storage_params[
                                                                       "energy_capacity"] is not None else MAX_CAPACITY
        energy_capacity = storage_params["power_capacity"] if storage_params[
                                                                       "power_capacity"] is not None else MAX_CAPACITY
        if not init_state:
            init_state = StorageState(state_of_charge=state_of_charge, charging_efficiency= charging_efficiency, discharging_efficiency=discharging_efficiency, power_capacity=power_capacity, energy_capacity=energy_capacity, current_time=init_time)
        super().__init__(storage_params, init_state = init_state)



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
        charging_efficiency = DEFAULT_EFFICIENCY if charging_efficiency is None else charging_efficiency
        assert charging_efficiency > MIN_EFFICIENCY, 'charging_efficiency must be > 0.'
        self.__charging_efficiency = charging_efficiency


    @property
    def discharging_efficiency(self) -> float:
        r"""Technical efficiency of the discharging process."""
        return self.__discharging_efficiency
    
    @discharging_efficiency.setter
    def discharging_efficiency(self, discharging_efficiency: float):
        discharging_efficiency = DEFAULT_EFFICIENCY if discharging_efficiency is None else discharging_efficiency
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
        

    
    
        



        


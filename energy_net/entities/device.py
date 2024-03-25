'''This code is based on https://github.com/intelligent-environments-lab/CityLearn/blob/master/citylearn/energy_model.py'''
from typing import Any, Iterable, List, Mapping, Union
import numpy as np
import sys
import os
sys.path.append(os.path.abspath('../network_entity.py'))
from network_entity import NetworkEntity, ElementaryNetworkEntity
np.seterr(divide='ignore', invalid='ignore')

class Device(ElementaryNetworkEntity):
    r"""Base device class.

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

    @property
    def efficiency(self) -> float:
        """Technical efficiency."""
        return self.__efficiency

    @efficiency.setter
    def efficiency(self, efficiency: float):
        if efficiency is None:
            self.__efficiency = 1.0
        else:
            assert efficiency > 0, 'efficiency must be > 0.'
            self.__efficiency = efficiency

    def get_metadata(self) -> Mapping[str, Any]:
        return {
            **super().get_metadata(),
            'efficiency': self.efficiency
        }

class ElectricDevice(Device):
    r"""Base electric device class.

    Parameters
    ----------
    nominal_power : float, default: 0.0
        Electric device nominal power >= 0.

    Other Parameters
    ----------------
    **kwargs : Any
        Other keyword arguments used to initialize super class.
    """

    def __init__(self, nominal_power: float = None, **kwargs: Any):
        super().__init__(**kwargs)
        self.nominal_power = nominal_power

    @property
    def nominal_power(self) -> float:
        r"""Nominal power."""

        return self.__nominal_power

    @property
    def electricity_consumption(self) -> np.ndarray:
        r"""Electricity consumption time series [kWh]."""

        return self.__electricity_consumption

    @property
    def available_nominal_power(self) -> float:
        r"""Difference between `nominal_power` and `electricity_consumption` at current `time_step`."""

        return None if self.nominal_power is None else self.nominal_power - self.electricity_consumption[
            self.time_step]

    @nominal_power.setter
    def nominal_power(self, nominal_power: float):
        nominal_power = 0.0 if nominal_power is None else nominal_power
        assert nominal_power >= 0, 'nominal_power must be >= 0.'
        self.__nominal_power = nominal_power

    def get_metadata(self) -> Mapping[str, Any]:
        return {
            **super().get_metadata(),
            'nominal_power': self.nominal_power,
        }

    def update_electricity_consumption(self, electricity_consumption: float, enforce_polarity: bool = None):
        r"""Updates `electricity_consumption` at current `time_step`.

        Parameters
        ----------
        electricity_consumption: float
            Value to add to current `time_step` `electricity_consumption`. Must be >= 0.
        enforce_polarity: bool, default: True
            Whether to allow only positive `electricity_consumption` values. Some electric
            devices like :py:class:`citylearn.energy_model.Battery` may be bi-directional and
            allow electricity discharge thus, cause negative electricity consumption.
        """

        enforce_polarity = True if enforce_polarity is None else enforce_polarity
        assert not enforce_polarity or electricity_consumption >= 0.0, \
            f'electricity_consumption must be >= 0 but value: {electricity_consumption} was provided.'
        self.__electricity_consumption[self.time_step] += electricity_consumption

    def reset(self):
        r"""Reset `ElectricDevice` to initial state and set `electricity_consumption` at `time_step` 0 to = 0.0."""

        super().reset()
        self.__electricity_consumption = np.zeros(self.episode_tracker.episode_time_steps, dtype='float32')

class StorageDevice(Device):
    r"""Base storage device class.

    Parameters
    ----------
    capacity : float, default: 0.0
        Maximum amount of energy the storage device can store in [kWh]. Must be >= 0.
    efficiency : float, default: 0.9
        Technical efficiency.
    

    Other Parameters
    ----------------
    **kwargs : Any
        Other keyword arguments used to initialize super class.
    """
    
    def __init__(self, capacity: float = None, efficiency: float = None, **kwargs: Any):
        self.capacity = capacity
        super().__init__(efficiency = efficiency, **kwargs)

    @property
    def capacity(self) -> float:
        r"""Maximum amount of energy the storage device can store in [kWh]."""

        return self.__capacity
    
        """Efficiency square root."""

        return self.efficiency**0.5

    @capacity.setter
    def capacity(self, capacity: float):
        capacity = 0.0 if capacity is None else capacity
        assert capacity >= 0, 'capacity must be >= 0.'
        self.__capacity = capacity

    def get_metadata(self) -> Mapping[str, Any]:
        return {
            **super().get_metadata(),
            'capacity': self.capacity,
        }

    def reset(self):
        r"""Reset `StorageDevice` to initial state."""

        super().reset()


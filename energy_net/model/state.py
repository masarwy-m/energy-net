from typing import Callable, Any, TypedDict, Optional
import numpy as np
from ..config import MIN_PRODUCTION, NO_CONSUMPTION, DEFAULT_INIT_POWER


class State(TypedDict, total=False):
    pass

class BatteryState(State):
    energy_capacity:float
    power_capacity:float
    state_of_charge:float = DEFAULT_INIT_POWER
    charging_efficiency:float = DEFAULT_EFFICIENCY
    discharging_efficiency:float =
    current_time:float =


class ProducerState(np.ndarray):
    def __new__(cls, max_produce, production):
        obj = np.array([production, max_produce], dtype=np.float32).view(cls)
        return obj

    def __init__(self, max_produce, production=MIN_PRODUCTION):
        self.max_produce = max_produce
        self.production = production

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.max_produce = obj[1]
        self.production = obj[0]

    @property
    def max_produce(self):
        return self[1]

    @max_produce.setter
    def max_produce(self, value):
        if self.shape == ():
            return
        self[1] = value

    @property
    def production(self):
        return self[0]

    @production.setter
    def production(self, value):
        if self.shape == ():
            return
        self[0] = value


class ConsumerState(np.ndarray):
    def __new__(cls, max_electric_power, efficiency, consumption=NO_CONSUMPTION):
        obj = np.array([consumption, max_electric_power, efficiency], dtype=np.float32).view(cls)
        return obj

    def __init__(self, max_electric_power, efficiency, consumption=NO_CONSUMPTION):
        self.max_electric_power = max_electric_power
        self.efficiency = efficiency
        self.consumption = consumption

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.max_electric_power = obj[1]
        self.efficiency = obj[2]
        self.consumption = obj[0]

    @property
    def max_electric_power(self):
        return self[1]

    @max_electric_power.setter
    def max_electric_power(self, value):
        if self.shape == ():
            return
        self[1] = value

    @property
    def efficiency(self):
        return self[2]

    @efficiency.setter
    def efficiency(self, value):
        if self.shape == ():
            return
        self[2] = value

    @property
    def consumption(self):
        return self[0]

    @consumption.setter
    def consumption(self, value):
        if self.shape == ():
            return
        self[0] = value





from typing import Callable, Any, TypedDict, Optional
import numpy as np
from env.config import MIN_PRODUCTION, NO_CONSUMPTION


# EnergyAction = dict[str, Any]
Reward = dict[str, float]

AmountPricePair = tuple[float, float]
PriceList = list[AmountPricePair]
ProductionPredFn = Callable[[Any, ...], PriceList]
ProductionFn = Callable[[Any, ...], AmountPricePair]

Bid = [float, float]


##################### Actions ######################

class ChargeAction(TypedDict, total=False):
    charge: float

class ProduceAction(TypedDict, total=False):
    produce: float

class ConsumeAction(TypedDict, total=False):
    consume: float


class EnergyAction(TypedDict, total=False):
    produce: Optional[ProduceAction]
    consume: Optional[ConsumeAction]
    charge: Optional[ChargeAction]



##################### States ######################
State = dict[str, Any]

class BatteryState(np.ndarray):
    def __new__(cls, energy_capacity, power_capacity, state_of_charge, charging_efficiency, discharging_efficiency, lifetime_constant, current_time):
        obj = np.asarray([[energy_capacity], [power_capacity], [state_of_charge], [charging_efficiency], [discharging_efficiency], [lifetime_constant], [current_time]], dtype=float).view(cls)
        return obj

    def __init__(self, energy_capacity, power_capacity, state_of_charge, charging_efficiency, discharging_efficiency, lifetime_constant, current_time):
        self.energy_capacity = energy_capacity
        self.power_capacity = power_capacity
        self.state_of_charge = state_of_charge
        self.charging_efficiency = charging_efficiency
        self.discharging_efficiency = discharging_efficiency
        self.lifetime_constant = lifetime_constant
        self.current_time = current_time

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.current_time = obj[6, 0]
        self.lifetime_constant = obj[5, 0]
        self.discharging_efficiency = obj[4, 0]
        self.charging_efficiency = obj[3, 0]
        self.state_of_charge = obj[2, 0]
        self.power_capacity = obj[1, 0]
        self.energy_capacity = obj[0, 0]
        
    @property
    def current_time(self):
        return self[6, 0]

    @current_time.setter
    def current_time(self, value):
        self[6, 0] = value
        
    @property
    def lifetime_constant(self):
        return self[5, 0]

    @lifetime_constant.setter
    def lifetime_constant(self, value):
        self[5, 0] = value
        
    @property
    def discharging_efficiency(self):
        return self[4, 0]

    @discharging_efficiency.setter
    def discharging_efficiency(self, value):
        self[4, 0] = value
        
    @property
    def charging_efficiency(self):
        return self[3, 0]

    @charging_efficiency.setter
    def charging_efficiency(self, value):
        self[3, 0] = value
        
    @property
    def state_of_charge(self):
        return self[2, 0]

    @state_of_charge.setter
    def state_of_charge(self, value):
        self[2, 0] = value

    @property
    def power_capacity(self):
        return self[1, 0]

    @power_capacity.setter
    def power_capacity(self, value):
        self[1, 0] = value

    @property
    def energy_capacity(self):
        return self[0, 0]

    @energy_capacity.setter
    def energy_capacity(self, value):
        self[0, 0] = value

# class ProducerState(TypedDict):
#     max_produce: float
#     genrated_power: float


class ProducerState(np.ndarray):
    def __new__(cls, max_produce, production):
        obj = np.asarray([[production], [max_produce]], dtype=float).view(cls)
        return obj

    def __init__(self, max_produce, production=MIN_PRODUCTION):
        self.max_produce = max_produce
        self.production = production

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.max_produce = obj[1, 0]
        self.production = obj[0, 0]

    @property
    def max_produce(self):
        return self[1, 0]

    @max_produce.setter
    def max_produce(self, value):
        self[1, 0] = value

    @property
    def production(self):
        return self[0, 0]

    @production.setter
    def production(self, value):
        self[0, 0] = value



# class ConsumerState(TypedDict):
#     efficiency: float
#     max_electric_power : float

class ConsumerState(np.ndarray):
    def __new__(cls, max_electric_power, efficiency, consumption=NO_CONSUMPTION):
        obj = np.asarray([[consumption], [max_electric_power], [efficiency]], dtype=float).view(cls)
        return obj

    def __init__(self, max_electric_power, efficiency, consumption=NO_CONSUMPTION):
        self.max_electric_power = max_electric_power
        self.efficiency = efficiency
        self.consumption = consumption

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.max_electric_power = obj[1, 0]
        self.efficiency = obj[2, 0]
        self.consumption = obj[0, 0]

    @property
    def max_electric_power(self):
        return self[1, 0]

    @max_electric_power.setter
    def max_electric_power(self, value):
        self[1, 0] = value

    @property
    def efficiency(self):
        return self[2, 0]

    @efficiency.setter
    def efficiency(self, value):
        self[2, 0] = value

    @property
    def consumption(self):
        return self[0, 0]

    @consumption.setter
    def consumption(self, value):
        self[0, 0] = value





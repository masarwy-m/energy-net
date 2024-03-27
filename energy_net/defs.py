from typing import Callable, Any, TypedDict, Optional

# EnergyAction = dict[str, Any]
Reward = dict[str, float]

AmountPricePair = tuple[float, float]
PriceList = list[AmountPricePair]
ProductionPredFn = Callable[[Any, ...], PriceList]
ProductionFn = Callable[[Any, ...], AmountPricePair]

Bid = [float, float]


class EnergyAction(TypedDict, total=False):
    produce: Optional[float]
    consume: Optional[float]
    charge: Optional[float]

##################### States ######################
State = dict[str, Any]

class BatteryState(TypedDict):
    capacity: float
    state_of_charge: float

class PVState(TypedDict):
    nominal_power: float
    efficiency: float


class HeaterState(TypedDict):
    efficiency: float
    max_electric_power : float



##################### Constants ######################
INITAL_CAPACITY = 0.0
MAX_ELECTRIC_POWER = 100
NO_EFFICIENCY = 1
MIN_POWER = 0


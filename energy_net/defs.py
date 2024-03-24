from typing import Callable, Any, TypedDict

EnergyAction = dict[str, Any]
State = dict[str, Any]
Reward = dict[str, float]

AmountPricePair = tuple[float, float]
PriceList = list[AmountPricePair]
ProductionPredFn = Callable[[Any, ...], PriceList]
ProductionFn = Callable[[Any, ...], AmountPricePair]

Bid = [float, float]

class BatteryState(TypedDict):
    capacity: float
    state_of_charge: float

from typing import Callable, Any

EnergyAction = dict[str, Any]
State = dict[str, Any]
Reward = dict[str, float]

AmountPricePair = tuple[float, float]
PriceList = list[AmountPricePair]
ProductionPredFn = Callable[[Any, ...], PriceList]
ProductionFn = Callable[[Any, ...], AmountPricePair]

Bid = [float, float]

from typing import Callable, Any, TypedDict

AmountPricePair = tuple[float, float]
PriceList = list[AmountPricePair]
ProductionPredFn = Callable[[Any, ...], PriceList]
ProductionFn = Callable[[Any, ...], AmountPricePair]

Bid = [float, float]

class Bounds(TypedDict):
    low:Any
    high:Any
    dtype:Any
    shape:Any

from typing import Callable, Any, TypedDict, Optional

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

class BatteryState(TypedDict):
    capacity: float
    state_of_charge: float

class ProducerState(TypedDict):
    max_produce: float
    efficiency: float


class ConsumerState(TypedDict):
    efficiency: float
    max_electric_power : float



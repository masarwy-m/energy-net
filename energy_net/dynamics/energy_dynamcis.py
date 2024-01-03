from abc import abstractmethod, ABC
from typing import Callable, Any

AmountPricePair = tuple[float, float]
PriceList = list[AmountPricePair]

ProductionPredFn = Callable[[Any, ...], PriceList]
ProductionFn = Callable[[Any, ...], AmountPricePair]


class EnergyDynamics():
    @abstractmethod
    def do(self, action, params, cur_state):
        pass

    @abstractmethod
    def predict(self, action, params, state):
        pass


class ProductionDynamics(EnergyDynamics, ABC):
    def __init__(self, production_capacity):
        self.production_capacity = production_capacity


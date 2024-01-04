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


class ProductionDynamics(EnergyDynamics):
    pass

class StorageDynamics(EnergyDynamics):
    @abstractmethod
    def get_current_discharge_capability(self):
        pass

    @abstractmethod
    def predict_discharge_capability(self, state):
        pass

    @abstractmethod
    def get_current_charge_capability(self):
        pass

    @abstractmethod
    def predict_charge_capability(self, state):
        pass

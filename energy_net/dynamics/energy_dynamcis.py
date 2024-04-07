from abc import abstractmethod
import sys
import os
from numpy.typing import ArrayLike
import numpy as np 
sys.path.append(os.path.abspath('../defs.py'))
from defs import State

class EnergyDynamics():
    @abstractmethod
    def do(self, action: ArrayLike, state: np.ndarray, lifetime_constant: float):
        pass

    @abstractmethod
    def predict(self, action: ArrayLike, state: np.ndarray, lifetime_constant: float):
        pass


class ProductionDynamics(EnergyDynamics):
    @abstractmethod
    def get_current_production_capability(self):
        pass

    @abstractmethod
    def predict_production_capability(self, state: State):
        pass


class ConsumptionDynamics(EnergyDynamics):
    @abstractmethod
    def get_current_consumption_capability(self):
        pass

    @abstractmethod
    def predict_consumption_capability(self, state:State):
        pass

class StorageDynamics(EnergyDynamics):
    
    @abstractmethod
    def get_current_discharge_capability(self):
        pass

    @abstractmethod
    def predict_discharge_capability(self, state:State):
        pass

    @abstractmethod
    def get_current_charge_capability(self):
        pass

    @abstractmethod
    def predict_charge_capability(self, state:State):
        pass

class TransmissionDynamics(EnergyDynamics):
    pass



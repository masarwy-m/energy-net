from abc import abstractmethod
import sys
import os
sys.path.append(os.path.abspath('../defs.py'))
from defs import EnergyAction, State

class EnergyDynamics():
    @abstractmethod
    def do(self, action:EnergyAction, params, cur_state:State):
        pass

    @abstractmethod
    def predict(self, action:EnergyAction, params, cur_state:State):
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



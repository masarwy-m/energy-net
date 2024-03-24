from abc import abstractmethod, ABC
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
    pass

class ConsumptionDynamics(EnergyDynamics):
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
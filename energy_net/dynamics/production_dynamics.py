from ..config import DEFAULT_PRODUCTION
from ..dynamics.energy_dynamcis import  ProductionDynamics
from ..model.energy_action import EnergyAction
from ..model.state import State
from numpy.typing import ArrayLike

class PVDynamics(ProductionDynamics):
    def __init__(self) -> None:
        super().__init__()

    def do(self, action: EnergyAction, state:State=None , params= None) -> float:

        """Get solar generation output.
        """
        value = action['produce']
        if value is not None:
           return value
        else:
            return self.get_current_production(state,params)
    def get_current_production(self, state, params):
        return DEFAULT_PRODUCTION
    def predict(self, action, params, state):
        pass

    def get_current_production_capability(self):
        pass

    def predict_production_capability(self, state):
        pass
    


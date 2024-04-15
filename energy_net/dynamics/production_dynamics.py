from ..dynamics.energy_dynamcis import  ProductionDynamics
from ..model.energy_action import EnergyAction
from ..model.state import State
from numpy.typing import ArrayLike

class PVDynamics(ProductionDynamics):
    def __init__(self) -> None:
        super().__init__()

    def do(self, action: EnergyAction, state: State) -> float:

        """Get solar generation output.
        """
        value = action['produce']
        if value is not None:
           return value
        else:
            raise ValueError('Invalid action')

    
    def predict(self, action, params, state):
        pass

    def get_current_production_capability(self):
        pass

    def predict_production_capability(self, state):
        pass
    


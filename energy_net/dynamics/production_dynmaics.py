from dynamics.energy_dynamcis import  ProductionDynamics
from defs import EnergyAction, PVState

class PVDynamics(ProductionDynamics):
    def __init__(self) -> None:
        super().__init__()

    def do(self, action:EnergyAction, state:PVState) -> float: 
        r"""Get solar generation output.

        Parameters
        ----------
        action : EnergyAction
            Action to be performed. Must be a dictionary with a single key-value pair.
        state : PVState
            Current state of the PV array.
        return : float
            Solar generation output in [kW].
        """

        value = action.get('produce')
        if value is not None:
            return state['nominal_power'] * state['efficiency']
        else:
            raise ValueError('Invalid action')

    
    def predict(self, action, params, state):
        pass

    def get_current_production_capability(self):
        pass

    def predict_production_capability(self, state):
        pass
    


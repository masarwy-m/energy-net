from dynamics.energy_dynamcis import  ProductionDynamics
from defs import  ProducerState
from numpy.typing import ArrayLike

class PVDynamics(ProductionDynamics):
    def __init__(self) -> None:
        super().__init__()

    def do(self, action:ArrayLike, state:ProducerState, **parameters) -> ProducerState: 
        """Get solar generation output.

        Parameters
        ----------
        action : ArrayLike
            Action to be performed. Must be a ArrayLike.
        state : PVState
            Current state of the PV array.
        return : ProducerState
            New state of the PV array.
        """
        assert action.ndim == 1, 'Only one action is allowed'
        value = action[0]
        if value is not None:
            new_state = state.copy()
            new_state.production = min(value, state.max_produce)
            return new_state	
        else:
            raise ValueError('Invalid action')

    
    def predict(self, action, params, state):
        pass

    def get_current_production_capability(self):
        pass

    def predict_production_capability(self, state):
        pass
    


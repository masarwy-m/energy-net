from dynamics.energy_dynamcis import ConsumptionDynamics
from defs import EnergyAction, HeaterState


class ElectricHeaterDynamics(ConsumptionDynamics):
    def __init__(self) -> None:
        super().__init__()

    def do(self, action:EnergyAction, state:HeaterState) -> float:
        r"""Get electric heater consumption.
        
        Parameters
        ----------
        action : EnergyAction
            Action to be performed. Must be a dictionary with a single key-value pair.
        state : HeaterState
            Current state of the electric heater.
        return : float
            Electric heater consumption in [kW].
        """
        value = action.get('consume')
        if value is not None:
            return min(value, state['max_electric_power']) * state['efficiency']
        else:
            raise ValueError('Invalid action')

    
    def predict(self, action, params, state):
        pass

    def get_current_consumption_capability(self):
        pass

    def predict_consumption_capability(self, state):
        pass
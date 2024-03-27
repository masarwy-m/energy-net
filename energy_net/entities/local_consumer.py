from entities.device import ElectricDevice
from typing import Any
from defs import MAX_ELECTRIC_POWER, NO_EFFICIENCY, MIN_POWER, HeaterState



class ElectricHeater(ElectricDevice):
    r"""Base electric heater class.

    Parameters
    ----------
    nominal_power : float, default: None
        Maximum amount of electric power that the electric heater can consume from the power grid.
    efficiency : float, default: None
        Technical efficiency.

    Other Parameters
    ----------------
    **kwargs : Any
        Other keyword arguments used to initialize super class.
    """
    
    def __init__(self, nominal_power: float = None, efficiency: float = None, max_electric_power:float = None, **kwargs: Any):
        super().__init__(nominal_power = nominal_power, efficiency = efficiency, **kwargs)
        self.max_electric_power = MAX_ELECTRIC_POWER if max_electric_power is None else max_electric_power

    @ElectricDevice.efficiency.setter
    def efficiency(self, efficiency: float):
        efficiency = NO_EFFICIENCY if efficiency is None else efficiency   
        ElectricDevice.efficiency.fset(self, efficiency)

    @property
    def max_electric_power(self):
        return self._max_electric_power
    
    @max_electric_power.setter
    def max_electric_power(self, max_electric_power: float):
        assert max_electric_power >= MIN_POWER, 'max_electric_power must be >= MIN_POWER.'
        self._max_electric_power = max_electric_power

    @property
    def current_state(self) -> HeaterState:
        return dict(efficiency=self.efficiency, max_electric_power=self.max_electric_power)
   


from entities.device import ElectricDevice
from typing import Any
from defs import PVState


class PrivatePVProducer(ElectricDevice):
    r"""Base photovoltaic class.

    Parameters
    ----------
    nominal_power : float, default: 0.0
        PV output power in [kW]. Must be >= 0.

    Other Parameters
    ----------------
    **kwargs : Any
        Other keyword arguments used to initialize super class.
    """
    
    def __init__(self, nominal_power: float = None, **kwargs: Any):
        super().__init__(nominal_power=nominal_power, **kwargs)

    @property
    def current_state(self) -> PVState:
        return dict(nominal_power=self.nominal_power, efficiency=self.efficiency)

    



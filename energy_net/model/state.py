from typing import Callable, Any, TypedDict, Optional
import numpy as np
from ..config import MIN_PRODUCTION, NO_CONSUMPTION, DEFAULT_INIT_POWER, DEFAULT_EFFICIENCY, INITIAL_TIME, MAX_PRODUCTION, MAX_ELECTRIC_POWER


class State(TypedDict, total=False):
    pass

class BatteryState(State):
    energy_capacity:float
    power_capacity:float
    state_of_charge:float = DEFAULT_INIT_POWER
    charging_efficiency:float = DEFAULT_EFFICIENCY
    discharging_efficiency:float = DEFAULT_EFFICIENCY
    current_time:float = INITIAL_TIME



class ProducerState(State):
    max_produce:float = MAX_PRODUCTION
    production:float = MIN_PRODUCTION


class ConsumerState(State):
    max_electric_power:float = MAX_ELECTRIC_POWER
    efficiency:float = DEFAULT_EFFICIENCY
    consumption:float = NO_CONSUMPTION



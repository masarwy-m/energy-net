from typing import NamedTuple

from energy_net.dynamics.energy_dynamcis import EnergyDynamics


class DeviceParams(NamedTuple):
    name: str
    lifetime_constant: float
    max_electric_power: float
    init_max_electric_power: float
    consumption: float
    efficiency: float
    energy_dynamics: EnergyDynamics


class StorageParams(DeviceParams):
    energy_capacity: float
    power_capacity: float
    inital_charge: float
    charging_efficiency: float
    discharging_efficiency: float


class LoadParams(DeviceParams):
    energy_capacity: float
    power_capacity: float
    inital_charge: float


class ProductionParams(DeviceParams):
    max_producion: float

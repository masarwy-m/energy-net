from abc import ABC
from typing import Dict, Union
import numpy as np

from ..network_entity import NetworkEntity
from ..dynamics.energy_dynamcis import EnergyAction, EnergyDynamics  # TODO tell Itay about typo in dynamics
from ..model.state import ProsumerState, State, ConsumerState, StorageState


class Prosumer(NetworkEntity, ABC):
    def __init__(self, name: str, generation_capacity: float, current_output: float, demand: float,
                 storage_capacity: float,
                 energy_dynamics: EnergyDynamics):
        super().__init__(name)
        self.generation_capacity = generation_capacity  # in Megawatts (MW)
        self.current_output = current_output  # in Megawatts (MW)
        self.demand = demand  # in Megawatts (MW)
        self.storage_capacity = storage_capacity  # in Megawatt-hours (MWh)
        self.stored_energy = 0  # Initially zero stored energy
        self.energy_dynamics = energy_dynamics  # This will be a composite of various dynamics

    def step(self, action: Dict[str, Union[np.ndarray, EnergyAction]]) -> State:
        """ Apply the given action to the prosumer and update the state accordingly. """
        if not isinstance(action, dict):
            raise ValueError("Action must be a dictionary")
        try:
            # Handle battery actions
            if 'charge' in action or 'discharge' in action:
                battery_state = StorageState(state_of_charge=self.stored_energy, energy_capacity=self.storage_capacity)
                new_battery_state = self.energy_dynamics['battery'].do(action, battery_state)
                self.stored_energy = new_battery_state['state_of_charge']

            # Handle consumption actions
            if 'consume' in action:
                heater_state = ConsumerState(consumption=self.demand)
                new_heater_state = self.energy_dynamics['heater'].do(action, heater_state)
                self.demand = new_heater_state['consumption']

            # Handle production actions
            if 'produce' in action:
                pv_output = self.energy_dynamics['pv'].do(action)
                self.current_output = min(pv_output, self.generation_capacity)
        except Exception as e:
            raise RuntimeError(f"Failed to execute action: {e}")

        return self.get_current_state()

    def predict(self, action: EnergyAction, state: State) -> State:
        """ Predict the outcome of performing an action without changing the internal state. """
        return state  # Simplified for illustration

    def get_current_state(self) -> ProsumerState:
        """ Return the current comprehensive state of the prosumer using the ProsumerState class. """
        return ProsumerState(
            generation_capacity=self.generation_capacity,
            current_output=self.current_output,
            demand=self.demand,
            storage_capacity=self.storage_capacity,
            stored_energy=self.stored_energy
        )

    def update_state(self, state: ProsumerState) -> None:
        """ Update the prosumer's state. """
        self.generation_capacity = state.get('generation_capacity', self.generation_capacity)
        self.current_output = state.get('current_output', self.current_output)
        self.demand = state.get('demand', self.demand)
        self.storage_capacity = state.get('storage_capacity', self.storage_capacity)
        self.stored_energy = state.get('stored_energy', self.stored_energy)

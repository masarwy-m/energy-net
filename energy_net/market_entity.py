from abc import abstractmethod
from typing import List

from .model.state import State
from .model.action import EnergyAction
from .model.reward import Reward
from .defs import Bid
from .network_entity import NetworkEntity
from .grid_entities.load_bus import LoadBus
from .grid_entities.generator_bus import GeneratorBus


# TODO define proper actions

class MarketEntity():
    def __init__(self, name, network_entity: NetworkEntity):
        self.name = name
        self.network_entity = network_entity

    @abstractmethod
    def get_bid(self, bid_type: str, state: State, args) -> Bid:
        pass

    def step(self, action: EnergyAction) -> [State, Reward]:
        return self.network_entity.step(action)

    def predict(self, action: EnergyAction, state: State) -> [State, Reward]:
        return self.network_entity.predict(action, state)


class MarketProducer(MarketEntity):
    def __init__(self, name: str, generator_buses: List[GeneratorBus]):
        super().__init__(name)
        self.generator_buses = generator_buses  # A list of GeneratorBus instances representing the utility company

    def get_total_capacity(self) -> float:
        """Calculate the total generation capacity from all generator buses."""
        return sum(generator.capacity for generator in self.generator_buses)

    def get_total_current_output(self) -> float:
        """Calculate the total current output from all generator buses."""
        return sum(generator.current_output for generator in self.generator_buses)

    def update_output(self, new_outputs: List[float]):
        """Update the output for each generator bus."""
        if len(new_outputs) != len(self.generator_buses):
            raise ValueError("The number of new output values must match the number of generator buses.")
        for generator, new_output in zip(self.generator_buses, new_outputs):
            generator.update_output(new_output)

    def get_bid(self, bid_type: str, state: State, args) -> Bid:
        """Generate a bid based on the aggregated capacity of the utility company."""
        total_output = self.get_total_current_output()
        # Example bidding strategy: bid the total output with a price that decreases with higher output
        price_per_mw = self.calculate_price_per_mw(total_output)
        return Bid(price=price_per_mw, quantity=total_output)

    def calculate_price_per_mw(self, total_output):
        """Calculate the price per MW based on output."""
        pass

    def step(self, action: EnergyAction) -> [State, Reward]:
        """Perform actions that impact the whole utility company, adjusting outputs or other parameters."""
        # Assume action dictates new outputs
        new_outputs = [action.output_change * generator.current_output for generator in self.generator_buses]
        self.update_output(new_outputs)
        return self.network_entity.step(action)


class MarketConsumer(MarketEntity):
    def __init__(self, name: str, load_buses: List[LoadBus]):
        super().__init__(name)
        self.load_buses = load_buses  # A list of LoadBus instances representing the consumer's household

    def get_total_demand(self) -> float:
        """Calculate the total demand from all load buses in this household."""
        return sum(load_bus.demand for load_bus in self.load_buses)

    def update_demand(self, new_demands: List[float]):
        """Update the demand for each load bus in the household."""
        if len(new_demands) != len(self.load_buses):
            raise ValueError("The number of new demand values must match the number of load buses.")
        for load_bus, new_demand in zip(self.load_buses, new_demands):
            load_bus.update_demand(new_demand)

    def get_bid(self, bid_type: str, state: State, args) -> Bid:
        """Generate a bid based on the aggregated demand of the household."""
        total_demand = self.get_total_demand()
        # Example bidding strategy: bid the total demand with a price that increases with higher demand
        price_per_mw = self.calculate_price_per_mw(total_demand)
        return Bid(price=price_per_mw, quantity=total_demand)

    def calculate_price_per_mw(self, total_demand):
        """Calculate the price per MW based on demand."""
        pass

    def step(self, action: EnergyAction) -> [State, Reward]:
        """Perform actions that impact the whole household, adjusting demands or other parameters."""
        # Assume action dictates new demands
        new_demands = [action.demand_change * load_bus.demand for load_bus in self.load_buses]
        self.update_demand(new_demands)
        return self.network_entity.step(action)

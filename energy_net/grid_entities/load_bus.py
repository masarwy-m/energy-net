from ..network_entity import NetworkEntity
from .prosumer_connection import ProsumerConnection


class LoadBus(NetworkEntity):
    def __init__(self, name, voltage_level, demand):
        super().__init__(name)
        self.voltage_level = voltage_level
        self.demand = demand
        self.connections = []  # Connections to prosumers and possibly other loads

    def update_demand(self, new_demand):
        """Update the demand attribute safely."""
        if new_demand < 0:
            raise ValueError("Demand cannot be negative.")
        self.demand = new_demand

    def add_connection(self, connection: ProsumerConnection):
        """Add a new connection and update demand accordingly."""
        self.connections.append(connection)
        self.update_demand(self.calculate_total_demand())

    def calculate_total_demand(self):
        """Calculate total demand from all connections."""
        return sum(conn.power_flow for conn in self.connections)

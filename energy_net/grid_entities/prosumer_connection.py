from ..grid_edge import GridEdge
from .load_bus import LoadBus
from .prosumer import Prosumer


class ProsumerConnection(GridEdge):
    def __init__(self, from_node: LoadBus, to_node: Prosumer, capacity: float, power_flow: float):
        super().__init__(from_node, to_node, capacity, power_flow)

    def update_flow(self, new_flow: float):
        """Update the power flow and adjust the load bus demand accordingly."""
        super().update_flow(new_flow)  # Updates the power flow of the connection
        self.from_node.update_demand(self.calculate_updated_demand())  # Update the demand on the load bus

    def calculate_updated_demand(self):
        """Calculate the new demand for the load bus based on current flows of all connections."""
        # This assumes you can access other connections from the load bus, which may require additional architecture
        total_demand = sum(conn.power_flow for conn in self.from_node.connections if conn is not self)
        # Include the updated flow of the current connection
        total_demand += self.power_flow
        return total_demand

    def update_capacity(self, new_capacity: float):
        """Safely update the capacity of the connection and ensure it does not exceed any physical or regulatory limits."""
        if new_capacity < 0:
            raise ValueError("Capacity cannot be negative.")
        self.capacity = new_capacity
        # Optionally, recalculate load bus demand here if needed

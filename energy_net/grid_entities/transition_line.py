from ..grid_edge import GridEdge


class TransitionLine(GridEdge):
    def __init__(self, from_node, to_node, capacity, power_flow, impedance):
        super().__init__(from_node, to_node, capacity, power_flow)
        self.impedance = impedance  # in Ohms

    def update_impedance(self, new_impedance):
        if new_impedance < 0:
            raise ValueError("Impedance cannot be negative.")
        self.impedance = new_impedance

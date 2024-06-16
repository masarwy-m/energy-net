class GridEdge:
    def __init__(self, from_node, to_node, capacity, power_flow):
        self.from_node = from_node
        self.to_node = to_node
        self.capacity = capacity  # in Megawatts (MW)
        self.power_flow = power_flow  # in Megawatts (MW)

    def update_flow(self, new_flow):
        if 0 <= new_flow <= self.capacity:
            self.power_flow = new_flow
        else:
            raise ValueError("New flow exceeds capacity or is negative.")

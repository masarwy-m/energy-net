from energy_net.dynamics.energy_dynamcis import StorageDynamics

class StorageStationDynamics(StorageDynamics):
    def __init__(self, dc_capacity, net_connection_size, efficiency, capacity):
        self.dc_capacity = dc_capacity
        self.net_connection_size = net_connection_size
        self.efficiency = efficiency
        self.kibolet = capacity

        self.soc = 0



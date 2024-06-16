from abc import ABC

from ..network_entity import NetworkEntity


class GeneratorBus(NetworkEntity, ABC):
    def __init__(self, name, generation_capacity, current_output):
        super().__init__(name)
        self.generation_capacity = generation_capacity  # in Megawatts (MW)
        self.current_output = current_output  # in Megawatts (MW)

    def update_output(self, new_output):
        if 0 <= new_output <= self.generation_capacity:
            self.current_output = new_output
        else:
            raise ValueError("New output exceeds generation capacity or is negative.")

from typing import TypedDict


class EnergyAction(TypedDict, total=False):
    pass
class StorageAction(EnergyAction, total=False):
    charge: float

class ProduceAction(EnergyAction, total=False):
    produce: float = None

class ConsumeAction(EnergyAction, total=False):
    consume: float = None



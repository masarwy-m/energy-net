from typing import TypedDict
import numpy as np


class EnergyAction(TypedDict, total=False):
    pass

class StorageAction(EnergyAction, total=False):
    charge: float
    
    @classmethod
    def from_numpy(cls, arr: np.ndarray):
        if arr.size != 1:
            raise ValueError("Input array must have a single element")
        return cls(charge=float(arr[0]))

class ProduceAction(EnergyAction, total=False):
    produce: float = None
    @classmethod
    def from_numpy(cls, arr: np.ndarray):
        if arr.size != 1:
            raise ValueError("Input array must have a single element")
        return cls(produce=float(arr[0]))

class ConsumeAction(EnergyAction, total=False):
    consume: float = None
    @classmethod
    def from_numpy(cls, arr: np.ndarray):
        if arr.size != 1:
            raise ValueError("Input array must have a single element")
        return cls(consume=float(arr[0]))

class TradeAction(EnergyAction, total=False):
    amount: float


from typing import Any, List, Mapping, Tuple, Union
from abc import ABC, abstractmethod

class RewardFunction(ABC):
    r"""Base and default reward function class.

    Parameters
    ----------
    env_metadata: Mapping[str, Any]:
        General static information about the environment.
    **kwargs : dict
        Other keyword arguments for custom reward calculation.
    """
    
    def __init__(self, env_metadata: Mapping[str, Any],  **kwargs):
        self.env_metadata = env_metadata
        
    @property
    def env_metadata(self) -> Mapping[str, Any]:
        """General static information about the environment."""

        return self.__env_metadata
    
    
    @env_metadata.setter
    def env_metadata(self, env_metadata: Mapping[str, Any]):
        self.__env_metadata = env_metadata

    @abstractmethod
    def calculate(self, observations: List[Mapping[str, Union[int, float]]]) -> List[float]:
        r"""Calculates reward.

        Parameters
        ----------
        observations: List[Mapping[str, Union[int, float]]]

        Returns
        -------
        reward: List[float]
            Reward for transition to current timestep.
        """
        pass


class DummyRewardFunction(RewardFunction):
    r"""Dummy reward function class.

    Parameters
    ----------
    env_metadata: Mapping[str, Any]:
        General static information about the environment.
    **kwargs : dict
        Other keyword arguments for custom reward calculation.
    """
    
    def __init__(self, env_metadata: Mapping[str, Any],  **kwargs):
        super().__init__(env_metadata, **kwargs)
        
    def calculate(self, observations: List[Mapping[str, Union[int, float]]]) -> List[float]:
        r"""Calculates reward.

        Parameters
        ----------
        observations: List[Mapping[str, Union[int, float]]]

        Returns
        -------
        reward: List[float]
            Reward for transition to current timestep.
        """
        return [0.0 for _ in observations]
    
    
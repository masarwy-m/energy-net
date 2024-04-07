from abc import abstractmethod
from collections import OrderedDict
from dynamics.energy_dynamcis import EnergyDynamics
from utils.utils import AggFunc
from defs import EnergyAction, State, Reward
from gymnasium import spaces
import numpy as np
from numpy.typing import ArrayLike
from env.config import INF
class NetworkEntity:
    """
    This is a base class for all network entities. It provides an interface for stepping through actions,
    predicting the outcome of actions, getting the current state, updating the state, and getting the reward.
    """

    def __init__(self, lifetime_constant: float = None, name: str = 'entity'):
        """
        Constructor for the NetworkEntity class.

        Parameters:
        name (str): The name of the network entity.
        """
        self.name = name
        self.lifetime_constant = lifetime_constant if lifetime_constant is not None else INF 

    @abstractmethod
    def step(self, action: EnergyAction) -> [State, Reward]:
        """
        Perform the given action and return the new state and reward.

        Parameters:
        action (EnergyAction): The action to perform.

        Returns:
        list: The new state and reward after performing the action.
        """
        pass

    @abstractmethod
    def predict(self, action: EnergyAction, state: State) -> [State, Reward]:
        """
        Predict the outcome of performing the given action on the given state.

        Parameters:
        action (EnergyAction): The action to perform.
        state (State): The current state.

        Returns:
        list: The predicted new state and reward after performing the action.
        """
        pass
    
    @abstractmethod
    def get_current_state(self) -> State:
        """
        Get the current state of the network entity.

        Returns:
        State: The current state.
        """
        pass

    @abstractmethod
    def update_state(self, state: State) -> None:
        """
        Update the state of the network entity.

        Parameters:
        state (State): The new state.
        """
        pass

    @abstractmethod
    def get_reward(self) -> Reward:
        """
        Get the current reward of the network entity.

        Returns:
        Reward: The current reward.
        """
        pass


    @abstractmethod
    def reset(self) -> State:
        """
        Reset the state of the network entity.

        Returns:
        State: The initial state.
        """
        pass

    @abstractmethod
    def get_action_space(self) -> spaces:
        """
        Get the action space of the network entity.

        Returns:
        spaces: The action space.
        """
        pass

    @abstractmethod
    def get_observation_space(self) -> spaces:
        """
        Get the observation space of the network entity.

        Returns:
        spaces: The observation space.
        """
        pass

    @property
    def get_lifetime(self) -> float:
        return self.lifetime_constant



class CompositeNetworkEntity(NetworkEntity):
    """ 
    This class is a composite network entity that is composed of other network entities. It provides an interface for stepping through actions,
    predicting the outcome of actions, getting the current state, updating the state, and getting the reward.
    """
    def __init__(self, name: str, sub_entities:list[NetworkEntity], agg_func:AggFunc):
        super().__init__(name)
        self.sub_entities = OrderedDict({entity.name: entity for entity in sub_entities})
        self.agg_func = agg_func


    def step(self, actions):
        if type(actions) is np.ndarray:
            sub_entities = list(self.sub_entities.values())
            for index , action in enumerate(actions):
                sub_entities[index].step(np.array([action]))
        else:
            for name, action  in actions.items():
                self.sub_entities[name].step(action)


    def predict(self, action: EnergyAction, state: State):
        predictions = [entity.predict(action, state) for entity in self.sub_entities]
        return self.agg_func(predictions)


class ElementaryNetworkEntity(NetworkEntity):
    """
    This class is an elementary network entity that is composed of other network entities. It provides an interface for stepping through actions,
    predicting the outcome of actions, getting the current state, updating the state, and getting the reward.
    """
    def __init__(self, name, energy_dynamics:EnergyDynamics, lifetime_constant: float=INF):
        super().__init__(lifetime_constant, name)
        self.energy_dynamics = energy_dynamics

    def step(self, action: ArrayLike) -> [State, Reward]:
        state = self.get_current_state()
        new_state =  self.energy_dynamics.do(action, state, self.lifetime_constant)
        self.update_state(new_state)
        reward = self.get_reward()
        return new_state, reward

    def predict(self, action: EnergyAction, state: State):
        state = self.get_current_state()
        new_state =  self.energy_dynamics.do(action, state)
        reward = self.get_reward()
        return new_state, reward


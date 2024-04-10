from abc import abstractmethod
from collections import OrderedDict
from typing import Any, Union

from dynamics.energy_dynamcis import EnergyDynamics
from utils.utils import AggFunc
from defs import EnergyAction, State, Reward
from gymnasium import spaces
import numpy as np
from numpy.typing import ArrayLike


class NetworkEntity:
    """
    This is a base class for all network entities. It provides an interface for stepping through actions,
    predicting the outcome of actions, getting the current state, updating the state, and getting the reward.
    """

    def __init__(self, name: str ):
        """
        Constructor for the NetworkEntity class.

        Parameters:
        name (str): The name of the network entity.
        """
        self.name = name
        
    @abstractmethod
    def step(self, action: EnergyAction):
        """
        Perform the given action and return the new state and reward.

        Parameters:
        action (EnergyAction): The action to perform.

        Returns:
        list: The new state and reward after performing the action.
        """
        pass

    @abstractmethod
    def predict(self, action: EnergyAction, state: State):
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


class CompositeNetworkEntity(NetworkEntity):
    """ 
    This class is a composite network entity that is composed of other network entities. It provides an interface for stepping through actions,
    predicting the outcome of actions, getting the current state, updating the state, and getting the reward.
    """
    def __init__(self, name: str, sub_entities:list[NetworkEntity]):
        super().__init__(name)
        self.sub_entities = OrderedDict({entity.name: entity for entity in sub_entities})

    def step(self, actions: Union[np.ndarray, dict[str,Any]]):
        states= {}
        if type(actions) is np.ndarray:
            # we convert the entity dict to a list and match action to entities by index
            sub_entities = list(self.sub_entities.values())
            for index , action in enumerate(actions):
                states[sub_entities[index].name] = sub_entities[index].step(np.array([action]))
        else:
            for name, action  in actions.items():
                states[name] = self.sub_entities[name].step(action)

        return states

    def predict(self, actions: Union[np.ndarray, dict[str,Any]]):

        predicted_states = {}
        if type(actions) is np.ndarray:
            # we convert the entity dict to a list and match action to entities by index
            sub_entities = list(self.sub_entities.values())
            for index, action in enumerate(actions):
                predicted_states[sub_entities[index].name] = sub_entities[index].predict(np.array([action]))

        else:
            for name, action in actions.items():
                predicted_states[name] = self.sub_entities[name].predict(action)

        return predicted_states
    

class ElementaryNetworkEntity(NetworkEntity):
    """
    This class is an elementary network entity that is composed of other network entities. It provides an interface for stepping through actions,
    predicting the outcome of actions, getting the current state, updating the state, and getting the reward.
    """
    def __init__(self, name, energy_dynamics:EnergyDynamics):
        super().__init__(name)
        self.energy_dynamics = energy_dynamics

    def step(self, action: ArrayLike):
        state = self.get_current_state()
        new_state =  self.energy_dynamics.do(action, state, **self.dynamic_parametrs())
        self.update_state(new_state)
        return {self.name: new_state}

    def predict(self, action: EnergyAction, state: State):
        state = self.get_current_state()
        predicted_state = self.energy_dynamics.predict(action, state)
        return {self.name: predicted_state}

    @abstractmethod
    def dynamic_parametrs(self):
        pass
        


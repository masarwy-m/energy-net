from abc import abstractmethod
from dynamics.energy_dynamcis import EnergyDynamics
from utils import AggFunc
from defs import EnergyAction, State, Reward
from gymnasium import spaces
from numpy.typing import ArrayLike

class NetworkEntity:
    """
    This is a base class for all network entities. It provides an interface for stepping through actions,
    predicting the outcome of actions, getting the current state, updating the state, and getting the reward.
    """

    def __init__(self, name: str):
        """
        Constructor for the NetworkEntity class.

        Parameters:
        name (str): The name of the network entity.
        """
        self.name = name

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



class CompositeNetworkEntity(NetworkEntity):
    def __init__(self, name: str, sub_entities:list[NetworkEntity], agg_func:AggFunc):
        super().__init__(name)
        self.sub_entities = {entity.name: entity for entity in sub_entities}
        self.agg_func = agg_func


    def step(self, actions: EnergyAction):
        for name, action  in actions.items():
            self.sub_entities[name].step(action)


    def predict(self, action: EnergyAction, state: State):
        predictions = [entity.predict(action, state) for entity in self.sub_entities]
        return self.agg_func(predictions)


class ElementaryNetworkEntity(NetworkEntity):
    def __init__(self, name, energy_dynamics:EnergyDynamics):
        super().__init__(name)
        self.energy_dynamics = energy_dynamics

    def step(self, action: ArrayLike) -> [State, Reward]:
        state = self.get_current_state()
        new_state =  self.energy_dynamics.do(action, state)
        self.update_state(new_state)
        reward = self.get_reward()
        return new_state, reward

    def predict(self, action: EnergyAction, state: State):
        state = self.get_current_state()
        new_state =  self.energy_dynamics.do(action, state)
        reward = self.get_reward()
        return new_state, reward


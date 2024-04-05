from typing import Any, List, Mapping, Tuple, Union
from copy import copy
from functools import lru_cache
from pathlib import Path
from gymnasium import Env, spaces
from gymnasium.utils import seeding
from pettingzoo import ParallelEnv
import numpy as np
import logging

from network_entity import NetworkEntity
from defs import EnergyAction
from env.reward_function import RewardFunction
from env.config import DEFAULT_TIME_STEP


class EnergyNetEnv(ParallelEnv):

    ##################
    # Pettingzoo API #
    ##################

    metadata = {"name": "energy_net_env_v0"}

    def __init__(self,
        network_entities: List[NetworkEntity] = None,
        root_directory: Union[str, Path] = None, 
        simulation_start_time_step: int = None,
        simulation_end_time_step: int = None,
        episode_time_steps: int = None, 
        seconds_per_time_step: float = None,
        initial_seed: int = None,
        **kwargs: Any):


        self.network_entities = network_entities if network_entities is not None else self.default_network_entities()
        self.timestep = None
        self.simulation_start_time_step = simulation_start_time_step
        self.simulation_end_time_step = simulation_end_time_step
        self.time_step_num = simulation_end_time_step - simulation_start_time_step if simulation_end_time_step is not None and simulation_start_time_step is not None else DEFAULT_TIME_STEP
        self.num_entities = len(self.network_entities)
        

        # set random seed if specified
        self.__np_random = None
        self.seed(initial_seed)

        # pettingzoo required attributes
        self.entities = {entity.name: entity for _, entity in enumerate(self.network_entities)}
        self.possible_agents = list(self.entities.keys())
        self.agents = []
        

        self.__observation_space = self.get_observation_space()
        self.__action_space = self.get_action_space()

        # state and env objects
        self.__state = None




    def reset(self, seed=None, return_info=True, options=None):
        # set seed if given
        if seed is not None:
            self.seed(seed)

        

        # reset agents
        self.agents = self.possible_agents.copy()
        self.timestep = 0

        for entity in self.entities.values():
            entity.reset()

        # get all observations
        observations = self.__observe_all()

        if not return_info:
            return observations
        else:
            infos = {agent: {} for agent in self.agents}
            return observations, infos

    def seed(self, seed=None):
        self.__np_random, seed = seeding.np_random(seed)


    def step(self, actions: dict[str, EnergyAction]):

        # Perform the actions
        for agent_name, action in actions.items():
            self.entities[agent_name].step(action)

        terminations = {a: False for a in self.agents}
        
        rewards = {a: 0 for a in self.agents}
        # Get dummy infos (not used in this example)
        infos = {a: {} for a in self.agents}

        # Get the rewards
        for agent in self.agents:
            rewards[agent] = self.entities[agent].get_reward()
           
        # get new observations according to the current state
        obs = self.__observe_all()
        self.__action_space = self.get_action_space()


        # Check if the simulation has reached the end
        truncs = {a: False for a in self.agents}
        if self.timestep == self.time_step_num:
            truncs = {a: True for a in self.agents}
            self.agents = []

        self.timestep += 1
 

        return obs, rewards, terminations, truncs, infos  
    

   

    @lru_cache(maxsize=None)
    def observation_space(self, agent: str):
        return self.__observation_space[agent]

   
    def action_space(self, agent: str):
        return self.__action_space[agent]
    
    @property
    def possible_agents(self):
        return self.__possible_agents
    
    @possible_agents.setter
    def possible_agents(self, possible_agents: List[str]):
        self.__possible_agents = possible_agents
    

    ######################
    # End Pettingzoo API #
    ######################


    #######################
    # Extra API Functions #
    #######################
    
    def agent_iter(self):
        """
        Returns an iterator over all agents.
        """
        return iter(self.agents)


    def observe_all(self):
        """
        gets all agent observations for the given state.
        This is an API exposure of an inner method.

        Returns:
            a dictionary for all agent observations.
        """
        return self.__observe_all()
    
    def __observe_all(self):
        return {agent: self.entities[agent].get_current_state() for agent in self.agents}
    

    def get_observation_space(self):
        return {name: entity.get_observation_space() for name, entity in self.entities.items()}
    

    def get_action_space(self):
        return {name: entity.get_action_space() for name, entity in self.entities.items()}
    

    def default_network_entities(self):
        from entities.household import default_household
        household = default_household()
        return [household]
        







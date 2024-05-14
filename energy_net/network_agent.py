from abc import ABC, abstractmethod
from stable_baselines3 import SAC
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.monitor import Monitor
import numpy as np
import os
import matplotlib.pyplot as plt

class NetworkAgent(ABC):
    """
    Abstract base class for network agents.
    """

    @abstractmethod
    def train(self, env, **kwargs):
        """
        Train the agent on the given environment.
        """
        pass

    @abstractmethod
    def eval(self, env, **kwargs):
        """
        Evaluate the agent on the given environment.
        """
        pass

    @abstractmethod
    def plot(self, **kwargs):
        """
        Plot the training and evaluation results.
        """
        pass


class SACAgent(NetworkAgent):
    """
    Soft Actor-Critic (SAC) agent using Stable Baselines.
    """

    def __init__(self, env, policy, log_dir = './logs/', verbose=1):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.env = Monitor(env, log_dir)
        self.unwrapped = env
        self.policy = policy
        self.verbose = verbose
        self.model = None
        self.eval_callback = None
        self.eval_rewards = []
        self.train_rewards = []
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

    def train(self, total_timesteps=10000, log_interval=10, eval_freq=1000, progress_bar=True, **kwargs):
        self.eval_callback = EvalCallback(self.env, log_path=self.log_dir, eval_freq=eval_freq, best_model_save_path=self.log_dir)

        self.model = SAC(self.policy, self.env, verbose=self.verbose, **kwargs)
        self.env = self.model.env
        self.model.learn(total_timesteps=total_timesteps, progress_bar=progress_bar, log_interval=log_interval,
                         callback=self.eval_callback)

    def eval(self, n_episodes=5):
        rewards, _ = evaluate_policy(self.model, self.env, n_eval_episodes=n_episodes, deterministic=True, render=False)
        return np.mean(rewards)


    def choose_action(self, observation, deterministic=False):
        """
        Choose an action based on the given observation.

        Args:
            observation (np.ndarray): The observation from the environment.
            deterministic (bool): Whether to choose the action deterministically or stochastically.

        Returns:
            np.ndarray: The chosen action.
        """
        
        self.model.env.action_space = self.unwrapped.action_space
        self.model.policy.action_space = self.unwrapped.action_space
        return self.model.predict(observation, deterministic=deterministic)[0]

    def _log_rewards(self, locals_, globals_):
        self.train_rewards.append(locals_['episode_rewards'][-1])
        self.eval_rewards.append(locals_['eval_rewards'][-1])

    def plot(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.train_rewards, label='Training Rewards')
        plt.plot(self.eval_rewards, label='Evaluation Rewards')
        plt.xlabel('Episode')
        plt.ylabel('Reward')
        plt.title('Training and Evaluation Rewards')
        plt.legend()
        plt.show()


class RandomAgent(NetworkAgent):
    """
    A random agent that takes random actions in the environment.
    """

    def __init__(self, env):
        self.env = env
        self.train_rewards = []
        self.eval_rewards = []
        self.soc = []
        self.action = []

    def train(self, total_timesteps=1000):
        pass

    def eval(self, n_episodes=100):
        observation = self.env.reset()[0]
        for _ in range(n_episodes):
            self.soc.append(observation[0])
            action = self.env.action_space.sample()
            self.action.append(action.item())
            observation, reward, done, _, info = self.env.step(action)
            self.eval_rewards.append(reward)


            if done:
                observation, info = self.env.reset()
        return np.mean(self.eval_rewards)
    
    def choose_action(self, observation=None, deterministic=False):
        """
        Choose an action based on the given observation.

        Args:
            observation (np.ndarray): The observation from the environment.
            deterministic (bool): Whether to choose the action deterministically or stochastically.

        Returns:
            np.ndarray: The chosen action.
        """
        
        return self.env.action_space.sample()
                

    def plot(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.train_rewards, label='Training Rewards')
        plt.plot(self.eval_rewards, label='Evaluation Rewards')
        plt.xlabel('Episode')
        plt.ylabel('Reward')
        plt.title('Training and Evaluation Rewards')
        plt.legend()
        plt.show()
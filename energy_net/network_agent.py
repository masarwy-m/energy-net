from abc import ABC, abstractmethod
from stable_baselines3 import SAC
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import BaseCallback
import numpy as np
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


class RewardLogger(BaseCallback):
    """
    A custom callback to log the rewards during training and evaluation.
    """

    def __init__(self, verbose=0):
        super(RewardLogger, self).__init__(verbose)
        self.train_rewards = []
        self.eval_rewards = []

    def _on_step(self) -> bool:
        return True

    def _on_rollout_end(self):
        self.train_rewards.append(self.locals["episode_rewards"][-1])

    def _on_evaluation_end(self, locals_, globals_):
        self.eval_rewards.append(locals_["eval_rewards"][-1])


class SACAgent(NetworkAgent):
    """
    Soft Actor-Critic (SAC) agent using Stable Baselines.
    """

    def __init__(self, env, policy, verbose=1):
        self.env = env
        self.policy = policy
        self.verbose = verbose
        self.model = None
        self.eval_callback = None
        self.eval_rewards = []
        self.train_rewards = []

    def train(self, total_timesteps=10000, log_interval=10, eval_freq=1000, progress_bar=True, **kwargs):
        self.eval_callback = EvalCallback(self.env, best_model_save_path='./logs/',
                                          log_path='./logs/', eval_freq=eval_freq,
                                          deterministic=True, render=False,
                                          callback_after_eval=RewardLogger())

        self.model = SAC(self.policy, self.env, verbose=self.verbose, **kwargs)
        self.model.learn(total_timesteps=total_timesteps, progress_bar=True, log_interval=log_interval,
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
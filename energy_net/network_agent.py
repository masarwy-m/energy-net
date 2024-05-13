from abc import ABC, abstractmethod
from energy_net.utils.utils import plot_data
from stable_baselines3 import SAC
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import BaseCallback
import numpy as np
import os
import matplotlib.pyplot as plt
from stable_baselines3 import TD3
from stable_baselines3.common.noise import NormalActionNoise
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.results_plotter import plot_results, ts2xy, load_results
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common import results_plotter



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


# class RewardLogger(BaseCallback):
#     """
#     A custom callback to log the rewards during training and evaluation.
#     """

#     def __init__(self, verbose=0):
#         super(RewardLogger, self).__init__(verbose)
#         self.train_rewards = []
#         self.eval_rewards = []

#     def _on_step(self) -> bool:
#         return True

#     def _on_rollout_end(self):
#         self.train_rewards.append(self.locals["episode_rewards"][-1])

#     def _on_evaluation_end(self, locals_, globals_):
#         self.eval_rewards.append(locals_["eval_rewards"][-1])


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
        self.env = self.model.get_env()
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
                

    def plot(self):

        plot_data(self.eval_rewards, 'Rewards')

        # Plot actions
        plot_data(self.action, 'Actions')

        # Plot soc
        plot_data(self.soc, 'State of Charge (SoC)')




# class SaveOnBestTrainingRewardCallback(BaseCallback):
#     """
#     Callback for saving a model (the check is done every ``check_freq`` steps)
#     based on the training reward (in practice, we recommend using ``EvalCallback``).

#     :param check_freq: (int)
#     :param log_dir: (str) Path to the folder where the model will be saved.
#       It must contains the file created by the ``Monitor`` wrapper.
#     :param verbose: (int)
#     """

#     def __init__(self, check_freq: int, log_dir: str, verbose=1):
#         super().__init__(verbose)
#         self.check_freq = check_freq
#         self.log_dir = log_dir
#         self.save_path = os.path.join(log_dir, "best_model")
#         self.best_mean_reward = -np.inf

#     def _init_callback(self) -> None:
#         # Create folder if needed
#         if self.save_path is not None:
#             os.makedirs(self.save_path, exist_ok=True)

#     def _on_step(self) -> bool:
#         if self.n_calls % self.check_freq == 0:

#             # Retrieve training reward
#             x, y = ts2xy(load_results(self.log_dir), "timesteps")
#             if len(x) > 0:
#                 # Mean training reward over the last 100 episodes
#                 mean_reward = np.mean(y[-100:])
#                 if self.verbose > 0:
#                     print(f"Num timesteps: {self.num_timesteps}")
#                     print(
#                         f"Best mean reward: {self.best_mean_reward:.2f} - Last mean reward per episode: {mean_reward:.2f}"
#                     )

#                 # New best model, you could save the agent here
#                 if mean_reward > self.best_mean_reward:
#                     self.best_mean_reward = mean_reward
#                     # Example for saving best model
#                     if self.verbose > 0:
#                         print(f"Saving new best model to {self.save_path}.zip")
#                     self.model.save(self.save_path)

#         return True
    


class TD3Agent(NetworkAgent):
    """
    Twin Delayed Deep Deterministic Policy Gradient (TD3) agent using Stable Baselines.
    """

    def __init__(self, env, policy, verbose=1):
        self.env = env
        self.policy = policy
        self.verbose = verbose
        self.model = None
        self.log_dir = "./logs/"
        self.eval_callback = None
        self.eval_rewards = []
        self.train_rewards = []

    def train(self, total_timesteps=10000, log_interval=10, eval_freq=1000, progress_bar=True, eval_episodes=5, **kwargs):
        os.makedirs(self.log_dir, exist_ok=True)
        env = Monitor(self.env, self.log_dir)

        n_actions = env.action_space.shape[-1]
        action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

        self.eval_callback = EvalCallback(env, log_path=self.log_dir, eval_freq=1000, best_model_save_path=self.log_dir)

        self.model = TD3(self.policy, env, action_noise=action_noise, verbose=self.verbose, **kwargs)
        self.model.learn(total_timesteps=total_timesteps, progress_bar=progress_bar, log_interval=log_interval,
                         callback=self.eval_callback)

    def eval(self, n_episodes=5):
        rewards, _ = evaluate_policy(self.model, self.env, n_eval_episodes=n_episodes, deterministic=True, render=False)
        return np.mean(rewards)

    def _log_rewards(self, locals_, globals_):
        self.train_rewards.append(locals_['episode_rewards'][-1])
        self.eval_rewards.append(locals_['eval_rewards'][-1])

    def plot(self):
        results_plotter.plot_results(
            [self.log_dir], 1e5, results_plotter.X_TIMESTEPS, "TD3 LunarLander")


def moving_average(values, window):
    """
    Smooth values by doing a moving average
    :param values: (numpy array)
    :param window: (int)
    :return: (numpy array)
    """
    weights = np.repeat(1.0, window) / window
    return np.convolve(values, weights, "valid")



def plot_results(log_folder, title="Learning Curve"):
    """
    plot the results

    :param log_folder: (str) the save location of the results to plot
    :param title: (str) the title of the task to plot
    """
    x, y = ts2xy(load_results(log_folder), "timesteps")
    y = moving_average(y, window=50)
    # Truncate x
    x = x[len(x) - len(y):]

    fig = plt.figure(title)
    plt.plot(x, y)
    plt.xlabel("Number of Timesteps")
    plt.ylabel("Rewards")
    plt.title(title + " Smoothed")
    plt.show()
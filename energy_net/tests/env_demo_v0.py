
import sys
import os
import warnings

# Add the project's root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from env.single_entity_v0 import gym_env
from common import single_agent_cfgs

def test_gym_api():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        for env_name, env_cfg in single_agent_cfgs.items():
            seed = hash(env_name)
            seed = abs(hash(str(seed)))
            env = gym_env(**env_cfg, initial_seed=seed)
            observation, info = env.reset()
            for _ in range(1000):
                action = env.action_space.sample()  # agent policy that uses the observation and info
                # print(action, "action")
                observation, reward, terminated, truncated, info = env.step(action)
                # print(observation, "obs")
                
                if terminated or truncated:
                    observation, info = env.reset()
                    
        env.close()



if __name__ == '__main__':
    test_gym_api()


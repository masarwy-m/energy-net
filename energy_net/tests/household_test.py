import sys
import os
import warnings

from energy_net.dynamics.storage_dynamics import BatteryDynamics
from energy_net.entities.household import Household
from energy_net.entities.params import StorageParams

# Add the project's root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from env.single_entity_v0 import gym_env
from common import single_agent_cfgs

def test_household():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        # initialize devices
        device_params_arr=[]

        # initialize storage devices
        storage_params_arr=[]
        storage_params = StorageParams(name = 'test_battery', energy_capacity = 100, power_capacity = 200,inital_charge = 50, charging_efficiency = 1,discharging_efficiency = 1, lifetime_constant = 15, energy_dynamics = BatteryDynamics())
        storage_params_arr.append(storage_params)

        # initialize storage devices
        production_params_arr=[]


        # initilaize household
        household = Household(name="test_household",device_params_dict=device_params_arr, storage_params_dict=storage_params_arr, production_params_dict=production_params_arr)
        print(household.step())

        '''
        # initialize environment
        for env_name, env_cfg in single_agent_cfgs.items():
            seed = hash(env_name)
            seed = abs(hash(str(seed)))
            env = gym_env(**env_cfg, initial_seed=seed)
            observation, info = env.reset()

        # run simulation
        for _ in range(1000):
            action = env.action_space.sample()  # agent policy that uses the observation and info
            print("action:", action)
            observation, reward, terminated, truncated, info = env.step(action)
            #print(observation, "obs")

            if terminated or truncated:
                observation, info = env.reset()

        env.close()
        '''

if __name__ == '__main__':
    test_household()


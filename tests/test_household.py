
import warnings

import numpy as np

from energy_net.entities.params import StorageParams, ConsumptionParams, ProductionParams
from energy_net.model.action import EnergyAction, ProduceAction, StorageAction, ConsumeAction
from energy_net.dynamics.consumption_dynamics import HouseholdConsumptionDynamics
from energy_net.dynamics.production_dynamics import PVDynamics
from energy_net.dynamics.storage_dynamics import BatteryDynamics
from energy_net.entities.household import Household
from energy_net.entities.params import StorageParams, ConsumptionParams, ProductionParams
from energy_net.config import DEFAULT_LIFETIME_CONSTANT
# Add the project's root directory to sys.path
from energy_net.env.single_entity_v0 import gym_env
from common import single_agent_cfgs

def test_household():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        # initialize consumer devices
        consumption_params_arr=[]
        consumption_params = ConsumptionParams(name='household_consumption', energy_dynamics=HouseholdConsumptionDynamics(), lifetime_constant=DEFAULT_LIFETIME_CONSTANT)
        consumption_params_arr.append(consumption_params)
        consumption_params_dict = {'household_consumption': consumption_params}

        # initialize storage devices
        storage_params_arr=[]
        storage_params = StorageParams(name = 'test_battery', energy_capacity = 100, power_capacity = 200,inital_charge = 50, charging_efficiency = 1,discharging_efficiency = 1, lifetime_constant = 15, energy_dynamics = BatteryDynamics())
        storage_params_arr.append(storage_params)
        storage_params_dict = {'test_battery': storage_params}

        # initialize production devices
        production_params_arr=[]
        production_params = ProductionParams(name='test_pv', max_production=100, efficiency=0.9, energy_dynamics=PVDynamics())
        production_params_arr.append(production_params)
        production_params_dict = {'test_pv': production_params}

        # initilaize household
        household = Household(name="test_household", consumption_params_dict=consumption_params_dict, storage_params_dict=storage_params_dict, production_params_dict=production_params_dict, agg_func= None)

        # check individual actions
        household.perform_joint_action({'test_battery':StorageAction(charge=10), 'household_consumption': ConsumeAction(consume=None), 'test_pv': ProduceAction(produce=None)})

        # perform system step
        #household.system_step()

        # initialize pettingzoo environment wrapper
        #for env_name, env_cfg in single_agent_cfgs.items():
        #    seed = hash(env_name)
        #    seed = abs(hash(str(seed)))
        #    env = gym_env(**env_cfg, initial_seed=seed, network_entities=[household])

        #    observation, info = env.reset()

        '''
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


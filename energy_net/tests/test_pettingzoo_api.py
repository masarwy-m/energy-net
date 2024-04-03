
import sys
import os

# Add the project's root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from defs import EnergyAction, ChargeAction, ProduceAction, ConsumeAction
from entities.local_storage import Battery
from dynamics.storage_dynamics import BatteryDynamics
from entities.private_producer import PrivateProducer
from dynamics.production_dynmaics import PVDynamics
from entities.local_consumer import ConsumerDevice
from dynamics.consumption_dynamic import ElectricHeaterDynamics
from entities.household import HouseHold

from env.EnergyNetEnv import EnergyNetEnv
from pettingzoo.test import  parallel_api_test, performance_benchmark, parallel_seed_test


class TestEnergyNetEnv(unittest.TestCase):
    def setUp(self):
        self.battery = Battery(capacity=100, efficiency=0.9, energy_dynamics=BatteryDynamics(), name='test_battery')
        self.pv = PrivateProducer(max_produce=100, efficiency=0.9, energy_dynamics=PVDynamics(), name='test_pv')
        self.load = ConsumerDevice(efficiency=0.9, max_electric_power=100, energy_dynamics=ElectricHeaterDynamics(), name='test_heater')
        self.household = HouseHold(name='test_household', sub_entities=[self.battery, self.pv, self.load], agg_func=lambda x: x)
        self.env = EnergyNetEnv(network_entities=[self.household], 
            simulation_start_time_step=0,
            simulation_end_time_step=100, 
            episode_time_steps=100, 
            seconds_per_time_step=1, 
            reward_function=None, 
            random_seed=None)

    def test_reset(self):
        self.env.reset()

    def test_step(self):
        self.env.reset()
        
        action = {'test_household': EnergyAction()}
        self.env.step(action)

    def test_observe_all(self):
        self.env.reset()
        self.env.observe_all()

    def test_get_observation_space(self):
        self.env.observation_space(self.env.entities['test_household'].name)

    def test_get_action_space(self):
        self.env.action_space(self.env.entities['test_household'].name)

    
    def test_parallel_api(self):
        self.env.reset()
        parallel_api_test(self.env, num_cycles=1000)

    # def test_performance_benchmark(self):
    #     self.env.reset()
    #     performance_benchmark(self.env)


    # def test_parallel_seed_test(self):
    #     def parallel_env_fn():
    #         return self.env
    #     self.env.reset()
    #     parallel_seed_test(parallel_env_fn=parallel_env_fn)

    




if __name__ == '__main__':
    unittest.main()
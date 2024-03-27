import sys
import os

# Add the project's root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from defs import EnergyAction
from entities.local_storage import Battery
from dynamics.storage_dynamics import BatteryDynamics
from entities.private_producer import PrivatePVProducer
from dynamics.production_dynmaics import PVDynamics
from entities.local_consumer import ElectricHeater
from dynamics.consumption_dynamic import ElectricHeaterDynamics
from network_entity import HouseHold




class TestBattery(unittest.TestCase):
    def setUp(self):
        self.battery = Battery(capacity=100, efficiency=0.9, energy_dynamics=BatteryDynamics(), name='test_battery')

    def test_initialization(self):
        self.assertEqual(self.battery.capacity, 100)
        self.assertEqual(self.battery._capacity_history, [100])

    def test_degraded_capacity(self):
        self.assertEqual(self.battery.degraded_capacity, 100)

    def test_capacity_history(self):
        self.assertEqual(self.battery.capacity_history, [100])

    def test_energy_dynamics(self):
        new_state_of_charge = self.battery.step(action=EnergyAction(charge=10), state=dict(state_of_charge=self.battery.state_of_charge, capacity=self.battery.capacity))
        self.assertEqual(new_state_of_charge, 10)
        self.battery.update_state_of_charge(new_state_of_charge)
        self.assertEqual(self.battery.capacity, 100)
        self.assertEqual(self.battery.state_of_charge, 10)
        new_state_of_charge = self.battery.step(action=EnergyAction(charge=100), state=dict(state_of_charge=self.battery.state_of_charge, capacity=self.battery.capacity))
        self.assertEqual(new_state_of_charge, 100)
        self.battery.update_state_of_charge(new_state_of_charge)
        self.assertEqual(self.battery.capacity, 100)


class TestPV(unittest.TestCase):
    def setUp(self):
        self.pv = PrivatePVProducer(nominal_power=100, efficiency=0.9, energy_dynamics=PVDynamics(), name='test_pv')

    def test_initialization(self):
        self.assertEqual(self.pv.nominal_power, 100)

    def test_efficiency(self):
        self.assertEqual(self.pv.efficiency, 0.9)
        
    def test_energy_dynamics(self):
        new_production = self.pv.step(action=EnergyAction(produce=80), state=dict(nominal_power=self.pv.nominal_power, efficiency=self.pv.efficiency))
        self.assertEqual(new_production, 90)
        new_production = self.pv.step(action=EnergyAction(produce=100), state=dict(nominal_power=self.pv.nominal_power, efficiency=self.pv.efficiency))
        self.assertEqual(new_production, 90)

class TestHeater(unittest.TestCase):
    def setUp(self):
        self.heater = ElectricHeater(efficiency=0.9, max_electric_power=100, energy_dynamics=ElectricHeaterDynamics(), name='test_heater')

    def test_initialization(self):
        self.assertEqual(self.heater.max_electric_power, 100)

    def test_efficiency(self):
        self.assertEqual(self.heater.efficiency, 0.9)
        
    def test_energy_dynamics(self):
        new_consumption = self.heater.step(action=EnergyAction(consume=80), state=dict(efficiency=self.heater.efficiency, max_electric_power=self.heater.max_electric_power))
        self.assertEqual(new_consumption, 80 * 0.9)
        new_consumption = self.heater.step(action=EnergyAction(consume=110), state=dict(efficiency=self.heater.efficiency, max_electric_power=self.heater.max_electric_power))
        self.assertEqual(new_consumption, 90)

class TestHouseHold(unittest.TestCase):
    def setUp(self):
        self.battery = Battery(capacity=100, efficiency=0.9, energy_dynamics=BatteryDynamics(), name='test_battery')
        self.pv = PrivatePVProducer(nominal_power=100, efficiency=0.9, energy_dynamics=PVDynamics(), name='test_pv')
        self.heater = ElectricHeater(efficiency=0.9, max_electric_power=100, energy_dynamics=ElectricHeaterDynamics(), name='test_heater')
        self.household = HouseHold(name='test_household', sub_entities=[self.battery, self.pv, self.heater], agg_func=lambda x: x)

    def test_step(self):
        self.household.step(action=EnergyAction(charge=10, produce=80, consume=80))
        
    

if __name__ == '__main__':
    unittest.main()
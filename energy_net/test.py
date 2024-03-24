import unittest
from defs import EnergyAction
from entities.local_storage import Battery
from dynamics.storage_dynamics import BatteryDynamics

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
        

if __name__ == '__main__':
    unittest.main()
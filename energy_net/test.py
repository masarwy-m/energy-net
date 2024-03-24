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
        self.battery.step(action=EnergyAction(charge=dict(charge_amount = 10, device=self.battery)))
        self.assertEqual(self.battery.capacity, 110)

if __name__ == '__main__':
    unittest.main()
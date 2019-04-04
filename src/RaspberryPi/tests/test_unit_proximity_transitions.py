import unittest
import sys
sys.path.append('classifier/')
sys.path.append('data/')
import s1_proximity
import data

class TestUnitProximityTransitions(unittest.TestCase):

    def setUp(self):
        self.data = data.Data()
        self.proximity = s1_proximity.ProximityState()

    def test_transition_19(self):
        self.data.set_proximity(19)
        ret = self.proximity.handle()

        self.assertTrue(ret == "Inductive", "The expected transition was Inductive, we got: " + ret)

    def test_transition_20(self):
        self.data.set_proximity(20)
        ret = self.proximity.handle()

        self.assertTrue(ret == "Proximity", "The expected transition was Proximity, we got: " + ret)

    def test_transition_10(self):
        self.data.set_proximity(10)
        ret = self.proximity.handle()

        self.assertTrue(ret == "Inductive", "The expected transition was Inductive, we got: " + ret)

    def test_transition_30(self):
        self.data.set_proximity(30)
        ret = self.proximity.handle()

        self.assertTrue(ret == "Proximity", "The expected transition was Proximity, we got: " +  ret)

if __name__ == '__main__':
    unittest.main()
    
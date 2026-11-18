import math, unittest
from orbits import *
class OrbitTests(unittest.TestCase):
    def test_same_orbit(self):
        t=hohmann(MU_EARTH,7e6,7e6)
        self.assertAlmostEqual(t.total_delta_v_m_s,0)
    def test_leo_geo(self):
        t=hohmann(MU_EARTH,EARTH_RADIUS+400e3,EARTH_RADIUS+35786e3)
        self.assertTrue(3800<t.total_delta_v_m_s<4000)
        self.assertTrue(18000<t.duration_s<22000)
    def test_retrograde_transfer(self):
        t=hohmann(MU_EARTH,4.2e7,7e6)
        self.assertLess(t.first_burn_m_s,0)
        self.assertLess(t.second_burn_m_s,0)
    def test_kepler(self):
        for e in (0,.2,.8,.99):
            E=solve_kepler(2.,e)
            self.assertAlmostEqual(E-e*math.sin(E),2)
    def test_circle_radius(self):
        p=position_2d(MU_EARTH,7000000,0,1452)
        self.assertAlmostEqual(math.hypot(*p),7000000)
if __name__=='__main__':unittest.main()

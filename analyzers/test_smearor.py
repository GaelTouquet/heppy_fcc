import unittest
from heppy_fcc.particles.tlv.particle import Particle
from ROOT import TLorentzVector
import random
import math
import copy
from heppy_fcc.particles.tlv.jet import Jet

def smear(particle_list, smear_factor):
    sm_list = []
    for ptc in particle_list:
        p4 = ptc.p4()
        f = random.gauss(1, smear_factor)
        sm_norm = f * p4.Vect().Mag()
        m = p4.M()
        new_E = math.sqrt( m*m + sm_norm*sm_norm )
        sm_ptc = copy.deepcopy(ptc)
        sm_ptc._tlv = TLorentzVector(p4.Px() * f,
                                     p4.Py() * f,
                                     p4.Pz() * f,
                                     new_E)
        sm_list.append(sm_ptc)
    return sm_list


class TestSmeeror(unittest.TestCase):


    def test_smeeror(self):
        ptcs = [ Particle(211, 1, TLorentzVector(1, 0, 0, 100)),
                 Particle(211, 1, TLorentzVector(2, 2, 2, 8.001)),
                 Jet(TLorentzVector(1, 0, 0, 100))
                 ]
        sm_ptcs = smear(ptcs, 0.02)
        self.assertEqual( ptcs[0].m(), sm_ptcs[0].m() )
        self.assertEqual( ptcs[0].eta(), sm_ptcs[0].eta() )
        self.assertEqual( ptcs[0].theta(), sm_ptcs[0].theta() )
        self.assertEqual( ptcs[0].phi(), sm_ptcs[0].phi() )
        self.assertEqual( ptcs[1].m(), sm_ptcs[1].m() )
        self.assertEqual( ptcs[1].eta(), sm_ptcs[1].eta() )
        self.assertEqual( ptcs[1].theta(), sm_ptcs[1].theta() )
        self.assertEqual( ptcs[1].phi(), sm_ptcs[1].phi() )
        self.assertEqual( ptcs[2].eta(), sm_ptcs[2].eta() )
        self.assertEqual( ptcs[2].theta(), sm_ptcs[2].theta() )
        self.assertEqual( ptcs[2].phi(), sm_ptcs[2].phi() )

if __name__ == '__main__':
    unittest.main()

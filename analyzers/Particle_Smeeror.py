from heppy.framework.analyzer import Analyzer
from ROOT import TLorentzVector
import random
import math
import copy

class ParticleSmearor(Analyzer):
    """Takes a list of particles or jets and creates a smeered list of those.

    The objects of the list must have a p4() method that returns a 
    TLorentzVector."""

    def process(self, event):
        particles = getattr( event, self.cfg_ana.particles )
        smearfactor = self.cfg_ana.smearfactor
        sm_ptcs = []
        for ptc in particles:
            sm_ptc = copy.deepcopy( ptc )
            sm_ptc._tlv = smear( ptc.p4(), smearfactor )
            sm_ptcs.append( sm_ptc )
        setattr( event,
                ( 'smeared_'+self.cfg_ana.particles),
                sm_ptcs
                 )

def smear(tlv, smear_factor):
    """Takes a TLorentzVector and create a smeared copy with smearfactor width 
    on a gaussian distribution."""

    f = random.gauss( 1, smear_factor )
    sm_norm = f * tlv.Vect().Mag()
    m = tlv.M()
    new_E = math.sqrt( m*m + sm_norm*sm_norm )
    sm_tlv = TLorentzVector(tlv.Px() * f,
                            tlv.Py() * f,
                            tlv.Pz() * f,
                            new_E)
    return sm_tlv

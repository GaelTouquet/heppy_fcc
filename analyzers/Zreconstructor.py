from heppy.framework.analyzer import Analyzer
from heppy_fcc.particles.tlv.resonance import Resonance
from itertools import combinations

class Zreconstructor(Analyzer):


    def process(self, event):
        particles = getattr(event, self.cfg_ana.particles)
        setattr( event,
                 ('zcandidates_from_'+self.cfg_ana.particles),
                 [ Resonance(couple[0],couple[1],23) for couple in combinations(particles,2) ]
                 )

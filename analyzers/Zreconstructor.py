from heppy.framework.analyzer import Analyzer
from heppy_fcc.particles.tlv.resonance import Resonance as ZBoson
from itertools import combinations

class Zreconstructor(Analyzer):


    def process(self, event):
        particles = getattr(event, self.cfg_ana.particles)
        setattr( event,('zcandidates_from_'+self.cfg_ana.particles),
                         [ ZBoson(couple[0],couple[1],23) 
                           for couple in combinations(particles,2) ]
                 )
        #print
        #if getattr(event,('zcandidates_from_'+self.cfg_ana.particles),False ):
        #    print ('zcandidates_from_'+self.cfg_ana.particles)
        #    for zb in getattr(event, ('zcandidates_from_'+self.cfg_ana.particles)):
        #        print zb

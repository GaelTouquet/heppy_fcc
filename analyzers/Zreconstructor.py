from heppy.framework.analyzer import Analyzer
from heppy_fcc.particles.tlv.resonance import Resonance
from itertools import combinations

ZBoson = Resonance

class Zreconstructor(Analyzer):

    def process(self, event):
        event.zcandidates = []
        particles_by_type = dict()
        for ptc in event.gen_particles_stable:
            pdgid = abs(ptc.pdgid())
            if pdgid in [11, 13]:
                particles_by_type.setdefault( pdgid, []).append(ptc) 
        for types in particles_by_type:
            for couple in combinations(particles_by_type[types],2):
                event.zcandidates.append(ZBoson(couple[0],couple[1], 23))
        print 'Z candidates'
        for zcand in event.zcandidates:
            print zcand

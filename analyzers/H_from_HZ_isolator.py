from heppy.framework.analyzer import Analyzer
from heppy_fcc.particles.tlv.particle import Particle
from ROOT import TLorentzVector

class H_isolator(Analyzer):
    

    def process(self, event):
        if hasattr(event, 'zcand'):
            zcand = getattr(event, 'zcand')
            subprocess_ee = [ptc for ptc in event.gen_particles if abs(ptc.pdgid())==11 and ptc.status()==21]
            p4 = subprocess_ee[0].p4()+subprocess_ee[1].p4()
            p4 = p4 - zcand.p4()
            event.H_candidate=Particle( 25, 0, p4 )

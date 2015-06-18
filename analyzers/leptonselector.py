from heppy.framework.analyzer import Analyzer
from heppy.utils.deltar import inConeCollection
from heppy_fcc.particles.tlv.resonance import Resonance
import copy

class LeptonSelector(Analyzer):
    """Creates a lists of e and mu particles from event.gen_particles_stable in event.e_particles and event.mu_particles. Also adds the closest photons to the leptons p4."""

    def process(self, event):
        pdgid = self.cfg_ana.pdgid
        leptons = []
        photons = [ptc for ptc in event.gen_particles_stable if ptc.pdgid()==22 and ptc.e()>1]
        for ptc in event.gen_particles_stable:
            if abs(ptc.pdgid()) == pdgid and ptc.e()>10:
                close_photons = inConeCollection(ptc, photons, 0.5)
                reso = copy.deepcopy(ptc)
                for photon in close_photons:
                    reso = Resonance(reso, photon, ptc.pdgid())
                leptons.append(reso)
        setattr(event, self.cfg_ana.particles, leptons)

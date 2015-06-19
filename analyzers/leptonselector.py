from heppy.framework.analyzer import Analyzer
from heppy.utils.deltar import inConeCollection
from heppy_fcc.particles.tlv.particle import Particle
import copy

class LeptonSelector(Analyzer):
    """Creates a lists of e and mu particles from event.gen_particles_stable in event.e_particles and event.mu_particles. Also adds the closest photons to the leptons p4."""

    def process(self, event):
        pdgid = self.cfg_ana.pdgid
        leptons = []
        for ptc in event.gen_particles_stable:
            if abs(ptc.pdgid()) == pdgid:
                other_ptcs = []
                for part in event.gen_particles_stable:
                    if part!=ptc:
                        if part.pdgid()==22:
                            if part.e()>0.5:
                                other_ptcs.append(part)
                        else:
                            other_ptcs.append(part)
                close_ptcs = inConeCollection(ptc, other_ptcs, 0.4)
                if any(particle.pdgid()!=22 for particle in close_ptcs):
                    continue
                reso = copy.deepcopy(ptc)
                for photon in [ph for ph in close_ptcs if ph.pdgid()==22]:
                    reso = Particle(ptc.pdgid(), ptc.q(), (reso.p4()+photon.p4()))
                leptons.append(reso)
        setattr(event, self.cfg_ana.particles, leptons)

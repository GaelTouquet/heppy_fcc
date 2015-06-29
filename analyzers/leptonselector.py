from heppy.framework.analyzer import Analyzer
from heppy.utils.deltar import inConeCollection
from heppy_fcc.particles.tlv.particle import Particle
import random
import copy

class LeptonSelector(Analyzer):
    """Creates a lists of e and mu particles from event.gen_particles_stable in event.e_particles and event.mu_particles. Also adds the closest photons to the leptons p4."""

    #def beginLoop(self, setup):
    #    super(LeptonSelector, self).beginLoop(setup)
    #    self.not_selected_events = 0

    def process(self, event):
        pdgid = self.cfg_ana.pdgid
        leptons = []
        event.not_selected_event = False
        for ptc in event.smeared_gen_particles_stable:
            if abs(ptc.pdgid()) == pdgid:
                if random.random() > self.cfg_ana.recognition_factor:
                    continue
                other_ptcs = []
                for part in event.smeared_gen_particles_stable:
                    if part!=ptc:
                        if part.pdgid()==22:
                            if part.e()>0.5:
                                other_ptcs.append(part)
                        else:
                            other_ptcs.append(part)
                if len(other_ptcs)==2 and any(part for part in other_ptcs if part.pdgid()==pdgid) and any(part for part in other_ptcs if part.pdgid()==22):
                    event.not_selected_event = True
                    self.not_selected_events += 1
                close_ptcs = inConeCollection(ptc, other_ptcs, 0.4)
                E_check = 0
                for part in close_ptcs:
                    E_check += part.e()
                if E_check>(0.2*ptc.e()):
                    continue
                reso = copy.deepcopy(ptc)
                for photon in [ph for ph in close_ptcs if ph.pdgid()==22]:
                    reso = Particle(ptc.pdgid(), ptc.q(), (reso.p4()+photon.p4()))
                leptons.append(reso)
        setattr(event, self.cfg_ana.particles, leptons)

    #def endLoop(self, setup):
    #    super(LeptonSelector, self).endLoop(setup)
    #    print 'not_selected_events :', self.not_selected_events

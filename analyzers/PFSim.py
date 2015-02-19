from heppy.framework.analyzer import Analyzer
from heppy_fcc.particles.physicsobjects import Particle 

import math
from heppy_fcc.fastsim.detectors.CMS import CMS
from heppy_fcc.fastsim.simulator import Simulator
from heppy_fcc.fastsim.vectors import Point
from heppy_fcc.fastsim.pfobjects import Particle as PFSimParticle
from heppy_fcc.fastsim.toyevents import particles
from heppy_fcc.display.core import Display
from heppy_fcc.display.geometry import GDetector
from heppy_fcc.display.pfobjects import GTrajectories

from ROOT import TLorentzVector, TVector3

def pfsimparticle(edmparticle):
    tp4 = TLorentzVector()
    core = edmparticle.read().Core
    p4 = core.P4
    tp4.SetPtEtaPhiM(p4.Pt, p4.Eta, p4.Phi, p4.Mass)
    vertex = TVector3()
    charge = core.Charge
    return PFSimParticle(tp4, vertex, charge, core.Type) 

class PFSimOutput(object):
    def __init__(self):
        self.genparticles_stable = []
        
        
class PFSim(Analyzer):
    def beginLoop(self, setup):
        # call the function of the base class defining self.counters
        # and self.averages
        super(PFSim, self).beginLoop(setup)
        self.cms = CMS()
        self.simulator = Simulator(self.cms)
        self.is_display = False
        self.init_display()
        
    def init_display(self):
        self.display = Display()
        self.gcms = GDetector(self.cms)
        self.display.register(self.gcms, layer=0, clearable=False)
        self.is_display = True
        
    def process(self, event):
        # move the following to a gen particle analyzer at some point 
        if self.is_display:
            self.display.clear()
        store = event.input
        output = PFSimOutput()
        edm_particles = store.get("GenParticle")
        pfsim_particles = []
        for ptc in edm_particles:
            core = ptc.read().Core
            if core.Status == 1 and core.P4.Pt>1.:
                pyptc = Particle(ptc) 
                output.genparticles_stable.append( pyptc )
                pfsim_particles.append(pfsimparticle(ptc))
                print pyptc
        if self.cfg_ana.verbose:
            print 'stable/all particles = {s}/{a}'.format(s=len(output.genparticles_stable),
                                                          a=len(edm_particles))
        self.simulator.simulate(pfsim_particles)
        self.display.register( GTrajectories(pfsim_particles), layer=1) 


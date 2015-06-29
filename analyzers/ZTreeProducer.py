from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy_fcc.analyzers.ntuple import *
from ROOT import TFile
import math

class ZTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(ZTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'z_tree.root']),
                              'recreate')
        self.tree = Tree( self.cfg_ana.tree_name,
                          self.cfg_ana.tree_title )
        bookZ(self.tree, 'z')
        bookZ(self.tree, 'leg1')
        bookZ(self.tree, 'leg2')
        bookJet(self.tree, 'jet1')
        bookJet(self.tree, 'jet2')
        bookJet(self.tree, 'jet3')
        bookParticle(self.tree, 'H')
        var(self.tree, 'leg1_leg2_acollinearity')
        var(self.tree, 'leg1_leg2_acoplanarity')

    def process(self, event):
        self.tree.reset()
        if event.not_selected_event == True:
            print 'found'
            return None
        zcands = getattr(event, 'zcands', [])
        if zcands != []:
            zcand = zcands[0]
        else:
            zcand = None
        if zcand:
            z = zcand
            fillZ(self.tree, 'z', z)
            fillZ(self.tree, 'leg1', z.leg1())
            fillZ(self.tree, 'leg2', z.leg2())
            acollinearity = 0
            for coord in ['Px','Py','Pz']:
                acollinearity += getattr(z.leg1().p4(), coord)()*getattr(z.leg2().p4(), coord)()
            acollinearity /= getattr(z.leg1().p4(), 'Mag')()*getattr(z.leg2().p4(), 'Mag')()
            if acollinearity >= 1.0 : acollinearity = 1. - (1e-12)
            if acollinearity <= -1.0 : acollinearity = -1. + (1e-12)
            acollinearity = math.acos(acollinearity)*180./(math.pi)
            fill(self.tree, 'leg1_leg2_acollinearity', acollinearity)
            acoplanarity = (z.leg1().p4().Vect().Unit().Cross(z.leg2().p4().Vect().Unit()))
            acoplanarity = abs(acoplanarity.z())
            acoplanarity = (math.asin(acoplanarity))*(180./(math.pi))
            fill(self.tree, 'leg1_leg2_acoplanarity', acoplanarity)
            if len(event.sorted_selected_jets)>0:
                sorted_jets = event.sorted_selected_jets
                jet = sorted_jets[0]
                fillJet(self.tree, 'jet1', jet)
                if( len(sorted_jets)>1 ):
                    jet = sorted_jets[1]
                    fillJet(self.tree, 'jet2', jet)
                    if( len(sorted_jets)>2 ):
                        jet = sorted_jets[2]
                        fillJet(self.tree, 'jet3', jet)
            fillParticle(self.tree, 'H', event.H_candidate)
            self.tree.tree.Fill()

    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()

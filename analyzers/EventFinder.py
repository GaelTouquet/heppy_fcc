from heppy.framework.analyzer import Analyzer

class EventFinder(Analyzer):

    def beginLoop(self, setup):
        super(EventFinder, self).beginLoop(setup)
        self.specialevents = []

    def process(self, event):
        for zcand in event.sorted_zcand:
            leg1 = zcand.leg1()
            leg2 = zcand.leg2()
            for anc in event.genbrowser.ancestors(leg1):
                if anc.status()==22 and anc.pdgid()!=23:
                    self.specialevents.append((event.iEv,zcand))
            for anc in event.genbrowser.ancestors(leg2):
                if anc.status()==22 and anc.pdgid()!=23:
                    self.specialevents.append((event.iEv,zcand))

    def endLoop(self, setup):
        print self.specialevents

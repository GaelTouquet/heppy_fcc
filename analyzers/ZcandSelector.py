from heppy.framework.analyzer import Analyzer

class Zcandselector(Analyzer):

    def process(self, event):
        zcand_types = self.cfg_ana.zcand_types
        zcands = []
        for typ in zcand_types:
            zcands.extend(getattr(event,
                                 'zcandidates_from_{typ}'.format(typ=typ),
                                 []))
        zcands = [cand for cand in zcands if cand.q()==0]
        sorted_zcands = sorted( zcands,
                               key = lambda x : abs(x.m() - 91.187621))
        if len(sorted_zcands)>0:
            event.zcands = sorted_zcands

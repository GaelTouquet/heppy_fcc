from heppy.framework.analyzer import Analyzer

class Zcandselector(Analyzer):

    def process(self, event):
        zcand_types = self.cfg_ana.zcand_types
        zcand = []
        for typ in zcand_types:
            zcand.extend(getattr(event,
                                 'zcandidates_from_{typ}'.format(typ=typ),
                                 []))
        
        sorted_zcand = sorted( zcand,
                               key = lambda x : abs(x.m() - 91.187621))
        if len(sorted_zcand)>0:
            event.zcands = sorted_zcand

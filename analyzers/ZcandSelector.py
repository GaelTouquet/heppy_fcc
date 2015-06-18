from heppy.framework.analyzer import Analyzer

class Zcandselector(Analyzer):

    def process(self, event):
        zcand = []
        zcand.extend(getattr(event,
                             'zcandidates_from_es',
                             []))
        zcand.extend(getattr(event,
                             'zcandidates_from_mus',
                             []))
        zcand.extend(getattr(event,
                             'zcandidates_from_jets_Zcandidates',
                             []))
        zcand.extend(getattr(event,
                             'zcandidates_from_smeared_es',
                             []))
        zcand.extend(getattr(event,
                             'zcandidates_from_smeared_mus',
                             []))
        zcand.extend(getattr(event,
                             'zcandidates_from_smeared_jets_Zcandidates',
                             []))
        sorted_zcand = sorted( zcand,
                               key = lambda x : abs(x.m() - 91.187621))
        if len(sorted_zcand)>0:
            event.zcand = sorted_zcand[0]

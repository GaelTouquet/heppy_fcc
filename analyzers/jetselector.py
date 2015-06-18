from heppy.framework.analyzer import Analyzer
from heppy.utils.deltar import cleanObjectCollection

class JetSelector(Analyzer):
    """Creates a lists of the three most energetic jets from event.gen_jets in event.jets_Zcandidates."""

    def process(self, event):
        if hasattr(event, self.cfg_ana.particle):
            zcand = getattr(event, self.cfg_ana.particle)
            legs = [zcand.leg1(), zcand.leg2()]
            selected_jets, useless = cleanObjectCollection( event.gen_jets,
                                                            legs,
                                                            0.5 )
            select_jets = [jet for jet in selected_jets if jet.e()>10]
            sorted_selected_jets = sorted([(jet.e(),jet) for jet in select_jets], reverse=True)
            event.sorted_selected_jets = [jet[1] for jet in sorted_selected_jets]
        else:
            event.sorted_selected_jets = []

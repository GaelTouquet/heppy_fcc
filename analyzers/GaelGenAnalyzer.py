from heppy.framework.analyzer import Analyzer
from heppy_fcc.tools.genbrowser import GenBrowser

class GaelGenAnalyzer(Analyzer):

    def process(self, event):
        event.genbrowser = GenBrowser(event.gen_particles,
                                      event.gen_vertices)

import os
import copy
import heppy.framework.config as cfg

# input component 
# several input components can be declared,
# and added to the list of selected components

gen_jobs = None
do_display = False
nevents_per_job = 20000

if gen_jobs>1:
    do_display = False

from heppy_fcc.samples.fccsamples import selected_event_type

selectedComponents  = selected_event_type

if gen_jobs:
    selectedComponents = []
    for i in range(gen_jobs):
        component = cfg.Component(''.join(['sample_Chunk',str(i)]), files=['dummy.root'])
        selectedComponents.append(component)
        

reader = None
if os.environ.get('FCCEDM'):
    from heppy_fcc.analyzers.FCCReader import FCCReader
    reader = cfg.Analyzer(
        FCCReader
        )    
elif os.environ.get('CMSSW_BASE'):
    from heppy_fcc.analyzers.CMSReader import CMSReader
    reader = cfg.Analyzer(
        CMSReader,
        gen_particles = 'genParticles',
        pf_particles = 'particleFlow'
        )
else:
    import sys
    sys.exit(1)

from heppy_fcc.analyzers.Gun import Gun
gun = cfg.Analyzer(
    Gun,
    pdgid = 130,
    ptmin = 0.,
    ptmax = 10.
)

from heppy_fcc.analyzers.GenAnalyzer import GenAnalyzer
genana = cfg.Analyzer(
    GenAnalyzer
)

from heppy_fcc.analyzers.leptonselector import LeptonSelector
es_selector = cfg.Analyzer(
    LeptonSelector,
    instance_label = 'es',
    particles = 'es',
    pdgid = 11
)

mus_selector = cfg.Analyzer(
    LeptonSelector,
    instance_label = 'mus',
    particles = 'mus',
    pdgid = 13
)

from heppy_fcc.analyzers.jetselector import JetSelector
es_jetselector = cfg.Analyzer(
    JetSelector,
    instance_label = 'es',
    particles = 'zcands'
)

mus_jetselector = cfg.Analyzer(
    JetSelector,
    instance_label = 'mus',
    particles = 'zcands'
)

from heppy_fcc.analyzers.Zreconstructor import Zreconstructor
smeared_ee_Zreconstructor = cfg.Analyzer(
    Zreconstructor,
    instance_label = 'ee',
    particles = 'smeared_es'
)

smeared_mumu_Zreconstructor = cfg.Analyzer(
    Zreconstructor,
    instance_label = 'mumu',
    particles = 'smeared_mus'
)

#jetjet_Zreconstructor = cfg.Analyzer(
#    Zreconstructor,
#    instance_label = 'jetjet',
#    particles = 'jets_Zcandidates'
#)

from heppy_fcc.analyzers.Particle_Smeeror import ParticleSmearor
mus_smearer = cfg.Analyzer(
    ParticleSmearor,
    instance_label = 'mus',
    particles = 'mus',
    smearfactor = 0.02
)

es_smearer = cfg.Analyzer(
    ParticleSmearor,
    instance_label = 'es',
    particles = 'es',
    smearfactor = 0.02
)

#jet_Smearor = cfg.Analyzer(
#    ParticleSmearor,
#    instance_label = 'jet',
#    particles = 'sorted_selected_jets',
#    smearfactor = 0.02
#)

from heppy_fcc.analyzers.ZcandSelector import Zcandselector
zcandselect = cfg.Analyzer(
    Zcandselector,
    zcand_types = ['smeared_es','smeared_mus','smeared_jets']
)

#from heppy_fcc.analyzers.EventFinder import EventFinder
#eventfinder = cfg.Analyzer(
#    EventFinder
#)

#from heppy_fcc.analyzers.GaelGenAnalyzer import GaelGenAnalyzer
#gaelgenana = cfg.Analyzer(
#    GaelGenAnalyzer
#)

from heppy_fcc.analyzers.H_from_HZ_isolator import H_isolator
h_isolator = cfg.Analyzer(
    H_isolator,
)

from heppy_fcc.analyzers.ZTreeProducer import ZTreeProducer
ztree = cfg.Analyzer(
    ZTreeProducer,
    tree_name = 'events',
    tree_title = 'Z'
)

from heppy_fcc.analyzers.PFSim import PFSim
pfsim = cfg.Analyzer(
    PFSim,
    display = do_display,
    verbose = False
)

from heppy_fcc.analyzers.JetClusterizer import JetClusterizer


genjets = cfg.Analyzer(
    JetClusterizer,
    instance_label = 'gen',
    particles = 'gen_particles_stable'
)

# jets from pfsim 

jets = cfg.Analyzer(
    JetClusterizer,
    instance_label = 'rec', 
    particles = 'particles'
)

from heppy_fcc.analyzers.JetAnalyzer import JetAnalyzer
jetana = cfg.Analyzer(
    JetAnalyzer,
    instance_label = 'rec', 
    jets = 'rec_jets',
    genjets = 'gen_jets'
)

from heppy_fcc.analyzers.JetTreeProducer import JetTreeProducer
tree = cfg.Analyzer(
    JetTreeProducer,
    instance_label = 'rec',
    tree_name = 'events',
    tree_title = 'jets',
    jets = 'rec_jets'
)

jetsequence = [
    jets,
    jetana, 
    tree
]

# pf jet sequence

pfjetsequence = copy.deepcopy(jetsequence)
for ana in pfjetsequence: 
    ana.instance_label = 'pf'
    if hasattr(ana, 'jets'):
        ana.jets = 'pf_jets'
    if hasattr(ana, 'particles'):
        ana.particles = 'pf_particles'
    


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    gun if gen_jobs else reader,
    pfsim,
    genjets,
    ] )

sequence.extend(jetsequence)
if os.environ.get('CMSSW_BASE'):
    sequence.extend(pfjetsequence)

gaelsequence = [
    #gaelgenana,
    es_selector,
    #mus_selector,
    es_smearer,
    #mus_smearer,
    smeared_ee_Zreconstructor,
    #smeared_mumu_Zreconstructor,
    #jetjet_Zreconstructor,
    zcandselect,
    es_jetselector,
    #mus_jetselector,
    h_isolator,
    ztree,
    #eventfinder
]

sequence.extend(gaelsequence)

# inputSample.files.append('albers_2.root')
# inputSample.splitFactor = 2  # splitting the component in 2 chunks

# finalization of the configuration object.
Events = None
if gen_jobs:
    from heppy.framework.eventsgen import Events 
elif os.environ.get('FCCEDM'):
    from ROOT import gSystem
    gSystem.Load("libdatamodel")
    from eventstore import EventStore as Events
elif os.environ.get('CMSSW_BASE'):
    from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)

    
if __name__ == '__main__':
    import sys
    from heppy.framework.looper import Looper
    import logging

    # next 2 lines necessary to deal with reimports from ipython
    logging.shutdown()
    reload(logging)
    logging.basicConfig(level=logging.ERROR)

    import random
    # for reproducible results
    random.seed(0xdeadbeef)

    def process(iev=None):
        if iev is None:
            iev = loop.iEvent
        loop.process(iev)
        if display:
            display.draw()

    def next():
        loop.process(loop.iEvent+1)
        if display:
            display.draw()            

    iev = None
    if len(sys.argv)==2:
        iev = int(sys.argv[1])
    loop = Looper( 'looper', config,
                   nEvents=nevents_per_job,
                   nPrint=5,
                   timeReport=True)
    pfsim = loop.analyzers[1]
    display = getattr(pfsim, 'display', None)
    simulator = pfsim.simulator
    detector = simulator.detector
    if iev is not None:
        process(iev)
    else:
        loop.loop()
        loop.write()

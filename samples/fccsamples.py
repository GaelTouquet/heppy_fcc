import heppy.framework.config as cfg

HZ = cfg.Component( 'HZ',
                    files = ['../rootfiles/HZ.root'])

WW = cfg.Component( 'WW',
                         files = ['../rootfiles/WW.root'])

WW_mumu = cfg.Component( 'WW_mumu',
                         files = ['../rootfiles/WW_mumu.root'])

WW_ee = cfg.Component( 'WW_ee',
                         files = ['../rootfiles/WW_ee.root'])

WW_tautau = cfg.Component( 'WW_tautau',
                         files = ['../rootfiles/WW_tautau.root'])

WW_mumu_ee = cfg.Component( 'WW_mumu_ee',
                         files = ['../rootfiles/WW_mumu_ee.root'])

#HZ_mumu = cfg.Component( 'HZ_mumu',
#                         files = ['../rootfiles/HZ_mumu.root'])
#
#HZ_mumu_ee = cfg.Component( 'HZ_mumu_ee',
#                         files = ['../rootfiles/HZ_mumu_ee.root'])
#
ZZ = cfg.Component( 'ZZ',
                    files = ['../rootfiles/ZZ.root'])

example = cfg.Component( 'example',
                    files = ['../gael/example.root'])

selected_event_type = [
    #WW
    #WW_mumu
    #WW_ee
    #WW_tautau
    #WW_mumu_ee
    #HZ
    #HZ_mumu
    #HZ_mumu_ee
    #ZZ
    example
]


#!/bin/env python

def var( tree, varName, type=float ):
    tree.var(varName, type)

def fill( tree, varName, value ):
    tree.fill( varName, value )

# simple particle

def bookParticle( tree, pName ):
    var(tree, '{pName}_e'.format(pName=pName))
    var(tree, '{pName}_pt'.format(pName=pName))
    var(tree, '{pName}_theta'.format(pName=pName))
    var(tree, '{pName}_eta'.format(pName=pName))
    var(tree, '{pName}_phi'.format(pName=pName))
    var(tree, '{pName}_m'.format(pName=pName))
    var(tree, '{pName}_px'.format(pName=pName))
    var(tree, '{pName}_py'.format(pName=pName))
    var(tree, '{pName}_pz'.format(pName=pName))

def fillParticle( tree, pName, particle ):
    fill(tree, '{pName}_e'.format(pName=pName), particle.e() )
    fill(tree, '{pName}_pt'.format(pName=pName), particle.pt() )
    fill(tree, '{pName}_theta'.format(pName=pName), particle.theta() )
    fill(tree, '{pName}_eta'.format(pName=pName), particle.eta() )
    fill(tree, '{pName}_phi'.format(pName=pName), particle.phi() )
    fill(tree, '{pName}_m'.format(pName=pName), particle.m() )
    fill(tree, '{pName}_px'.format(pName=pName), particle.p4().Px() )
    fill(tree, '{pName}_py'.format(pName=pName), particle.p4().Py() )
    fill(tree, '{pName}_pz'.format(pName=pName), particle.p4().Pz() )
    
# jet

def bookComponent( tree, pName ):
    var(tree, '{pName}_e'.format(pName=pName))
    var(tree, '{pName}_pt'.format(pName=pName))
    var(tree, '{pName}_num'.format(pName=pName))

def fillComponent(tree, pName, component):
    fill(tree, '{pName}_e'.format(pName=pName), component.e() )
    fill(tree, '{pName}_pt'.format(pName=pName), component.pt() )
    fill(tree, '{pName}_num'.format(pName=pName), component.num() )
    
    
pdgids = [211, 22, 130, 11, 13]
    
def bookJet( tree, pName ):
    bookParticle(tree, pName )
    for pdgid in pdgids:
        bookComponent(tree, '{pName}_{pdgid:d}'.format(pName=pName, pdgid=pdgid))
    # var(tree, '{pName}_npart'.format(pName=pName))

def fillJet( tree, pName, jet ):
    fillParticle(tree, pName, jet )
    for pdgid in pdgids:
        component = jet.constituents.get(pdgid, None)
        if component is not None:
            fillComponent(tree,
                          '{pName}_{pdgid:d}'.format(pName=pName, pdgid=pdgid),
                          component )
        else:
            import pdb; pdb.set_trace()
            print jet


# reconstructed Z (gael)

def bookZ( tree, pName ):
    var(tree, '{pName}_e'.format(pName=pName))
    var(tree, '{pName}_pt'.format(pName=pName))
    var(tree, '{pName}_theta'.format(pName=pName))
    var(tree, '{pName}_phi'.format(pName=pName))
    var(tree, '{pName}_m'.format(pName=pName))
    var(tree, '{pName}_pdgid'.format(pName=pName))
    var(tree, '{pName}_px'.format(pName=pName))
    var(tree, '{pName}_py'.format(pName=pName))
    var(tree, '{pName}_pz'.format(pName=pName))


def fillZ( tree, pName, particle ):
    fill(tree, '{pName}_e'.format(pName=pName), particle.e() )
    fill(tree, '{pName}_pt'.format(pName=pName), particle.pt() )
    fill(tree, '{pName}_theta'.format(pName=pName), particle.theta() )
    fill(tree, '{pName}_phi'.format(pName=pName), particle.phi() )
    fill(tree, '{pName}_m'.format(pName=pName), particle.m() )
    fill(tree, '{pName}_px'.format(pName=pName), particle.p4().Px() )
    fill(tree, '{pName}_py'.format(pName=pName), particle.p4().Py() )
    fill(tree, '{pName}_pz'.format(pName=pName), particle.p4().Pz() )
    if hasattr(particle, 'pdgid'):
        fill(tree, '{pName}_pdgid'.format(pName=pName), particle.pdgid())
    else:
        fill(tree, '{pName}_pdgid'.format(pName=pName), 0)

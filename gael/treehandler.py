from OfficialStyle import *
from ROOT import *
from ROOT import gDirectory
from cpyroot import *

import sys

#officialStyle(gStyle)

class Tree(object):

    def __init__(self, rootfile, sigma, nevents, name):
        self.name = name
        luminosity = (float(nevents)/(float(sigma)*1e12))
        self.factor = 500/luminosity
        self.rfile = TFile(rootfile)
        self.tree = self.rfile.Get('events')
        
    def build_cut(self, cut):
        return '{cut} * ({factor})'.format(cut=cut, factor=self.factor)

    def draw(self, var, cut, *args):
        self.tree.Draw(var, self.build_cut(cut), *args)

    def project(self, var, cut, bins, xmin, xmax, TreeStack):
        tree = self.tree
        hname = TreeStack.hname(self.name)
        hist = TH1F(hname, hname, bins, xmin, xmax)
        TreeStack.hists.append(hist)
        TreeStack.styles[self.name].formatHisto(hist)
        tree.Project(hname, var, cut)
        if TreeStack.histsum is None:
            TreeStack.histsum = hist.Clone(TreeStack.hname('sum'))
        else:
            TreeStack.histsum.Add(hist)
        TreeStack.stack.Add(hist)

    def __str__(self):
        return self.nevents

if __name__ == '__main__':

    t_WW = Tree('../rootfiles/analyzed_WW.root',
                '1.635e-08',
                '100000',
                'WW')
    t_HZ = Tree('../rootfiles/analyzed_HZ.root',
                '2.018e-10',
                '20000',
                'HZ')
    t_HZ_fr_ee = Tree('../rootfiles/analyzed_HZ-fr_ee.root',
                      '2.018e-10',
                      '20000',
                      'HZ_fr_ee')
    t_HZ_fr_mumu = Tree('../rootfiles/analyzed_HZ-fr_mumu.root',
                        '2.018e-10',
                        '20000',
                        'HZ_fr_mumu')
    t_ZZ = Tree('../rootfiles/analyzed_ZZ.root',
                '1.361e-09',
                '20000',
                'ZZ')
    t_ZZ_fr_ee = Tree('../rootfiles/analyzed_ZZ-fr_ee.root',
                      '1.361e-09',
                      '20000',
                      'ZZ-ee')
    t_ZZ_fr_mumu = Tree('../rootfiles/analyzed_ZZ-fr_mumu.root',
                        '1.361e-09',
                        '20000',
                        'ZZ-mumu')
    t_WW_mumu = Tree('../rootfiles/analyzed_WW_mumu.root',
                     '1.900e-10',#a preciser
                     '20000',
                     'WW_mumu')
    t_WW_ee = Tree('../rootfiles/analyzed_WW_ee.root',
                   '1.909e-10',
                   '20000',
                   'WW_ee')  
    t_WW_mumu_fr_ee = Tree('../rootfiles/analyzed_WW_mumu-fr_ee.root',
                           '1.900e-10',#a preciser
                           '20000',
                           'WW_mumu-ee')
    t_WW_ee_fr_ee = Tree('../rootfiles/analyzed_WW_ee-fr_ee.root',
                         '1.909e-10',
                         '20000',
                         'WW_ee-ee')
    t_WW_mumu_fr_mumu = Tree('../rootfiles/analyzed_WW_mumu-fr_mumu.root',
                           '1.909e-10',
                           '20000',
                           'WW_mumu-mumu')
    #t_WW_ee_fr_mumu = Tree('../rootfiles/analyzed_WW_ee-fr_mumu.root',
    #                     '1.909e-10',
    #                     '20000',
    #                     'WW_ee-mumu')
    t_WW_tautau = Tree('../rootfiles/analyzed_WW_tautau.root',
                       '1.909e-10',
                       '20000',
                       'WW_tautau')
    t_WW_tautau_fr_ee = Tree('../rootfiles/analyzed_WW_tautau-fr_ee.root',
                       '1.909e-10',
                       '20000',
                       'WW_tautau-ee')
    t_WW_tautau_fr_mumu = Tree('../rootfiles/analyzed_WW_tautau-fr_mumu.root',
                       '1.909e-10',
                       '20000',
                       'WW_tautau-mumu')
    t_HZ_mumu = Tree('../rootfiles/analyzed_HZ_mumu.root',
                     '6.606e-12',#a preciser
                     '20000',
                     'HZ_mumu')
    t_WW_mumu_ee = Tree('../rootfiles/analyzed_WW_mumu_ee.root',
                        '7.628e-10',
                        '20000',
                        'WW_mumu_ee')
    t_HZ_mumu_ee = Tree('../rootfiles/analyzed_HZ_mumu_ee.root',
                        '1.316e-11',
                        '20000',
                        'HZ_mumu_ee')
    treestack = TreeStack('H_m_stack')
    style_WW = Style(fillColor=4)
    style_HZ = Style(fillColor=2)
    style_ZZ = Style(fillColor=3)
    treestack.add(t_WW.name, t_WW.tree, style_WW)
    #treestack.add(t_WW_mumu.name, t_WW_mumu.tree, style_WW)
    #treestack.add(t_WW_ee.name, t_WW_ee.tree, style_WW)
    #treestack.add(t_WW_mumu_fr_ee.name, t_WW_mumu_fr_ee.tree, style_WW)
    #treestack.add(t_WW_ee_fr_ee.name, t_WW_ee_fr_ee.tree, style_WW)
    #treestack.add(t_WW_mumu_fr_mumu.name, t_WW_mumu_fr_mumu.tree, style_WW)
    #treestack.add(t_WW_tautau_fr_mumu.name, t_WW_tautau_fr_mumu.tree, style_WW)
    #treestack.add(t_WW_tautau_fr_ee.name, t_WW_tautau_fr_ee.tree, style_WW)
    #treestack.add(t_WW_ee_fr_mumu.name, t_WW_ee_fr_mumu.tree, style_WW)
    #treestack.add(t_WW_tautau.name, t_WW_tautau.tree, style_WW)
    #treestack.add(t_WW_mumu_ee.name, t_WW_mumu_ee.tree, style_WW)
    treestack.add(t_ZZ.name, t_ZZ.tree, style_ZZ)
    #treestack.add(t_ZZ_fr_ee.name, t_ZZ_fr_ee.tree, style_ZZ)
    #treestack.add(t_ZZ_fr_mumu.name, t_ZZ_fr_mumu.tree, style_ZZ)
    treestack.add(t_HZ.name, t_HZ.tree, style_HZ)
    #treestack.add(t_HZ_fr_ee.name, t_HZ_fr_ee.tree, style_HZ)
    #treestack.add(t_HZ_fr_mumu.name, t_HZ_fr_mumu.tree, style_HZ)
    #treestack.add(t_HZ_mumu.name, t_HZ_mumu.tree, style_HZ)
    #treestack.add(t_HZ_mumu_ee.name, t_HZ_mumu_ee.tree, style_HZ)
    cuts = []
    cuts.append('z_m>86.2 && z_m<96.2')
    cuts.append('leg1_leg2_acollinearity>100')
    cuts.append('leg1_leg2_acoplanarity>10')
    cuts.append('z_pt>10')
    cuts.append('z_q==0')
    cuts.append('abs(z_pz)<50')
    cut = ' && '.join(cuts)
    cut = '(' + cut
    cut += ')*({factor})'
    t_WW.project('H_m',cut.format(factor=t_WW.factor),50,50,150,treestack)
    #t_WW_mumu.project('H_m',cut.format(factor=t_WW_mumu.factor),50,50,150,treestack)
    #t_WW_ee.project('H_m',cut.format(factor=t_WW_ee.factor),50,50,150,treestack)
    #t_WW_mumu_fr_ee.project('H_m',cut.format(factor=t_WW_mumu_fr_ee.factor),50,50,150,treestack)
    #t_WW_ee_fr_ee.project('H_m',cut.format(factor=t_WW_ee_fr_ee.factor),50,50,150,treestack)
    #t_WW_tautau_fr_ee.project('H_m',cut.format(factor=t_WW_tautau_fr_ee.factor),50,50,150,treestack)
    #t_WW_tautau_fr_mumu.project('H_m',cut.format(factor=t_WW_tautau_fr_mumu.factor),50,50,150,treestack)
    #t_WW_mumu_fr_mumu.project('H_m',cut.format(factor=t_WW_mumu_fr_mumu.factor),50,50,150,treestack)
    #t_WW_ee_fr_mumu.project('H_m',cut.format(factor=t_WW_ee_fr_mumu.factor),50,50,150,treestack)
    #t_WW_tautau.project('H_m',cut.format(factor=t_WW_tautau.factor),25,50,150,treestack)
    #t_WW_mumu_ee.project('H_m',cut.format(factor=t_WW_mumu_ee.factor),50,50,150,treestack)
    t_ZZ.project('H_m',cut.format(factor=t_ZZ.factor),50,50,150,treestack)
    #t_ZZ_fr_ee.project('H_m',cut.format(factor=t_ZZ_fr_ee.factor),50,50,150,treestack)
    #t_ZZ_fr_mumu.project('H_m',cut.format(factor=t_ZZ_fr_mumu.factor),50,50,150,treestack)
    t_HZ.project('H_m',cut.format(factor=t_HZ.factor),50,50,150,treestack)
    #t_HZ_fr_ee.project('H_m',cut.format(factor=t_HZ_fr_ee.factor),50,50,150,treestack)
    #t_HZ_fr_mumu.project('H_m',cut.format(factor=t_HZ_fr_mumu.factor),50,50,150,treestack)    #t_HZ_mumu.project('H_m',cut.format(factor=t_HZ_mumu.factor),50,50,150,treestack)
    #t_HZ_mumu_ee.project('H_m',cut.format(factor=t_HZ_mumu_ee.factor),50,50,150,treestack)
    print treestack
    c1 = TCanvas()
    treestack.draw()

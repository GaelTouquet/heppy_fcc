from heppy.framework.analyzer import Analyzer
from collections import Counter

class AnalyzerTry(Analyzer):
    
    def beginLoop(self, setup):
        super(AnalyzerTry, self).beginLoop(setup)
        self.eventcounter = {'ee': 0, 'mumu': 0, 'tautau': 0, 'jetjet': 0, 'other' : 0}
        self.trueeventcounter = {'ee': 0, 'mumu': 0, 'tautau': 0, 'jetjet': 0, 'other': 0}
        self.poorlyrecocounter= {'ee': 0, 'mumu': 0, 'tautau': 0, 'jetjet': 0, 'other': 0}
        self.errorcounter = {'ee': 0,'mumu': 0,'tautau': 0, 'jetjet': 0, 'other': 0}
        self.Nevent=0

    def process(self, event):
        self.Nevent+=1
        true_decay_event = self.hardest_Z_decay_finder(event)
        ##recognizes events from generated particles
        particles = event.gen_particles_stable
        charged = [ptc for ptc in particles if ptc.q()]
        partcounter = Counter([x.pdgid() for x in charged])
        if len(charged)==0:
            self.eventcounter['other']+=1
            if true_decay_event!='other':
                self.errorcounter[true_decay_event]+=1
                self.poorlyrecocounter['other']+=1
        elif len(charged)==2 and partcounter[11]==partcounter[-11]==1:
            self.eventcounter['ee']+=1
            if true_decay_event!='ee':
                import pdb; pdb.set_trace()
                self.errorcounter[true_decay_event]+=1
                self.poorlyrecocounter['ee']+=1
        elif len(charged)==2 and partcounter[13]==partcounter[-13]==1:
            self.eventcounter['mumu']+=1
            if true_decay_event!='mumu':
                self.errorcounter[true_decay_event]+=1
                self.poorlyrecocounter['mumu']+=1
        else :
            chargedlepfree = [ptc for ptc in charged if ptc.pdgid() not in [11,-11,13,-13]]
            if len(chargedlepfree)<5:
                self.eventcounter['tautau']+=1
                if true_decay_event!='tautau':
                    self.errorcounter[true_decay_event]+=1
                    self.poorlyrecocounter['tautau']+=1
            else :
                self.eventcounter['jetjet']+=1
                if true_decay_event!='jetjet':
                    self.errorcounter[true_decay_event]+=1
                    self.poorlyrecocounter['jetjet']+=1
        print self.eventcounter
        print self.trueeventcounter

    def endLoop(self, setup):
        self.mainLogger.info(str(self.eventcounter))
        print 'counted events :', self.eventcounter
        print 'real events :', self.trueeventcounter
        print 'poorly recognized events :', self.errorcounter
        print 'efficacite :'
        for elem in self.trueeventcounter:
            if self.trueeventcounter[elem]!=0:
                print elem , float(self.trueeventcounter[elem]-self.errorcounter[elem])/float(self.trueeventcounter[elem])
        print 'purete :'
        for elem in self.trueeventcounter:
            if self.trueeventcounter[elem]!=0:
                print elem , float(self.poorlyrecocounter[elem])/float(self.eventcounter[elem])

    def hardest_Z_decay_finder(self, event):
        Z_decay_products = []
        particles = event.gen_particles
        if any((ptc.status()==22 and ptc.pdgid()==23) for ptc in particles):
            for ptcs in particles :
                if ptcs.status()==23:
                    Z_decay_products.append(ptcs.pdgid())
            for x in range(8):
                if  Z_decay_products==[x,-x] or Z_decay_products==[-x,x] :
                    self.trueeventcounter['jetjet']+=1
                    return 'jetjet'
            if Z_decay_products==[11,-11] or Z_decay_products==[-11,11] :
                self.trueeventcounter['ee']+=1
                return 'ee'
            elif Z_decay_products==[13,-13] or Z_decay_products==[-13,13]:
                self.trueeventcounter['mumu']+=1
                return 'mumu'
            elif Z_decay_products==[15,-15] or Z_decay_products==[-15,15]:
                self.trueeventcounter['tautau']+=1
                return 'tautau'
            else :
                self.trueeventcounter['other']+=1
                return 'other'
        return 'not Z'

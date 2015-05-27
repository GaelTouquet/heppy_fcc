from heppy.framework.analyzer import Analyzer

class EventCounter(Analyzer):
    
    def beginLoop(self, setup):
        super(EventCounter, self).beginLoop(setup)
        self.eventcounter = {'ee': 0, 'mumu': 0, 'tautau': 0, 'jetjet': 0, 'other' : 0}
        self.trueeventcounter = {'ee': 0, 'mumu': 0, 'tautau': 0, 'jetjet': 0, 'other': 0, 'not Z': 0}
        self.errorcounter = {'ee': 0,'mumu': 0,'tautau': 0, 'jetjet': 0, 'other': 0}

    def process(self, event):
        particles = event.gen_particles_stable
        sortedparticles = {'e': [], 'mu': [], 'hadrons': [], 'nu': []}
        true_decay_event = self.hardest_Z_decay_finder(event)

        #sorting out particles
        for ptc in particles: 
            if ptc.pdgid()!=22:
                if abs(ptc.pdgid())==11:
                    sortedparticles['e'].append(ptc)
                elif abs(ptc.pdgid())==13:
                    sortedparticles['mu'].append(ptc)
                elif abs(ptc.pdgid()) in [12,14,16]:
                    sortedparticles['nu'].append(ptc)
                else:
                    sortedparticles['hadrons'].append(ptc)

        #finding ee couple from Z decay
        if len(sortedparticles['e'])>1:
            while True:
                match = {'E': 70., 'elec': None, 'posi': None} #decided to put minimum energy reconstruction for Z at 70
                eleclist = [elec for elec in sortedparticles['e'] if elec.q()==-1]
                posilist = [posi for posi in sortedparticles['e'] if elec.q()==1]
                #finding best match
                for elec in eleclist:
                    for posi in posilist:
                        if abs(elec.e()+posi.e()-91.1876)<match['E']:
                            match['E']=elec.e()+posi.e()
                            match['elec']=elec
                            match['posi']=posi
                if match=={'E': 70., 'elec': None, 'posi': None}: break
                

            
            
       
        
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
        

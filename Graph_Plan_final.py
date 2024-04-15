import pddlpy
import pddl 
import random
from itertools import product

class Action:
    def __init__(self, name, preconditions_pos,preconditions_neg, effects_pos,effects_neg):
        self.name = name
        self.preconditions_pos = preconditions_pos
        self.preconditions_neg = preconditions_neg
        self.effects_pos = effects_pos
        self.effects_neg = effects_neg

    def is_applicable(self, state_pos,state_neg):
        bo_liste=[]
        for cond in self.preconditions_pos:
            bo_liste.append(False)
            for cond_ in state_pos:
                if str(cond)==str(cond_):
                    bo_liste[-1]=True
        
        for cond in self.preconditions_neg:
            bo_liste.append(False)
            for cond_ in state_neg:
                if str(cond)==str(cond_):
                    bo_liste[-1]=True
        return(all(bo_liste))
    
    def is_applicable_for_graph_plan(self, state_pos):
        bo_liste=[]
        for cond in self.preconditions_pos:
            bo_liste.append(False)
            for cond_ in state_pos:
                if str(cond)==str(cond_):
                    bo_liste[-1]=True
        return(all(bo_liste))

    def apply(self, state_pos,state_neg):
        if self.is_applicable(state_pos,state_neg):
            new_state_pos = state_pos.copy()
            new_state_neg = state_neg.copy()
            
            for neg in self.effects_neg :
                if neg in new_state_pos :
                    new_state_pos.remove(neg)
            for effect_pos in self.effects_pos:
                new_state_pos.append(effect_pos)
                
            for effect_neg in self.effects_neg:
                new_state_neg.append(effect_neg)
            
            for effect_pos in self.effects_pos:
                if effect_pos in new_state_neg :
                    new_state_neg.remove(effect_pos)
            return new_state_pos, new_state_neg
        else:
            return None
        
    def __hash__(self):
        return hash(self.name, self.preconditions_pos, self.preconditions_neg, self.effects_pos, self.effects_neg)

class GraphPlan:
    def __init__(self,domain_file, problem_file):

        parsed = Parseur(domain_file, problem_file)
        self.actions = parsed.actions
        self.init_pos = parsed.initial_state_pos
        self.init_neg = parsed.initial_state_neg
        self.goal = parsed.goal_state
        couche_initiale = parsed.initial_state_pos.copy()
        self.graph = []
        
        liste_couche_initiale_pos = []
        for etat in couche_initiale:
            liste_couche_initiale_pos.append([etat,[]])
        self.graph.append([liste_couche_initiale_pos,[]]) ## a faire ajouter none aux positions
        

    def ajouter_couche_action(self): 

        if len(self.graph)%2 == 0:
            print("Erreur, on ne peut pas ajouter une couche d'action après une couche d'action")
            return None
        nouvelle_couche_action = []

        # Ajouter l'action de ne rien faire
        for i in range(len(self.graph[- 1])):
            precon =self.graph[- 1][i]
            for j in range(len(precon)):
                nouvelle_couche_action.append([None, [(i,j)]]) # None signifie que c'est l'action ne rien faire

        # Ajouter les actions faisables
        list_for_applicable=[ x[0] for x in self.graph[-1][0] ]
        applicable_actions = [action for action in self.actions if action.is_applicable_for_graph_plan(list_for_applicable)]
        # Chercher les indices des preconditions de chaque action
        for action in applicable_actions:
            liste_positions_precedent = []
            for precondition_pos in action.preconditions_pos:
                for i, precond in enumerate(self.graph[-1][0]):
                    if precond[0] == precondition_pos:
                        liste_positions_precedent.append((0,i))
            
            for precondition_neg in action.preconditions_neg:
                for i, precond in enumerate(self.graph[-1][1]):
                    if precond[0] == precondition_neg:
                        liste_positions_precedent.append((1,i))
            
            nouvelle_couche_action.append([action,liste_positions_precedent])                  
                    
        self.graph.append(nouvelle_couche_action)
        
    
    def ajouter_couche_state(self):
        if len(self.graph)%2 == 1:
            print("Erreur, on ne peut pas ajouter une couche d'état après une couche d'état")
            return None
        nouvelle_couche_state_pos = []
        nouvelle_couche_state_neg = []

        seen_pos = {}
        seen_neg = {}
        for i,action in enumerate(self.graph[-1]):
            #Action ne rien faire
            if action[0] == None :
                position = action[1][0]
                etat_a_ajouter = self.graph[-2][position[0]][position[1]]
                if position[0]==0:
                    if not(etat_a_ajouter[0] in seen_pos.keys()) :
                        nouvelle_couche_state_pos.append([etat_a_ajouter[0],[i]])
                        seen_pos[etat_a_ajouter[0]] = (0,len(nouvelle_couche_state_pos)-1)
                    else :
                        position = seen_pos[etat_a_ajouter[0]]
                        nouvelle_couche_state_pos[position[1]][1].append(i)                    
                    
                    
                else :
                    if not(etat_a_ajouter[0] in seen_neg.keys()) :
                        nouvelle_couche_state_neg.append([etat_a_ajouter[0],[i]])
                        seen_neg[etat_a_ajouter[0]] = (1,len(nouvelle_couche_state_neg)-1)
                    else :
                        position = seen_neg[etat_a_ajouter[0]]
                        nouvelle_couche_state_neg[position[1]][1].append(i)
            # Actions applicables
            else :
                for effet in action[0].effects_pos:
                    if not(effet in seen_pos.keys()):
                        nouvelle_couche_state_pos.append([effet,[i]])
                        seen_pos[effet] = (0,len(nouvelle_couche_state_pos)-1)
                    else :
                        position = seen_pos[effet]
                        nouvelle_couche_state_pos[position[1]][1].append(i)

                for effet in action[0].effects_neg: 
                    if not(effet in seen_neg.keys()):
                        nouvelle_couche_state_neg.append([effet,[i]])
                        seen_neg[effet] = (0,len(nouvelle_couche_state_neg)-1)
                    else :
                        position = seen_neg[effet]
                        nouvelle_couche_state_neg[position[1]][1].append(i)
        
        self.graph.append([nouvelle_couche_state_pos,nouvelle_couche_state_neg])

    def add_mutex(self):

        mutex=[]
        for couche in self.graph:
            mutex_couche = []
            if len(mutex)%2==0 : # couche etat
                #Negation l'un de l'autre 
                for i,pos in enumerate(couche[0]):
                    for j,neg in enumerate(couche[1]):
                        if pos[0] == neg[0]:
                            mutex_couche.append(((0,i),(1,j)))
                        
                        #l'autre sur les littéraux / toute paire possible d’actions pouvant accomplir ces 2 littéraux est mutex
                liste_pos = [(0,i)for i in range(len(couche[0]))] + [(1,i)for i in range(len(couche[1]))]
                liste_pos_ = liste_pos.copy()
                for pos1 in liste_pos:
                    liste_pos_.remove(pos1)
                    for pos2 in liste_pos_:

                        liste_pos_action_precedent1 = couche[pos1[0]][pos1[1]][1]
                        liste_pos_action_precedent2 = couche[pos2[0]][pos2[1]][1]
                        ca_passe = False 
                        if liste_pos_action_precedent1 == [] or liste_pos_action_precedent2 == []:
                            ca_passe = True
                        for pos_action_precedent1, pos_action_precedent2 in product(liste_pos_action_precedent1,liste_pos_action_precedent2):
                            
                            if not((pos_action_precedent1,pos_action_precedent2) in mutex[-1]):
                                ca_passe = True
                                #break #pas sur

                        if ca_passe == False and not((pos1,pos2) in mutex_couche):
                            mutex_couche.append((pos1,pos2))
                
                            

                       

            
            else:   # couche action
                # Effet inconsistent & Interférence
                couche_=couche.copy()
                for i,action_ref in enumerate(couche) : 
                    couche_.remove(action_ref)
                    if action_ref[0] == None:
                        num_couche = len(mutex)
                        if action_ref[1][0][0] == 0:
                            effet_pos_ref = set([self.graph[num_couche-1][0][action_ref[1][0][1]][0]])
                            effet_neg_ref = set()
                            precondition_pos_ref = set([self.graph[num_couche-1][0][action_ref[1][0][1]][0]])
                            precondition_neg_ref = set()
                        else:
                            effet_pos_ref = set()
                            effet_neg_ref = set([self.graph[num_couche-1][1][action_ref[1][0][1]][0]])
                            precondition_pos_ref = set()
                            precondition_neg_ref = set([self.graph[num_couche-1][1][action_ref[1][0][1]][0]])
                    else:
                        effet_pos_ref=set(action_ref[0].effects_pos)
                        effet_neg_ref=set(action_ref[0].effects_neg)
                        precondition_pos_ref = set(action_ref[0].preconditions_pos)
                        precondition_neg_ref = set(action_ref[0].preconditions_neg)


                    for j,action_comparaison in enumerate(couche_):
                        
                        if action_comparaison[0] == None:
                            num_couche = len(mutex)

                            if action_comparaison[1][0][0] == 0:
                                effet_pos_comparaison = set([self.graph[num_couche-1][0][action_comparaison[1][0][1]][0]])
                                effet_neg_comparaison = set()
                                precondition_pos_comparaison = set([self.graph[num_couche-1][0][action_comparaison[1][0][1]][0]])
                                precondition_neg_comparaison = set()
                            else:
                                effet_pos_comparaison = set()
                                effet_neg_comparaison = set([self.graph[num_couche-1][1][action_comparaison[1][0][1]][0]])
                                precondition_pos_comparaison = set()
                                precondition_neg_comparaison = set([self.graph[num_couche-1][1][action_comparaison[1][0][1]][0]])
                        else:
                            effet_pos_comparaison=set(action_comparaison[0].effects_pos)
                            effet_neg_comparaison=set(action_comparaison[0].effects_neg)
                            precondition_pos_comparaison = set(action_comparaison[0].preconditions_pos)
                            precondition_neg_comparaison = set(action_comparaison[0].preconditions_neg)
                        





                        if (len(effet_pos_ref & effet_neg_comparaison) 
                            + len(effet_neg_ref & effet_pos_comparaison)
                            + len(precondition_pos_ref & effet_neg_comparaison)
                            + len(precondition_neg_ref & effet_pos_comparaison)
                            + len(precondition_pos_comparaison & effet_neg_ref)
                            + len(precondition_neg_comparaison & effet_pos_ref ) != 0):
                            mutex_couche.append((i,i+j+1))

                        
                        else: # Besoins concurrents
                            precond_ref, precond_comparaison =action_ref[1], action_comparaison[1]
                            cest_mutex = False
                            for precond_ref_, precond_comparaison_ in product(precond_ref,precond_comparaison):
                                if (precond_ref_, precond_comparaison_) in mutex[-1]:
                                    cest_mutex = True
                                    # break # pas sur de comment ça marche
                            
                            if cest_mutex:
                                mutex_couche.append((i,i+j+1))

            # Ajout de la couche
            mutex.append(mutex_couche)
        
        return mutex
    
    def update(self):
        self.ajouter_couche_action()
        self.ajouter_couche_state()

                                    
    

class Parseur:
    def __init__(self, domain_file, problem_file):

        self.object= list(pddlpy.DomainProblem(domain_file,problem_file).problem.objects)
        self.actions = self.parse_domain(domain_file,problem_file)
        self.initial_state_pos, self.initial_state_neg, self.goal_state = self.parse_problem_function(domain_file,problem_file)
        

    def parse_domain(self, domain_file,problem_file):
        domain = pddlpy.DomainProblem(domain_file,problem_file)
        actions = []
        for action in list( domain.operators()):
            name=action
            action_list=list(domain.ground_operator(name))
            for i in range(len(action_list)):
                var=list(action_list[i].variable_list.values())
                if all(elem in self.object for elem in var):
                    name = tuple( [str(action)] + [str(elem) for elem in var])
                    preconditions_pos = list(action_list[i].precondition_pos)
                    preconditions_neg = list(action_list[i].precondition_neg)
                    effects_pos=list(action_list[i].effect_pos)
                    effects_neg=list(action_list[i].effect_neg)
                    # variables_list=list(list(domain.ground_operator(name))[0].variable_list.values())
                    actions.append(Action(name, preconditions_pos,preconditions_neg,effects_pos,effects_neg))
            
        return actions
    

    def parse_problem_function(self, domain_file,problem_file):
        problem_pddly = pddlpy.DomainProblem(domain_file,problem_file)
        problem=pddl.parse_problem(problem_file)
        pb_list=list(problem.init)
        init_pos=[]
        init_neg=[]
        for predi in pb_list : 
            if isinstance(predi, pddl.logic.base.Not ):
                predi_intermedaire = predi.argument
                tuple_l = tuple([str(predi_intermedaire.name)] + [str(c.name) for c in predi_intermedaire.terms])
                init_neg.append(tuple_l)
            if isinstance(predi, pddl.logic.predicates.Predicate) :
                tuple_l = tuple([str(predi.name)] + [str(c.name) for c in predi.terms])
                init_pos.append(tuple_l)
        return init_pos, init_neg, list(problem_pddly.goals())

# Exemple d'utilisation
if __name__ == "__main__":
    domain_file = r"C:\Users\liams\Desktop\Cours\PO - Planification Automatique\generateur_pddl\domain.pddl"
    problem_file = r"C:\Users\liams\Desktop\Cours\PO - Planification Automatique\generateur_pddl\problems\pb_facile.pddl"
    problem = pddlpy.DomainProblem(domain_file,problem_file)

    gp = GraphPlan(domain_file, problem_file)
    gp.update()
    #gp.update()
    print(gp.goal)
    print(gp.graph)
    for action in gp.graph[1]:
        if action[0] != None:
            print(action[0].name)
    print(gp.add_mutex())

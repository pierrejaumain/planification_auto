import pddlpy
import pddl 
import random

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
    
    def is_applicable_for_graph_plan(self, state_pos,state_neg):
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

class GraphPlan:
    def __init__(self,actions,init_pos, init_neg, goal):
        self.actions = actions
        self.init_pos = init_pos
        self.init_neg = init_neg
        self.goal = goal
        couche_initiale = init_pos.copy()
        self.graph = []
        
        liste_couche_initiale_pos = []
        for etat in couche_initiale:
            liste_couche_initiale_pos.append([etat,None])
        self.graph.append([liste_couche_initiale_pos,[]]) ## a faire ajouter none aux positions
        

    def ajouter_couche_action(self): 

        if len(self.graph)%2 == 1:
            print("Erreur, on ne peut pas ajouter une couche d'action après une couche d'action")
            return None
        nouvelle_couche_action = []

        # Ajouter l'action de ne rien faire
        for i in range(len(self.graph[- 1])):
            precon =self.graph[- 1][i]
            for j in range(len(precon)):
                nouvelle_couche_action.append([None, [(i,j)]]) # None signifie que c'est l'action ne rien faire

        # Ajouter les actions faisables
        applicable_actions = [action for action in self.actions if action.is_applicable_for_graph_plan(self.graph[-1][0])]
        
        # Chercher les indices des preconditions de chaque action
        for action in applicable_actions:
            liste_positions_precedent = []
            for precondition_pos in action.precondition_pos:
                for i, precond in enumerate(self.graph[-1][0]):
                    if precond[0] == precondition_pos:
                        liste_positions_precedent.append((0,i))
            
            for precondition_neg in action.precondition_neg:
                for i, precond in enumerate(self.graph[-1][1]):
                    if precond[0] == precondition_neg:
                        liste_positions_precedent.append((1,i))
            
            nouvelle_couche_action.append([action,liste_positions_precedent])                  
                    
            self.graph.append(nouvelle_couche_action)
        
    
    def ajouter_couche_state(self):
        if len(self.graph)%2 == 0:
            print("Erreur, on ne peut pas ajouter une couche d'état après une couche d'état")
            return None
        nouvelle_couche_state_pos = []
        nouvelle_couche_state_neg = []

        seen = {}
        for i,action in enumerate(self.graph[-1]):

            #Action ne rien faire
            if action[0] == None :
                position = action[1][0]
                etat_a_ajouter = self.graph[-2][position[0]][position[1]]
                if ~(etat_a_ajouter[0] in seen.keys()) :
                    if position[0]==0:
                        nouvelle_couche_state_pos.append([etat_a_ajouter[0],[i]])
                        seen[etat_a_ajouter[0]] = (0,len(nouvelle_couche_state_pos)-1)
                    else :
                        nouvelle_couche_state_neg.append([etat_a_ajouter[0],[i]])
                        seen[etat_a_ajouter[0]] = (1,len(nouvelle_couche_state_neg)-1)
                    
                else :
                    position = seen[etat_a_ajouter[0]]
                    if position[0]==0 :
                        nouvelle_couche_state_pos[position[1]][1].append(i)
                    else :
                        nouvelle_couche_state_neg[position[1]][1].append(i)

            # Actions applicables
            else :
                for effet in action.effects_pos: 
                    if ~(effet in seen.keys()):
                        nouvelle_couche_state_pos.append([effet,[i]])
                        seen[effet] = (0,len(nouvelle_couche_state_pos)-1)
                    else :
                        position = seen[effet]
                        nouvelle_couche_state_pos[position[1]][1].append(i)

                for effet in action.effects_neg: 
                    if ~(effet in seen.keys()):
                        nouvelle_couche_state_neg.append([effet,[i]])
                        seen[effet] = (0,len(nouvelle_couche_state_neg)-1)
                    else :
                        position = seen[effet]
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
                            mutex_couche.append((i,j))
            
            else:   # couche action
                # Effet inconsistent & Interférence
                couche_=couche.copy()
                for i,action_ref in enumerate(couche) : 
                    couche_.remove(action_ref)
                    effet_pos_ref=set(action_ref.effects_pos)
                    effet_neg_ref=set(action_ref.effects_neg)
                    precondition_pos_ref = set(action_ref.preconditions_pos)
                    precondition_neg_ref = set(action_ref.preconditions_neg)
                    for j,action_comparaison in enumerate(couche_):
                        effet_pos_comparaison=set(action_comparaison.effects_pos)
                        effet_neg_comparaison=set(action_comparaison.effects_pos)
                        precondition_pos_comparaison = set(action_comparaison.preconditions_pos)
                        precondition_neg_comparaison = set(action_comparaison.preconditions_neg)

                        if (len(effet_pos_ref & effet_neg_comparaison) 
                            + len(effet_neg_ref & effet_pos_comparaison)
                            + len(precondition_pos_ref & effet_neg_comparaison)
                            + len(precondition_neg_ref & effet_pos_ref)
                            + len(precondition_pos_comparaison & effet_neg_ref)
                            + len(precondition_neg_comparaison & effet_pos_ref ) != 0):
                            mutex_couche.append((i,i+j))
                






                        
                
                        

        
        # Effet inconsistent
        # Interférence
        # Besoins concurrents

        # Négation l'un de l'autre 
        # l'autre sur les littéraux





    

class FastForwardPlanner:
    def __init__(self, domain_file, problem_file,object):
        self.object=object
        self.actions = self.parse_domain(domain_file,problem_file)
        self.initial_state_pos, self.initial_state_neg, self.goal_state = self.parse_problem_funtion(domain_file,problem_file)
        

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
    

    def parse_problem_funtion(self, domain_file,problem_file):
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

    def plan(self):
        current_state_pos =self.initial_state_pos
        current_state_neg =self.initial_state_neg
        goal_state_set = self.goal_state 
        plan = []
        print(current_state_neg)
        
        # for i in range (1):
        while current_state_pos != self.goal_state:
            applicable_actions = [action for action in self.actions if action.is_applicable(current_state_pos,current_state_neg)]
            
            if not applicable_actions:
                print("No applicable actions to reach the goal state.")
                return None

            # best_action=random.choice(applicable_actions)
            best_action = max(applicable_actions, key=lambda x: len(set(x.effects_pos) & set(goal_state_set)))
            # print(best_action.name)
            # print(current_state_pos,current_state_neg)
            current_state_pos,current_state_neg = best_action.apply(current_state_pos, current_state_neg)
            print(current_state_pos,current_state_neg)

        return plan

# Exemple d'utilisation
if __name__ == "__main__":
    domain_file = r"C:\Users\lisa\planification-2023-2024\Group_4\TSP.pddl"
    problem_file = r"C:\Users\lisa\planification-2023-2024\Group_4\pb-5cities_5edges.pddl"
    problem = pddlpy.DomainProblem(domain_file,problem_file)
    object=list(problem.problem.objects)

    planner = FastForwardPlanner(domain_file, problem_file,object)
    plan = planner.plan()
    if plan:
        print("Plan found:")
        for action in plan:
            print(action.name)
    else:
        print("No plan found.")

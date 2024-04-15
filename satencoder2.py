from pysat.formula import CNF
from pysat.solvers import Glucose3


class satEncoder:

    def __init__(self,graphPlan):
        self.graphPlan = graphPlan
        #self.cnf = CNF()
        self.solver = Glucose3()
        self.dict = {}
        self.dict_inverse = {}
        self.dict_seen_pos_by_couche = {}
        self.dict_seen_neg_by_couche = {}
        self.max_couche_decimal = len(str(len(self.graphPlan.graph)))
        self.mutex = self.graphPlan.add_mutex()
        self.test = []
        self.encode()


    def encode(self):
        self.encode_etat_initial()
        for couche in range(len(self.graphPlan.graph)):
            if couche%2 == 0:
                self.encode_couche_litteral(self.graphPlan.graph[couche],couche)
            else:
                self.encode_couche_action(self.graphPlan.graph[couche],couche)
            
            self.encode_mutex_couche(couche)
        self.encode_goal()
    

    def encode_couche_litteral(self,couche,num_couche):
        seen_pos = []
        seen_neg = []
        for litteral_pos in couche[0]:
            seen_pos.append(litteral_pos[0])
            id_litteral_pos = int(str(len(seen_pos)) + '0'*(self.max_couche_decimal - len(str(num_couche))) + str(num_couche))
            self.dict[id_litteral_pos] = litteral_pos[0]
            self.dict_inverse[litteral_pos[0]] = id_litteral_pos

            precedent_indice = []
            for precedent_position in litteral_pos[1]:
                id_precedent = int(str(precedent_position)+ '0'*(self.max_couche_decimal - len(str(num_couche-1))) + str(num_couche-1))
                precedent_indice.append(id_precedent)
            
                #self.cnf.append([-id_litteral_pos]+ precedent_indice)
            if len(precedent_indice) > 0:
                self.solver.add_clause([-id_litteral_pos]+ precedent_indice)
                self.test.append([-id_litteral_pos]+ precedent_indice)
        
        for litteral_neg in couche[1]:
            if litteral_neg[0] in seen_neg:
                id_litteral_neg = self.dict_inverse[litteral_neg[0]]

                precedent_indice = []
                for precedent_position in litteral_neg[1]:
                    id_precedent = int(str(precedent_position)+ '0'*(self.max_couche_decimal - len(str(num_couche-1))) + str(num_couche-1))
                    precedent_indice.append(id_precedent)
                #self.cnf.append([-id_litteral_neg]+ precedent_indice)
                self.solver.add_clause([id_litteral_neg]+ precedent_indice)
                self.test.append([id_litteral_neg]+ precedent_indice)

            else:
                seen_neg.append(litteral_neg[0])
                id_litteral_neg = int(str(len(seen_neg)+len(seen_pos)) + '0'*(self.max_couche_decimal - len(str(num_couche))) + str(num_couche))
                self.dict[id_litteral_neg] = litteral_neg[0]
                self.dict_inverse[litteral_neg[0]] = id_litteral_neg

                precedent_id = []
                for precedent_position in litteral_neg[1]:
                    id_precedent = int(str(precedent_position)+ '0'*(self.max_couche_decimal - len(str(num_couche-1))) + str(num_couche-1))
                    precedent_id.append(id_precedent)
                #self.cnf.append([-id_litteral_neg]+precedent_id)
                self.solver.add_clause([id_litteral_neg]+precedent_id)
                self.test.append([id_litteral_neg]+precedent_id)
        
        
        self.dict_seen_pos_by_couche[num_couche] =  seen_pos
        self.dict_seen_neg_by_couche[num_couche] =  seen_neg
        
    def encode_couche_action(self,couche,num_couche):

        for position, action in enumerate(couche):
            id_action = int(str(position) + '0'*(self.max_couche_decimal - len(str(num_couche))) + str(num_couche))
            self.dict[id_action] = action[0]

            for precedent_position in action[1]:
                id_precedent = self.dict_inverse[self.graphPlan.graph[num_couche-1][precedent_position[0]][precedent_position[1]][0]]


                #self.cnf.append([-id_action, id_precedent])
                self.solver.add_clause([-id_action, id_precedent])
                self.test.append([-id_action, id_precedent])
    

    def encode_mutex_couche(self,num_couche):

        couche_mutex = self.mutex[num_couche]
        if num_couche%2 == 0: # couche literal

            for couple_position in couche_mutex:
                seen_neg =self.dict_seen_neg_by_couche[num_couche]
                seen_pos = self.dict_seen_pos_by_couche[num_couche]

                pos1 = couple_position[0]
                literal1 = self.graphPlan.graph[num_couche][pos1[0]][pos1[1]][0]
                if pos1[0] == 1:
                    indice1 = seen_neg.index(literal1) +1 + len(seen_pos)
                else:
                    indice1 = seen_pos.index(literal1) +1
                indice1 = int(str(indice1) + '0'*(self.max_couche_decimal - len(str(num_couche))) + str(num_couche))
                if pos1[0] == 1:
                    indice1 = -indice1

                pos2 = couple_position[1]
                literal2 = self.graphPlan.graph[num_couche][pos2[0]][pos2[1]][0]
                if pos2[0] == 1:
                    indice2 = seen_neg.index(literal2) +1 + len(seen_pos)
                else:
                    indice2 = seen_pos.index(literal2) + 1
                indice2 = int(str(indice2) + '0'*(self.max_couche_decimal - len(str(num_couche))) + str(num_couche))
                if pos2[0] == 1:
                    indice2 = -indice2

                #self.cnf.append([-indice1,-indice2])
                self.solver.add_clause([-indice1,-indice2])
                self.test.append([-indice1,-indice2])

        else: # couche action
            for couple_position in couche_mutex:
                pos1 = couple_position[0]
                indice1 = int(str(pos1)+ '0'*(self.max_couche_decimal - len(str(num_couche))) + str(num_couche))

                pos2 = couple_position[1]
                indice2 = int(str(pos2)+ '0'*(self.max_couche_decimal - len(str(num_couche))) + str(num_couche))

                #self.cnf.append([-indice1,-indice2])
                self.solver.add_clause([-indice1,-indice2])
                self.test.append([-indice1,-indice2])


    def encode_mutex(self):
        mutex = self.mutex

        for i, couche_mutex in enumerate(mutex):

            if i%2 == 0: # couche literal

                for couple_position in couche_mutex:
                    seen =self.dict_seen_by_couche[i]

                    pos1 = couple_position[0]
                    literal1 = self.graphPlan.graph[i][pos1[0]][pos1[1]]
                    indice1 = seen.index(literal1) + 1
                    indice1 = int(str(indice1) + '0'*(self.max_couche_decimal - len(str(i))) + str(i))
                    if pos1[0] == 1:
                        indice1 = -indice1


                    pos2 = couple_position[1]
                    literal2 = self.graphPlan.graph[i][pos2[0]][pos2[1]]
                    indice2 = seen.index(literal2) + 1
                    indice2 = int(str(indice2) + '0'*(self.max_couche_decimal - len(str(i))) + str(i))
                    if pos2[0] == 1:
                        indice2 = -indice2

                    #self.cnf.append([-indice1,-indice2])
                    self.solver.add_clause([-indice1,-indice2])
                    self.test.append([-indice1,-indice2])

            else:
                for couple_position in couche_mutex:
                    pos1 = couple_position[0]
                    indice1 = int(str(pos1)+ '0'*(self.max_couche_decimal - len(str(i))) + str(i))

                    pos2 = couple_position[1]
                    indice2 = int(str(pos2)+ '0'*(self.max_couche_decimal - len(str(i))) + str(i))

                #self.cnf.append([-indice1,-indice2])
                self.solver.add_clause([-indice1,-indice2])
                self.test.append([-indice1,-indice2])
                

    def encode_etat_initial(self):
        couche_initiale = self.graphPlan.graph[0][0]
        for k in range(1,len(couche_initiale)+1):
            id_litteral = int(str(k) + '0'*(self.max_couche_decimal))
            
            #self.cnf.append([id_litteral])
            self.solver.add_clause([id_litteral])
            self.test.append([id_litteral])

    def encode_goal(self):  # résoudre les goal négatif
        goal = self.graphPlan.goal
        seen = self.dict_seen_pos_by_couche[len(self.graphPlan.graph)-1]
        for litteral in goal:
            litteral = tuple(litteral.predicate)
            if (litteral in seen):
                id_litteral = int( str(seen.index(litteral) + 1) + str(len(self.graphPlan.graph)-1))
                #self.cnf.append([id_litteral])
                self.solver.add_clause([id_litteral])
                self.test.append([id_litteral])
            else:
                id_litteral = int(str(len(seen)+1) + '0'*(self.max_couche_decimal - len(str(len(self.graphPlan.graph)-1))) + str(len(self.graphPlan.graph)-1))
                
                #self.cnf.append([id_litteral])
                self.solver.add_clause([id_litteral])
                self.test.append([id_litteral])
                #self.cnf.append([-id_litteral])
                self.solver.add_clause([-id_litteral])
                self.test.append([-id_litteral])


     
    def give_solution(self):
        #print(self.test)
        #self.solver.solve()
        #print(self.solver.get_model())
        if self.solver.solve():
            model = self.solver.get_model()
            print("Solution trouvée:")
            self.solution = []
            for var in model:
                if var > 0:
                    self.solution.append(var)
            print(self.solution)
            return True
        else:
            print("Aucune solution trouvée.")
            return False
        

    def give_plan(self):
        plan = [[] for k in range(len(self.graphPlan.graph)//2)]
        var_action = []
        for var in self.solution:
            if int(str(var)[-self.max_couche_decimal:])%2 == 1:
                var_action.append(var)
        
        for var in var_action:
            print(var)
            num_couche = int(str(var)[-self.max_couche_decimal:])
            action = self.dict[var]
            if action != None:
                plan[num_couche//2].append(action.name)
            else:
                plan[num_couche//2].append(None)

        return plan



    
            

            
            
            
                



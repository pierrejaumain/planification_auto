from time import time
from pddl import parse_domain, parse_problem

from satencoder2 import satEncoder
from pysat.solvers import Glucose3
from Graph_Plan_final import GraphPlan





if __name__ == "__main__":

    start = time()
    domain_file = r"./generateur_pddl/tpsdomain.pddl"
    problem_file = r"./generateur_pddl/pb_5_5.pddl"
    
    
    gp = GraphPlan(domain_file,problem_file)
    t = 0
    Tmax = 100
    solve = False
    while not solve and t<Tmax: 
        t+=1
        print(f"Résolution du plan étape :  {t+1}/{Tmax}")
        gp.update()
        #print(len(gp.graph[len(gp.graph)-2]))
        #print(gp.graph[len(gp.graph)-1])
        #solver = Glucose3()
        sat_enc = satEncoder(gp)
        #solver.append_formula(sat_enc.getCNF())
        solve = sat_enc.give_solution()
    #print(sat_enc.test)
    #print(sat_enc.dict)
    end = time()
    #print(gp.graph)
    print(f"La planification a durée {end-start} secondes")
    print(sat_enc.give_plan())
    
    
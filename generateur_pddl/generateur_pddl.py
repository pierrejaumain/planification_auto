from pddl.logic import Predicate, Constant, constants, variables
from pddl.core import Domain, Problem
from pddl.action import Action
from pddl.formatter import domain_to_string, problem_to_string
from pddl.requirements import Requirements
import networkx as nx
import random

x,y = variables("x y")



#On définit les prédicats

in_ = Predicate("in", x)
delivered = Predicate("delivered", x)
connected = Predicate("connected", x, y)

#On définit les actions
go_to = Action(
    "go_to",
    parameters=[x, y],
    precondition=connected(x, y) & in_(x),
    effect= ~in_(x) & in_(y)
)

deliver = Action(
    "deliver",
    parameters=[x],
    precondition=in_(x) & ~delivered(x),
    effect=delivered(x)
)


#On définit le domaine
requirements = [Requirements.STRIPS]
domain = Domain("tps",
                requirements=requirements,
                predicates=[in_, delivered, connected],
                actions=[go_to, deliver]
)

print(domain_to_string(domain))






#Génération d'un graphe (à changer pour que ça générer un graphe connexe quelconque)
import matplotlib.pyplot as plt
def generate_connected_graph(nb_edges, nb_nodes):
    G = nx.Graph()
    G.add_node(0)
    for i in range(1, nb_nodes):
        G.add_node(i)
        nodes_for_edge = random.randint(0, i-1)
        G.add_edge(i, nodes_for_edge)
    
    while G.number_of_edges() < nb_edges:
        node1 = random.randint(0, nb_nodes-1)
        node2 = random.randint(0, nb_nodes-1)
        while node1 == node2 or G.has_edge(node1, node2):
            node1 = random.randint(0, nb_nodes - 1)
            node2 = random.randint(0, nb_nodes - 1)
        G.add_edge(node1, node2)
    
    
    G = nx.relabel_nodes(G, {i: c[i] for i in range(nb_nodes)})
    #A décommenter si on souhaite afficher le problème créé
    #nx.draw(G, with_labels=True)
    #plt.show()
    
    return G
        


def extract_connections(graph):
    connections = []
    for edge in graph.edges:
        connections.append(connected(edge[0], edge[1]))
        connections.append(connected(edge[1], edge[0]))
    return connections

# Nombre de villes
num_cities = 20
num_edges = 50
c = [Constant("c"+str(i)) for i in range(num_cities)]
graph = generate_connected_graph(num_edges, num_cities)
connections = extract_connections(graph)


initial_state = [in_(c[0]), ~delivered(c[0])] + [~in_(c[i]) for i in range(1, num_cities)] + connections

goal_state = in_(c[0])
for i in range(num_cities):
    goal_state = goal_state & delivered(c[i])

# Create the problem
problem = Problem(
    "pb-" + str(num_cities) + "cities",
    domain=domain, 
    requirements=requirements, 
    objects=c,
    init=initial_state,  
    goal=goal_state
)

print(problem_to_string(problem))
# Planification automatique Groupe 2 : Graph plan/SAT encoder

L'objectif de ce projet est l'implémentation d'un planifieur classique. Notre choix s'est porté sur l'implémentation d'un GraphPlan que nous avons ensuite encodé au format SAT. Le solveur utilisé pour la résolution du problème SAT est Glucose3.


## Installation

1. Assurez-vous d'avoir les bibliothèques suivantes installées (l'ensemble du code a été testé sur Python 3.8 mais ne devrait pas poser de problème de version) :
   - `pysat`
   - `pddl`
   - `pddl-py`

2. Le fichier Graph_Plan_Final gère la création du GraphPlae, satencoder.py l'encode et résoud le problème SAT associé.

## Utilisation

Pour lancer le code de test de performances, exécutez le script `main.py` avec Python :
```
python main.py
```

## Tableau des performances

Le tableau suivant récapitule les performances du planificateur en fonction de différentes tailles de problèmes sur notre problème TSP et sur un autre problème Labyrinthe :

### TSP : Voyageur de commerce revisité

| Taille du problème | Temps d'exécution moyen (secondes) |
|--------------------|------------------------------------|
| Petit (5 villes )  | 0.56                               |
| Moyen (10 villes)  | 2.27                               |
| Grand (20 villes)  | 16.16                              |

### Labyrinthe 

| Taille du problème | Temps d'exécution moyen (secondes) |
|--------------------|------------------------------------|
| P0                 | 9.62                               |
| P1                 | 3.82                               |
| P2                 | 3.99                               |
| P3                 | 66.996                             |
| P4                 | 953.69                             |



---

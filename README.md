# Planification automatique Groupe 2 : Graph plan/SAT encoder

L'objectif de ce projet est l'implémentation d'un planifieur classique. Notre choix s'est porté sur l'implémentation d'un GraphPlan que nous avons ensuite encodé au format SAT.


## Installation

1. Assurez-vous d'avoir les bibliothèques suivantes installées (l'ensemble du code a été testé sur Python 3.8 mais ne devrait pas posé de problème de version) :
   - `pysat`
   - `pddl`
   - `pddl-py`

2. Le fichier Graph_Plan_Final gère la création du GraphPlane, satencoder.py l'encode et résoud le problème SAT associé.

## Utilisation

Pour lancer le code de test de performances, exécutez le script `main.py` avec Python :
```
python main.py
```

## Tableau des performances

Le tableau suivant récapitule les performances du planificateur en fonction de différentes tailles de problèmes :

| Taille du problème | Temps d'exécution moyen (secondes) |
|--------------------|------------------------------------|
| Petit (5 villes )  | 0.56                               |
| Moyen (10 villes)  | 2.27                               |
| Grand (20 villes)  | 16.16                              |

---

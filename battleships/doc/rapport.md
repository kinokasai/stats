---
documentclass: scrreprt
title: "Rapport Projet 1 : Bataille navale"
subtitle: "3I005 -- Probabilités, Statistiques et Informatique"
institute: "Université Pierre et Marie Curie -- Paris 6"
author:
- Pablo Donato
- Alexandre Doussot
date: \today
lang: fr
---

# Combinatoire du jeu

## Question 1

Pour une grille vide $G \in \{0\}^{m \times n}$ et un bateau de longueur $l$, on peut calculer le nombre de placements possibles du bateau sur $G$, que l'on appelle $n_l$, avec la formule :
$$n_l = (m - l + 1) * n + (n - l + 1) * m$$
Dans le fichier `combinatoire.py`, nous avons défini une fonction `nb_placements_bateau` permettant de calculer $n_l$ en énumérant toutes les combinaisons possibles sur une grille donnée à l'aide de la fonction `Grille.peut_placer`.

En appliquant la formule précédente et en appelant la fonction `nb_placements_bateau` sur une grille vide de taille $10\times10$, on obtient bien des résultats identiques :

 l   $n_l$   `nb_placements_bateaux`
--- ------- -------------------------
5   120     120
4   140     140
3   160     160
2   180     180

<!--$$P(X=x) = \frac{C^{17}_{x} - C^{17}_{x-1}}{C^{17}_{100}}$$-->

import numpy as np
import pydot
import random

from utils import methodaliases


class Arc:
    """Classe représentant un arc dans un graphe probabiliste.

    Attributs:
        trans (np.ndarray[float]): Référence vers la matrice de transition du graphe contenant l'arc.
        tail (Node): Référence vers le noeud sortant.
        head (Node): Référence vers le noeud entrant.
        prob (Optional[float]): Probabilité de transition associée à l'arc.
    """
    def __init__(self, trans, tail, head, prob=None):
        self.trans = trans
        self.tail = tail
        self.head = head
        self.prob = prob

    def update_trans(self, prob):
        """Met à jour la probabilité de transition associée à l'arc.

        S'occupe aussi de mettre à jour le coefficient correspondant 
        dans la matrice de transition du graphe contenant l'arc.

        Paramètres:
            prob (float): Nouvelle probabilité de transition.
        """
        self.prob = prob
        self.trans[self.tail.id, self.head.id] = prob

    def plot(self, graph):
        """Dessine l'arc dans un graphe pydot."""
        arc = pydot.Edge(self.tail.id, self.head.id)
        graph.add_edge(arc)


class Node:
    """Classe représentant un noeud dans un graphe probabiliste.

    Attributs:
        id (int): Identifiant du noeud dans le graphe.
        in_arcs (Set[Arc]): Références vers les arcs entrants.
        out_arcs (Set[Arc]): Références vers les arcs sortants.
    """
    def __init__(self, ident):
        self.id = ident
        self.in_arcs = []
        self.out_arcs = []

    def update_trans(self):
        """Met à jour uniformément la probabilité de transition des arcs sortants."""
        for arc in self.out_arcs:
            arc.update_trans(1 / len(self.out_arcs))

    def plot(self, graph):
        """Dessine le noeud dans un graphe pydot."""
        node = pydot.Node(self.id, shape='circle')
        graph.add_node(node)
        for arc in self.out_arcs:
            arc.plot(graph)


@methodaliases(add_arc='addArc', update_trans='updateProbas', write_png='writeGraph', next_step='nextStep')
class SimpleWeb:
    """Classe représentant un graphe probabiliste.

    Attributs:
        n (int): Nombre de noeuds que contient le graphe.
        nodes (Dict[int, Node]): Dictionnaire {identifiant: noeud}.
        trans (np.ndarray[float]): Matrice de transition.
    """
    def __init__(self, n):
        """Construit un graphe sans arcs.

        Exceptions:
            ValueError: Si n < 1.
        """
        if n < 1:
            raise ValueError("Un SimpleWeb doit contenir au moins 1 noeud")
        self.n = n
        self.nodes = [Node(ident) for ident in range(n)]
        self.trans = np.zeros((n,) * 2)

    def add_arc(self, tail_id, head_id):
        """Construit un arc sans probabilité entre deux noeuds.

        Paramètres:
            tail_id (int): Identifiant du noeud sortant.
            head_id (int): Identifiant du noeud entrant.

        Exceptions:
            IndexError: Si l'un des identifiants n'est pas compris entre
                0 et le nombre maximum de noeuds du graphe.
            ValueError: Si l'arc existe déjà.
        """
        for id_ in (tail_id, head_id):
            if id_ < 0 or id_ >= self.n:
                raise IndexError("Identifiant de noeud invalide: {}".format(id_))

        tail = self.nodes[tail_id]
        for arc in tail.out_arcs:
            if arc.head.id == head_id:
                raise ValueError("L'arc {} -> {} existe déjà".format(tail_id, head_id))
        head = self.nodes[head_id]

        arc = Arc(self.trans, tail, head)
        tail.out_arcs.append(arc)
        head.in_arcs.append(arc)

    def update_trans(self):
        """Met à jour les probabilités de transition."""
        for node in self.nodes:
            node.update_trans()

    def __str__(self):
        return str(self.trans)

    def write_png(self, path):
        """Écrit une représentation graphique du graphe dans un fichier PNG.

        Paramètres:
            path (str): Chemin du fichier PNG.
        """
        graph = pydot.Dot(graph_type='digraph')
        for node in self.nodes:
            node.plot(graph)
        graph.write_png(path)

    def next_step(self, pi_t):
        return np.matmul(pi_t, self.trans)

    def convergence(self, n, epsilon):
        """Calcule l'évolution de la convergence des puissances de la matrice de transition.

        Paramètres:
            n (int): Calcule au plus jusqu'à la puissance n.
            epsilon (float): Seuil de convergence.
        """
        trans = self.trans.copy()
        eps = 1
        epsilons = []
        k = 2
        while k <= n and eps > epsilon:
            new_trans = np.matmul(trans, self.trans)
            eps = np.linalg.norm(trans - new_trans)
            epsilons.append(eps)
            trans = new_trans
            k += 1
        return epsilons

    @staticmethod
    def generate(n):
        """Génère un SimpleWeb ergodique sans auto-référence.

        Actuellement l'algorithme ne fonctionne pas,
        certaines des chaînes générées ne sont pas irréductibles.

        Paramètres:
            n (int): Nombre de pages web.
        """
        if n < 3:
            raise ValueError("Un SimpleWeb ergodique sans auto-référence doit contenir au moins 3 pages")

        web = SimpleWeb(n)
        pages = list(range(n))
        accessible = [False] * n
        leavable = [False] * n

        for page in pages:
            # On génère un lien entrant si nécessaire
            if not accessible[page]:
                sources = pages.copy()
                # Pas d'auto-référence
                sources.remove(page)
                # On évite les cycles de période 2
                for link in web.nodes[page].out_arcs:
                    sources.remove(link.head.id)
                # On tire la source au hasard
                source = random.choice(sources)
                web.add_arc(source, page)
                # On met à jour le statut des 2 pages dans le réseau
                accessible[page] = True
                leavable[source] = True

            # On génère un lien sortant si nécessaire
            if not leavable[page]:
                targets = pages.copy()
                # Pas d'auto-référence
                targets.remove(page)
                # On évite les cycles de période 2
                for link in web.nodes[page].in_arcs:
                    targets.remove(link.tail.id)
                # On tire la cible au hasard
                target = random.choice(targets)
                web.add_arc(page, target)
                # On met à jour le statut des 2 pages dans le réseau
                accessible[target] = True
                leavable[page] = True

        web.update_trans()
        return web

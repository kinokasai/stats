import numpy as np
import pydot

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

        S'occupe aussi de mettre à jour la case correspondante dans la
        matrice de transition du graphe contenant l'arc.

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


@methodaliases(add_arc='addArc', update_trans='updateProbas', write_png='writeGraph')
class SimpleWeb:
    """Classe représentant un graphe probabiliste.

    Attributs:
        nb_max_nodes (int): Nombre maximum de noeuds que peut contenir le graphe.
        nodes (Dict[int, Node]): Dictionnaire {identifiant: noeud}.
        trans (np.ndarray[float]): Matrice de transition.
    """
    def __init__(self, nb_max_nodes):
        """Construit un graphe sans arcs.

        Exceptions:
            ValueError: Si nb_max_nodes < 1.
        """
        if nb_max_nodes < 1:
            raise ValueError("Un SimpleWeb doit contenir au moins 1 noeud")
        self.nb_max_nodes = nb_max_nodes
        self.nodes = {}
        self.trans = np.zeros((nb_max_nodes,) * 2)

    def add_arc(self, tail_id, head_id):
        """Construit un arc sans probabilité entre deux noeuds.

        Si le noeud correspondant à un des identifiants n'existe pas encore,
        on le construit et le rajoute au graphe.

        Paramètres:
            tail_id (int): Identifiant du noeud sortant.
            head_id (int): Identifiant du noeud entrant.

        Exceptions:
            IndexError: Si l'un des identifiants n'est pas compris entre
                0 et le nombre maximum de noeuds du graphe.
            ValueError: Si l'arc existe déjà.
        """
        for id_ in (tail_id, head_id):
            if id_ < 0 or id_ >= self.nb_max_nodes:
                raise IndexError("Identifiant de noeud invalide: {}".format(id_))

        try:
            tail = self.nodes[tail_id]
            for arc in tail.out_arcs:
                if arc.head.id == head_id:
                    raise ValueError("L'arc {} -> {} existe déjà".format(tail_id, head_id))
        except KeyError:
            tail = Node(tail_id)
            self.nodes[tail_id] = tail
        try:
            head = self.nodes[head_id]
        except KeyError:
            head = Node(head_id)
            self.nodes[head_id] = head

        arc = Arc(self.trans, tail, head)
        tail.out_arcs.append(arc)
        head.in_arcs.append(arc)

    def update_trans(self):
        """Met à jour les probabilités de transition."""
        for node in self.nodes.values():
            node.update_trans()

    def __str__(self):
        return str(self.trans)

    def write_png(self, path):
        """Écrit une représentation graphique du graphe dans un fichier PNG.

        Paramètres:
            path (str): Chemin du fichier PNG.
        """
        graph = pydot.Dot(graph_type='digraph')
        for node in self.nodes.values():
            node.plot(graph)
        graph.write_png(path)

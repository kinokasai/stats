import numpy as np

from utils import methodaliases, sample_index


class Simulation:
    """Classe abstraite permettant de calculer une approximation de la distribution stationnaire d'un SimpleWeb.

    Attributs:
        web (SimpleWeb): Référence vers le SimpleWeb.
        dim (int): Nombre d'états possibles.
        state (np.ndarray[float]): Vecteur d'état (distribution de probabilités courante).
        epsilon (float): Estimateur de convergence des probabilités.
        epsilon_path (str): Chemin du fichier où est enregistrée l'évolution de la convergence.
        epsilon_interval (int): Nombre d'itérations séparant deux échantillonnages de la convergence.
    """
    def __init__(self, web):
        self.web = web
        self.dim = web.trans.shape[0]

    def trace(self, interval, path):
        """Configure la trace de l'évolution de la convergence."""
        self.epsilon_interval = interval
        self.epsilon_path = path

    def step(self, t):
        """Effectue une itération de la simulation.

        Paramètres:
            t (int): Pas de temps (nombre d'itérations déjà effectuées).

        Retourne:
            new_state (np.ndarray[float]): Vecteur d'état mis à jour.
        """
        raise NotImplementedError

    def walk(self, nb_max_iters, epsilon, init_state=None):
        """Simule un parcours du web jusqu'à convergence des probabilités.

        La simulation s'arrête au bout de nb_max_iters itérations
        si les probabilités ne convergent pas avant.

        Paramètres:
            nb_max_iters (int): Nombre maximum d'itérations.
            epsilon (float): Seuil de convergence des probabilités.
            init_state (np.ndarray[float]): Vecteur d'état initial.
        """
        if init_state is None:
            self.state = np.ones(self.dim) / self.dim
        else:
            self.state = init_state
        self.epsilon = 1
        t = 0
        with open(self.epsilon_path, 'w') as log:
            while t < nb_max_iters and self.epsilon >= epsilon:
                new_state = self.step(t)
                self.epsilon = max([abs(self.state[i] - new_state[i]) for i in range(self.dim)])
                if t % self.epsilon_interval == 0:
                    log.write(str(self.epsilon) + '\n')
                self.state = new_state
                t += 1


@methodaliases(goto='goTo', show_freqs='showFrequencies')
class Internaute(Simulation):
    """Simulation approximant la distribution stationnaire par un comptage des fréquences.

    Attributs:
        page (Node): Référence vers la page où se trouve l'internaute.
        freqs (np.ndarray): Nombre de visites de l'internaute sur chaque page du web.
    """
    def goto(self, page_id):
        """Visite une page web.

        Paramètres:
            page_id (int): Identifiant de la page visitée.
        """
        self.page = self.web.nodes[page_id]

    def step(self, t):
        if t == 0:
            self.freqs = np.zeros(self.dim)
            self.freqs[self.page.id] += 1
            self.state = self.freqs

        model = self.web.trans[self.page.id]
        next_page_id = sample_index(model)
        self.goto(next_page_id)
        self.freqs[next_page_id] += 1

        return self.freqs / (t+2)

    def show_freqs(self):
        print(self.freqs)


class InternauteV2(Simulation):
    """Simulation approximant la distribution stationnaire avec l'équation matricielle de transition."""
    def step(self, t):
        return self.web.next_step(self.state)

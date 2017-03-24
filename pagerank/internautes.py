import numpy as np

from utils import methodaliases, sample_index


@methodaliases(goto='goTo', show_freqs='showFrequencies')
class Internaute:
    """Classe permettant le parcours d'un SimpleWeb.

    Attributs:
        web (SimpleWeb): Référence vers le SimpleWeb.
        page (Node): Référence vers la page où se trouve l'internaute.
        state (np.ndarray[float]): Vecteur d'état de l'internaute.
        epsilon (float): Estimateur de convergence des probabilités.
        epsilon_path (str): Chemin du fichier où est enregistrée l'évolution de la convergence.
        epsilon_interval (int): Nombre d'itérations séparant deux échantillonnages de la convergence.
        freqs (np.ndarray): Nombre de visites de l'internaute sur chaque page du web.
    """
    def __init__(self, web):
        self.web = web

    def goto(self, page_id):
        """Visite une page web.

        Paramètres:
            page_id (int): Identifiant de la page visitée.
        """
        self.page = self.web.nodes[page_id]

    def trace(self, interval, path):
        """Configure la trace de l'évolution de la convergence."""
        self.epsilon_interval = interval
        self.epsilon_path = path

    def walk(self, nb_max_iters, epsilon):
        """Parcours le web jusqu'à convergence des probabilités.

        Le parcours s'arrête au bout de nb_max_iters itérations
        si les probabilités ne convergent pas avant.

        Paramètres:
            nb_max_iters (int): Nombre maximum d'itérations.
            epsilon (float): Seuil de convergence des probabilités.
        """
        d = self.web.trans.shape[0]
        self.state = np.ones(d) / d
        self.freqs = np.zeros(d)
        self.epsilon = 1
        t = 0

        with open(self.epsilon_path, 'w') as log:
            while t < nb_max_iters and self.epsilon >= epsilon:
                model = self.web.trans[self.page.id]
                next_page_id = sample_index(model)
                self.goto(next_page_id)
                self.freqs[next_page_id] += 1

                new_state = np.matmul(self.state, self.web.trans)
                self.epsilon = max([abs(self.state[i] - new_state[i]) for i in range(d)])
                if t % self.epsilon_interval == 0:
                    log.write(str(self.epsilon) + '\n')

                self.state = new_state
                t += 1

    def show_freqs(self):
        print(self.freqs)

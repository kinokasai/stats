import numpy as np


def methodaliases(**kwargs):
    """Décorateur pour ajouter des alias à certaines méthodes d'une classe.

    Paramètres:
        kwargs (Dict[str, str]): Dictionnaire {nom de méthode: alias}.
    """
    def wrap(cls):
        for method_name, alias in kwargs.items():
            setattr(cls, alias, getattr(cls, method_name))
        return cls
    return wrap


def sample_index(model):
    """Tire un index aléatoirement selon une distribution de probabilités.

    Paramètres:
        model (Sequence[float]): Distribution de probabilités.

    Retourne:
        i (int): L'index aléatoirement tiré.
    """
    cum_model = np.array(model).cumsum()
    n = np.random.ranf()
    for i in range(len(model)):
        if n < cum_model[i]:
            return i

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

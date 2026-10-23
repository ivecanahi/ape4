from estado import Estado


class Individuo:
    """Guarda y cambia el estado de una persona."""

    def __init__(self):
        # Pseudocodigo: "PARA cada individuo... Asignar estado = SUSCEPTIBLE".
        self.estado = Estado.SUSCEPTIBLE

    # Consultas sobre el estado actual.
    def esta_susceptible(self):
        return self.estado == Estado.SUSCEPTIBLE

    def esta_infectado(self):
        return self.estado == Estado.INFECTADO

    # Transiciones del modelo: S -> I (contagio) e I -> R (recuperacion).
    def infectar(self):
        self.estado = Estado.INFECTADO

    def recuperar(self):
        self.estado = Estado.RECUPERADO

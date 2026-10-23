from estado import Estado
from individuo import Individuo


class Poblacion:
    """Contiene a los individuos y cuenta cuantos hay en cada estado."""

    def __init__(self, tamano):
        # Pseudocodigo: "Crear poblacion". Todos empiezan como susceptibles.
        self.individuos = [Individuo() for _ in range(tamano)]

    # Permiten usar len(poblacion) y poblacion[i] como si fuera una lista.
    def __len__(self):
        return len(self.individuos)

    def __getitem__(self, indice):
        return self.individuos[indice]

    def infectar_al_azar(self, cantidad, rng):
        # Pseudocodigo: "Seleccionar 5 individuos... Cambiar estado = INFECTADO".
        # replace=False evita elegir dos veces al mismo individuo.
        for indice in rng.choice(len(self), size=cantidad, replace=False):
            self.individuos[indice].infectar()

    def infectados(self):
        # Devuelve (posicion, individuo) de cada infectado. La posicion se usa
        # para que un infectado no se elija a si mismo como contacto.
        return [
            (indice, individuo)
            for indice, individuo in enumerate(self.individuos)
            if individuo.esta_infectado()
        ]

    def contar(self):
        # Pseudocodigo: "Contar SUSCEPTIBLES, INFECTADOS y RECUPERADOS".
        # Devuelve la tupla (S, I, R).
        estados = [individuo.estado for individuo in self.individuos]
        return (
            estados.count(Estado.SUSCEPTIBLE),
            estados.count(Estado.INFECTADO),
            estados.count(Estado.RECUPERADO),
        )

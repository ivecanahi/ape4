class RegistroSIR:
    """Almacena los valores de S, I y R en cada tiempo."""

    # Nombres de las columnas; el CSV usa este mismo encabezado.
    ENCABEZADO = ("tiempo", "susceptibles", "infectados", "recuperados")

    def __init__(self):
        # Pseudocodigo: "Crear estructura para almacenar resultados".
        # Cada fila es una tupla (tiempo, S, I, R).
        self.filas = []

    def registrar(self, tiempo, conteo):
        # Pseudocodigo: "Guardar: tiempo, susceptibles, infectados, recuperados".
        # *conteo separa la tupla (S, I, R) en tres valores.
        self.filas.append((tiempo, *conteo))

    def pico_infectados(self):
        # Fila con la mayor cantidad de infectados (columna 2).
        return max(self.filas, key=lambda fila: fila[2])

    def final(self):
        # Ultima fila: estado de la poblacion al terminar la simulacion.
        return self.filas[-1]

from enum import Enum


# Un Enum evita usar textos sueltos como "S" o "I" por todo el codigo:
# si se escribe mal un estado, Python lanza un error en lugar de fallar en silencio.
class Estado(Enum):
    """Estados posibles de un individuo en el modelo SIR."""

    SUSCEPTIBLE = "S"  # puede contagiarse
    INFECTADO = "I"  # esta enfermo y puede contagiar
    RECUPERADO = "R"  # ya no contagia ni puede volver a contagiarse

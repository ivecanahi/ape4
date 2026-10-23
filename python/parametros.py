from dataclasses import dataclass


# frozen=True hace que los parametros no se puedan modificar despues de
# crearlos, asi se garantiza que toda la simulacion usa los mismos valores.
@dataclass(frozen=True)
class ParametrosSIR:
    """Valores de configuracion del modelo, iguales para todas las herramientas."""

    poblacion: int = 100  # N: total de individuos (N = S + I + R)
    infectados_iniciales: int = 5  # I(0); por lo tanto S(0) = 95
    beta: float = 0.30  # probabilidad de contagio en cada contacto
    gamma: float = 0.10  # probabilidad de recuperarse en cada paso de tiempo
    tiempo_simulacion: int = 100  # numero de pasos de tiempo a simular

    @property
    def r0(self):
        # Numero reproductivo basico: R0 = beta / gamma = 0.30 / 0.10 = 3.
        # Un infectado genera en promedio unas 3 infecciones antes de recuperarse.
        return self.beta / self.gamma

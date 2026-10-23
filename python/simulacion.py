import numpy as np
import simpy

from modelo_sir import ModeloSIR
from poblacion import Poblacion
from registro import RegistroSIR


class SimulacionSIR:
    """Controla el tiempo de la simulacion con SimPy."""

    def __init__(self, parametros, semilla=None):
        self.parametros = parametros

        # La semilla fija la secuencia de numeros aleatorios: con la misma
        # semilla se obtienen siempre los mismos resultados. Con otra semilla
        # (u otra herramienta, como Java o NetLogo) los resultados cambian.
        rng = np.random.default_rng(semilla)

        # Estado inicial: 100 individuos, de los cuales 5 estan infectados.
        self.poblacion = Poblacion(parametros.poblacion)
        self.poblacion.infectar_al_azar(parametros.infectados_iniciales, rng)

        self.modelo = ModeloSIR(parametros, rng)
        self.registro = RegistroSIR()

        # Entorno de SimPy: lleva el reloj de la simulacion (env.now).
        self.env = simpy.Environment()

    def _proceso_epidemia(self):
        # Proceso de SimPy. Es un generador: cada "yield" pausa el proceso
        # hasta que el reloj avance.
        # Pseudocodigo: "PARA tiempo = 0 HASTA 100 HACER".
        while True:
            # 1. Registrar S, I y R en el tiempo actual.
            self.registro.registrar(int(self.env.now), self.poblacion.contar())

            # 2. Terminar al llegar al tiempo maximo (despues de registrar t = 100).
            if self.env.now >= self.parametros.tiempo_simulacion:
                return

            # 3. Aplicar contagios y recuperaciones.
            self.modelo.avanzar(self.poblacion)

            # 4. Avanzar el reloj una unidad de tiempo.
            yield self.env.timeout(1)

    def ejecutar(self):
        # Registra el proceso en el entorno y corre hasta que no queden eventos.
        self.env.process(self._proceso_epidemia())
        self.env.run()
        return self.registro

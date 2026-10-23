"""Modelo epidemiologico SIR como simulacion discreta de agentes con SimPy.

Cada individuo tiene un estado (S, I o R). En cada unidad de tiempo, cada
infectado contacta a un individuo al azar; si el contacto es susceptible se
contagia con probabilidad BETA. Luego el infectado se recupera con
probabilidad GAMMA. Los cambios se calculan sobre una copia del estado
actual, de modo que todos los individuos se actualizan a la vez.
"""

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import simpy

POBLACION = 100
INFECTADOS_INICIALES = 5
BETA = 0.30
GAMMA = 0.10
TIEMPO_SIMULACION = 100

SUSCEPTIBLE = "S"
INFECTADO = "I"
RECUPERADO = "R"

ENCABEZADO = ["tiempo", "susceptibles", "infectados", "recuperados"]


def crear_poblacion(rng):
    estados = [SUSCEPTIBLE] * POBLACION
    for indice in rng.choice(POBLACION, size=INFECTADOS_INICIALES, replace=False):
        estados[indice] = INFECTADO
    return estados


def contar(estados):
    return (
        estados.count(SUSCEPTIBLE),
        estados.count(INFECTADO),
        estados.count(RECUPERADO),
    )


def elegir_contacto(indice, rng):
    """Elige al azar a otro individuo de la poblacion (distinto de si mismo)."""
    contacto = int(rng.integers(POBLACION - 1))
    return contacto + 1 if contacto >= indice else contacto


def paso_epidemia(estados, rng):
    nuevos_estados = list(estados)
    for indice, estado in enumerate(estados):
        if estado != INFECTADO:
            continue
        contacto = elegir_contacto(indice, rng)
        if estados[contacto] == SUSCEPTIBLE and rng.random() < BETA:
            nuevos_estados[contacto] = INFECTADO
        if rng.random() < GAMMA:
            nuevos_estados[indice] = RECUPERADO
    return nuevos_estados


def proceso_epidemia(env, estados, rng, resultados):
    while True:
        resultados.append((int(env.now), *contar(estados)))
        if env.now >= TIEMPO_SIMULACION:
            return
        estados[:] = paso_epidemia(estados, rng)
        yield env.timeout(1)


def simular(semilla=None):
    rng = np.random.default_rng(semilla)
    estados = crear_poblacion(rng)
    resultados = []
    env = simpy.Environment()
    env.process(proceso_epidemia(env, estados, rng, resultados))
    env.run()
    return resultados


def guardar_csv(resultados, ruta):
    with Path(ruta).open("w", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(ENCABEZADO)
        escritor.writerows(resultados)


def graficar(resultados, ruta):
    tiempo, susceptibles, infectados, recuperados = zip(*resultados)
    figura, ejes = plt.subplots(figsize=(9, 5))
    ejes.plot(tiempo, susceptibles, label="Susceptibles (S)", color="tab:blue")
    ejes.plot(tiempo, infectados, label="Infectados (I)", color="tab:red")
    ejes.plot(tiempo, recuperados, label="Recuperados (R)", color="tab:green")
    ejes.set_title(
        f"Modelo SIR - Python/SimPy (N={POBLACION}, β={BETA}, γ={GAMMA})"
    )
    ejes.set_xlabel("Tiempo")
    ejes.set_ylabel("Individuos")
    ejes.set_xlim(0, TIEMPO_SIMULACION)
    ejes.set_ylim(0, POBLACION)
    ejes.grid(alpha=0.3)
    ejes.legend()
    figura.tight_layout()
    figura.savefig(ruta, dpi=120)
    plt.close(figura)


def main():
    parser = argparse.ArgumentParser(description="Simulacion SIR con SimPy")
    parser.add_argument("--semilla", type=int, default=42)
    parser.add_argument("--csv", default="resultados_python.csv")
    parser.add_argument("--grafica", default="grafica_python.png")
    args = parser.parse_args()

    resultados = simular(args.semilla)
    guardar_csv(resultados, args.csv)
    graficar(resultados, args.grafica)

    pico = max(resultados, key=lambda fila: fila[2])
    final = resultados[-1]
    print(f"R0 = BETA / GAMMA = {BETA / GAMMA:.1f}")
    print(f"Pico de infectados: {pico[2]} en t = {pico[0]}")
    print(f"Estado final (t = {final[0]}): S={final[1]} I={final[2]} R={final[3]}")
    print(f"CSV: {args.csv} | Grafica: {args.grafica}")


if __name__ == "__main__":
    main()

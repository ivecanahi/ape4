import argparse

from exportador_csv import ExportadorCSV
from graficador import GraficadorSIR
from parametros import ParametrosSIR
from simulacion import SimulacionSIR


def main():
    # Opciones de linea de comandos, por ejemplo: python main.py --semilla 7
    parser = argparse.ArgumentParser(description="Simulacion SIR con SimPy")
    parser.add_argument("--semilla", type=int, default=42)
    parser.add_argument("--csv", default="resultados_python.csv")
    parser.add_argument("--grafica", default="grafica_python.png")
    args = parser.parse_args()

    # 1. Ejecutar la simulacion con los parametros de la practica.
    parametros = ParametrosSIR()
    registro = SimulacionSIR(parametros, args.semilla).ejecutar()

    # 2. Pseudocodigo: "Guardar resultados" (CSV para importar en NetLogo).
    ExportadorCSV().exportar(registro, args.csv)

    # 3. Pseudocodigo: "Generar grafica".
    GraficadorSIR(parametros).graficar(registro, args.grafica)

    # 4. Resumen en consola.
    pico = registro.pico_infectados()
    final = registro.final()
    print(f"R0 = beta / gamma = {parametros.r0:.1f}")
    print(f"Pico de infectados: {pico[2]} en t = {pico[0]}")
    print(f"Estado final (t = {final[0]}): S={final[1]} I={final[2]} R={final[3]}")
    print(f"CSV: {args.csv} | Grafica: {args.grafica}")


if __name__ == "__main__":
    main()

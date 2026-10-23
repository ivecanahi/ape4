import csv
import tempfile
import unittest
from pathlib import Path

from modelo_sir import (
    INFECTADOS_INICIALES,
    POBLACION,
    TIEMPO_SIMULACION,
    guardar_csv,
    simular,
)


class SimulacionSIRTest(unittest.TestCase):
    def setUp(self):
        self.resultados = simular(semilla=42)

    def test_registra_un_valor_por_cada_tiempo_de_0_a_100(self):
        tiempos = [fila[0] for fila in self.resultados]
        self.assertEqual(tiempos, list(range(TIEMPO_SIMULACION + 1)))

    def test_estado_inicial_95_susceptibles_5_infectados(self):
        self.assertEqual(
            self.resultados[0],
            (0, POBLACION - INFECTADOS_INICIALES, INFECTADOS_INICIALES, 0),
        )

    def test_la_poblacion_total_se_conserva(self):
        for _, s, i, r in self.resultados:
            self.assertEqual(s + i + r, POBLACION)

    def test_susceptibles_no_aumentan_y_recuperados_no_disminuyen(self):
        for anterior, actual in zip(self.resultados, self.resultados[1:]):
            self.assertLessEqual(actual[1], anterior[1])
            self.assertGreaterEqual(actual[3], anterior[3])

    def test_misma_semilla_produce_mismos_resultados(self):
        self.assertEqual(simular(semilla=42), self.resultados)

    def test_guardar_csv_escribe_encabezado_y_filas(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "resultados_python.csv"
            guardar_csv(self.resultados, ruta)
            with ruta.open(newline="") as archivo:
                filas = list(csv.reader(archivo))
        self.assertEqual(
            filas[0], ["tiempo", "susceptibles", "infectados", "recuperados"]
        )
        self.assertEqual(len(filas), TIEMPO_SIMULACION + 2)


if __name__ == "__main__":
    unittest.main()

import csv
import tempfile
import unittest
from pathlib import Path

import numpy as np

from estado import Estado
from exportador_csv import ExportadorCSV
from individuo import Individuo
from modelo_sir import ModeloSIR
from parametros import ParametrosSIR
from poblacion import Poblacion
from registro import RegistroSIR
from simulacion import SimulacionSIR


class IndividuoTest(unittest.TestCase):
    def test_nace_susceptible(self):
        self.assertEqual(Individuo().estado, Estado.SUSCEPTIBLE)

    def test_se_infecta_y_luego_se_recupera(self):
        individuo = Individuo()
        individuo.infectar()
        self.assertTrue(individuo.esta_infectado())
        individuo.recuperar()
        self.assertEqual(individuo.estado, Estado.RECUPERADO)


class PoblacionTest(unittest.TestCase):
    def test_infecta_la_cantidad_indicada(self):
        poblacion = Poblacion(100)
        poblacion.infectar_al_azar(5, np.random.default_rng(1))
        self.assertEqual(poblacion.contar(), (95, 5, 0))


class ModeloSIRTest(unittest.TestCase):
    def test_el_contacto_nunca_es_el_mismo_individuo(self):
        modelo = ModeloSIR(ParametrosSIR(), np.random.default_rng(3))
        for _ in range(500):
            self.assertNotEqual(modelo.elegir_contacto(0, 100), 0)
            self.assertNotEqual(modelo.elegir_contacto(99, 100), 99)

    def test_sin_infectados_nada_cambia(self):
        poblacion = Poblacion(10)
        ModeloSIR(ParametrosSIR(), np.random.default_rng(3)).avanzar(poblacion)
        self.assertEqual(poblacion.contar(), (10, 0, 0))


class SimulacionSIRTest(unittest.TestCase):
    def setUp(self):
        self.parametros = ParametrosSIR()
        self.filas = SimulacionSIR(self.parametros, semilla=42).ejecutar().filas

    def test_registra_un_valor_por_cada_tiempo_de_0_a_100(self):
        tiempos = [fila[0] for fila in self.filas]
        self.assertEqual(tiempos, list(range(self.parametros.tiempo_simulacion + 1)))

    def test_estado_inicial_95_susceptibles_5_infectados(self):
        self.assertEqual(self.filas[0], (0, 95, 5, 0))

    def test_la_poblacion_total_se_conserva(self):
        for _, s, i, r in self.filas:
            self.assertEqual(s + i + r, self.parametros.poblacion)

    def test_susceptibles_no_aumentan_y_recuperados_no_disminuyen(self):
        for anterior, actual in zip(self.filas, self.filas[1:]):
            self.assertLessEqual(actual[1], anterior[1])
            self.assertGreaterEqual(actual[3], anterior[3])

    def test_misma_semilla_produce_mismos_resultados(self):
        otra = SimulacionSIR(self.parametros, semilla=42).ejecutar().filas
        self.assertEqual(otra, self.filas)


class ExportadorCSVTest(unittest.TestCase):
    def test_escribe_encabezado_y_filas(self):
        registro = RegistroSIR()
        registro.registrar(0, (95, 5, 0))
        registro.registrar(1, (93, 7, 0))
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "resultados_python.csv"
            ExportadorCSV().exportar(registro, ruta)
            with ruta.open(newline="") as archivo:
                filas = list(csv.reader(archivo))
        self.assertEqual(
            filas,
            [
                ["tiempo", "susceptibles", "infectados", "recuperados"],
                ["0", "95", "5", "0"],
                ["1", "93", "7", "0"],
            ],
        )


if __name__ == "__main__":
    unittest.main()

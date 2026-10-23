import csv
from pathlib import Path


class ExportadorCSV:
    """Guarda un registro de resultados en un archivo CSV."""

    def exportar(self, registro, ruta):
        # newline="" evita lineas en blanco extra entre filas (sobre todo en Windows).
        with Path(ruta).open("w", newline="") as archivo:
            escritor = csv.writer(archivo)
            # Primera fila: tiempo,susceptibles,infectados,recuperados
            escritor.writerow(registro.ENCABEZADO)
            # Una fila por cada tiempo, de 0 a 100.
            escritor.writerows(registro.filas)

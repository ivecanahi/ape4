import matplotlib

# "Agg" dibuja directamente en un archivo, sin abrir una ventana.
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class GraficadorSIR:
    """Dibuja la evolucion de S, I y R y la guarda como imagen."""

    def __init__(self, parametros):
        self.parametros = parametros

    def graficar(self, registro, ruta):
        p = self.parametros

        # zip(*filas) convierte la lista de filas en cuatro columnas:
        # tiempos, susceptibles, infectados y recuperados.
        tiempo, susceptibles, infectados, recuperados = zip(*registro.filas)

        # Una curva por estado: S(t), I(t) y R(t).
        figura, ejes = plt.subplots(figsize=(9, 5))
        ejes.plot(tiempo, susceptibles, label="Susceptibles (S)", color="tab:blue")
        ejes.plot(tiempo, infectados, label="Infectados (I)", color="tab:red")
        ejes.plot(tiempo, recuperados, label="Recuperados (R)", color="tab:green")

        # Titulo, ejes y leyenda.
        ejes.set_title(
            f"Modelo SIR - Python/SimPy (N={p.poblacion}, β={p.beta}, γ={p.gamma})"
        )
        ejes.set_xlabel("Tiempo")
        ejes.set_ylabel("Individuos")
        ejes.set_xlim(0, p.tiempo_simulacion)
        ejes.set_ylim(0, p.poblacion)
        ejes.grid(alpha=0.3)
        ejes.legend()

        # Guardar la imagen y liberar la memoria de la figura.
        figura.tight_layout()
        figura.savefig(ruta, dpi=120)
        plt.close(figura)

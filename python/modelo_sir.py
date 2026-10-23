class ModeloSIR:
    """Aplica las reglas de contagio y recuperacion durante un paso de tiempo.

    Cada infectado contacta a otro individuo al azar; si el contacto es
    susceptible se contagia con probabilidad beta. Luego el infectado se
    recupera con probabilidad gamma. Los cambios se deciden sobre el estado
    actual y se aplican al final, para que todos se actualicen a la vez.

    Con un contacto por infectado, la probabilidad de que el contacto sea
    susceptible es S/N, asi que los contagios esperados por paso son
    beta * S * I / N, el mismo termino de la ecuacion dS/dt = -beta*S*I/N.
    """

    def __init__(self, parametros, rng):
        self.parametros = parametros
        self.rng = rng  # generador de numeros aleatorios (NumPy)

    def elegir_contacto(self, indice, tamano):
        # Se sortea entre los otros (tamano - 1) individuos. Si el numero
        # sorteado cae en la posicion propia o despues, se corre una posicion;
        # asi nunca sale el mismo individuo y todos tienen igual probabilidad.
        contacto = int(self.rng.integers(tamano - 1))
        return contacto + 1 if contacto >= indice else contacto

    def avanzar(self, poblacion):
        # Pseudocodigo: "Crear copia del estado actual de la poblacion".
        # En vez de copiar la poblacion, se anotan los cambios en estas listas
        # y se aplican al final. Asi, quien se contagia en este paso todavia
        # no contagia ni se recupera hasta el paso siguiente.
        nuevos_infectados = []
        nuevos_recuperados = []

        # Pseudocodigo: "PARA cada individuo INFECTADO HACER".
        for indice, individuo in poblacion.infectados():
            contacto = poblacion[self.elegir_contacto(indice, len(poblacion))]

            # Contagio: "SI numero aleatorio < BETA ENTONCES ... INFECTADO".
            # Solo se sortea si el contacto es susceptible.
            if contacto.esta_susceptible() and self.rng.random() < self.parametros.beta:
                nuevos_infectados.append(contacto)

            # Recuperacion: "SI numero aleatorio < GAMMA ENTONCES ... RECUPERADO".
            if self.rng.random() < self.parametros.gamma:
                nuevos_recuperados.append(individuo)

        # Se actualizan todos los estados a la vez.
        for individuo in nuevos_infectados:
            individuo.infectar()
        for individuo in nuevos_recuperados:
            individuo.recuperar()

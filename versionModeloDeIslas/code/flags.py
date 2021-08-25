import random

# Objecto flag


class Flag:
    def __init__(self, nombre):
        self.nombre = nombre
        self.flag = nombre

    def mutateFlag(self):
        pass

    def getRandomTuple(self):
        return (self.flag, random.randint(0, 1))


class rangoFlag:
    def __init__(self, nombre, min, max):
        self.nombre = nombre
        self.flag = nombre + str(random.randint(min, max))
        self.minimo = min
        self.maximo = max

    def mutateFlag(self):
        self.flag = self.nombre + str(random.randint(self.minimo, self.maximo))
        return self.flag

    def getRandomTuple(self):
        return (self.flag, random.randint(0, 1))


class intervaloFLag:
    def __init__(self, nombre, intervalo):
        self.nombre = nombre
        self.flag = nombre + random.choice(intervalo)
        self.intervalo = intervalo

    def mutateFlag(self):
        self.flag = self.nombre + random.choice(self.intervalo)
        return self.flag

    def getRandomTuple(self):
        return (self.flag, random.randint(0, 1))

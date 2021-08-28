import random
from abc import ABC, abstractmethod

# Objecto flag
class Flag(ABC):

    @abstractmethod
    def __init__(self, nombre, flag):
        self.nombre= nombre
        self.flag = flag

    @abstractmethod
    def mutateFlag(self):
        ''' Cambia aleatoriamente el atributo flag y lo revuelve'''
        pass

    @abstractmethod
    def getRandomTuple(self):
        ''' Genera una tupla aleatoria (flag, booleano) '''
        pass

class binariaFlag(Flag):
    def __init__(self, nombre):
        self.nombre = nombre
        self.flag = nombre

    def mutateFlag(self):
        pass

    def getRandomTuple(self):
        return (self.flag, random.randint(0, 1))


class rangoFlag(Flag):
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


class intervaloFLag(Flag):
    def __init__(self, nombre, intervalo):
        self.nombre = nombre
        self.flag = nombre + random.choice(intervalo)
        self.intervalo = intervalo

    def mutateFlag(self):
        self.flag = self.nombre + random.choice(self.intervalo)
        return self.flag

    def getRandomTuple(self):
        return (self.flag, random.randint(0, 1))

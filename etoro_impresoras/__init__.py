
class Impresora(object):
    def __init__(self, etoro):
        self.__etoro = etoro

    @property
    def etoro(self):
        return self.__etoro

    @etoro.setter
    def depositos(self, etoro):
        self.__etoro = etoro

    def imprimir(self, destino=None):
        pass

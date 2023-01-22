"""
consola.py
"""

from . import Impresora


class ImpresoraConsola(Impresora):
    def __init__(self, etoro):
        super().__init__(etoro)

    def imprimir_depositos(self):
        print("\nDepositos ----------------")
        print("Fecha \t\t\t Detalle \t\t\t Monto")
        for deposito in self.etoro.depositos:
            linea = f"{deposito.fecha} \t {deposito.detalle} \t\t {deposito.monto}"
            print(linea)

    def imprimir_detalles_posiciones(self, detalles_posicion):
        print("Fecha \t\t\t Detalle \t\t\t Monto")
        for detalle in detalles_posicion:
            linea = f"{detalle.fecha} \t {detalle.descripcion} \t\t {detalle.monto}"
            print(linea)

    def imprimir_posiciones(self):
        print("\nPosiciones ---------------")
        for posicion in self.etoro.posiciones:
            print(f"\n{posicion.ticket} ({posicion.id}) -----")
            self.imprimir_detalles_posiciones(posicion.detalles)

    def imprimir(self, destino=None):
        print("Etoro --------------------")
        self.imprimir_depositos()
        self.imprimir_posiciones()

"""
modelos.py
"""

from datetime import datetime


class Deposito(object):
    def __init__(self, monto, detalle, fecha):
        self.__monto = monto  # Monto del deposito.
        self.__detalle = detalle  # Detalle del deposito.
        self.__fecha = datetime.strptime(fecha, '%d/%m/%Y %H:%M:%S')

    @property
    def monto(self):
        return self.__monto

    @monto.setter
    def monto(self, monto):
        self.__monto = monto

    @property
    def detalle(self):
        return self.__detalle

    @detalle.setter
    def detalle(self, detalle):
        self.__detalle = detalle

    @property
    def fecha(self):
        return self.__fecha

    @fecha.setter
    def fecha(self, fecha):
        self.__fecha = fecha

    def __str__(self):
        return self.__detalle + "|" + str(self.__monto) + "|" + str(self.__fecha)


class Tenencia(object):
    def __init__(self, id, ticket, detalles):
        self.__id = id  # Id de la tenencia.
        self.__ticket = ticket  # Nombre de la tenencia (accion, etf, etc.).
        # Detalles asociados a la tenencia (cobro de dividendos y otras cosas).
        self.__detalles = detalles

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def ticket(self):
        return self.__ticket

    @ticket.setter
    def ticket(self, ticket):
        self.__ticket = ticket

    @property
    def detalles(self):
        return self.__detalles

    @detalles.setter
    def detalles(self, detalles):
        self.__detalles = detalles

    def __str__(self):
        return str(self.id) + "|" + self.ticket + "|" + str(len(self.detalles))


class DetalleTenencia(object):
    def __init__(self, monto, fecha, descripcion, unidades):
        self.__monto = monto  # Monto del detalle.
        self.__fecha = fecha
        self.__descripcion = descripcion
        self.__unidades = unidades

    @property
    def monto(self):
        return self.__monto

    @monto.setter
    def monto(self, monto):
        self.__monto = monto

    @property
    def fecha(self):
        return self.__fecha

    @fecha.setter
    def dia(self, fecha):
        self.__fecha = fecha

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion

    @property
    def unidades(self):
        return self.__unidades

    @unidades.setter
    def unidades(self, unidades):
        self.__unidades = unidades

    def __str__(self):
        return str(self.monto) + "|" + str(self.fecha) + "|" + self.descripcion + "|" + self.unidades


class DividendoMensual(object):
    def __init__(self, anio, mes, monto):
        self.__monto = monto
        self.__anio = anio
        self.__mes = mes

    @property
    def monto(self):
        return self.__monto

    @monto.setter
    def monto(self, monto):
        self.__monto = monto

    @property
    def anio(self):
        return self.__anio

    @anio.setter
    def anio(self, anio):
        self.__anio = anio

    @property
    def mes(self):
        return self.__mes

    @mes.setter
    def mes(self, mes):
        self.__mes = mes

    def __str__(self):
        return f'{self.anio} | {self.mes} | {str(self.monto)}'


class Etoro(object):
    def __init__(self, depositos, posiciones, dividendos, cerradas):
        self.__depositos = depositos
        self.__posiciones = posiciones
        self.__dividendos = dividendos
        self.__cerradas = cerradas

    @property
    def depositos(self):
        return self.__depositos

    @depositos.setter
    def depositos(self, depositos):
        self.__depositos = depositos

    @property
    def posiciones(self):
        return self.__posiciones

    @posiciones.setter
    def posiciones(self, posiciones):
        self.__posiciones = posiciones

    @property
    def dividendos(self):
        return self.__dividendos

    @dividendos.setter
    def dividendos(self, dividendos):
        self.__dividendos = dividendos

    @property
    def cerradas(self):
        return self.__cerradas

    @cerradas.setter
    def cerradas(self, cerradas):
        self.__cerradas = cerradas

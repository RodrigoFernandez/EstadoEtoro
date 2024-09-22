"""
constantes.py
"""

from enum import Enum


class Columnas(object):
    DEPOSITO = '-'
    ID_DE_POSICION = 'ID de posicion'
    FECHA = 'Fecha'
    FECHA2 = 'Fecha2'
    TIPO = 'Tipo'
    DETALLES = 'Detalles'
    IMPORTE = 'Importe'
    UNIDADES = 'Unidades'
    ANIO = 'anio'
    MES = 'mes'


class ColumnasReporteEtoro(Enum):
    """
    Fecha -> 0
    Tipo -> 1
    Detalles -> 2
    Importe -> 3
    Unidades > 4
    Cambio de capital realizado -> 5
    Capital realizado -> 6
    Saldo -> 7
    ID de posición -> 8
    Importe no retirable -> 9
    """
    FECHA = 0
    TIPO = 1
    DETALLES = 2
    IMPORTE = 3
    UNIDADES = 4
    CAMBIO_CAPITAL = 5  # Cambio de capital realizado
    CAPITAL_REALIZADO = 6  # Capital realizado
    SALDO = 7
    ID_POSICION = 8  # ID de posición
    IMP_NO_RET = 9  # Importe no retirable

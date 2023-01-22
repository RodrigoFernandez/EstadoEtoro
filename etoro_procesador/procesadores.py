"""
procesadores.py
"""
from openpyxl import load_workbook
import pandas as pd
from etoro_modelos.modelos import Deposito, DetalleTenencia, Tenencia
from etoro_modelos.modelos import DividendoMensual, Etoro


class Generador(object):
    def __init__(self, ruta):
        self.ruta = ruta
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

    def procesar_fila(self, fila):
        rta = {
            "Fecha": fila[0].value,
            "Tipo": fila[1].value,
            "Detalles": fila[2].value,
            "Importe": fila[3].value,
            "Unidades": "" if fila[4].value == '-' else fila[4].value,
            "ID de posicion": fila[8].value if fila[8].value is not None else "",
        }

        return rta

    def procesar_datos(self, datos):
        df = pd.DataFrame(datos)
        df.set_index('Fecha', inplace=True)
        agrupados = df.groupby('ID de posicion')

        depositos = self.convert_2_depositos(agrupados.get_group(''))
        tenencias = self.convert_2_tenencias(agrupados)

        return depositos, tenencias

    def convert_2_depositos(self, depos):
        rta = [Deposito(dep['Importe'], dep['Detalles'], indice_fila_fecha)
               for indice_fila_fecha, dep in depos.iterrows()]
        return rta

    def get_ticket(self, detalle):
        if detalle:
            partes = detalle.split("/")
            return partes[0]
        return ""

    def convert_2_tenencias(self, tenencias):
        rta = []
        for clave in tenencias.groups.keys():
            if clave != '':
                una_tenencia = tenencias.get_group(clave)
                es_primer_movimiento = True
                ticket = ""
                detalles = []
                for indice_fecha, t in una_tenencia.iterrows():
                    if es_primer_movimiento:
                        es_primer_movimiento = False
                        ticket = self.get_ticket(t['Detalles'])
                    detalles.append(DetalleTenencia(
                        t['Importe'], indice_fecha, t['Detalles'], t['Unidades']))
                rta.append(Tenencia(clave, ticket, detalles))

        a = sorted(rta, key=lambda t: t.ticket)
        return a

    def preprocesar_actividad(self, hoja):
        es_titulo = True
        pre_procesadas = []

        for fila in hoja.rows:
            if es_titulo:
                es_titulo = False
            else:
                pre_procesadas.append(self.procesar_fila(fila))
        return pre_procesadas

    def convert_2_dividendos_mensuales(self, sumatorias):
        rta = []

        for index, fila in sumatorias.iterrows():
            rta.append(DividendoMensual(fila['anio'], fila['mes'], fila['Importe']))

        return rta

    def procesar_fila_div(self, fila):
        rta = {
            "Fecha": fila[0].value,
            "Detalles": fila[1].value,
            "Importe": fila[2].value,
            "ID de posicion": fila[5].value,
        }

        return rta

    def preprocesar_dividendos(self, hoja):
        es_titulo = True
        pre_procesadas = []

        for fila in hoja.rows:
            if es_titulo:
                es_titulo = False
            else:
                pre_procesadas.append(self.procesar_fila_div(fila))
        return pre_procesadas

    def procesar_datos_dividendos(self, datos):
        df = pd.DataFrame(datos)

        df['Fecha2'] = pd.to_datetime(df['Fecha'], format="%d/%m/%Y")

        df['anio'] = pd.DatetimeIndex(df['Fecha2']).year
        df['mes'] = pd.DatetimeIndex(df['Fecha2']).month

        sumatorias = df.groupby(['anio', 'mes']).agg({'Importe': 'sum'}).reset_index()
        sumatorias.sort_values(by=['anio', 'mes'], inplace=True, ascending=False)
        rta = self.convert_2_dividendos_mensuales(sumatorias)
        return rta

    def leer_excel(self):
        planilla = load_workbook(self.ruta)
        hoja_actividades = planilla[planilla.sheetnames[2]]

        pre_procesadas = self.preprocesar_actividad(hoja_actividades)

        depositos, posiciones = self.procesar_datos(pre_procesadas)

        hoja_dividendos = planilla[planilla.sheetnames[3]]
        pre_procesadas_div = self.preprocesar_dividendos(hoja_dividendos)
        dividendos = self.procesar_datos_dividendos(pre_procesadas_div)

        return depositos, posiciones, dividendos

    def generar_etoro(self):
        depositos, posiciones, dividendos = self.leer_excel()
        rta = Etoro(depositos, posiciones, dividendos)
        return rta

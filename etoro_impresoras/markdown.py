"""
markdown.py
"""

import markdown  # https://github.com/Python-Markdown/markdown

from . import Impresora


class ColAling(object):
    IZQ = 1
    CEN = 2
    DER = 3


class ImpresoraMarkdown(Impresora):
    def get_separador(self, cantidad=1):
        sep = ['---'] * cantidad
        return "\n\n".join(sep)

    def get_titulo(self, texto, nivel=1, estilo=""):
        rta = f"{'#' * nivel} {texto}"
        if estilo:
            rta = rta + ' { ' + estilo + '}'
        return rta

    def get_cita(self, texto, nivel=1):
        return f"{'>' * nivel}{texto}"

    def get_fila_tabla(self, columnas):
        return f"|{'&nbsp;|&nbsp;'.join(columnas)}|"

    def get_cabecera_tabla(self, titulos):
        return f"|{'|'.join(titulos)}|"

    def get_alineacion_columna(self, alineacion):
        comun = "---"
        if alineacion == ColAling.DER:
            return comun + ":"
        elif alineacion == ColAling.CEN:
            return ":" + comun + ":"

        return comun

    def get_alineaciones_columnas(self, alineaciones):
        return self.get_cabecera_tabla([self.get_alineacion_columna(alineacion)
                                        for alineacion in alineaciones])

    def get_encabezado(self):
        return self.get_titulo("Etoro", estilo='.encabezado')

    def get_depositos(self):
        partes = []
        partes.append(self.get_titulo("Depositos", nivel=2, estilo='.encabezado_2'))
        partes.append("\n")

        titulos = ['Fecha', 'Descripcion', 'Monto']
        partes.append(self.get_cita(self.get_cabecera_tabla(titulos)))

        alineaciones = [ColAling.IZQ, ColAling.IZQ, ColAling.DER]
        partes.append(self.get_cita(self.get_alineaciones_columnas(alineaciones)))

        for deposito in self.etoro.depositos:
            fila = [str(deposito.fecha), deposito.detalle if deposito.detalle else '',
                    "{:.2f}".format(deposito.monto)]
            partes.append(self.get_cita(self.get_fila_tabla(fila) + " { .fila}"))

        partes.append("\n")
        return "\n".join(partes)

    def get_detalles_posiciones(self, detalles, nivel=2):
        partes = []
        titulos = ['Fecha', 'Descripcion', 'Monto', 'Unidades']
        partes.append(self.get_cita(self.get_cabecera_tabla(titulos), nivel=nivel))

        alineaciones = [ColAling.IZQ, ColAling.IZQ, ColAling.DER, ColAling.DER]
        partes.append(self.get_cita(self.get_alineaciones_columnas(alineaciones), nivel=nivel))

        for detalle in detalles:
            fila = [str(detalle.fecha), detalle.descripcion if detalle.descripcion else "", "{:.2f}".format(
                detalle.monto), detalle.unidades]
            partes.append(self.get_cita(self.get_fila_tabla(fila), nivel=nivel))

        return "\n".join(partes)

    def get_posciones(self):
        partes = []
        partes.append(self.get_titulo("Posiciones", nivel=2, estilo='.encabezado_2'))
        partes.append("\n")

        for posicion in self.etoro.posiciones:
            titulo_posicion = f"{posicion.ticket} ({str(posicion.id)}) - {'CERRADA' if posicion.id in self.etoro.cerradas else 'ABIERTA'}"
            partes.append(self.get_cita(self.get_titulo(titulo_posicion, nivel=3)))
            partes.append("\n")
            partes.append(self.get_detalles_posiciones(posicion.detalles))
            partes.append("\n")

        partes.append("\n")
        return "\n".join(partes)

    def get_comisiones(self):
        partes = []
        partes.append(self.get_titulo("Comisiones", nivel=2, estilo='.encabezado_2'))
        partes.append("\n")

        partes.append(self.get_detalles_posiciones(self.etoro.comisiones, nivel=1))

        partes.append("\n")
        return "\n".join(partes)

    def get_dividendos_mensuales(self):
        partes = []
        partes.append(self.get_titulo("Dividendos Mensuales", nivel=2, estilo='.encabezado_2'))
        partes.append("\n")

        titulos = ['Fecha', 'Monto']
        partes.append(self.get_cita(self.get_cabecera_tabla(titulos), nivel=1))

        alineaciones = [ColAling.IZQ, ColAling.DER]
        partes.append(self.get_cita(self.get_alineaciones_columnas(alineaciones), nivel=1))

        for un_mes in self.etoro.dividendos:
            # print(un_mes)
            fila = [f"{'{:.0f}'.format(un_mes.anio)}/{'{:.0f}'.format(un_mes.mes).zfill(2)}",
                    f"{'{:.2f}'.format(un_mes.monto)}"]
            partes.append(self.get_cita(self.get_fila_tabla(fila), nivel=1))

        partes.append("\n")
        return "\n".join(partes)

    def get_markdown(self):
        partes = []
        partes.append(self.get_encabezado())
        partes.append(self.get_separador(cantidad=3))
        partes.append(self.get_depositos())
        partes.append(self.get_separador(cantidad=2))
        partes.append(self.get_posciones())
        partes.append(self.get_separador(cantidad=2))
        partes.append(self.get_comisiones())
        partes.append(self.get_separador(cantidad=2))
        partes.append(self.get_dividendos_mensuales())

        return "\n".join(partes)

    def get_estilo(self):
        return """<style type="text/css">
    .encabezado { color: green; }

    .encabezado_2 { color: blue; }

    thead tr { background-color: #ccc; }
    tbody tr:nth-child(2n+1) { background-color: #ddd; }
    tbody tr:nth-child(2n+0) { background-color: #eee; }
</style>"""

    def get_html(self, estilo, body):
        partes = []

        apertura = """<!DOCTYPE html>
<html lang="es">
\t<head>
\t\t<meta charset="utf-8">
"""
        partes.append(apertura)

        partes.append(estilo)

        cierre_apertura = """
\t</head>
\t<body>"""

        partes.append(cierre_apertura)

        partes.append(body)

        cierre = """\t</body>\n</html>"""
        partes.append(cierre)

        return "\n".join(partes)

    def get_body(self):
        md = self.get_markdown()
        # Mirar como agregar css en el markdow para usar esto
        # https://github.com/Python-Markdown/markdown/blob/master/docs/extensions/attr_list.md
        body = markdown.markdown(md, extensions=['tables', 'attr_list'])
        return body

    def imprimir(self, destino=None):
        pass


class ImpresoraHtml(ImpresoraMarkdown):
    def imprimir(self, destino=None):

        if destino is None:
            print("Se debe pasar un destino de generación")

        estilo = self.get_estilo()
        body = self.get_body()

        html = self.get_html(estilo, body)
        # print(html)
        with open(destino, "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
            output_file.write(html)

        print(f"Se generó el reporte: {destino}")

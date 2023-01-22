"""
estado_etoro.py
"""

import argparse
from pathlib import Path
# https://realpython.com/python-toml/
import tomli
from etoro_procesador.procesadores import Generador
from etoro_impresoras.markdown import ImpresoraHtml


def get_parser():
    parser = argparse.ArgumentParser(description="Generador de reporte etoro")
    parser.add_argument('reporte_etoro', help='ruta reporte de estado de etoro')
    return parser


if __name__ == '__main__':
    configuracion = tomli.loads(Path(".estado_etoro.toml").read_text(encoding='utf-8'))
    args = get_parser().parse_args()

    generador = Generador(args.reporte_etoro)
    etoro = generador.generar_etoro()

    impresora = ImpresoraHtml(etoro)
    impresora.imprimir(
        destino=f'{configuracion["reporte"]["ubicacion"]}{configuracion["reporte"]["nombre"]}')

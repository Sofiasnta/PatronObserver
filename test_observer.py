"""Pruebas de la Actividad 3.6 (unittest). Ejecutar: python -m unittest -v"""
from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout
from typing import Any

from alerta_por_correo import AlertaPorCorreo
from aviso_por_whatsapp import AvisoPorWhatsApp
from cliente_interesado import ClienteInteresado
from gestor_eventos import GestorEventos
from registro_de_eventos import RegistroDeEventos
from tienda import PRECIO_CAMBIADO, PRODUCTO_DISPONIBLE, Tienda


class PruebasObserver(unittest.TestCase):
    def setUp(self) -> None:
        self.tienda = Tienda("Tienda de prueba")
        self._silencio = redirect_stdout(io.StringIO())  # oculta los print
        self._silencio.__enter__()

    def tearDown(self) -> None:
        self._silencio.__exit__(None, None, None)

    # 1. Un suscriptor recibe el evento al que se suscribió
    def test_recibe_evento_suscrito(self) -> None:
        ana = ClienteInteresado("Ana")
        self.tienda.eventos.suscribir(PRODUCTO_DISPONIBLE, ana)
        self.tienda.reabastecer("iPhone")
        self.assertEqual(len(ana.avisos), 1)
        self.assertEqual(ana.avisos[0]["producto"], "iPhone")

    # 2. Un suscriptor no recibe eventos de otro tipo
    def test_no_recibe_eventos_de_otro_tipo(self) -> None:
        ana = ClienteInteresado("Ana")
        self.tienda.eventos.suscribir(PRODUCTO_DISPONIBLE, ana)
        self.tienda.cambiar_precio("iPhone", 4_000_000)
        self.assertEqual(ana.avisos, [])

    # 3. Tras cancelar la suscripción, no recibe más avisos
    def test_no_recibe_tras_cancelar(self) -> None:
        ana = ClienteInteresado("Ana")
        self.tienda.eventos.suscribir(PRODUCTO_DISPONIBLE, ana)
        self.tienda.reabastecer("iPhone")
        self.tienda.eventos.cancelar(PRODUCTO_DISPONIBLE, ana)
        self.tienda.reabastecer("AirPods")
        self.assertEqual(len(ana.avisos), 1)  # solo el aviso previo a la baja

    # 4. Con varios suscriptores, todos son notificados
    def test_todos_los_suscriptores_son_notificados(self) -> None:
        ana = ClienteInteresado("Ana")
        registro = RegistroDeEventos()
        correo = AlertaPorCorreo("x@y.co", "Llegó {producto}")
        for s in (ana, registro, correo):
            self.tienda.eventos.suscribir(PRODUCTO_DISPONIBLE, s)
        self.tienda.reabastecer("iPhone")
        self.assertEqual(len(ana.avisos), 1)
        self.assertEqual(len(registro.eventos), 1)
        self.assertEqual(correo.enviados, ["Llegó iPhone"])

    # Pruebas adicionales ------------------------------------------------
    def test_suscriptor_funcional_lambda(self) -> None:
        recibidos: list[dict[str, Any]] = []
        self.tienda.eventos.suscribir(PRECIO_CAMBIADO, recibidos.append)
        self.tienda.cambiar_precio("iPhone", 3_900_000)
        self.assertEqual(recibidos[0]["precio_nuevo"], 3_900_000)

    def test_nuevo_suscriptor_sin_modificar_tienda(self) -> None:
        whatsapp = AvisoPorWhatsApp("+57 300")
        self.tienda.eventos.suscribir(PRODUCTO_DISPONIBLE, whatsapp)
        self.tienda.reabastecer("iPad")
        self.assertEqual(len(whatsapp.mensajes), 1)

    def test_no_duplica_suscripciones(self) -> None:
        gestor = GestorEventos()
        ana = ClienteInteresado("Ana")
        gestor.suscribir("e", ana)
        gestor.suscribir("e", ana)
        self.assertEqual(len(gestor.suscriptores_de("e")), 1)

    def test_reabastecer_con_stock_no_notifica(self) -> None:
        ana = ClienteInteresado("Ana")
        self.tienda.reabastecer("iPhone")  # antes de suscribirse
        self.tienda.eventos.suscribir(PRODUCTO_DISPONIBLE, ana)
        self.tienda.reabastecer("iPhone")  # ya había stock: no es novedad
        self.assertEqual(ana.avisos, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)

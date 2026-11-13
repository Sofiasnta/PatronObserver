"""Actividad 3.2 — Notificador concreto. Usa composición (atributo `eventos`).

Esta clase NO importa ningún suscriptor concreto.
"""
from __future__ import annotations

from gestor_eventos import GestorEventos

PRODUCTO_DISPONIBLE = "producto_disponible"
PRECIO_CAMBIADO = "precio_cambiado"


class Tienda:
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.eventos = GestorEventos()
        self._inventario: dict[str, int] = {}
        self._precios: dict[str, float] = {}

    def reabastecer(self, producto: str, cantidad: int = 1) -> None:
        estaba_agotado = self._inventario.get(producto, 0) == 0
        self._inventario[producto] = self._inventario.get(producto, 0) + cantidad
        if estaba_agotado:  # solo es noticia si vuelve a estar disponible
            self.eventos.notificar(PRODUCTO_DISPONIBLE, {
                "tienda": self.nombre,
                "producto": producto,
                "cantidad": self._inventario[producto],
            })

    def cambiar_precio(self, producto: str, precio: float) -> None:
        anterior = self._precios.get(producto)
        self._precios[producto] = precio
        self.eventos.notificar(PRECIO_CAMBIADO, {
            "tienda": self.nombre,
            "producto": producto,
            "precio_anterior": anterior,
            "precio_nuevo": precio,
        })

    def stock(self, producto: str) -> int:
        return self._inventario.get(producto, 0)

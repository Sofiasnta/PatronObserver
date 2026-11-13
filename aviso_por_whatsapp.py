"""Actividad 4.2 — Cuarto suscriptor, agregado SIN modificar Tienda.

Solo se creó este archivo y se registró en main.py.
"""
from __future__ import annotations

from typing import Any

from suscriptor import Suscriptor


class AvisoPorWhatsApp(Suscriptor):
    def __init__(self, telefono: str) -> None:
        self.telefono = telefono
        self.mensajes: list[str] = []

    def actualizar(self, datos: dict[str, Any]) -> None:
        mensaje = f"Novedad en {datos['tienda']}: {datos['producto']}"
        self.mensajes.append(mensaje)
        print(f"[WhatsApp {self.telefono}] {mensaje}")

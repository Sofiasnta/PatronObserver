"""Actividad 3.3 — Suscriptor concreto: simula el envío de un correo con print."""

from __future__ import annotations

from typing import Any

from suscriptor import Suscriptor


class AlertaPorCorreo(Suscriptor):
    def __init__(self, correo: str, plantilla: str) -> None:
        self.correo = correo
        self.plantilla = plantilla  # usa {producto}
        self.enviados: list[str] = []

    def actualizar(self, datos: dict[str, Any]) -> None:
        mensaje = self.plantilla.format(producto=datos["producto"])
        self.enviados.append(mensaje)
        print(f"[correo a {self.correo}] {mensaje}")

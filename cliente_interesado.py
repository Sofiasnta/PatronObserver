"""Actividad 3.3 — Suscriptor concreto: imprime un aviso con su nombre."""

from __future__ import annotations

from typing import Any

from suscriptor import Suscriptor


class ClienteInteresado(Suscriptor):
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.avisos: list[dict[str, Any]] = []  # historial para las pruebas

    def actualizar(self, datos: dict[str, Any]) -> None:
        self.avisos.append(datos)
        if "precio_nuevo" in datos:
            print(f"[{self.nombre}] {datos['producto']} ahora cuesta "
                  f"${datos['precio_nuevo']:,.0f}")
        else:
            print(f"[{self.nombre}] ¡{datos['producto']} ya está disponible "
                  f"en {datos['tienda']}!")

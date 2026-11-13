"""Actividad 3.3 — Suscriptor concreto: guarda cada evento en una lista o archivo."""

from __future__ import annotations

from typing import Any, Optional

from suscriptor import Suscriptor


class RegistroDeEventos(Suscriptor):
    def __init__(self, ruta_archivo: Optional[str] = None) -> None:
        self.eventos: list[dict[str, Any]] = []
        self.ruta_archivo = ruta_archivo

    def actualizar(self, datos: dict[str, Any]) -> None:
        self.eventos.append(datos)
        if self.ruta_archivo:
            with open(self.ruta_archivo, "a", encoding="utf-8") as archivo:
                archivo.write(f"{datos}\n")

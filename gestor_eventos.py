"""Actividad 3.1 — Lista de suscripción por tipo de evento (EventManager)."""

from __future__ import annotations

from typing import Any

from suscriptor import Oyente, Suscriptor


class GestorEventos:
    def __init__(self) -> None:
        self._oyentes: dict[str, list[Oyente]] = {}

    def suscribir(self, tipo_evento: str, suscriptor: Oyente) -> None:
        lista = self._oyentes.setdefault(tipo_evento, [])
        if suscriptor not in lista:  # evita avisos duplicados
            lista.append(suscriptor)

    def cancelar(self, tipo_evento: str, suscriptor: Oyente) -> None:
        lista = self._oyentes.get(tipo_evento, [])
        if suscriptor in lista:
            lista.remove(suscriptor)

    def notificar(self, tipo_evento: str, datos: dict[str, Any]) -> None:
        # Se recorre una copia para permitir bajas durante la notificación.
        for oyente in list(self._oyentes.get(tipo_evento, [])):
            if isinstance(oyente, Suscriptor):
                oyente.actualizar(datos)
            else:
                oyente(datos)

    def suscriptores_de(self, tipo_evento: str) -> list[Oyente]:
        return list(self._oyentes.get(tipo_evento, []))

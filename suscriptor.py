"""Actividad 3.1 — Interfaz suscriptora (rol «Suscriptor» del patrón)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Union


class Suscriptor(ABC):
    """El notificador solo conoce este método."""

    @abstractmethod
    def actualizar(self, datos: dict[str, Any]) -> None:
        """Reacciona a un evento. `datos` es la información de contexto."""


# Un oyente puede ser un objeto Suscriptor o una función.
Oyente = Union[Suscriptor, Callable[[dict[str, Any]], None]]

"""Cliente: crea el notificador y los suscriptores y los conecta.

Cubre las actividades 3.4 (configuración y filtrado por evento),
3.5 (baja en tiempo de ejecución), 3.7 (suscriptor como función) y
4.2 (cuarto suscriptor sin tocar Tienda).
"""
from __future__ import annotations

from alerta_por_correo import AlertaPorCorreo
from aviso_por_whatsapp import AvisoPorWhatsApp
from cliente_interesado import ClienteInteresado
from registro_de_eventos import RegistroDeEventos
from tienda import PRECIO_CAMBIADO, PRODUCTO_DISPONIBLE, Tienda


def titulo(texto: str) -> None:
    print(f"\n--- {texto} ---")


def main() -> None:
    tienda = Tienda("TecnoQuindío")

    # 1. Crear suscriptores
    ana = ClienteInteresado("Ana")
    luis = ClienteInteresado("Luis")
    registro = RegistroDeEventos()
    correo = AlertaPorCorreo("ventas@tecnoquindio.co",
                             "Revisar campaña para {producto}")

    # 2. Registrarlos solo en los eventos que les interesan
    tienda.eventos.suscribir(PRODUCTO_DISPONIBLE, ana)
    tienda.eventos.suscribir(PRODUCTO_DISPONIBLE, luis)
    tienda.eventos.suscribir(PRECIO_CAMBIADO, luis)
    tienda.eventos.suscribir(PRODUCTO_DISPONIBLE, registro)
    tienda.eventos.suscribir(PRECIO_CAMBIADO, registro)
    tienda.eventos.suscribir(PRECIO_CAMBIADO, correo)

    titulo("Llega el iPhone (producto_disponible)")
    tienda.reabastecer("iPhone 17", 5)

    titulo("Cambia el precio (precio_cambiado): Ana NO recibe nada")
    tienda.cambiar_precio("iPhone 17", 4_200_000)

    titulo("Actividad 3.5: Ana cancela su suscripción en tiempo de ejecución")
    tienda.eventos.cancelar(PRODUCTO_DISPONIBLE, ana)
    tienda.reabastecer("AirPods", 10)

    titulo("Actividad 3.7: suscriptor como lambda")
    tienda.eventos.suscribir(
        PRODUCTO_DISPONIBLE,
        lambda d: print(f"[lambda] Stock nuevo de {d['producto']}: {d['cantidad']}"),
    )
    tienda.reabastecer("Apple Watch", 3)

    titulo("Actividad 4.2: cuarto suscriptor sin modificar Tienda")
    tienda.eventos.suscribir(PRODUCTO_DISPONIBLE, AvisoPorWhatsApp("+57 300 000 0000"))
    tienda.reabastecer("iPad", 2)

    titulo("Resumen")
    print(f"Avisos recibidos por Ana: {len(ana.avisos)}")
    print(f"Avisos recibidos por Luis: {len(luis.avisos)}")
    print(f"Eventos en el registro: {len(registro.eventos)}")
    print(f"Correos enviados: {len(correo.enviados)}")


if __name__ == "__main__":
    main()

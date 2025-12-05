TEXTO_OPCIONES = ["Mostrar Gráfico Acumulado Diario",
                  "Mostrar Gráfico Tarta por Provincia",
                  "Comentarios"]


def mostrar_menu() -> None:
    print(f"""
    P R O Y E C T O   F I N A L

      1) {TEXTO_OPCIONES[0]}
      2) {TEXTO_OPCIONES[1]}
      3) {TEXTO_OPCIONES[2]}

      0) Salir del menú
      """)

def solicitar_opcion() -> str:
    return input("Elige una opción (0-3): ").strip()

def mostrar_despedida() -> None:
    print("\nMuchas gracias por usar nuestra aplicación, hasta la próxima vez.")

def mostrar_mensaje(mensaje: str):
    print(f"\n{mensaje}")
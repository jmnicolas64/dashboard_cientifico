TEXTO_OPCIONES = ["Mostrar Gráfico Acumulado Diario",
                  "Mostrar Gráfico Tarta por Provincia"]


def mostrar_menu() -> None:
    print(f"""
    P R O Y E C T O   F I N A L

      1) {TEXTO_OPCIONES[0]}
      2) {TEXTO_OPCIONES[1]}

      0) Salir del menú
      """)

def solicitar_opcion() -> str:
    return input("Elige una opción (0-2): ").strip()

def mostrar_despedida() -> None:
    print("\nMuchas gracias por usar nuestra aplicación, hasta la próxima vez.")
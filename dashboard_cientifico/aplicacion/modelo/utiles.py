import os


def limpiar_pantalla() -> None:
    if os.name == 'nt':
        os.system('cls')  # Windows
        pass
    else:
        os.system('clear')  # Mac/linux


def cabecera(opcion: str, texto_opcion: str) -> None:
    print(f"\nOPCION {opcion}: {texto_opcion}")
    print("-" * (10 + len(texto_opcion)), "\n")


def pie() -> None:
    input("\nPulsa una tecla para continuar ")

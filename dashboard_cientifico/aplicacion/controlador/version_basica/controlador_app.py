# C:\...\controlador\version_basica\controlador_app.py

# Importación de los módulos Modelo y Vista
from aplicacion.modelo.version_basica import modelo_datos as modelo
from aplicacion.vista.version_basica import vista_graficos as vista
from aplicacion.config.settings import NOMBRE_JSON, OPCIONES_GRAFICOS

class ControladorBasico:
    
    def __init__(self):
        self.datos_agrupados = None
        self.nombre_json = NOMBRE_JSON

    def _cargar_datos_si_necesario(self):
        """Intenta cargar los datos del JSON si aún no están en memoria."""
        if self.datos_agrupados is None:
            self.datos_agrupados = modelo.cargar_datos(self.nombre_json)
        return self.datos_agrupados

    def ejecutar_menu_ejercicio2(self):
        datos = self._cargar_datos_si_necesario()
        if not datos: return
        
        while True:
            vista.mostrar_menu_ejercicio_secundario("GRÁFICAS DE BARRAS POR PROVINCIA")
            opcion = input("Introduce tu elección (1-5): ")
            if opcion == '5': break
            
            try:
                opcion_int = int(opcion)
                if opcion_int in OPCIONES_GRAFICOS:
                    metrica = OPCIONES_GRAFICOS[opcion_int]['metrica']
                    vista.generar_grafica_barras(datos, metrica)
                else:
                    print("Opción no válida.")
            except ValueError:
                print("Entrada no válida.")

    def ejecutar_menu_ejercicio3(self):
        datos = self._cargar_datos_si_necesario()
        if not datos: return

        while True:
            vista.mostrar_menu_ejercicio_secundario("ANÁLISIS DE EXTREMOS Y GRÁFICAS DE QUESO")
            opcion = input("Introduce tu elección (1-5): ")
            if opcion == '5': break

            try:
                opcion_int = int(opcion)
                if opcion_int in OPCIONES_GRAFICOS:
                    metrica = OPCIONES_GRAFICOS[opcion_int]['metrica']
                    totales, p_max, p_min = modelo.calcular_totales_y_extremos(datos, metrica)
                    if totales:
                        vista.generar_grafica_queso(totales, metrica, p_max, p_min)
                else:
                    print("Opción no válida.")
            except ValueError:
                print("Entrada no válida.")

    def ejecutar_menu_principal(self):
        """Bucle principal de la versión básica."""
        while True:
            vista.mostrar_menu_principal()
            opcion = input("Selecciona una opción (1-4): ")
            
            if opcion == '1':
                self.datos_agrupados = modelo.procesar_datos_csv(modelo.NOMBRE_CSV, self.nombre_json)
            
            elif opcion == '2':
                self.ejecutar_menu_ejercicio2()
            
            elif opcion == '3':
                self.ejecutar_menu_ejercicio3()
                
            elif opcion == '4':
                print("Programa finalizado. ¡Hasta pronto!")
                break
            
            else:
                print("Opción no válida. Por favor, introduce un número del 1 al 4.")


def iniciar_version_basica():
    """Función de entrada que será llamada por el selector de versión."""
    controlador = ControladorBasico()
    controlador.ejecutar_menu_principal()
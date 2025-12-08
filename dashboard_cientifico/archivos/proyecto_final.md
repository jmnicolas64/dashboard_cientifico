## Proyecto fin de curso

Ejecución: python -m dashboard\_cientifico.aplicacion.basica


Ejecución: python -m dashboard\_cientifico.aplicacion.avanzada

El framework utilizado, o más precisamente la librería, es Streamlit (http://streamlit.io/).

He intentado seguir el modelo MVC así que he consultado unas buenas prácticas y he intentado seguirlas lo más posible en la estructura de archivos y carpetas.

La utilidad de seguir el patrón MVC la he comprobado desarrollando 2 versiones:

* Básica: desarrollado en base a menus Python
* Avanzada: desarrollada con Streamlit

En la versión **Avanzada** para que el proyecto resultase más sustancial he generado aleatoriamente los datos de los meses de junio a diciembre de 2021, datos que se pueden ir incorporando a la aplicación en el apartado Gestión. He decidido utilizar como fuente de datos una base de datos sqlite, pero como el ejercicio 1 del proyecto solicitaba crear un JSON con los datos lo que hago es generarlo y descargarlo a la carpeta ‘descargas’ y dar la posibilidad de visualizarlo directamente en la aplicación en el apartado Datos. Este JSON se va actualizando conforme se van añadiendo los datos de los meses generados.

En la versión **Básica** se muestra lo que pide el ejercicio. El archivo JSON se genera automáticamente cuando carga inicialmente los datos y queda disponible en la carpeta 'descargas'. La fuente de datos es la db para compatibilizar las 2 versiones.

Me he centrado en el estudio de Streamlit, Pandas y gráficos.

Los apartados de la aplicación avanzada son:

* **Dashboard**; responde a los ejercicios 2 y 3 del proyecto.
* **Datos**; responde al ejercicio 1 del proyecto además de presentar los datos en bruto para poder consultarlos.
* **Análisis**; en este apartado he querido ensayar con distintos métodos de pandas y formatos de gráficos. Dada la baja calidad de los datos, pues son completamente aleatorios, el significado de los gráficos no es relevante, lo que he considerado relevante es su elaboración.
* **Gestión**; este apartado es para manejar los datos que se van incorporando.

# Waters-Game

Este proyecto implementa una versión del juego Snake utilizando Python. El repositorio está organizado en varias carpetas que separan recursos, datos, código principal y archivos generados durante la compilación. A continuación se describe de manera general qué contiene cada parte del proyecto y para qué sirve.

## Carpeta SnakeFight

Esta es la carpeta principal del proyecto. Dentro de ella se encuentra todo el código fuente, los recursos gráficos, los datos utilizados por el juego y los archivos generados por PyInstaller cuando se crea el ejecutable.

## Carpeta Assets

Contiene los recursos visuales del juego. En la subcarpeta Images se incluyen las imágenes utilizadas durante la ejecución, como íconos o elementos gráficos del juego. Esta carpeta se usa únicamente para almacenar archivos que serán cargados desde el código.

## Carpeta build/main

Esta carpeta es generada automáticamente al crear un ejecutable del juego mediante PyInstaller. Los archivos que se encuentran aquí no forman parte del código fuente. Son archivos temporales que PyInstaller utiliza internamente para empaquetar la aplicación. No es necesario modificarlos ni usarlos directamente.

## Carpeta Core

Aquí se encuentra la lógica principal del juego. Es la parte más importante del proyecto.

- __init__.py: define la carpeta como un módulo de Python.
- config.py: contiene configuraciones generales como parámetros del juego, dimensiones y valores constantes.
- game.py: implementa el comportamiento del juego, incluyendo el movimiento, las reglas y la actualización del estado.
- menu.py: maneja el menú principal y cualquier interacción inicial antes de entrar al juego.
- utils.py: contiene funciones auxiliares que apoyan al resto del código.

Esta carpeta concentra toda la funcionalidad principal del programa.

## Carpeta Data

Almacena información que el juego usa o genera. El archivo settings.json guarda configuraciones del usuario o valores ajustables. El archivo users.csv contiene datos relacionados con usuarios o puntajes. También incluye el script generate_users_csv.py, que sirve para generar o actualizar dicho archivo.

## Carpeta dist

Esta carpeta se genera después de compilar el proyecto con PyInstaller. Contiene el archivo ejecutable final (main.exe). Esta es la carpeta que se entrega a un usuario final que desea ejecutar el juego sin necesidad de Python instalado.

## Archivos en la raíz de SnakeFight

El archivo main.py es el punto de entrada de la aplicación cuando se corre directamente desde Python. El archivo main.spec pertenece a PyInstaller y define cómo debe construirse el ejecutable. También se incluye un archivo .gitignore para evitar que archivos temporales o generados automáticamente sean añadidos al repositorio.

## Instrucciones de ejecución

Para ejecutar el juego desde Python, es necesario tener instalado Python 3. El juego se inicia ejecutando el archivo main.py ubicado en la carpeta SnakeFight. Desde la terminal, la ejecución se realiza con:

python main.py

Para crear un ejecutable independiente, se utiliza PyInstaller. Una vez instalado PyInstaller, se puede generar el ejecutable ejecutando:

pyinstaller main.spec

Esto creará una carpeta dist donde aparecerá el archivo main.exe listo para ejecutarse.

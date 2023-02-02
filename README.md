# TFG: Esteban Martínez Hoces
# Hundsor

## Table of Contents
1. [Descripcion](#desc)
2. [Technologies](#technologies)
3. [Instalacion](#instalacion)
4. [Instrucciones de uso](#instruc)

## Descripcion
***
Este proyecto busca permitir a la gran mayoría de usuarios el uso de su ordenador a través de gestos con la mano haciendo uso de la cámara. Hundsor es un sistema programado integramente en python, el cual te da distintas opciones para el control del dispositivo. Este sistema hace uso de dos redes neuronales y una red recurrente. Además, permite el ajuste de uso del sistema en el caso de disponer dos cámaras basandose en el cálculo de distancias de la geometría multivista. Además, se incluyen los sets de datos que se han usado para los modelos, así como el código de entrenamiento y creación de modelos en un caso en un archivo py y el otro en u cuaderno de jupyter.

## Technologies
***
En este proyecto se han usado diversidad de librerías como tensorflow, keras, mouse, twinkter, que han hecho posible el desarrollo del sistema. Para más detalle consultar la memoria. 

## Instalacion
***
Para que el sistema pueda ejecutar lo primero que debe hacer es clonar el repositorio e importar los módulos necesarios haciendo uso del comando.
```
$ git clone https://example.com
$ cd proyect
$ pip install -r requirements.txt
```
Opcional. Si desea usar la visión estereo deberá modificar los archivos confi.csv en la carpeta UI/Depth y confiMinMax.csv en UI/Prediction. Para más detalle consultar el archivo Instrucciones_Calibracion.txt.
Por último para ejecutar el sistema, introduzca el siguiente comando 
```
$ python3 UI/gui.py
```

## Instrucciones de uso
***
En la interfaz gráfica del sistema se describen las distintas acciones las cuales se pueden realizar.

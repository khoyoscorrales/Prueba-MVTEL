# Resumen de Transacciones - Proyecto Flask

Este proyecto es una aplicación web construida con Flask que permite gestionar transacciones comerciales. 
Los usuarios pueden agregar nuevas transacciones mediante un formulario o mediante un formato JSON, y la aplicación calcula 
un resumen con la información sobre el cliente con mayor gasto y los productos más vendidos.

## Requisitos

Para ejecutar el proyecto, asegúrate de tener instalados los siguientes requisitos:

- Python 3.6 o superior
- Pip (gestor de paquetes de Python)

### Dependencias

El proyecto utiliza las siguientes dependencias de Python:

- Flask: Framework web para construir la aplicación.
- JSON: Para leer y escribir los datos de las transacciones.
- Collections (defaultdict): Para facilitar el manejo de datos agregados.

Puedes instalar las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt


*Archivos
app.py: El archivo principal que contiene la aplicación Flask.
data.json: El archivo JSON que almacena las transacciones.
templates/resumen.html: La plantilla HTML que muestra el resumen de las transacciones.


Inicia la aplicación:

python app.py

Abre tu navegador y ve a la URL http://127.0.0.1:5000/resumen para ver el resumen de las transacciones.
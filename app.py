from flask import Flask, render_template, request, jsonify
import json
from collections import defaultdict

app = Flask(__name__)

DATA_FILE = (r"data.json")

# Helper para leer y escribir datos en el archivo JSON
def leer_datos():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def escribir_datos(datos):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(datos, file, ensure_ascii=False, indent=4)

@app.route('/transacciones', methods=['POST'])
def agregar_transaccion():
    try:
        if request.is_json:
            # Si se recibe un JSON, procesar como se hacía antes
            nueva_transaccion = request.json
        else:
            # Si se recibe un formulario, procesar los datos de ese formulario
            nueva_transaccion = {
                "id": len(leer_datos()) + 1,  # Se genera un nuevo id secuencial
                "cliente": request.form.get('cliente'),
                "productos": [
                    {
                        "nombre": request.form.get('producto_nombre_1'),
                        "precio": float(request.form.get('producto_precio_1')),
                        "cantidad": int(request.form.get('producto_cantidad_1'))
                    },
                    {
                        "nombre": request.form.get('producto_nombre_2'),
                        "precio": float(request.form.get('producto_precio_2')),
                        "cantidad": int(request.form.get('producto_cantidad_2'))
                    }
                ],
                "fecha": request.form.get('fecha')
            }

        # Validación básica
        if not nueva_transaccion or not all(k in nueva_transaccion for k in ("id", "cliente", "productos", "fecha")):
            return jsonify({"error": "Datos incompletos o mal formateados"}), 400

        # Validar que los productos tengan los campos correctos
        for producto in nueva_transaccion["productos"]:
            if not all(k in producto for k in ("nombre", "precio", "cantidad")):
                return jsonify({"error": "Producto incompleto: falta nombre, precio o cantidad"}), 400

        transacciones = leer_datos()

        # Verificar duplicados por ID
        if any(t["id"] == nueva_transaccion["id"] for t in transacciones):
            return jsonify({"error": "La transacción con este ID ya existe"}), 400

        transacciones.append(nueva_transaccion)
        escribir_datos(transacciones)

        return jsonify({"mensaje": "Transacción agregada exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": f"Error al procesar la transacción: {str(e)}"}), 500

@app.route('/resumen', methods=['GET'])
def obtener_resumen():
    transacciones = leer_datos()

    if not transacciones:
        return jsonify({"error": "No hay transacciones disponibles"}), 404

    cliente_gasto = defaultdict(float)
    producto_ventas = defaultdict(int)

    for transaccion in transacciones:
        cliente = transaccion["cliente"]
        productos = transaccion["productos"]

        for producto in productos:
            nombre = producto["nombre"]
            try:
                precio = float(producto["precio"])
                cantidad = int(producto["cantidad"])
            except ValueError:
                return jsonify({"error": "Precio o cantidad mal formateados en la transacción"}), 400

            cliente_gasto[cliente] += precio * cantidad
            producto_ventas[nombre] += cantidad

    cliente_mayor_gasto = max(cliente_gasto, key=cliente_gasto.get, default="N/A")
    gasto_mayor = cliente_gasto[cliente_mayor_gasto]

    max_cantidad = max(producto_ventas.values(), default=0)
    productos_mas_vendidos = [
        {"producto": producto, "cantidad": cantidad}
        for producto, cantidad in producto_ventas.items() if cantidad == max_cantidad
    ]

    resumen = {
        "cliente_mayor_gasto": cliente_mayor_gasto,
        "gasto_mayor": gasto_mayor,
        "productos_mas_vendidos": productos_mas_vendidos
    }

    return render_template('resumen.html', resumen=resumen)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
import sqlite3 
import mysql.connector
import pymysql

app = Flask(__name__)

# Conexión a la base de datos
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="db",
            user="admin",
            password="123456",
            database="pfddatabase",
            port=3306
        )
        return connection
    except mysql.connector.errors.DatabaseError as e:
        print(f"Error de conexión: {e}")
        return None
    
# Endpoint para obtener logs
@app.route('/logs', methods=['GET'])
def get_logs():
    tipo = request.args.get('tipo')
    documento = request.args.get('documento')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM main_log WHERE 1=1"
        params = []

        if tipo:
            query += " AND tipo = %s"
            params.append(tipo)
        if documento:
            query += " AND documento LIKE %s"
            params.append(f"%{documento}%")
        if fecha_inicio:
            query += " AND DATE(fecha) >= %s"
            params.append(fecha_inicio)
        if fecha_fin:
            query += " AND DATE(fecha) <= %s"
            params.append(fecha_fin)
        cursor.execute(query, params)
        logs = cursor.fetchall()

        cursor.close()
        connection.close()

        if not logs:
            return jsonify([])

        return jsonify(logs)

    except pymysql.MySQLError as e:
        print(f"Error al conectar o ejecutar la consulta: {e}")
        return jsonify([])

    except Exception as e:
        print(f"Error inesperado: {e}")
        return jsonify([])

@app.route('/persona', defaults={'id': None}, methods=['GET'])
@app.route('/persona/<int:id>', methods=['GET'])
def get_persona(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if id is None:
        # Consulta para obtener todas las personas
        cursor.execute("SELECT * FROM auth_mysite_persona")
        personas = cursor.fetchall()  # Obtener todos los resultados
        cursor.close()
        connection.close()
        return jsonify(personas)
    else:
        # Consulta para obtener una persona específica por id
        cursor.execute("SELECT * FROM auth_mysite_persona WHERE id = %s", (id,))
        persona = cursor.fetchone()  # Obtener un solo resultado
        cursor.close()
        connection.close()

        if persona:
            return jsonify(persona)
        else:
            return jsonify({'message': 'Persona no encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)
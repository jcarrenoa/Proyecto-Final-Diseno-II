import sqlite3

# Conecta al archivo db.sqlite3
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Listar todas las tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Ver los registros de cada tabla
for table in tables:
    print(f"Registros de la tabla {table[0]}:")
    cursor.execute(f"SELECT * FROM {table[0]};")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    print("\n" + "="*50 + "\n")

# Cerrar la conexión
conn.close()

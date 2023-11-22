import mysql.connector
import json

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='next_game'
)

cursor = conn.cursor()

nombres = ['Juan', 'María', 'Pedro']

nombres_json = json.dumps(nombres)

try:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Laptop (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Name TEXT,
            Price INT,
            Purchase_date DATE
        )
    ''')

    mySql_insert_query = """INSERT INTO Laptop (Name) VALUES (%s) """
    records_to_insert = ['HP Pavilion Power', 'MSI WS75 9TL-496', 'Microsoft Surface']
    
    """ cursor.execute('INSERT INTO ejemplos (nombres_json) VALUES (%s)', (nombres_json,))  # Asegúrate de tener la coma después de (nombres_json,) """
    mySql_insert_query = f"INSERT INTO Laptop (Name) VALUES (%s)"

    for record in records_to_insert:
        cursor.execute(mySql_insert_query, (record,))

    conn.commit()

    print("Inserción exitosa.")

except mysql.connector.Error as err:
    print(f"Error de MySQL: {err}")

finally:
    cursor.close()
    conn.close()
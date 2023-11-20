import mysql.connector

conexion = mysql.connector.connect(
    user='sa', 
    password='root', 
    host='localhost', 
    database='Next_Game', 
    port='3306'
)

print(conexion)
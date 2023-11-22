import requests 
from bs4 import BeautifulSoup
import mysql.connector
import json

conexion = mysql.connector.connect(
    user='root', 
    password='root', 
    host='localhost', 
    database='next_game', 
    port='3306'
)

cursor = conexion.cursor()

def resultadosContextoEquipoLocal(equipo, fecha):
    query = """
        SELECT resultados.*, posiciones.posicion
        FROM resultados
        JOIN posiciones ON resultados.local = posiciones.equipo
        WHERE resultados.local = %s
            AND resultados.fecha = %s
            AND posiciones.fecha = %s
            AND resultados.year = posiciones.year
    """

    cursor.execute(query, (equipo, fecha, fecha))
    resultados = cursor.fetchall()
    
    return resultados
    
def resultadosContextoEquipoVisitante(equipo, fecha):
    query = """
        SELECT resultados.*, posiciones.posicion
        FROM resultados
        JOIN posiciones ON resultados.visitante = posiciones.equipo
        WHERE resultados.visitante = %s
            AND resultados.fecha = %s
            AND posiciones.fecha = %s
            AND resultados.year = posiciones.year
    """

    cursor.execute(query, (equipo, fecha, fecha))
    resultados = cursor.fetchall()
    
    return resultados

def posicionesAdversariosLocal(resultadosContextoVisitante):   
    response = []
    for adversarioData in resultadosContextoVisitante:
        fecha = adversarioData[1]
        equipo = adversarioData[2]
        year = adversarioData[5]

        cursor.execute("""
            SELECT posicion
            FROM posiciones
            WHERE equipo = %s
            AND fecha = %s
            AND year = %s
        """, (equipo, fecha, year))

        posicionAdversario, = cursor.fetchall()
        
        obj_response = {
            'year': adversarioData[5],
            'fecha': adversarioData[1],
            'local': adversarioData[2],
            'local_posicion': posicionAdversario,
            'visitante': adversarioData[3],
            'visitante_posicion': adversarioData[6],
            'resultado': adversarioData[4]
        } 
        
        response.append(obj_response)
    
    return response

def posicionesAdversariosVisitante(resultadosContextoVisitante):   
    response = []
    for adversarioData in resultadosContextoVisitante:
        fecha = adversarioData[1]
        equipo = adversarioData[2]
        year = adversarioData[5]

        cursor.execute("""
            SELECT posicion
            FROM posiciones
            WHERE equipo = %s
            AND fecha = %s
            AND year = %s
        """, (equipo, fecha, year))

        posicionAdversario, = cursor.fetchall()
        
        obj_response = {
            'year': adversarioData[5],
            'fecha': adversarioData[1],
            'local': adversarioData[2],
            'local_posicion': posicionAdversario,
            'visitante': adversarioData[3],
            'visitante_posicion': adversarioData[6],
            'resultado': adversarioData[4]
        } 
        
        response.append(obj_response)
    
    return response

try:
    fecha = 14
    equipoLocal = 'Cadiz'
    equipoVisitante = 'Real Madrid'
    
    contextoLocal = resultadosContextoEquipoLocal(equipoLocal, fecha)
    contextoVisitante = resultadosContextoEquipoVisitante(equipoVisitante, fecha)
    
    resultadoContextoLocal = posicionesAdversariosLocal(contextoLocal)
    resultadoContextoVisitante = posicionesAdversariosVisitante(contextoVisitante)
    
    print(resultadoContextoVisitante)
    

except mysql.connector.Error as err:
    print("Error de MySQL: {err}")
finally:
    cursor.close()
    conexion.close()
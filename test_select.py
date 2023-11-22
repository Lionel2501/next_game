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

def contextoLocalFechaData(equipo, fecha):
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
    
def contextoVisitanteFechaData(equipo, fecha):
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

def getContextoLocalFecha(resultadosContextoVisitante):   
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

def getContextoVisitanteFecha(resultadosContextoVisitante):   
    response = []
    for adversarioData in resultadosContextoVisitante:
        fecha = adversarioData[1]
        equipo = adversarioData[2]
        year = adversarioData[5]

        cursor.execute(""" SELECT posicion FROM posiciones WHERE equipo = %s AND fecha = %s AND year = %s """, (equipo, fecha, year))

        posicionAdversario = cursor.fetchall()
        
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

def getContextoRivalida(equipoLocal, equipoVisitante):
    query = """
        SELECT 
            resultados.*, 
            posiciones_local.posicion AS local_posicion, 
            posiciones_visitante.posicion AS visitante_posicion
        FROM resultados
        LEFT JOIN posiciones AS posiciones_local ON resultados.local = posiciones_local.equipo
        LEFT JOIN posiciones AS posiciones_visitante ON resultados.visitante = posiciones_visitante.equipo
        WHERE 
            resultados.local = %s 
            AND resultados.visitante = %s
            AND resultados.fecha = posiciones_local.fecha
            AND resultados.year = posiciones_local.year
            AND resultados.fecha = posiciones_visitante.fecha
            AND resultados.year = posiciones_visitante.year;
    """

    cursor.execute(query, (equipoLocal, equipoVisitante))
    resultados = cursor.fetchall()
    
    return resultados
    
    
try:
    fecha = 14
    equipoLocal = 'Cadiz'
    equipoLocalPosicion = 16
    equipoVisitante = 'Real Madrid'
    equipoVisitantePosicion = 2
    
    contextoLocalFecha = contextoLocalFechaData(equipoLocal, fecha)
    contextoVisitanteFecha = contextoVisitanteFechaData(equipoVisitante, fecha)
    
    resultadoContextoLocalFecha = getContextoLocalFecha(contextoLocalFecha)
    resultadoContextoVisitanteFecha = getContextoVisitanteFecha(contextoVisitanteFecha)
    
    """     
    resultadoContextoRivalida = getContextoRivalida(equipoLocal, equipoVisitante)
    print(resultadoContextoRivalida) 
    """
    

except mysql.connector.Error as err:
    print("Error de MySQL: {err}")
finally:
    cursor.close()
    conexion.close()
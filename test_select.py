import requests 
from bs4 import BeautifulSoup
import mysql.connector
import json
from prettytable import PrettyTable

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

def getContextoLocalFecha(resultadosContextoVisitante, equipoVisitantePosicion):   
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

        if (int(posicionAdversario[0])  - equipoVisitantePosicion) > 10 :
            obj_response = {
                'year': adversarioData[5],
                'fecha': adversarioData[1],
                'local': adversarioData[2],
                'local_posicion': posicionAdversario,
                'visitante': adversarioData[3],
                'visitante_posicion': adversarioData[6],
                'resultado': adversarioData[4],
                'contexto': 'local fecha'
            } 
            
            response.append(obj_response)
    
    return response

def getContextoVisitanteFecha(resultadosContextoVisitante, equipoLocalPosicion):   
    response = []
    for adversarioData in resultadosContextoVisitante:
        fecha = adversarioData[1]
        equipo = adversarioData[2]
        year = adversarioData[5]

        cursor.execute(""" SELECT posicion FROM posiciones WHERE equipo = %s AND fecha = %s AND year = %s """, (equipo, fecha, year))

        posicionAdversario = cursor.fetchall()
        posicionAdversario_transform = posicionAdversario
        posicionAdversario_clear = int(posicionAdversario_transform[0][0])
        if (posicionAdversario_clear  - equipoVisitantePosicion) > 10:
            obj_response = {
                'year': adversarioData[5],
                'fecha': adversarioData[1],
                'local': adversarioData[2],
                'local_posicion': posicionAdversario_clear,
                'visitante': adversarioData[3],
                'visitante_posicion': adversarioData[6],
                'resultado': adversarioData[4],
                'contexto': 'visitante fecha'
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
    response = []
    
    for resultado in resultados:
        obj_response = {
            'year': resultado[5],
            'fecha': resultado[1],
            'local': resultado[2],
            'local_posicion': resultado[6],
            'visitante': resultado[3],
            'visitante_posicion': resultado[7],
            'resultado': resultado[4],
            'contexto': 'rivalida'
        } 
        
        response.append(obj_response)
    
    return response
    
    
try:
    fecha = 14
    equipoLocal = 'Cadiz'
    equipoLocalPosicion = 16
    equipoVisitante = 'Real Madrid'
    equipoVisitantePosicion = 2
    
    contextoLocalFecha = contextoLocalFechaData(equipoLocal, fecha)
    contextoVisitanteFecha = contextoVisitanteFechaData(equipoVisitante, fecha)
    
    resultadoContextoLocalFecha = getContextoLocalFecha(contextoLocalFecha, equipoVisitantePosicion)
    resultadoContextoVisitanteFecha = getContextoVisitanteFecha(contextoVisitanteFecha, equipoLocalPosicion) 

    resultadoContextoRivalida = getContextoRivalida(equipoLocal, equipoVisitante)
    
    todos = resultadoContextoLocalFecha + resultadoContextoVisitanteFecha + resultadoContextoRivalida
    partido = {
        'local': equipoLocal,
        'visitante': equipoVisitante,
        'resultado': '',
        'porcentaje': '',
        'count': len(todos)
    }
    
    for row in todos:
        print(row)
            


    """   
    tabla = PrettyTable()
    if len(resultadoContextoLocalFecha) > 0:
        tabla.field_names = resultadoContextoLocalFecha[0].keys()
    if len(resultadoContextoVisitanteFecha) > 0:
        tabla.field_names = resultadoContextoVisitanteFecha[0].keys()
    if len(resultadoContextoRivalida) > 0:
        tabla.field_names = resultadoContextoRivalida[0].keys()  
    for resultado in resultadoContextoLocalFecha:
        tabla.add_row(resultado.values())
    for resultado in resultadoContextoVisitanteFecha:
        tabla.add_row(resultado.values())
    for resultado in resultadoContextoRivalida:
        tabla.add_row(resultado.values()) 
        
    print(tabla)
    """

    

except mysql.connector.Error as err:
    print("Error de MySQL: {err}")
finally:
    cursor.close()
    conexion.close()
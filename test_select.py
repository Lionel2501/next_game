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

def getPartidosDelDia(fecha):
    query = """
        SELECT resultados.local, resultados.visitante
        FROM resultados
        WHERE fecha = %s AND year = "2023-2024"
    """
    cursor.execute(query, (fecha,))
    resultados = cursor.fetchall()
    
    return resultados
    
def contextoLocalFechaData(equipo, fecha, posicion_local, posicion_visitante):
    fecha_l_1 = fecha - 1
    fecha_l_1 = str(fecha_l_1)
    fecha_l_2 = fecha - 2
    fecha_l_2 = str(fecha_l_2)
    fecha_l_3 = fecha - 3
    fecha_l_3 = str(fecha_l_3)
    fecha_m_1 = fecha + 1
    fecha_m_1 = str(fecha_m_1)
    fecha_m_2 = fecha + 2
    fecha_m_2 = str(fecha_m_2)
    fecha_m_3 = fecha + 3
    fecha_m_3 = str(fecha_m_3)
    
    posicion_local_menos_1 = posicion_local - 1
    posicion_local_menos_1 = str(posicion_local_menos_1)
    posicion_local_menos_2 = posicion_local - 2
    posicion_local_menos_2 = str(posicion_local_menos_2)
    posicion_local_mas_1 = posicion_local + 1
    posicion_local_mas_1 = str(posicion_local_mas_1)
    posicion_local_mas_2 = posicion_local + 2
    posicion_local_mas_2 = str(posicion_local_mas_2)
    
    posicion_visitante_menos_1 = posicion_visitante - 1
    posicion_visitante_menos_1 = str(posicion_visitante_menos_1)
    posicion_visitante_menos_2 = posicion_visitante - 2
    posicion_visitante_menos_2 = str(posicion_visitante_menos_2)
    posicion_visitante_mas_1 = posicion_visitante + 1
    posicion_visitante_mas_1 = str(posicion_visitante_mas_1)
    posicion_visitante_mas_2 = posicion_visitante + 2
    posicion_visitante_mas_2 = str(posicion_visitante_mas_2)
    
    
    query = """
        SELECT liga.*
        FROM liga
        WHERE liga.local = %s
            AND (liga.fecha = %s OR liga.fecha = %s OR liga.fecha = %s  OR liga.fecha = %s  OR liga.fecha = %s  OR liga.fecha = %s  OR liga.fecha = %s)
            AND (liga.local_posicion = %s OR liga.local_posicion = %s OR liga.local_posicion = %s OR liga.local_posicion = %s OR liga.local_posicion = %s)
            AND (liga.visitante_posicion = %s OR liga.visitante_posicion = %s OR liga.visitante_posicion = %s OR liga.visitante_posicion = %s OR liga.visitante_posicion = %s)
    """
    """
    fecha_arr = [fecha_l_1, fecha_l_2, fecha_l_3, fecha_m_1, fecha_m_2, fecha_m_3]
    fechas_tuple = tuple(fecha_arr,) 
    """
    cursor.execute(query, (equipo, 
        fecha_l_3, fecha_l_2, fecha_l_1, fecha, fecha_m_1, fecha_m_2, fecha_m_3, 
        posicion_local_menos_2, posicion_local_menos_1, posicion_local, posicion_local_mas_1, posicion_local_mas_2, 
        posicion_visitante_menos_2, posicion_visitante_menos_1, posicion_visitante, posicion_visitante_mas_1, posicion_visitante_mas_2))
    resultados = cursor.fetchall()
    
    return resultados
    
def contextoVisitanteFechaData(equipo, fecha, posicion_local, posicion_visitante):
    fecha_l_1 = fecha - 1
    fecha_l_1 = str(fecha_l_1)
    fecha_l_2 = fecha - 2
    fecha_l_2 = str(fecha_l_2)
    fecha_l_3 = fecha - 3
    fecha_l_3 = str(fecha_l_3)
    fecha_m_1 = fecha + 1
    fecha_m_1 = str(fecha_m_1)
    fecha_m_2 = fecha + 2
    fecha_m_2 = str(fecha_m_2)
    fecha_m_3 = fecha + 3
    fecha_m_3 = str(fecha_m_3)
    
    posicion_local_menos_1 = posicion_local - 1
    posicion_local_menos_1 = str(posicion_local_menos_1)
    posicion_local_menos_2 = posicion_local - 2
    posicion_local_menos_2 = str(posicion_local_menos_2)
    posicion_local_mas_1 = posicion_local + 1
    posicion_local_mas_1 = str(posicion_local_mas_1)
    posicion_local_mas_2 = posicion_local + 2
    posicion_local_mas_2 = str(posicion_local_mas_2)
    
    posicion_visitante_menos_1 = posicion_visitante - 1
    posicion_visitante_menos_1 = str(posicion_visitante_menos_1)
    posicion_visitante_menos_2 = posicion_visitante - 2
    posicion_visitante_menos_2 = str(posicion_visitante_menos_2)
    posicion_visitante_mas_1 = posicion_visitante + 1
    posicion_visitante_mas_1 = str(posicion_visitante_mas_1)
    posicion_visitante_mas_2 = posicion_visitante + 2
    posicion_visitante_mas_2 = str(posicion_visitante_mas_2)
    
    
    query = """
        SELECT liga.*
        FROM liga
        WHERE liga.visitante = %s
            AND (liga.fecha = %s OR liga.fecha = %s OR liga.fecha = %s  OR liga.fecha = %s  OR liga.fecha = %s  OR liga.fecha = %s  OR liga.fecha = %s)
            AND (liga.local_posicion = %s OR liga.local_posicion = %s OR liga.local_posicion = %s OR liga.local_posicion = %s OR liga.local_posicion = %s)
            AND (liga.visitante_posicion = %s OR liga.visitante_posicion = %s OR liga.visitante_posicion = %s OR liga.visitante_posicion = %s OR liga.visitante_posicion = %s)
    """
    """
    fecha_arr = [fecha_l_1, fecha_l_2, fecha_l_3, fecha_m_1, fecha_m_2, fecha_m_3]
    fechas_tuple = tuple(fecha_arr,) 
    """
    cursor.execute(query, (equipo, 
        fecha_l_3, fecha_l_2, fecha_l_1, fecha, fecha_m_1, fecha_m_2, fecha_m_3, 
        posicion_local_menos_2, posicion_local_menos_1, posicion_local, posicion_local_mas_1, posicion_local_mas_2, 
        posicion_visitante_menos_2, posicion_visitante_menos_1, posicion_visitante, posicion_visitante_mas_1, posicion_visitante_mas_2))
    resultados = cursor.fetchall()
    
    return resultados

def getContextoLocalFecha(resultadosContextoVisitante):   
    response = []
    for data in resultadosContextoVisitante:
            obj_response = {
                'year': data[7],
                'fecha': data[1],
                'local': data[2],
                'local_posicion': data[3],
                'visitante': data[4],
                'visitante_posicion': data[5],
                'resultado': data[6],
                'contexto': 'local fecha'
            } 
            
            response.append(obj_response)
    
    return response

def getContextoVisitanteFecha(resultadosContextoVisitante):   
    response = []
    for data in resultadosContextoVisitante:
            obj_response = {
                'year': data[7],
                'fecha': data[1],
                'local': data[2],
                'local_posicion': data[3],
                'visitante': data[4],
                'visitante_posicion': data[5],
                'resultado': data[6],
                'contexto': 'visitante fecha'
            } 
            
            response.append(obj_response)
    
    return response

def getContextoRivalida(equipoLocal, equipoVisitante):    
    query = """
        SELECT liga.*
        FROM liga
        WHERE liga.local = %s AND liga.visitante = %s 
    """
    
    cursor.execute(query, (equipoLocal, equipoVisitante))
    resultados = cursor.fetchall()
    
    response = []
    for data in resultados:
            obj_response = {
                'year': data[7],
                'fecha': data[1],
                'local': data[2],
                'local_posicion': data[3],
                'visitante': data[4],
                'visitante_posicion': data[5],
                'resultado': data[6],
                'contexto': 'rivalida'
            } 
            
            response.append(obj_response)
    
    return response

def getResultadoFinal(equipoLocal, equipoVisitante, todos):
    countLocal = {
        'count': 0,
        'equipo': equipoLocal
    }
    countEmpate = {
        'count': 0,
        'equipo': 'empate'
    }
    countVisitante = {
        'count': 0,
        'equipo': equipoVisitante
    }
    
    for row in todos:
        resultado = row['resultado']
        partes = resultado.split(' - ')
        resultadoLocal = partes[0]
        resultadoVisitante = partes[1]
        resultadoLocal = int(resultadoLocal)
        resultadoVisitante = int(resultadoVisitante)
        
        if resultadoLocal > resultadoVisitante:
            countLocal['count'] += 1
        if resultadoVisitante > resultadoLocal:
            countVisitante['count'] += 1
        if resultadoLocal == resultadoVisitante:
            countEmpate['count'] += 1
            
    mayor_count = max(countEmpate['count'], countLocal['count'], countVisitante['count'])
    resultado = 'empate'
    if mayor_count == countLocal['count']:
        resultado = countLocal['equipo']
    if mayor_count == countVisitante['count']:
        resultado = countVisitante['equipo']
        
    total = len(todos)
    porcentaje_calcul = mayor_count / total * 100
    porcentaje_round = round(porcentaje_calcul, 2)
    porcentaje_string = str(porcentaje_round) + '%'
    
    partido = {
        'local': equipoLocal,
        'visitante': equipoVisitante,
        'resultado': resultado,
        'porcentaje': porcentaje_string,
        'resultado_local': countLocal['count'],
        'resultado_empate': countEmpate['count'],
        'resultado_visitante': countVisitante['count'],
        'count': total
    }
    
    
    return partido
    
try:
    partidosDelDia = getPartidosDelDia('14')
    
    print(partidosDelDia)
    """
    fecha = 14
    equipoLocal = 'valencia'
    equipoLocalPosicion = 9
    equipoVisitante = 'celta'
    equipoVisitantePosicion = 18
    
    contextoLocalFecha = contextoLocalFechaData(equipoLocal, fecha, equipoLocalPosicion, equipoVisitantePosicion)
    resultadoContextoLocalFecha = getContextoLocalFecha(contextoLocalFecha)
    
    contextoVisitanteFecha = contextoVisitanteFechaData(equipoVisitante, fecha, equipoLocalPosicion, equipoVisitantePosicion)
    resultadoContextoVisitanteFecha = getContextoVisitanteFecha(contextoVisitanteFecha) 

    resultadoContextoRivalida = getContextoRivalida(equipoLocal, equipoVisitante)
    
    todos = resultadoContextoLocalFecha + resultadoContextoVisitanteFecha + resultadoContextoRivalida
    
    resultadoFinal = getResultadoFinal(equipoLocal, equipoVisitante, todos)

    tabla = PrettyTable()
    if len(resultadoContextoLocalFecha) > 0:
        tabla.field_names = resultadoContextoLocalFecha[0].keys()
    if len(resultadoContextoVisitanteFecha) > 0:
        tabla.field_names = resultadoContextoVisitanteFecha[0].keys()
        
    for resultado in resultadoContextoLocalFecha:
        tabla.add_row(resultado.values())
    for resultado in resultadoContextoVisitanteFecha:
        tabla.add_row(resultado.values())
    for resultado in resultadoContextoRivalida:
        tabla.add_row(resultado.values())  

    print(tabla) 
    print(resultadoFinal) 
    """

except mysql.connector.Error as err:
    print("Error de MySQL: {err}")
finally:
    cursor.close()
    conexion.close()
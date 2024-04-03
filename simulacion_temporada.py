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
        SELECT local, visitante, local_posicion, visitante_posicion, resultado
        FROM resultados_ligas
        WHERE fecha = %s AND year = "2022-2023"
    """
    cursor.execute(query, (fecha,))
    resultados = cursor.fetchall()
    
    response = []
    for data in resultados:
        obj_response = {
            'local': data[0],
            'local_posicion': data[2],
            'visitante': data[1],
            'visitante_posicion': data[3],
            'resultado': data[4]
        } 
        
        response.append(obj_response)
    
    return response
    
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

def getResultado(equipoLocal, equipoVisitante, contexto_global, fecha, score_real):
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
    
    count_total = 0
    
    for row in contexto_global:
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
        
        count_total = count_total + 1
            
    mayor_count = max(countEmpate['count'], countLocal['count'], countVisitante['count'])
    pronostico = 'empate'
    if mayor_count == countLocal['count']:
        pronostico = countLocal['equipo']
    if mayor_count == countVisitante['count']:
        pronostico = countVisitante['equipo']
        
    total = len(contexto_global)
    porcentaje_calcul = mayor_count / total * 100
    porcentaje = round(porcentaje_calcul, 2)
    
    score_partes = score_real.split(' - ')
    score_local = score_partes[0]
    score_visitante = score_partes[1]
    score_local = int(score_local)
    score_visitante = int(score_visitante)
    
    resultado_real = 'empate'
    if score_local > score_visitante:
        resultado_real  = equipoLocal
    if score_visitante > score_local:
        resultado_real = equipoVisitante
    
    valido = 0
    if resultado_real == pronostico:
        valido = 1 
    
    response = {
        'local': equipoLocal,
        'visitante': equipoVisitante,
        'resultado_real': resultado_real,
        'pronostico': pronostico,
        'valido': valido,
        'count_local': countLocal['count'],
        'count_empate': countEmpate['count'],
        'count_visitante': countVisitante['count'],
        'count_total': count_total,
        'porcentaje': porcentaje,
        'fecha': fecha,
        'year': '2022-2023'
    }
    
    return response
    
def postResultadoSimulacion(result_data):   
    cursor.execute('''INSERT INTO simulacion_resultados (
        local, 
        visitante, 
        resultado_real, 
        pronostico, 
        valido, 
        count_local,
        count_empate,
        count_visitante,
        count_total,
        porcentaje, 
        fecha, 
        year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
        (result_data['local'], 
        result_data['visitante'], 
        result_data['resultado_real'], 
        result_data['pronostico'], 
        result_data['valido'], 
        result_data['count_local'], 
        result_data['count_empate'], 
        result_data['count_visitante'], 
        result_data['count_total'], 
        result_data['porcentaje'], 
        result_data['fecha'], 
        result_data['year']))
    
    
    conexion.commit()
    
try:
    for i in range(1, 39):      
        i_str = str(i)
        partidosDelDia = getPartidosDelDia(i_str)
    
        for partido in partidosDelDia:
            fecha = i
            equipoLocal = partido["local"]
            equipoLocalPosicion = int(partido["local_posicion"])
            equipoVisitante = partido["visitante"]
            equipoVisitantePosicion = int(partido["visitante_posicion"])
            resultado = partido["resultado"]
            
            contextoLocalFecha = contextoLocalFechaData(equipoLocal, fecha, equipoLocalPosicion, equipoVisitantePosicion)
            resultadoContextoLocalFecha = getContextoLocalFecha(contextoLocalFecha)
            
            contextoVisitanteFecha = contextoVisitanteFechaData(equipoVisitante, fecha, equipoLocalPosicion, equipoVisitantePosicion)
            resultadoContextoVisitanteFecha = getContextoVisitanteFecha(contextoVisitanteFecha) 

            resultadoContextoRivalida = getContextoRivalida(equipoLocal, equipoVisitante)
            
            contexto_global = resultadoContextoLocalFecha + resultadoContextoVisitanteFecha + resultadoContextoRivalida
            result_data = getResultado(equipoLocal, equipoVisitante, contexto_global, fecha, resultado)
            
            postResultadoSimulacion(result_data)
            
        print('success')

except mysql.connector.Error as err:
    print("Error de MySQL: {err}")
finally:
    cursor.close()
    conexion.close()
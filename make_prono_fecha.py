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
        WHERE fecha = %s AND year = "2023-2024"
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
    
def getContextoLocalFechaData(equipo, fecha, posicion_local, posicion_visitante):
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
    
def getContextoVisitanteFechaData(equipo, fecha, posicion_local, posicion_visitante):
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

def setContextoLocalFecha(resultadosContextoVisitante):   
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

def setContextoVisitanteFecha(resultadosContextoVisitante):   
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
    
    count_games = 0
    
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
        
        count_games = count_games + 1
            
    mayor_count = max(countEmpate['count'], countLocal['count'], countVisitante['count'])
        
    pronostico, pierde_prono = determinar_pronosticos(countLocal, countVisitante, equipoLocal, equipoVisitante, mayor_count)
    total = len(contexto_global)
    porcentaje_calcul = mayor_count / total * 100
    porcentaje = round(porcentaje_calcul, 2)
    
    resultado_real = ''
    
    valido = 0
    if resultado_real == pronostico:
        valido = 1 
        
    pierde_valido, pierde_porcentaje = calcular_pierde_valido_y_porcentaje(resultado_real, pierde_prono, mayor_count, countEmpate, total)
    
    response = {
        'year': '2023-2024',
        'fecha': fecha,
        'local': equipoLocal,
        'visitante': equipoVisitante,
        'resultado_real': resultado_real,
        'count_games': count_games,
        'pronostico': pronostico,
        'porcentaje': porcentaje,
        'valido': valido,
        'pierde_prono': pierde_prono,
        'pierde_porcentaje': pierde_porcentaje,
        'pierde_valido': pierde_valido,
    }
    
    return response

def calcular_pierde_valido_y_porcentaje(resultado_real, pierde_prono, mayor_count, countEmpate, total):
    pierde_valido = 0
    pierde_porcentaje = 0

    if resultado_real != pierde_prono:
        pierde_valido = 1 
        
    pierde_porcentaje_calcul = (mayor_count + countEmpate['count']) / total * 100
    pierde_porcentaje = round(pierde_porcentaje_calcul, 2)

    return pierde_valido, pierde_porcentaje
    
def setResultadoReal(score_real):
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
        
    return resultado_real

def determinar_pronosticos(countLocal, countVisitante, equipoLocal, equipoVisitante, mayor_count):
    pronostico = 'empate'
    pierde_prono = 'empate'
    
    if mayor_count == countLocal['count']:
        pronostico = countLocal['equipo']
        pierde_prono = equipoVisitante
    if mayor_count == countVisitante['count']:
        pronostico = countVisitante['equipo']
        pierde_prono = equipoLocal

    return pronostico, pierde_prono
    
def postPronoFecha(result_data):   
    cursor.execute('''INSERT INTO prono_fecha (
        year,
        fecha, 
        local, 
        visitante, 
        count_games,
        porcentaje, 
        pronostico, 
        pierde_prono,
        pierde_porcentaje
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
        result_data['year'],
        result_data['fecha'],
        result_data['local'], 
        result_data['visitante'], 
        result_data['count_games'], 
        result_data['porcentaje'], 
        result_data['pronostico'], 
        result_data['pierde_prono'], 
        result_data['pierde_porcentaje'], 
    ))
    
    conexion.commit()

def postPronoHistory(result_data):   
    cursor.execute('''INSERT INTO prono_history (
        year,
        fecha, 
        local, 
        visitante, 
        resultado_real, 
        count_games,
        porcentaje, 
        pronostico, 
        valido, 
        pierde_prono,
        pierde_porcentaje,
        pierde_valido
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
        result_data['year'],
        result_data['fecha'],
        result_data['local'], 
        result_data['visitante'], 
        result_data['resultado_real'], 
        result_data['count_games'], 
        result_data['porcentaje'], 
        result_data['pronostico'], 
        result_data['valido'], 
        result_data['pierde_prono'], 
        result_data['pierde_porcentaje'], 
        result_data['pierde_valido']
    ))
    
    conexion.commit()
    
try:
    i_str = str('32')
    partidosDelDia = getPartidosDelDia(i_str)
    
    print(partidosDelDia)

    for partido in partidosDelDia:
        fecha = 32
        equipoLocal = partido["local"]
        equipoLocalPosicion = int(partido["local_posicion"])
        equipoVisitante = partido["visitante"]
        equipoVisitantePosicion = int(partido["visitante_posicion"])
        resultado = partido["resultado"]
        
        contextoLocalFecha = getContextoLocalFechaData(equipoLocal, fecha, equipoLocalPosicion, equipoVisitantePosicion)
        resultadoContextoLocalFecha = setContextoLocalFecha(contextoLocalFecha)
        
        contextoVisitanteFecha = getContextoVisitanteFechaData(equipoVisitante, fecha, equipoLocalPosicion, equipoVisitantePosicion)
        resultadoContextoVisitanteFecha = setContextoVisitanteFecha(contextoVisitanteFecha) 

        resultadoContextoRivalida = getContextoRivalida(equipoLocal, equipoVisitante)
        
        contexto_global = resultadoContextoLocalFecha + resultadoContextoVisitanteFecha + resultadoContextoRivalida
        result_data = getResultado(equipoLocal, equipoVisitante, contexto_global, fecha, resultado)
        
        postPronoFecha(result_data)
        postPronoHistory(result_data)
        
    print('success')

except mysql.connector.Error as err:
    print("Error de MySQL: {err}")
finally:
    cursor.close()
    conexion.close()
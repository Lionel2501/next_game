test_query_local = """
        SELECT resultados.*, posiciones.posicion
        FROM resultados
        JOIN posiciones ON resultados.local = posiciones.equipo
        WHERE resultados.local = 'Cadiz'
            AND resultados.fecha = 14
            AND posiciones.fecha = 14
            AND posiciones.posicion = 16
    """
    
test_query_visitante = """
    SELECT resultados.*, posiciones.posicion
    FROM resultados
    JOIN posiciones ON resultados.visitante = posiciones.equipo
    WHERE resultados.visitante = 'Real Madrid'
        AND resultados.fecha = 14
        AND posiciones.fecha = 14
        AND resultados.year = posiciones.year
        AND posiciones.posicion = 2
"""

def resultadosContextoEquipoLocal(equipo, fecha, posicion):
    query = """
            SELECT resultados.*, posiciones.posicion
            FROM resultados
            JOIN posiciones ON resultados.local = posiciones.equipo
            WHERE resultados.local = %s
                AND resultados.fecha = %s
                AND posiciones.fecha = %s
                AND posiciones.posicion = posiciones.year
        """

    cursor.execute(query, (equipo, fecha, fecha, posicion))
    resultados = cursor.fetchall()
    
    return resultados
    
def resultadosContextoEquipoVisitante(equipo, fecha, posicion):
    query = """
        SELECT resultados.*, posiciones.posicion
        FROM resultados
        JOIN posiciones ON resultados.visitante = posiciones.equipo
        WHERE resultados.visitante = %s
            AND resultados.fecha = %s
            AND posiciones.fecha = %s
            AND resultados.year = posiciones.year
    """

    cursor.execute(query, (equipo, fecha, fecha, posicion))
    resultados = cursor.fetchall()
    
    return resultados
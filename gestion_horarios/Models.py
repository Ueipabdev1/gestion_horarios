from binascii import Error


def obtener_secciones(conn):
    """Obtiene todas las secciones"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.nombre, a.nombre 
            FROM secciones s
            JOIN areas a ON s.area_id = a.id
            ORDER BY s.area_id, s.id
        """)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener secciones: {e}")
        return []

def obtener_periodos(conn):
    """Obtiene todos los períodos"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, hora_inicio, hora_fin FROM periodos ORDER BY hora_inicio")
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener períodos: {e}")
        return []

def obtener_clases_sin_asignar(conn):
    """Obtiene clases sin asignación de recursos"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT hs.id, s.nombre, hs.dia, p.nombre, p.hora_inicio, p.hora_fin
            FROM horarios_seccion hs
            LEFT JOIN asignaciones a ON hs.id = a.horario_seccion_id
            JOIN secciones s ON hs.seccion_id = s.id
            JOIN periodos p ON hs.periodo_id = p.id
            WHERE a.id IS NULL
            ORDER BY hs.dia, p.hora_inicio
        """)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener clases: {e}")
        return []

def obtener_profesores(conn):
    """Obtiene todos los profesores"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.nombre, a.nombre, s.nombre
            FROM profesores p
            JOIN areas a ON p.area_id = a.id
            JOIN secciones s ON p.seccion_id = s.id
            ORDER BY p.area_id, p.id
        """)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener profesores: {e}")
        return []

def obtener_aulas(conn):
    """Obtiene todas las aulas"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM aulas ORDER BY id")
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener aulas: {e}")
        return []

def obtener_materias(conn):
    """Obtiene todas las materias"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id, m.nombre, a.nombre
            FROM materias m
            JOIN areas a ON m.area_id = a.id
            ORDER BY m.area_id, m.id
        """)
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener materias: {e}")
        return []

def obtener_horario_seccion(conn, seccion_id):
    """Obtiene el horario completo de una sección"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                s.id, s.nombre AS seccion, a.nombre AS area,
                hs.dia, p.id AS periodo_id, p.nombre AS periodo,
                p.hora_inicio, p.hora_fin,
                prof.nombre AS profesor, m.nombre AS materia, au.nombre AS aula
            FROM horarios_seccion hs
            JOIN secciones s ON hs.seccion_id = s.id
            JOIN areas a ON s.area_id = a.id
            JOIN periodos p ON hs.periodo_id = p.id
            JOIN asignaciones asig ON hs.id = asig.horario_seccion_id
            JOIN profesores prof ON asig.profesor_id = prof.id
            JOIN materias m ON asig.materia_id = m.id
            JOIN aulas au ON asig.aula_id = au.id
            WHERE s.id = %s
            ORDER BY FIELD(hs.dia, 'Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'), p.hora_inicio
        """, (seccion_id,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error al obtener horario: {e}")
        return []

def crear_clase_seccion(conn, seccion_id, dia, periodo_id):
    """Crea una nueva clase para una sección"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO horarios_seccion (seccion_id, dia, periodo_id)
            VALUES (%s, %s, %s)
        """, (seccion_id, dia, periodo_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al crear la clase: {e}")
        return False

def crear_asignacion(conn, horario_seccion_id, profesor_id, aula_id, materia_id):
    """Asigna recursos a una clase"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO asignaciones (horario_seccion_id, profesor_id, aula_id, materia_id)
            VALUES (%s, %s, %s, %s)
        """, (horario_seccion_id, profesor_id, aula_id, materia_id))
        conn.commit()
        return True
    except Error as e:
        print(f"Error al asignar recursos: {e}")
        return False
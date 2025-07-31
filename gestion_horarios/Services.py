from Models import crear_asignacion, crear_clase_seccion, obtener_aulas, obtener_clases_sin_asignar, obtener_horario_seccion, obtener_materias, obtener_periodos, obtener_profesores, obtener_secciones


def crear_nueva_clase(conn):
    """Guía al usuario para crear una nueva clase"""
    print("\n--- CREAR NUEVA CLASE PARA SECCIÓN ---")
    
    secciones = obtener_secciones(conn)
    if not secciones:
        print("No hay secciones disponibles")
        return
    
    print("\nSecciones disponibles:")
    for sec in secciones:
        print(f"{sec[0]}: {sec[1]} ({sec[2]})")
    
    seccion_id = int(input("\nID de la sección: "))
    
    if not any(sec[0] == seccion_id for sec in secciones):
        print("ID de sección inválido")
        return
    
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    print("\nDías disponibles:")
    for i, dia in enumerate(dias, 1):
        print(f"{i}. {dia}")
    
    dia_idx = int(input("\nSeleccione el día (1-6): ")) - 1
    if dia_idx < 0 or dia_idx >= len(dias):
        print("Selección inválida")
        return
    dia = dias[dia_idx]
    
    periodos = obtener_periodos(conn)
    if not periodos:
        print("No hay períodos disponibles")
        return
    
    print("\nPeríodos disponibles:")
    for p in periodos:
        print(f"{p[0]}: {p[1]} ({p[2]} - {p[3]})")
    
    periodo_id = int(input("\nID del período: "))
    
    if not any(p[0] == periodo_id for p in periodos):
        print("ID de período inválido")
        return
    
    if crear_clase_seccion(conn, seccion_id, dia, periodo_id):
        print("\n✅ Clase creada exitosamente!")
    else:
        print("\n❌ Error al crear la clase")

def asignar_recursos_clase(conn):
    """Guía al usuario para asignar recursos a una clase existente"""
    print("\n--- ASIGNAR RECURSOS A CLASE ---")
    
    clases = obtener_clases_sin_asignar(conn)
    if not clases:
        print("No hay clases disponibles para asignar")
        return
    
    print("\nClases disponibles para asignar:")
    for c in clases:
        print(f"{c[0]}: Sección {c[1]} - {c[2]} {c[3]} ({c[4]} - {c[5]})")
    
    clase_id = int(input("\nID de la clase a asignar: "))
    
    if not any(c[0] == clase_id for c in clases):
        print("ID de clase inválido")
        return
    
    profesores = obtener_profesores(conn)
    if not profesores:
        print("No hay profesores disponibles")
        return
    
    print("\nProfesores disponibles:")
    for p in profesores:
        print(f"{p[0]}: {p[1]} - {p[2]} ({p[3]})")
    
    profesor_id = int(input("\nID del profesor: "))
    
    if not any(p[0] == profesor_id for p in profesores):
        print("ID de profesor inválido")
        return
    
    aulas = obtener_aulas(conn)
    if not aulas:
        print("No hay aulas disponibles")
        return
    
    print("\nAulas disponibles:")
    for a in aulas:
        print(f"{a[0]}: {a[1]}")
    
    aula_id = int(input("\nID del aula: "))
    
    if not any(a[0] == aula_id for a in aulas):
        print("ID de aula inválido")
        return
    
    materias = obtener_materias(conn)
    if not materias:
        print("No hay materias disponibles")
        return
    
    print("\nMaterias disponibles:")
    for m in materias:
        print(f"{m[0]}: {m[1]} ({m[2]})")
    
    materia_id = int(input("\nID de la materia: "))
    
    if not any(m[0] == materia_id for m in materias):
        print("ID de materia inválido")
        return
    
    if crear_asignacion(conn, clase_id, profesor_id, aula_id, materia_id):
        print("\n✅ Recursos asignados exitosamente!")
    else:
        print("\n❌ Error al asignar recursos")

def generar_horario(conn):
    """Genera el horario completo para una sección"""
    print("\n--- HORARIO POR SECCIÓN ---")
    
    secciones = obtener_secciones(conn)
    if not secciones:
        print("No hay secciones disponibles")
        return
    
    print("\nSecciones disponibles:")
    for sec in secciones:
        print(f"{sec[0]}: {sec[1]} ({sec[2]})")
    
    seccion_id = int(input("\nID de la sección: "))
    
    horario = obtener_horario_seccion(conn, seccion_id)
    
    if not horario:
        print("\nNo hay clases asignadas para esta sección")
        return
    
    print(f"\nHORARIO - {horario[0][1]} ({horario[0][2]})")
    print("+-----------------+-----------------+-----------------+-----------------+")
    print("|      Horario    |      Lunes      |     Martes      |    Miércoles    |")
    print("+-----------------+-----------------+-----------------+-----------------+")
    
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    horario_por_dia = {dia: [] for dia in dias}
    
    for h in horario:
        horario_por_dia[h[3]].append((
            h[4], h[5], h[6], h[7],  # periodo_id, periodo, hora_inicio, hora_fin
            h[8], h[9], h[10]         # profesor, materia, aula
        ))
    
    periodos = obtener_periodos(conn)
    for p in periodos:
        if p[1].startswith("REC"):  # Saltar recesos
            continue
            
        fila = f"| {p[1]} ({p[2]}) |"
        
        for dia in dias[:3]:  # Solo mostramos tres días por simplicidad
            clases_dia = [c for c in horario_por_dia[dia] if c[0] == p[0]]
            
            if clases_dia:
                clase = clases_dia[0]
                texto = f"{clase[5]} ({clase[4]})"
                if len(texto) > 15:
                    texto = texto[:12] + "..."
                fila += f" {texto:<15} |"
            else:
                fila += " {:<15} |".format('')
        
        print(fila)
        print("+-----------------+-----------------+-----------------+-----------------+")
import csv
import os

# --- 1. CONFIGURACIÓN Y ESTRUCTURA DE DATOS ---

NOMBRE_ARCHIVO_CSV = "datos_paises.csv"
# Esta lista define los encabezados que vamos a usar en el diccionario y en el CSV. Es clave para el orden.
CAMPOS_PAIS = ['nombre', 'poblacion', 'superficie', 'continente']

# Dejamos estos datos acá por si el archivo CSV se borra o no existe. Es nuestro Plan B.
PAISES_RESPALDO = [
    {'nombre': 'Argentina', 'poblacion': 45376763, 'superficie': 2780400, 'continente': 'America'},
    {'nombre': 'Brasil', 'poblacion': 213993437, 'superficie': 8515767, 'continente': 'America'}, 
    {'nombre': 'Chile', 'poblacion': 19116201, 'superficie': 756102, 'continente': 'America'},
    {'nombre': 'Espana', 'poblacion': 47351567, 'superficie': 505990, 'continente': 'Europa'},
    {'nombre': 'Francia', 'poblacion': 67750000, 'superficie': 551695, 'continente': 'Europa'},
    {'nombre': 'Japon', 'poblacion': 125800000, 'superficie': 377975, 'continente': 'Asia'},
    {'nombre': 'Australia', 'poblacion': 25920000, 'superficie': 7692024, 'continente': 'Oceania'}
]

# --- 2. MÓDULO DE PERSISTENCIA (CSV) Y VALIDACIÓN DE ENTRADAS ---

def cargar_paises_desde_csv(nombre_archivo):
    """Cargamos todos los datos del CSV a nuestra lista de diccionarios al iniciar."""
    paises = []
    
    # Primero verificamos si el archivo existe. Si no existe, usamos los datos de Plan B.
    if not os.path.exists(nombre_archivo):
        print(f"Advertencia: El archivo '{nombre_archivo}' no se encontró. Usaremos el dataset de respaldo.")
        return PAISES_RESPALDO

    # Usamos encoding='utf-8' para la compatibilidad con acentos si los hubiera.
    with open(nombre_archivo, mode='r', newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv)
        for fila in lector_csv:
            # Usamos isdigit() para verificar antes de convertir.
            if fila.get('poblacion', '').isdigit() and fila.get('superficie', '').isdigit():
                pais = {
                    'nombre': fila.get('nombre', 'N/A'),
                    'poblacion': int(fila['poblacion']),
                    'superficie': int(fila['superficie']),
                    'continente': fila.get('continente', 'N/A')
                }
                paises.append(pais)
            else:
                print(f"Alerta: Saltando una fila porque los números del CSV están mal escritos.")
                
    if not paises:
        print("Advertencia: El CSV estaba vacío. Usando datos de respaldo.")
        return PAISES_RESPALDO
        
    return paises

def guardar_paises_en_csv(paises, nombre_archivo):
    """Esta función guarda todo, logrando la persistencia en el archivo."""
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=CAMPOS_PAIS)
        escritor_csv.writeheader() # Ponemos el encabezado
        escritor_csv.writerows(paises) # Escribimos toda la lista
    print(f"Guardado Listo. Los cambios están a salvo en '{nombre_archivo}'.")

def validar_entrada_numerica(mensaje):
    """Con esto verificamos que la entrada sea un número, sin usar excepciones."""
    while True:
        valor_str = input(mensaje).strip()
        
        if valor_str.isdigit():
            return int(valor_str)
        else:
            print("ERROR: Solo puedes ingresar números enteros. Intenta de nuevo.")

def limpiar_texto(texto):
    """Hace que el texto sea más fácil de buscar (todo en minúsculas y sin espacios extra)."""
    return " ".join(texto.split()).lower()

def buscar_pais_por_nombre(paises, nombre_a_buscar):
    """Busca el país exacto. Devuelve el índice si lo encuentra, si no, devuelve -1."""
    nombre_limpio_a_buscar = limpiar_texto(nombre_a_buscar)
    
    for i, pais in enumerate(paises):
        if limpiar_texto(pais["nombre"]) == nombre_limpio_a_buscar:
            return i
    return -1

# --- 3. FUNCIONES DEL MENÚ (LÓGICA DEL NEGOCIO) ---

def mostrar_menu():
    """Muestra las opciones del sistema."""
    print("\n\t--- SISTEMA DE GESTIÓN DE PAÍSES ---")
    print("1. Agregar país")
    print("2. Ver todos los países")
    print("3. Buscar país por nombre")
    print("4. Actualizar población/superficie")
    print("5. Filtrar por continente")
    print("6. Filtrar por rango (Población/Superficie)")
    print("7. Ordenar países")
    print("8. Estadísticas")
    print("9. Salir (Guarda el CSV)")
    print("------------------------------------------")

def agregar_pais(paises):
    """Agregamos un país nuevo, validando que no haya campos vacíos."""
    print("\n\t--- Agregar País ---")
    nombre = input("Nombre: ").strip()
    
    if not nombre:
        print("ERROR: El nombre no puede ir vacío.")
        return
    
    if buscar_pais_por_nombre(paises, nombre) != -1:
        print("ERROR: Ese país ya está en la lista. No podemos duplicarlo.")
        return

    poblacion = validar_entrada_numerica("Población (solo números): ")
    superficie = validar_entrada_numerica("Superficie en km² (solo números): ")

    continente = input("Continente: ").strip()
    if not continente:
        print("ERROR: Falta el continente.")
        return
    
    nuevo_pais = {
        'nombre': nombre,
        'poblacion': poblacion,
        'superficie': superficie,
        'continente': continente
    }
    
    paises.append(nuevo_pais)
    print(f"Registro exitoso: El país '{nombre}' ya está agregado a la lista.")
    guardar_paises_en_csv(paises, NOMBRE_ARCHIVO_CSV) # Guardamos por si las dudas

def mostrar_paises(paises):
    """Recorremos la lista y mostramos los datos de cada país."""
    print("\n\t--- Lista de Países ---")
    if not paises:
        print("No hay países para mostrar.")
        return
    
    for i, pais in enumerate(paises):
        print(f"{i + 1}. {pais['nombre']} - Población: {pais['poblacion']:,} hab. - Superficie: {pais['superficie']:,} km² - Continente: {pais['continente']}")

def buscar_pais_menu(paises):
    """Buscamos países por una parte del nombre (búsqueda parcial)."""
    print("\n\t--- Buscar País ---")
    nombre_busqueda = input("Escribe parte del nombre a buscar: ").strip().lower()
    
    if not nombre_busqueda:
        print("ERROR: No escribiste nada para buscar.")
        return
        
    encontrados = []
    for p in paises:
        if nombre_busqueda in p['nombre'].lower():
            encontrados.append(p)
    
    if encontrados:
        print(f"\nResultados de la búsqueda ('{nombre_busqueda}'):")
        for p in encontrados:
            print(f"-> {p['nombre']}, Población: {p['poblacion']:,}")
    else:
        print(f"No se encontraron países que coincidan con la búsqueda.")

def actualizar_pais(paises):
    """Actualizamos la población o superficie de un país existente."""
    print("\n\t--- Actualizar Población/Superficie ---")
    nombre_busqueda = input("Escribe el nombre del país a cambiar: ").strip()
    
    indice = buscar_pais_por_nombre(paises, nombre_busqueda)
    
    if indice == -1:
        print("ERROR: Ese país no está en la lista. Revisa la escritura.")
        return
    
    pais = paises[indice]
    print(f"Cambiando datos de: {pais['nombre']} (Pob. actual: {pais['poblacion']:,}, Sup. actual: {pais['superficie']:,})")
    print("Si no quieres cambiar algo, déjalo vacío.")
    
    nueva_poblacion_str = input("Nueva Población: ").strip()
    if nueva_poblacion_str != "":
        if nueva_poblacion_str.isdigit():
            paises[indice]['poblacion'] = int(nueva_poblacion_str)
        else:
            print("ERROR: La población debe ser un número. Cancelando el cambio.")
            return

    nueva_superficie_str = input("Nueva Superficie: ").strip()
    if nueva_superficie_str != "":
        if nueva_superficie_str.isdigit():
            paises[indice]['superficie'] = int(nueva_superficie_str)
        else:
            print("ERROR: La superficie debe ser un número. Cancelando el cambio.")
            return
    
    print(f"Actualización completada: Los datos de '{pais['nombre']}' ya están actualizados.")
    guardar_paises_en_csv(paises, NOMBRE_ARCHIVO_CSV) 

def filtrar_continente(paises):
    """Filtramos y mostramos solo los países que coincidan con el continente pedido."""
    print("\n\t--- Filtrar por Continente ---")
    continente_filtro = input("¿Qué continente quieres ver?: ").strip().lower()
    
    if not continente_filtro:
        print("ERROR: Tienes que escribir el nombre de un continente.")
        return

    resultados = []
    for p in paises:
        if continente_filtro in p['continente'].lower(): 
            resultados.append(p)
    
    if resultados:
        print(f"\nPaíses encontrados en '{continente_filtro}':")
        for p in resultados:
            print(f"-> {p['nombre']}, Población: {p['poblacion']:,}")
    else:
        print(f"No se encontraron países en ese continente. Prueba con otro filtro.")

def filtrar_por_rango(paises):
    """Filtramos según un rango numérico para población o superficie."""
    print("\n\t--- Filtrar por Rango ---")
    print("1. Por Población")
    print("2. Por Superficie")
    opcion = input("Elige 1 o 2 para filtrar: ").strip()
    
    if opcion not in ("1", "2"):
        print("ERROR: Tienes que elegir 1 o 2.")
        return

    min_val = validar_entrada_numerica("Valor mínimo: ")
    max_val = validar_entrada_numerica("Valor máximo: ")

    resultados = []
    
    if opcion == "1":
        for p in paises:
            if min_val <= p['poblacion'] <= max_val:
                resultados.append(p)
        criterio = "población"
        unidad = "hab."
    elif opcion == "2":
        for p in paises:
            if min_val <= p['superficie'] <= max_val:
                resultados.append(p)
        criterio = "superficie"
        unidad = "km²"

    if resultados:
        print(f"\nPaíses encontrados con {criterio} entre {min_val:,} y {max_val:,} {unidad}:")
        for p in resultados:
            valor = p['poblacion'] if opcion == "1" else p['superficie']
            print(f"-> {p['nombre']} ({valor:,} {unidad})")
    else:
        print("No hay países en ese rango.")

def ordenar_paises(paises):
    """Esta es la función para ordenar la lista. Usamos un método simple para mover los elementos."""
    if not paises:
        print("No hay países para ordenar.")
        return

    print("\n\t--- Ordenar Países ---")
    print("1. Nombre (A-Z)")
    print("2. Nombre (Z-A)")
    print("3. Poblacion (Menor a Mayor)")
    print("4. Poblacion (Mayor a Menor)")
    print("5. Superficie (Menor a Mayor)")
    print("6. Superficie (Mayor a Menor)")
    opcion = input("Elige cómo quieres ordenar (1-6): ").strip()
    
    criterio = ""
    es_inverso = False
    
    if opcion == "1" or opcion == "2":
        criterio = "nombre"
        es_inverso = opcion == "2"
    elif opcion == "3" or opcion == "4":
        criterio = "poblacion"
        es_inverso = opcion == "4"
    elif opcion == "5" or opcion == "6":
        criterio = "superficie"
        es_inverso = opcion == "6"
    else:
        print("ERROR: Opción no válida. Elige un número del 1 al 6.")
        return

    # Acá aplicamos la lógica de ordenamiento (con loops anidados).
    n = len(paises)
    for i in range(n):
        for j in range(0, n - i - 1):
            valor_a = paises[j][criterio]
            valor_b = paises[j + 1][criterio]
            
            if (not es_inverso and valor_a > valor_b) or (es_inverso and valor_a < valor_b):
                paises[j], paises[j + 1] = paises[j + 1], paises[j]

    print(f"Ordenamiento completado: La lista va por {criterio}.")
    mostrar_paises(paises)

def mostrar_estadisticas(paises):
    """Calculamos la población y superficie total, el promedio, el máximo, el mínimo y contamos por continente."""
    print("\n\t--- Estadísticas ---")
    if not paises:
        print("No hay países para calcular estadísticas.")
        return
    
    total_pob = 0
    total_sup = 0
    max_pob = paises[0]
    min_pob = paises[0]
    
    continentes_contador = {}
    
    for p in paises:
        total_pob += p['poblacion']
        total_sup += p['superficie']
        
        if p['poblacion'] > max_pob['poblacion']:
            max_pob = p
        if p['poblacion'] < min_pob['poblacion']:
            min_pob = p
            
        nombre_cont = p['continente']
        if nombre_cont in continentes_contador:
            continentes_contador[nombre_cont] += 1
        else:
            continentes_contador[nombre_cont] = 1

    promedio_pob = total_pob / len(paises)
    promedio_sup = total_sup / len(paises)
    
    print(f"Total de países registrados: {len(paises)}")
    print(f"País con más gente: **{max_pob['nombre']}** ({max_pob['poblacion']:,} hab.)")
    print(f"País con menos gente: **{min_pob['nombre']}** ({min_pob['poblacion']:,} hab.)")
    print(f"Promedio de población: {promedio_pob:,.0f} hab.")
    print(f"Promedio de superficie: {promedio_sup:,.0f} km²")
    
    print("\nPaíses por Continente:")
    for cont, cantidad in continentes_contador.items():
        print(f"- {cont}: {cantidad} países")

# --- 4. BLOQUE PRINCIPAL (MAIN) CON match/case ---

def main():
    """Esta es la función principal que corre el programa. Es el cerebro de todo."""
    
    paises = cargar_paises_desde_csv(NOMBRE_ARCHIVO_CSV) 
    
    # Mensaje de inicio
    print("\n*** Gestión de Países: Programa Iniciado ***")

    ejecutando = True
    while ejecutando:
        mostrar_menu()
        opcion = input("Seleccione opción: ").strip()
        
        match opcion:
            case "1":
                agregar_pais(paises)
            case "2":
                mostrar_paises(paises)
            case "3":
                buscar_pais_menu(paises)
            case "4":
                actualizar_pais(paises)
            case "5":
                filtrar_continente(paises)
            case "6":
                filtrar_por_rango(paises)
            case "7":
                ordenar_paises(paises)
            case "8":
                mostrar_estadisticas(paises)
            case "9":
                guardar_paises_en_csv(paises, NOMBRE_ARCHIVO_CSV)
                print("Cerrando sistema y guardando datos. ¡Adiós!")
                ejecutando = False
            case _:
                print("ERROR: Escribe un número válido del 1 al 9.")

if __name__ == "__main__":
    main()
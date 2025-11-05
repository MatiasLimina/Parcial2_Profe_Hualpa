from Manejo_archivo import *

def eliminar_item_por_nombre(nombre_item_a_eliminar: str) -> bool:
    """
    Busca un ítem por su nombre en toda la base de datos y lo elimina
    del archivo CSV correspondiente.

    Args:
        nombre_item_a_eliminar (str): El nombre exacto del ítem a eliminar.

    Returns:
        bool: True si el ítem fue encontrado y eliminado, False en caso contrario.
    """
    print(f"Iniciando búsqueda para eliminar '{nombre_item_a_eliminar}'...")
    
    # 1. Cargar todos los datos para encontrar el ítem y su ruta
    lista_completa = crear_lista_desde_csv(RUTA_BASE_DATOS)
    if not lista_completa:
        print("La base de datos está vacía. No hay nada que eliminar.")
        return False

    item_a_eliminar = None
    for item in lista_completa:
        # Usamos .strip() y .lower() para una comparación más robusta
        if item.get('nombre', '').strip().lower() == nombre_item_a_eliminar.strip().lower():
            item_a_eliminar = item
            break
    
    # 2. Si no se encontró el ítem, informar y salir
    if not item_a_eliminar:
        print(f"No se encontró ningún ítem con el nombre '{nombre_item_a_eliminar}'.")
        return False

    # 3. Reconstruir la ruta al archivo CSV específico del ítem
    try:
        ruta_archivo_especifico = os.path.join(
            RUTA_BASE_DATOS,
            item_a_eliminar['categoria'],
            item_a_eliminar['tipo'],
            item_a_eliminar['procesamiento'],
            "items.csv"
        )
        print(f"Ítem encontrado en: {ruta_archivo_especifico}")
    except KeyError:
        print("ERROR: El ítem encontrado no tiene la información de ruta completa (categoría/tipo/procesamiento).")
        return False

    # 4. Leer el archivo, filtrar los datos y reescribir
    filas_a_mantener = []
    encabezados = []
    try:
        with open(ruta_archivo_especifico, 'r', encoding='utf-8', newline='') as f:
            lector = csv.DictReader(f)
            encabezados = lector.fieldnames
            for fila in lector:
                # Si el nombre de la fila actual NO es el que queremos eliminar, la guardamos
                if fila.get('nombre', '').strip().lower() != nombre_item_a_eliminar.strip().lower():
                    filas_a_mantener.append(fila)
        
        # Ahora, sobrescribimos el archivo original con las filas filtradas
        with open(ruta_archivo_especifico, 'w', encoding='utf-8', newline='') as f:
            escritor = csv.DictWriter(f, fieldnames=encabezados)
            escritor.writeheader()
            escritor.writerows(filas_a_mantener)
        
        print(f"¡Éxito! Ítem '{nombre_item_a_eliminar}' eliminado.")
        return True

    except (IOError, FileNotFoundError) as e:
        print(f"ERROR CRÍTICO al intentar leer o reescribir el archivo: {e}")
        return False
    except Exception as e:
        print(f"ERROR INESPERADO durante la eliminación: {e}")
        return False


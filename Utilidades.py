from Manejo_archivo import *
import csv
import os
def eliminar_item_por_nombre(nombre_item_a_eliminar: str) -> bool:
    """
    Busca ítems por su nombre. Si hay múltiples coincidencias, muestra un menú
    interactivo para que el usuario elija cuál eliminar.
    """
    print(f"Iniciando búsqueda para eliminar '{nombre_item_a_eliminar}'...")
    
    lista_completa = crear_lista_desde_csv(RUTA_BASE_DATOS)
    if not lista_completa:
        print("La base de datos está vacía. No hay nada que eliminar.")
        return False
    
    # 1. Encontrar TODAS las coincidencias, no solo la primera.
    items_encontrados = [
        item for item in lista_completa 
        if item.get('nombre', '').strip().lower() == nombre_item_a_eliminar.strip().lower()
    ]
    
    if not items_encontrados:
        print(f"No se encontró ningún ítem con el nombre '{nombre_item_a_eliminar}'.")
        return False

    item_a_eliminar = None

    # 2. Lógica del menú interactivo si hay más de una coincidencia.
    if len(items_encontrados) > 1:
        print(f"Se encontraron múltiples ítems con el nombre '{nombre_item_a_eliminar}'. Por favor, elija cuál desea eliminar:")
        for i, item in enumerate(items_encontrados):
            # Mostramos la "ruta" completa para que el usuario pueda diferenciarlos.
            ruta_display = f"{item.get('categoria', '?')} > {item.get('tipo', '?')} > {item.get('procesamiento', '?')}"
            print(f"  {i + 1}) {item.get('nombre')} (Calorías: {item.get('calorias_100g', 'N/A')}) en [{ruta_display}]")
        
        while True:
            try:
                opcion_str = input(f"Ingrese el número del ítem a eliminar (1-{len(items_encontrados)}) o 0 para cancelar: ")
                opcion = int(opcion_str)
                if 0 < opcion <= len(items_encontrados):
                    item_a_eliminar = items_encontrados[opcion - 1]
                    break
                elif opcion == 0:
                    print("Eliminación cancelada por el usuario.")
                    return False
                else:
                    print("Opción inválida. Por favor, ingrese un número de la lista.")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número.")
    else:
        # Si solo hay un resultado, lo seleccionamos automáticamente.
        item_a_eliminar = items_encontrados[0]
        print("Se encontró 1 ítem:")
        ruta_display = f"{item_a_eliminar.get('categoria', '?')} > {item_a_eliminar.get('tipo', '?')} > {item_a_eliminar.get('procesamiento', '?')}"
        print(f"  - {item_a_eliminar.get('nombre')} (Calorías: {item_a_eliminar.get('calorias_100g', 'N/A')}) en [{ruta_display}]")
        confirmacion = input("¿Desea eliminarlo? (s/n): ").lower()
        if confirmacion != 's':
            print("Eliminación cancelada por el usuario.")
            return False

    # 3. Proceder con la eliminación del ítem seleccionado.
    try:
        ruta_archivo_especifico = os.path.join(
            RUTA_BASE_DATOS,
            item_a_eliminar['categoria'],
            item_a_eliminar['tipo'],
            item_a_eliminar['procesamiento'],
            "items.csv"
        )
        print(f"Procediendo a eliminar de: {ruta_archivo_especifico}")
    except KeyError:
        print("ERROR: El ítem encontrado no tiene la información de ruta completa (categoría/tipo/procesamiento).")
        return False

    filas_a_mantener = []
    encabezados = []
    try:
        with open(ruta_archivo_especifico, 'r', encoding='utf-8', newline='') as f: # Leemos el CSV específico
            lector = csv.DictReader(f)
            encabezados = lector.fieldnames
            for fila in lector:
                # Comparamos no solo el nombre, sino también las calorías para ser más precisos
                # en caso de que haya ítems con el mismo nombre en el MISMO archivo.
                if not (fila.get('nombre', '').strip().lower() == item_a_eliminar['nombre'].strip().lower() and 
                        fila.get('calorias_100g') == item_a_eliminar['calorias_100g']):
                    filas_a_mantener.append(fila)
        
        # Llamamos a la función de sobrescritura que está en Manejo_archivo.py
        if sobrescribir_csv(ruta_archivo_especifico, encabezados, filas_a_mantener):
            print(f"¡Éxito! Ítem '{nombre_item_a_eliminar}' eliminado.")
            return True
        else:
            print(f"Fallo al sobrescribir el archivo para eliminar el ítem.")
            return False
    
    except (IOError, FileNotFoundError) as e:
        print(f"ERROR CRÍTICO al intentar leer el archivo para eliminar: {e}")
        return False
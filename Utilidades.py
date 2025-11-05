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

def modificar_item_por_nombre(nombre_item_a_modificar: str) -> bool:
    """
    Busca ítems por su nombre. Si hay múltiples coincidencias, muestra un menú
    interactivo para que el usuario elija cuál modificar. Luego, pide los nuevos
    valores y actualiza el archivo CSV correspondiente.
    """
    print(f"Iniciando búsqueda para modificar '{nombre_item_a_modificar}'...")
    
    lista_completa = crear_lista_desde_csv(RUTA_BASE_DATOS)
    if not lista_completa:
        print("La base de datos está vacía. No hay nada que modificar.")
        return False
    
    items_encontrados = [
        item for item in lista_completa 
        if item.get('nombre', '').strip().lower() == nombre_item_a_modificar.strip().lower()
    ]
    
    if not items_encontrados:
        print(f"No se encontró ningún ítem con el nombre '{nombre_item_a_modificar}'.")
        return False

    item_a_modificar = None

    if len(items_encontrados) > 1:
        print(f"Se encontraron múltiples ítems con el nombre '{nombre_item_a_modificar}'. Por favor, elija cuál desea modificar:")
        for i, item in enumerate(items_encontrados):
            ruta_display = f"{item.get('categoria', '?')} > {item.get('tipo', '?')} > {item.get('procesamiento', '?')}"
            print(f"  {i + 1}) {item.get('nombre')} (Calorías: {item.get('calorias_100g', 'N/A')}) en [{ruta_display}]")
        
        while True:
            try:
                opcion_str = input(f"Ingrese el número del ítem a modificar (1-{len(items_encontrados)}) o 0 para cancelar: ")
                opcion = int(opcion_str)
                if 0 < opcion <= len(items_encontrados):
                    item_a_modificar = items_encontrados[opcion - 1]
                    break
                elif opcion == 0:
                    print("Modificación cancelada por el usuario.")
                    return False
                else:
                    print("Opción inválida. Por favor, ingrese un número de la lista.")
            except ValueError:
                print("Entrada inválida. Por favor, ingrese un número.")
    else:
        item_a_modificar = items_encontrados[0]
        print("Se encontró 1 ítem:")
        ruta_display = f"{item_a_modificar.get('categoria', '?')} > {item_a_modificar.get('tipo', '?')} > {item_a_modificar.get('procesamiento', '?')}"
        print(f"  - {item_a_modificar.get('nombre')} (Calorías: {item_a_modificar.get('calorias_100g', 'N/A')}) en [{ruta_display}]")
        confirmacion = input("¿Desea modificarlo? (s/n): ").lower()
        if confirmacion != 's':
            print("Modificación cancelada por el usuario.")
            return False

    # --- Inicio del bloque de modificación ---
    print("\n--- Editando Ítem ---")
    print("Deje el campo en blanco y presione Enter para conservar el valor actual.")

    # Pedir nuevos valores
    nuevo_nombre = input(f"Nuevo nombre (actual: {item_a_modificar['nombre']}): ").strip()
    if not nuevo_nombre:
        nuevo_nombre = item_a_modificar['nombre']

    while True:
        nuevas_calorias_str = input(f"Nuevas calorías (actual: {item_a_modificar['calorias_100g']}): ").strip()
        if not nuevas_calorias_str:
            # Si se deja en blanco, mantenemos el valor original, asegurándonos de que sea float.
            try:
                nuevas_calorias = float(item_a_modificar['calorias_100g'])
            except (ValueError, TypeError):
                print(f"ADVERTENCIA: No se pudo convertir el valor de calorías original '{item_a_modificar['calorias_100g']}' a número. Se mantendrá como está.")
                nuevas_calorias = item_a_modificar['calorias_100g']
            break
        try:
            nuevas_calorias = float(nuevas_calorias_str)
            if nuevas_calorias <= 0:
                print("Error: Las calorías deben ser un número positivo mayor a cero.")
            else:
                # El valor es un float válido y positivo.
                break
        except ValueError:
            print("Error: Debe ingresar un valor numérico válido.")

    item_modificado = item_a_modificar.copy()
    item_modificado['nombre'] = nuevo_nombre
    item_modificado['calorias_100g'] = nuevas_calorias

    try:
        ruta_archivo_especifico = os.path.join(
            RUTA_BASE_DATOS,
            item_a_modificar['categoria'],
            item_a_modificar['tipo'],
            item_a_modificar['procesamiento'],
            "items.csv"
        )
    except KeyError:
        print("ERROR: El ítem encontrado no tiene la información de ruta completa (categoría/tipo/procesamiento).")
        return False

    filas_actualizadas = []
    encabezados = []
    try:
        with open(ruta_archivo_especifico, 'r', encoding='utf-8', newline='') as f:
            lector = csv.DictReader(f)
            encabezados = lector.fieldnames
            for fila in lector:
                # CORRECCIÓN: Comparamos los valores de calorías como números (float) para evitar errores de tipo.
                # El valor de 'calorias_100g' en 'fila' viene como string del CSV, y en 'item_a_modificar' también.
                try:
                    calorias_fila_float = float(fila.get('calorias_100g', 0))
                    calorias_original_float = float(item_a_modificar.get('calorias_100g', -1))
                except (ValueError, TypeError):
                    calorias_fila_float, calorias_original_float = -2, -3 # Valores que no coincidirán

                if (fila.get('nombre', '').strip().lower() == item_a_modificar['nombre'].strip().lower() and calorias_fila_float == calorias_original_float):
                    # CORRECCIÓN: Se reemplaza la fila vieja por la nueva, pero antes se eliminan los campos extra
                    # que no existen en el archivo CSV de destino ('categoria', 'tipo', 'procesamiento').
                    item_limpio = item_modificado.copy()
                    del item_limpio['categoria']
                    del item_limpio['tipo']
                    del item_limpio['procesamiento']
                    filas_actualizadas.append(item_limpio) # Se añade la versión "limpia" en lugar de la original.
                else:
                    filas_actualizadas.append(fila) # Mantenemos la fila como estaba
        
        if sobrescribir_csv(ruta_archivo_especifico, encabezados, filas_actualizadas):
            print(f"¡Éxito! Ítem '{item_a_modificar['nombre']}' modificado a '{nuevo_nombre}'.")
            return True
        else:
            print(f"Fallo al sobrescribir el archivo para modificar el ítem.")
            return False
    except (IOError, FileNotFoundError) as e:
        print(f"ERROR CRÍTICO al intentar leer/escribir el archivo para modificar: {e}")
        return False

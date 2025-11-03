import os
import csv

RUTA_BASE_DATOS = "base_de_datos_alimentos"

def alta_nuevo_item(categoria, tipo, procesamiento, nuevo_item):
    """
    Da de alta un nuevo ítem en la base de datos.

    Crea la estructura de directorios necesaria y escribe (o añade)
    el ítem en el archivo 'items.csv' correspondiente.

    Args:
        categoria (str): La categoría del alimento (ej: "Frutas").
        tipo (str): El tipo de alimento (ej: "Cítricos").
        procesamiento (str): El tipo de procesamiento (ej: "Fresco").
        nuevo_item (dict): Un diccionario con los datos del alimento.
    """
    print(f"Iniciando alta para: {nuevo_item.get('nombre', 'N/A')}...")
    try:
        # 1. Construir la ruta del directorio de forma segura.
        # os.path.join se asegura de que la ruta sea correcta en cualquier
        # sistema operativo (Windows, Linux, macOS).
        ruta_directorio = os.path.join(RUTA_BASE_DATOS, categoria, tipo, procesamiento)

        # 2. Crear la estructura de carpetas.
        # os.makedirs crea todos los directorios intermedios que no existan.
        # El parámetro `exist_ok=True` es crucial: evita que el programa
        # lance un error si las carpetas ya existen.
        os.makedirs(ruta_directorio, exist_ok=True)
        print(f"Directorio asegurado: {ruta_directorio}")

        # 3. Definir la ruta completa del archivo CSV.
        ruta_archivo_csv = os.path.join(ruta_directorio, "items.csv")

        # 4. Escribir en el archivo CSV.
        # Verificamos si el archivo es nuevo para saber si debemos escribir los encabezados.
        escribir_encabezado = not os.path.exists(ruta_archivo_csv)

        # Usamos 'with open' para que el archivo se cierre automáticamente.
        # El modo 'a' (append) nos permite agregar nuevas filas sin borrar las anteriores.
        with open(ruta_archivo_csv, 'a', encoding='utf-8', newline='') as f:
            # Los nombres de los campos se toman de las claves del diccionario.
            campos = nuevo_item.keys()
            escritor = csv.DictWriter(f, fieldnames=campos)

            if escribir_encabezado:
                escritor.writeheader() # Escribe la primera línea con los nombres de las columnas.
            
            escritor.writerow(nuevo_item) # Escribe los datos del nuevo ítem.
        
        print(f"¡Éxito! Ítem agregado en {ruta_archivo_csv}")

    # 3. Manejo de Excepciones
    except (OSError, PermissionError) as e:
        print(f"ERROR CRÍTICO: No se pudo escribir en el disco. Verifique los permisos. Detalles: {e}")
    except Exception as e:
        print(f"ERROR INESPERADO durante el alta: {e}")

def leer_alimentos_recursivo(ruta_actual, lista_global_alimentos):
    """
    Recorre recursivamente el sistema de archivos desde una ruta dada,
    lee todos los archivos 'items.csv' y acumula los datos en una lista.

    Args:
        ruta_actual (str): El directorio a procesar en la llamada actual.
        lista_global_alimentos (list): La lista que acumula los diccionarios.

    Returns:
        list: La lista con todos los alimentos encontrados.
    """
    # Usamos un try-except por si la ruta inicial no existe.
    try:
        # 1. Listamos todo lo que hay en la carpeta actual.
        elementos = os.listdir(ruta_actual)
    except FileNotFoundError:
        print(f"ADVERTENCIA: El directorio base '{ruta_actual}' no fue encontrado.")
        return [] # Si no existe, devolvemos una lista vacía.

    # 2. Recorremos cada elemento encontrado.
    for elemento in elementos:
        ruta_completa = os.path.join(ruta_actual, elemento)

        # 3. Decidimos qué hacer: ¿es un archivo o una carpeta?

        # --- PASO RECURSIVO ---
        # Si es un directorio, nos volvemos a llamar a nosotros mismos
        # para que la función "baje" a ese nuevo nivel.
        if os.path.isdir(ruta_completa):
            leer_alimentos_recursivo(ruta_completa, lista_global_alimentos)

        # --- CASO BASE ---
        # Si es un archivo y se llama "items.csv", lo leemos.
        # Esta es la condición de corte de la recursividad.
        elif os.path.isfile(ruta_completa) and elemento.lower() == "items.csv":
            try:
                with open(ruta_completa, 'r', encoding='utf-8', newline='') as f:
                    lector = csv.DictReader(f)
                    for fila in lector:
                        # ¡Mejora! Añadimos la jerarquía al diccionario para tener el contexto.
                        partes_ruta = ruta_actual.split(os.sep)
                        if len(partes_ruta) >= 4: # Asumiendo base/cat/tipo/proc
                            fila['procesamiento'] = partes_ruta[-1]
                            fila['tipo'] = partes_ruta[-2]
                            fila['categoria'] = partes_ruta[-3]
                        lista_global_alimentos.append(fila)
            except Exception as e:
                print(f"ADVERTENCIA: Error al leer el archivo {ruta_completa}: {e}")
    
    return lista_global_alimentos
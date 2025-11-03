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
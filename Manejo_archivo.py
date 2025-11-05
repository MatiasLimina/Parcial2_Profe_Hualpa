import os
import csv

ruta_script = os.path.dirname(os.path.abspath(__file__))
RUTA_BASE_DATOS = os.path.join(ruta_script, "base_de_datos_alimentos")


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

def _encontrar_rutas_csv_recursivo(ruta_actual, lista_rutas,nombre_archivo):
    """
    (Función auxiliar) Recorre recursivamente los directorios para encontrar
    todos los archivos 'items.csv' y acumula sus rutas en una lista.

    Args:
        ruta_actual (str): Directorio desde donde empezar la búsqueda.
        lista_rutas (list): Lista donde se acumulan las rutas encontradas.
    """
    try:
        elementos = os.listdir(ruta_actual)
    except FileNotFoundError:
        # No se imprime advertencia aquí para no saturar la consola si la base no existe.
        # La función principal se encargará de notificar si no se encuentra nada.
        return

    for elemento in elementos:
        ruta_completa = os.path.join(ruta_actual, elemento)
        if os.path.isdir(ruta_completa):
            _encontrar_rutas_csv_recursivo(ruta_completa, lista_rutas, nombre_archivo)
        elif os.path.isfile(ruta_completa) and elemento.lower() == nombre_archivo.lower():
            lista_rutas.append(ruta_completa)

def crear_lista_desde_csv(ruta_base, nombre_archivo="items.csv"):
    """
    Crea una lista consolidada de alimentos a partir de todos los
    archivos 'items.csv' encontrados en la estructura de directorios.

    Args:
        ruta_base (str): El directorio raíz donde buscar (ej: "base_de_datos_alimentos").


    Returns:
        list: Una lista de diccionarios, cada uno representando un alimento.
            Retorna una lista vacía si no se encuentran datos o el directorio no existe.
    """
    rutas_csv = []
    _encontrar_rutas_csv_recursivo(ruta_base, rutas_csv, nombre_archivo)

    if not rutas_csv:
        print(f"ADVERTENCIA: No se encontraron archivos '{nombre_archivo}' en '{ruta_base}'.")
        return []

    lista_global_alimentos = []
    for ruta_archivo in rutas_csv:
        try:
            with open(ruta_archivo, 'r', encoding='utf-8', newline='') as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    # Añadimos la jerarquía al diccionario para tener el contexto completo.
                    partes_ruta = os.path.dirname(ruta_archivo).split(os.sep)
                    if len(partes_ruta) >= 4: # Asumiendo base/cat/tipo/proc
                        fila['procesamiento'] = partes_ruta[-1]
                        fila['tipo'] = partes_ruta[-2]
                        fila['categoria'] = partes_ruta[-3]
                    lista_global_alimentos.append(fila)
        except Exception as e:
            print(f"ADVERTENCIA: No se pudo leer el archivo {ruta_archivo}. Detalles: {e}")

    return lista_global_alimentos

def sobrescribir_csv(ruta_archivo: str, encabezados: list, filas: list) -> bool:
    """
    (Función auxiliar) Sobrescribe de forma segura un archivo CSV con una nueva lista de filas.

    Args:
        ruta_archivo (str): La ruta completa al archivo CSV que se va a sobrescribir.
        encabezados (list): Una lista de strings con los nombres de las columnas.
        filas (list): Una lista de diccionarios, donde cada diccionario es una fila.

    Returns:
        bool: True si la escritura fue exitosa, False en caso de error.
    """
    try:
        with open(ruta_archivo, 'w', encoding='utf-8', newline='') as f:
            escritor = csv.DictWriter(f, fieldnames=encabezados)
            escritor.writeheader()
            escritor.writerows(filas)
        return True
    except (IOError, FileNotFoundError) as e:
        print(f"ERROR CRÍTICO al intentar reescribir el archivo: {e}")
        return False
    except Exception as e:
        print(f"ERROR INESPERADO durante la reescritura del archivo: {e}")
        return False


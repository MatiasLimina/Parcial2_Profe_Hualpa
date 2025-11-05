from Manejo_archivo import *
import unicodedata
import os, csv
from Utilidades import mostrar_tabla_alimentos, imprimir_menu

def normalizar_texto_para_ruta(texto: str) -> str:
    """
    Limpia y normaliza un texto para ser usado en nombres de carpetas.
    Usa la librería estándar 'unicodedata' para quitar acentos.
    """
    if not isinstance(texto, str):
        return ""
    
    # 1. Quitar espacios y convertir a minúsculas
    texto = texto.strip().lower()      
    
    # 2. Quitar acentos (ej: "Cítricos" -> "citricos")
    # Normaliza a 'NFD' (descomposición canónica) 
    # Esto separa el caracter de su acento (ej: "é" -> "e" + "´")
    texto_normalizado = unicodedata.normalize('NFD', texto)
    
    # Codifica a 'ascii' ignorando los caracteres que no lo son (los acentos)
    # y luego decodifica de vuelta a 'utf-8' para tener un string normal.
    texto_sin_acentos = texto_normalizado.encode('ascii', 'ignore').decode('utf-8')
    
    return texto_sin_acentos

def opcion_1_alta():
    print("\n====================================")
    print("       Alta de Nuevo Alimento       ")
    print("====================================")

    num_items_a_agregar = 0
    while True:
        try:
            num_items_str = input("¿Cuántos ítems desea agregar? (Ingrese 0 para cancelar): ")
            num_items_a_agregar = int(num_items_str)
            if num_items_a_agregar < 0:
                print("Error: Debe ingresar un número positivo.")
                continue
            break # Salir del bucle si el número es válido
        except ValueError:
            print("Error: Entrada inválida. Por favor, ingrese un número entero.")

    if num_items_a_agregar == 0:
        print("Alta de ítems cancelada.")
        return

    # Leemos la lista una sola vez al principio.
    lista_completa_en_memoria = crear_lista_desde_csv(RUTA_BASE_DATOS)

    for i in range(num_items_a_agregar):
        print(f"\n--- Agregando Ítem {i + 1} de {num_items_a_agregar} ---")
        
        # 1. Obtener y mostrar categorías existentes para guiar al usuario.
        # Ahora usamos la lista en memoria, que es más rápida.
        if lista_completa_en_memoria:
            # Usamos un set para obtener categorías únicas y luego lo ordenamos.
            categorias_existentes = sorted(list(set(item.get('categoria') for item in lista_completa_en_memoria if 'categoria' in item)))
            if categorias_existentes:
                print("\nCategorías existentes:", ", ".join(categorias_existentes))
        
        # Pedir jerarquía
        # 1. Pedir Categoría y mostrar Tipos existentes
        categoria_input = input("Ingrese Categoría (ej: Frutas): ")
        categoria = normalizar_texto_para_ruta(categoria_input)

        if lista_completa_en_memoria:
            items_en_categoria = [item for item in lista_completa_en_memoria if item.get('categoria') == categoria]
            if items_en_categoria:
                tipos_existentes = sorted(list(set(item.get('tipo') for item in items_en_categoria if 'tipo' in item)))
                if tipos_existentes:
                    print(f" -> Tipos existentes en '{categoria}':", ", ".join(tipos_existentes))

        # 2. Pedir Tipo y mostrar Procesamientos existentes
        tipo_input = input("Ingrese Tipo (ej: Cítricos): ")
        tipo = normalizar_texto_para_ruta(tipo_input)

        if lista_completa_en_memoria:
            items_en_tipo = [item for item in lista_completa_en_memoria if item.get('categoria') == categoria and item.get('tipo') == tipo]
            if items_en_tipo:
                procesamientos_existentes = sorted(list(set(item.get('procesamiento') for item in items_en_tipo if 'procesamiento' in item)))
                if procesamientos_existentes:
                    print(f" -> Procesamientos existentes en '{tipo}':", ", ".join(procesamientos_existentes))

        procesamiento_input = input("Ingrese Procesamiento (ej: Fresco): ")
        procesamiento = normalizar_texto_para_ruta(procesamiento_input)
        
        # (Opcional) Informar al usuario la normalización
        print(f"Guardando en -> Categoría: {categoria}, Tipo: {tipo}, Procesamiento: {procesamiento}")
        
        # --- VALIDACIÓN DE EXISTENCIA ---
        # Bucle para pedir el nombre y validar que no exista.
        while True:
            nombre_input = input("Ingrese Nombre del alimento: ")
            nombre = nombre_input.strip()
            if not nombre:
                print("Error: El nombre no puede estar vacío.")
                continue

            ruta_archivo_especifico = os.path.join(RUTA_BASE_DATOS, categoria, tipo, procesamiento, "items.csv")
            
            item_existe = False
            if os.path.exists(ruta_archivo_especifico):
                with open(ruta_archivo_especifico, 'r', encoding='utf-8', newline='') as f:
                    lector = csv.DictReader(f)
                    for fila in lector:
                        # Comparamos usando la misma normalización para ser insensibles a mayúsculas/acentos
                        if normalizar_texto_para_ruta(fila.get('nombre', '')) == normalizar_texto_para_ruta(nombre):
                            item_existe = True
                            break
            
            if item_existe:
                print(f"Error: El ítem '{nombre}' ya existe en esta jerarquía. Por favor, ingrese un nombre diferente.")
            else:
                break # El nombre es válido y no existe, salimos del bucle.

        # Pedir atributos
        
        # Validación estricta 
        calorias = 0
        while True:
            try:
                calorias_str = input("Ingrese Calorías (por 100g): ")
                if not calorias_str:
                    print("Error: El valor no puede estar vacío.") 
                    continue
                calorias = float(calorias_str)
                if calorias <= 0:
                    print("Error: Las calorías deben ser un número positivo mayor a cero.") 
                else:
                    break
            except ValueError:
                print("Error: Debe ingresar un valor numérico.") 

        # Crear el diccionario
        nuevo_item = {
            'nombre': nombre,
            'calorias_100g': calorias,
            # ... otros campos que definas ...
        }
        
        # Llamar a tu función de Fase 2
        alta_nuevo_item(categoria, tipo, procesamiento, nuevo_item)

def opcion_2_mostrar_y_filtrar():
    """
    Menú para mostrar y filtrar la lista de alimentos.
    """
    lista_completa = crear_lista_desde_csv(RUTA_BASE_DATOS)
    if not lista_completa:
        print("La base de datos está vacía. No hay nada que mostrar.")
        return

    while True:
        opciones_menu = [
            "Mostrar todos los alimentos",
            "Filtrar por jerarquía (Categoría -> Tipo)",
            "Filtrar por rango de calorías",
            "Elegir Top por calorías"
        ]
        imprimir_menu("Menú de Visualización y Filtrado", opciones_menu, "Volver al menú principal")
        opc = input("Elija una opción: ").strip()

        match opc:
            case "1": # Mostrar todo
                print("\n--- Lista Completa de Alimentos ---")
                mostrar_tabla_alimentos(lista_completa)

            case "2": # Filtrado Jerárquico
                # 1. Elegir Categoría
                categorias = sorted(list(set(item['categoria'] for item in lista_completa if 'categoria' in item)))
                print("\n--- Filtrar por Jerarquía: Elija una Categoría ---")
                for i, cat in enumerate(categorias):
                    print(f"{i + 1}) {cat}")
                print("-------------------------------------------------")
                print("0) Cancelar")
                print("-------------------------------------------------")
                
                try:
                    opc_cat_str = input(f"Elija una categoría (1-{len(categorias)}): ")
                    if opc_cat_str == '0': continue
                    opc_cat = int(opc_cat_str) - 1

                    if 0 <= opc_cat < len(categorias):
                        categoria_elegida = categorias[opc_cat]
                        # 2. Filtrar por esa categoría y mostrar los Tipos disponibles
                        items_en_categoria = [item for item in lista_completa if item.get('categoria') == categoria_elegida]
                        tipos = sorted(list(set(item['tipo'] for item in items_en_categoria if 'tipo' in item)))
                        
                        print(f"\n--- Tipos en '{categoria_elegida}': Elija un Tipo ---")
                        for i, tipo in enumerate(tipos):
                            print(f"{i + 1}) {tipo}")
                        print("-------------------------------------------------")
                        print("0) Ver todos los alimentos de esta categoría")
                        print("-------------------------------------------------")
                        
                        opc_tipo_str = input(f"Elija un tipo (1-{len(tipos)}): ")
                        opc_tipo = int(opc_tipo_str) - 1

                        if opc_tipo == -1: # Opción 0
                            mostrar_tabla_alimentos(items_en_categoria)
                        elif 0 <= opc_tipo < len(tipos):
                            tipo_elegido = tipos[opc_tipo]
                            items_en_tipo = [item for item in items_en_categoria if item.get('tipo') == tipo_elegido]
                            mostrar_tabla_alimentos(items_en_tipo)
                        else:
                            print("Opción de tipo inválida.")
                    else:
                        print("Opción de categoría inválida.")
                except (ValueError, IndexError):
                    print("Entrada no válida. Intente de nuevo.")

            case "3": # Filtrar por Rango de Calorías
                print("\n====================================")
                print("    Filtrar por Rango de Calorías   ")
                print("====================================")
                try:
                    min_cal = float(input("Ingrese calorías mínimas: "))
                    max_cal = float(input("Ingrese calorías máximas: "))
                    if min_cal > max_cal:
                        print("Error: El mínimo no puede ser mayor que el máximo.")
                        continue
                    
                    # Filtra solo los que tienen calorías y están en el rango
                    filtrados = []
                    for item in lista_completa:
                        try:
                            calorias = float(item.get('calorias_100g', -1))
                            if min_cal <= calorias <= max_cal:
                                filtrados.append(item)
                        except (ValueError, TypeError):
                            continue # Ignora items con calorías no numéricas
                    
                    mostrar_tabla_alimentos(filtrados)
                except ValueError:
                    print("Error: Ingrese valores numéricos para las calorías.")

            case "4": # Top por Calorías
                print("\n====================================")
                print("         Top por Calorías           ")
                print("====================================")
                try:
                    n_str = input("¿Cuántos alimentos del top desea ver? (ej: 5): ")
                    n = int(n_str)
                    if n <= 0:
                        print("Debe ingresar un número positivo.")
                        continue
                    
                    # Aquí está la solución a tu preocupación:
                    # 1. Creamos una lista solo con items que tienen calorías válidas.
                    items_con_calorias = []
                    for item in lista_completa:
                        try:
                            # Intentamos convertir la caloría a float y la guardamos
                            item_copy = item.copy()
                            item_copy['calorias_100g_float'] = float(item.get('calorias_100g'))
                            items_con_calorias.append(item_copy)
                        except (ValueError, TypeError, AttributeError):
                            continue # Ignoramos los que no tienen calorias o no son números

                    # 2. Ordenamos esa lista limpia de mayor a menor
                    items_ordenados = sorted(items_con_calorias, key=lambda x: x['calorias_100g_float'], reverse=True)

                    # 3. Mostramos los primeros 'n' resultados
                    mostrar_tabla_alimentos(items_ordenados[:n])

                except ValueError:
                    print("Error: Ingrese un número entero válido.")

            case "0": # Volver
                break
            case _:
                print("Opción no válida.")

def opcion_5_estadisticas():
    """
    Muestra un menú con diferentes estadísticas sobre la base de datos de alimentos.
    """
    lista_completa = crear_lista_desde_csv(RUTA_BASE_DATOS)
    if not lista_completa:
        print("La base de datos está vacía. No se pueden calcular estadísticas.")
        return

    # --- Preparación de Datos ---
    # Crear una lista solo con ítems que tienen calorías válidas para los cálculos.
    # Esto hace que todas las operaciones sean robustas y seguras.
    items_con_calorias = []
    for item in lista_completa:
        try:
            item_copy = item.copy()
            item_copy['calorias_float'] = float(item.get('calorias_100g'))
            items_con_calorias.append(item_copy)
        except (ValueError, TypeError, AttributeError):
            continue # Ignora ítems sin calorías o con valores no numéricos.

    while True:
        opciones_menu = [
            "Resumen General de la Base de Datos",
            "Cantidad de Alimentos por Categoría",
            "Análisis Detallado por Categoría",
            "Ranking de Calorías Promedio por Categoría",
            "Top 3 Más/Menos Calóricos por Categoría"
        ]
        imprimir_menu("Menú de Estadísticas", opciones_menu, "Volver al menú principal")
        opc = input("Elija una opción: ").strip()

        match opc:
            case "1": # Resumen General
                print("\n--- Resumen General ---")
                print(f"- Cantidad total de alimentos: {len(lista_completa)}")
                if items_con_calorias:
                    suma_calorias = sum(item['calorias_float'] for item in items_con_calorias)
                    promedio_global = suma_calorias / len(items_con_calorias)
                    max_item = max(items_con_calorias, key=lambda x: x['calorias_float'])
                    min_item = min(items_con_calorias, key=lambda x: x['calorias_float'])
                    
                    print(f"- Promedio de calorías global: {promedio_global:.2f} cal")
                    print(f"- Alimento con MÁS calorías: {max_item['nombre']} ({max_item['calorias_float']:.1f} cal)")
                    print(f"- Alimento con MENOS calorías: {min_item['nombre']} ({min_item['calorias_float']:.1f} cal)")
                else:
                    print("- No hay datos de calorías para calcular estadísticas.")

            case "2": # Distribución por Categoría
                print("\n--- Distribución de Alimentos por Categoría ---")
                from collections import Counter
                # Counter es una forma muy eficiente de contar elementos
                conteo_categorias = Counter(item['categoria'] for item in lista_completa if 'categoria' in item)
                if conteo_categorias:
                    for categoria, cantidad in conteo_categorias.items():
                        print(f"- {categoria}: {cantidad} ítems")
                else:
                    print("No se encontraron categorías.")

            case "3": # Análisis Detallado por Categoría (Interactivo)
                print("\n--- Análisis Detallado por Categoría ---")
                categorias = sorted(list(set(item['categoria'] for item in items_con_calorias if 'categoria' in item)))
                if not categorias:
                    print("No hay categorías con datos de calorías para analizar.")
                    continue

                for i, cat in enumerate(categorias):
                    print(f"  ID {i}) {cat}")
                
                try:
                    id_cat_str = input(f"Ingrese el ID de la categoría a analizar (0-{len(categorias)-1}): ")
                    id_cat = int(id_cat_str)
                    if 0 <= id_cat < len(categorias):
                        categoria_elegida = categorias[id_cat]
                        items_categoria = [item for item in items_con_calorias if item.get('categoria') == categoria_elegida]
                        
                        if items_categoria:
                            suma_cal = sum(item['calorias_float'] for item in items_categoria)
                            promedio_cat = suma_cal / len(items_categoria)
                            max_item_cat = max(items_categoria, key=lambda x: x['calorias_float'])
                            min_item_cat = min(items_categoria, key=lambda x: x['calorias_float'])
                            
                            print(f"\nEstadísticas para la categoría '{categoria_elegida}':")
                            print(f"- Promedio de calorías: {promedio_cat:.2f} cal")
                            print(f"- Alimento MÁS calórico: {max_item_cat['nombre']} ({max_item_cat['calorias_float']:.1f} cal)")
                            print(f"- Alimento MENOS calórico: {min_item_cat['nombre']} ({min_item_cat['calorias_float']:.1f} cal)")
                    else:
                        print("ID de categoría inválido.")
                except (ValueError, IndexError):
                    print("Entrada no válida. Debe ingresar un número de ID.")

            case "4": # Ranking de Calorías Promedio por Categoría
                print("\n--- Ranking de Calorías Promedio por Categoría ---")
                categorias = sorted(list(set(item['categoria'] for item in items_con_calorias if 'categoria' in item)))
                promedios_por_categoria = []

                for cat in categorias:
                    items_categoria = [item for item in items_con_calorias if item.get('categoria') == cat]
                    if items_categoria:
                        suma_cal = sum(item['calorias_float'] for item in items_categoria)
                        promedio = suma_cal / len(items_categoria)
                        promedios_por_categoria.append({'categoria': cat, 'promedio': promedio})
                
                # Ordenar la lista de promedios de mayor a menor
                ranking = sorted(promedios_por_categoria, key=lambda x: x['promedio'], reverse=True)

                if ranking:
                    for i, data in enumerate(ranking):
                        print(f"{i+1}. {data['categoria']} ({data['promedio']:.1f} cal en promedio)")
                else:
                    print("No hay suficientes datos para generar un ranking.")

            case "5": # Top 3 Más/Menos Calóricos por Categoría (Interactivo)
                print("\n--- Top 3 Más/Menos Calóricos por Categoría ---")
                categorias = sorted(list(set(item['categoria'] for item in items_con_calorias if 'categoria' in item)))
                if not categorias:
                    print("No hay categorías con datos de calorías para analizar.")
                    continue

                for i, cat in enumerate(categorias):
                    print(f"  ID {i}) {cat}")
                
                try:
                    id_cat_str = input(f"Ingrese el ID de la categoría a analizar (0-{len(categorias)-1}): ")
                    id_cat = int(id_cat_str)
                    if 0 <= id_cat < len(categorias):
                        categoria_elegida = categorias[id_cat]
                        items_categoria = [item for item in items_con_calorias if item.get('categoria') == categoria_elegida]
                        
                        if len(items_categoria) < 1:
                            print(f"No hay suficientes datos en la categoría '{categoria_elegida}'.")
                            continue

                        # Ordenar la lista de ítems de la categoría por calorías
                        items_ordenados = sorted(items_categoria, key=lambda x: x['calorias_float'])
                        
                        print(f"\n--- Categoría: {categoria_elegida} ---")
                        
                        # Top 3 Más Calóricos (los últimos 3 de la lista ordenada)
                        print("  Top 3 Más Calóricos:")
                        top_mas = items_ordenados[-3:] # Tomamos los últimos 3
                        top_mas.reverse() # Los invertimos para que el más alto quede primero
                        if not top_mas: print("    No hay datos.")
                        for i, item in enumerate(top_mas):
                            print(f"    {i+1}. {item['nombre']} ({item['calorias_float']:.1f} cal)")

                        # Top 3 Menos Calóricos (los primeros 3 de la lista ordenada)
                        print("  Top 3 Menos Calóricos:")
                        top_menos = items_ordenados[:3] # Tomamos los primeros 3
                        if not top_menos: print("    No hay datos.")
                        for i, item in enumerate(top_menos):
                            print(f"    {i+1}. {item['nombre']} ({item['calorias_float']:.1f} cal)")

                    else:
                        print("ID de categoría inválido.")
                except (ValueError, IndexError):
                    print("Entrada no válida. Debe ingresar un número de ID.")

            case "0": # Volver
                break
            case _:
                print("Opción no válida.")

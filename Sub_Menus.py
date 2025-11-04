from Manejo_archivo import *
import unicodedata
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
    print("--- Alta de Nuevo Alimento ---")
    
    # Pedir jerarquía
    categoria_input = input("Ingrese Categoría (ej: Frutas): ")
    tipo_input = input("Ingrese Tipo (ej: Cítricos): ")
    procesamiento_input = input("Ingrese Procesamiento (ej: Fresco): ")

    # --- VALIDACIÓN DE NORMALIZACIÓN ---
    # Llama a la nueva función (la de unicodedata)
    categoria = normalizar_texto_para_ruta(categoria_input)
    tipo = normalizar_texto_para_ruta(tipo_input)
    procesamiento = normalizar_texto_para_ruta(procesamiento_input)
    
    # (Opcional) Informar al usuario la normalización
    print(f"Guardando en -> Categoría: {categoria}, Tipo: {tipo}, Procesamiento: {procesamiento}")
    
    # Pedir atributos
    nombre = input("Ingrese Nombre del alimento: ")
    
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
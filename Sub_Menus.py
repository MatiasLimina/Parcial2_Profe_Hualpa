from Manejo_archivo import *
def opcion_1_alta():
    print("--- Alta de Nuevo Alimento ---")
    
    # Pedir jerarquía [cite: 63]
    categoria = input("Ingrese Categoría (ej: Frutas): ")
    tipo = input("Ingrese Tipo (ej: Cítricos): ")
    procesamiento = input("Ingrese Procesamiento (ej: Fresco): ")

    # Pedir atributos [cite: 64]
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
                print("Error: Las calorías deben ser un número positivo mayor a cero.") [cite: 68]
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
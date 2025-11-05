from Manejo_archivo import *
from Sub_Menus import *
from Utilidades import *
def main():
    salir = False
    while not salir:
        print("--- MENU ---")
        print("1) Alta de nuevo item")
        print("2) Mostrar lista global y filtrado")
        print("3) Modificacion de un item")
        print("4) Eliminacion de un item")
        print("5) Estadisticas y ordenamiento")
        print("6) Salir")
        opc = input("Elija una opcion ")
        match opc:
            case "1":
                #1) Alta de nuevo item
                opcion_1_alta()
            case "2":
                #2) Mostrar lista global y filtrado
                continue
            case "3":
                #3) Modificacion de un item
                nombre = input("Ingrese el nombre exacto del ítem que desea modificar: ")
                if nombre:
                    modificar_item_por_nombre(nombre) # Llamada a la nueva función
                else:
                    print("No ingresó un nombre. Volviendo al menú.")
            case "4":
                #4) Eliminacion de un item/Busqueda multiples coincidencias
                nombre = input("Ingrese el nombre exacto del ítem que desea eliminar: ")
                if nombre:
                    eliminar_item_por_nombre(nombre) # Llamada a la nueva función
                else:
                    print("No ingresó un nombre. Volviendo al menú.")
            case "5":
                #5) Estadisticas y ordenamiento
                continue
            case "6":
                print("Gracias vuelva pronto!")
                salir = True

main()
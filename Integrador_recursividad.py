from Manejo_archivo import *
from Sub_Menus import *
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
                continue
            case "4":
                #4) Eliminacion de un item
                continue
            case "5":
                #5) Estadisticas y ordenamiento
                continue
            case "6":
                print("Gracias vuelva pronto!")
                salir = True

main()
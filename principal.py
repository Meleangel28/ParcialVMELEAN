from menu_empleados import MenuEmpleados
from menu_factura_pago import MenuFacturas
from json import load

if __name__ == "__main__":
    with open('config.json', 'r') as config_file:
        config_data = load(config_file)

    menu_empleados = MenuEmpleados(config_data["archivo_empleados"])#Arbol de busqueda binaria
    menu_facturas = MenuFacturas(config_data["facturas_file"])#Arbol AVL
    
    
    while True:
        print("Menú Principal:")
        print("1. Gestión de Empleados")
        print("2. Módulo de Facturación y Pagos")
        print("3. Salir")

        try:
            opcion = int(input("Ingrese el número de la opción deseada: "))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue
        
        print("\n"+"="*40)
            
        if opcion == 1:
            menu_empleados.mostrar_menu()
        elif opcion == 2:
            menu_facturas.mostrar_menu()
        elif opcion == 3:
            print("Saliendo del Programa.")
            break
        else:
            print("Opción no válida. Por favor, ingrese una opción válida.")
        print("="*40+"\n")
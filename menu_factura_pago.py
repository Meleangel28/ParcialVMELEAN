from Gestión_facturacion_pagos import SistemaReservaciones, Factura

class MenuFacturas:
    def __init__(self, facturas_file):
        self.facturas_file = facturas_file
        self.sistema = SistemaReservaciones()
        
        #Respaldo de datos por defecto
        # # Ejemplo 1:
        # factura1 = Factura("Juan Pérez", 250.0, ["Desayuno", "Wi-Fi"], "Tarjeta de Crédito", "Pendiente")
        # self.sistema.raiz = self.sistema.agregar(factura1, self.sistema.raiz)

        # # Ejemplo 2:
        # factura2 = Factura("María López", 180.5, ["Estacionamiento"], "Efectivo", "Pagado")
        # self.sistema.raiz = self.sistema.agregar(factura2, self.sistema.raiz)

        # # Ejemplo 3:
        # factura3 = Factura("Carlos González", 320.0, ["Gimnasio", "Spa"], "Tarjeta de Crédito", "Pagado")
        # self.sistema.raiz = self.sistema.agregar(factura3, self.sistema.raiz)

        # # Ejemplo 4:
        # factura4 = Factura("Ana Rodríguez", 150.0, ["Desayuno"], "Efectivo", "Pendiente")
        # self.sistema.raiz = self.sistema.agregar(factura4, self.sistema.raiz)

        # # Ejemplo 5:
        # factura5 = Factura("Luis García", 280.0, ["Wi-Fi"], "Tarjeta de Crédito", "Pagado")
        # self.sistema.raiz = self.sistema.agregar(factura5, self.sistema.raiz)

        # # Ejemplo 6:
        # factura6 = Factura("Laura Martínez", 210.0, ["Estacionamiento", "Spa"], "Efectivo", "Pendiente")
        # self.sistema.raiz = self.sistema.agregar(factura6, self.sistema.raiz)

        # # Ejemplo 7:
        # factura7 = Factura("Javier Ramírez", 190.5, ["Gimnasio"], "Tarjeta de Crédito", "Pagado")
        # self.sistema.raiz = self.sistema.agregar(factura7, self.sistema.raiz)

        # # Ejemplo 8:
        # factura8 = Factura("Patricia Silva", 300.0, ["Desayuno", "Wi-Fi", "Gimnasio"], "Tarjeta de Crédito", "Pagado")
        # self.sistema.raiz = self.sistema.agregar(factura8, self.sistema.raiz)

        # # Ejemplo 9:
        # factura9 = Factura("Oscar Torres", 220.0, ["Estacionamiento"], "Efectivo", "Pendiente")
        # self.sistema.raiz = self.sistema.agregar(factura9, self.sistema.raiz)

        # # Ejemplo 10:
        # factura10 = Factura("Carolina Vargas", 260.0, ["Spa"], "Tarjeta de Crédito", "Pagado")
        # self.sistema.raiz = self.sistema.agregar(factura10, self.sistema.raiz)
        
        if SistemaReservaciones.deserializar(facturas_file) is not None:
            self.sistema = SistemaReservaciones.deserializar(facturas_file)
            # Obtener la lista de facturas existentes
            facturas_existentes = self.sistema.listar_facturas(self.sistema.raiz)

            # Determinar el valor máximo actual del número de factura
            max_numero_factura = max([factura.numero_factura for factura in facturas_existentes])

            # Establecer el contador de facturas en el valor máximo actual + 1
            Factura.contador_facturas = max_numero_factura + 1
        
    def mostrar_menu(self):
        while True:
            print("Menú de Facturación y Pagos:")
            print("1. Agregar Factura")
            print("2. Buscar Factura")
            print("3. Eliminar Factura")
            print("4. Listar Facturas")
            print("5. Listar Facturas por Método de Pago (Recorrido en postorden)")
            print("6. Mostrar Altura del Árbol")
            print("7. Mostrar Estructura del Árbol (Recorrido en preorden)")
            print("8. Salir")

            
            try:
                opcion = int(input("Ingrese el número de la opción deseada: "))
            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue
            
            print("\n"+"="*40)
            
            if opcion == 1:
                self.agregar_factura()
            elif opcion == 2:
                self.buscar_factura()
            elif opcion == 3:
                self.eliminar_factura()
            elif opcion == 4:
                self.listar_facturas()
            elif opcion == 5:
                self.listar_facturas_por_metodo_pago_postorden()
            elif opcion == 6:
                self.mostrar_altura_arbol()
            elif opcion == 7:
                self.mostrar_estructura_arbol()
            elif opcion == 8:
                print("Saliendo de la Gestión de Facturación y Pagos.")
                break
            else:
                print("Opción no válida. Por favor, ingrese una opción válida.")
            print("="*40+"\n")
            self.sistema.serializar(self.facturas_file)
            
    def agregar_factura(self):
        try:
            cliente = input("Ingrese el nombre del cliente: ")
            costo_total = float(input("Ingrese el costo total: "))
            servicios_adicionales = input("Ingrese los servicios adicionales (separados por comas): ").split(',')
            metodo_pago = input("Ingrese el método de pago: ")
            estado_pago = input("Ingrese el estado del pago: ")

            factura = Factura(cliente, costo_total, servicios_adicionales, metodo_pago, estado_pago)
            self.sistema.raiz = self.sistema.agregar(factura, self.sistema.raiz)
            print("Factura agregada exitosamente. Número de Factura:", factura.numero_factura)
            print("Fecha de Factura:", factura.fecha)
        except ValueError:
            print("Error: Ingrese valores válidos para los campos numéricos.")


    def buscar_factura(self):
        try:
            numero_factura = int(input("Ingrese el número de factura a buscar: "))
            factura = self.sistema.buscar(numero_factura, self.sistema.raiz)
            if factura:
                print("Número de Factura:", factura.numero_factura)
                print("Fecha:", factura.fecha)
                print("Cliente:", factura.cliente)
                print("Costo Total:", factura.costo_total)
                print("Servicios Adicionales:", ', '.join(factura.servicios_adicionales))
                print("Método de Pago:", factura.metodo_pago)
                print("Estado del Pago:", factura.estado_pago)
            else:
                print("Factura no encontrada.")
        except ValueError:
            print("Error: Ingrese un número válido para el número de factura.")

    def eliminar_factura(self):
        try:
            numero_factura = int(input("Ingrese el número de factura a eliminar: "))
            factura = self.sistema.buscar(numero_factura, self.sistema.raiz)
            if factura:
                self.sistema.raiz = self.sistema.eliminar(numero_factura, self.sistema.raiz)
                print("Factura eliminada exitosamente.")
            else:
                print("Factura no encontrada.")
        except ValueError:
            print("Error: Ingrese un número válido para el número de factura.")

    def listar_facturas(self):
        facturas = self.sistema.listar_facturas(self.sistema.raiz)
        if facturas:
            print("Lista de Facturas:")
            for k, factura in enumerate(facturas):
                print("Número de Factura:", factura.numero_factura)
                print("Fecha:", factura.fecha)
                print("Cliente:", factura.cliente)
                print("Costo Total:", factura.costo_total)
                print("Servicios Adicionales:", ', '.join(factura.servicios_adicionales))
                print("Método de Pago:", factura.metodo_pago)
                print("Estado del Pago:", factura.estado_pago)
                if k != len(facturas)-1:
                    print("\n")
        else:
            print("No hay facturas en el sistema.")
            
    def listar_facturas_por_metodo_pago_postorden(self):
        metodo_pago = input("Ingrese el método de pago para listar las facturas (Postorden): ")
        facturas = self.sistema.listar_facturas_por_metodo_pago_postorden(metodo_pago, self.sistema.raiz)
        if facturas:
            print(f"\nFacturas con Método de Pago '{metodo_pago}' (Postorden):")
            for factura in facturas:
                print("Número de Factura:", factura.numero_factura)
                print("Fecha:", factura.fecha)
                print("Cliente:", factura.cliente)
                print("Costo Total:", factura.costo_total)
                print("Servicios Adicionales:", ', '.join(factura.servicios_adicionales))
                print("Método de Pago:", factura.metodo_pago)
                print("Estado del Pago:", factura.estado_pago)
                print("")
        else:
            print(f"No hay facturas con Método de Pago '{metodo_pago}' en el sistema (Postorden).")

    def mostrar_altura_arbol(self):
        altura = self.sistema.altura_arbol(self.sistema.raiz)
        print(f"Altura del Árbol: {altura}")

    def mostrar_estructura_arbol(self):
        print("Estructura del Árbol:")
        self.sistema.mostrar_arbol(self.sistema.raiz)
from gestion_empleado import Empleado, ArbolEmpleados
from datetime import datetime

class MenuEmpleados:
    def __init__(self, archivo_empleados):
        self.archivo_empleados = archivo_empleados
        self.arbol_empleados = ArbolEmpleados()
        # self.arbol_empleados.cargar_empleados_desde_archivo("empleados.json")
        # self.arbol_empleados.serializar(archivo_empleados)

        if ArbolEmpleados.deserializar(archivo_empleados) is not None:
            self.arbol_empleados = ArbolEmpleados.deserializar(archivo_empleados)
        

        #print(self.arbol_empleados.raiz.derecha.derecha.derecha.izquierda.izquierda.derecha.derecha)
        
        
    def mostrar_menu(self):
        while True:
            print("Menú de Gestión de Empleados:")
            print("1. Agregar Empleado - Inserción por cédula")
            print("2. Buscar Empleado por cédula")
            print("3. Eliminar Empleado por cédula")
            print("4. Listar Empleados (Inorden)")
            print("5. Mostrar Altura del Árbol")
            print("6. Mostrar Árbol Completo (preorden)")
            print("7. Listar Empleados por Fecha de Contratación")
            print("8. Mostrar los cinco empleados más antiguos (Recorrido inorden)")
            print("9. Salir")
            
            opcion = input("Ingrese el número de la opción deseada: ")

            print("\n"+"="*40)
            if opcion == '1':
                self.agregar_empleado()
            elif opcion == '2':
                self.buscar_empleado()
            elif opcion == '3':
                self.eliminar_empleado()
            elif opcion == '4':
                self.listar_empleados()
            elif opcion == '5':
                self.mostrar_altura_del_arbol()
            elif opcion == '6':
                self.mostrar_arbol_completo()
            elif opcion == '7':
                self.listar_empleados_por_fecha()
            elif opcion == '8':
                self.mostrar_cinco_empleados_mas_antiguos()
            elif opcion == '9':
                print("Saliendo de Gestión de Empleados.")
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")
            self.arbol_empleados.serializar(self.archivo_empleados)
            print("="*40+"\n")

    def mostrar_cinco_empleados_mas_antiguos(self):
        self.arbol_empleados.mostrar_cinco_empleados_mas_antiguos()
        
    def mostrar_arbol_completo(self):
        print("Árbol de Empleados (Preorden):")
        self.arbol_empleados.mostrar_arbol()

    def agregar_empleado(self):
        try:
            cedula = int(input("Ingrese la cédula del empleado: "))
            
            existe = self.arbol_empleados.buscar(cedula)
            
            if existe is None:
                nombre = input("Ingrese el nombre del empleado: ")
                posicion = input("Ingrese la posición del empleado: ")
                salario = float(input("Ingrese el salario del empleado: "))
                
                # Validar la fecha en formato "DD/MM/YYYY"
                fecha_contratacion = input("Ingrese la fecha de contratación del empleado (DD/MM/YYYY): ")
                fecha_formato_correcto = datetime.strptime(fecha_contratacion, "%d/%m/%Y").strftime("%d/%m/%Y")
                
                if fecha_contratacion != fecha_formato_correcto:
                    raise ValueError("El formato de fecha debe ser DD/MM/YYYY")
                
                empleado = Empleado(cedula, nombre, posicion, salario, fecha_contratacion)
                self.arbol_empleados.insertar(empleado)
                print("Empleado agregado con éxito.")
            else:
                print("Empleado ya existe.")
        
        except ValueError as e:
            print(f"Error: {e}. Por favor, ingrese datos válidos.")
        except Exception as e:
            print(f"Se ha producido un error: {e}. Por favor, inténtelo de nuevo.")

    def buscar_empleado(self):
        try:
            cedula = int(input("Ingrese la cédula del empleado que desea buscar: "))
        except ValueError:
            print("Error: Por favor, ingrese un número de cédula válido.")
            return
        
        empleado = self.arbol_empleados.buscar(cedula)

        if empleado:
            print("Empleado encontrado:")
            print("Cédula:", empleado.cedula)
            print("Nombre:", empleado.nombre)
            print("Posición:", empleado.posicion)
            print("Salario:", empleado.salario)
            print("Fecha de Contratación:", empleado.fecha_contratacion)
        else:
            print("Empleado no encontrado.")

    def eliminar_empleado(self):
        try:
            cedula = int(input("Ingrese la cédula del empleado que desea eliminar: "))
        except ValueError:
            print("Error: Por favor, ingrese un número de cédula válido.")
            return
        
        empleado_eliminado = self.arbol_empleados.eliminar(cedula)
        
        if empleado_eliminado:
            print("Empleado eliminado con éxito.")
        else:
            print("Empleado no encontrado.")

    def listar_empleados(self):
        empleados = self.arbol_empleados.listar_empleados()
        if empleados:
            print("Lista de Empleados:")
            for pos, empleado in enumerate(empleados):
                print("Cédula:", empleado.cedula)
                print("Nombre:", empleado.nombre)
                print("Posición:", empleado.posicion)
                print("Salario:", empleado.salario)
                print("Fecha de Contratación:", empleado.fecha_contratacion)
                if pos != len(empleados)-1:
                    print("\n")
        else:
            print("No hay empleados registrados.")

    def mostrar_altura_del_arbol(self):
        altura = self.arbol_empleados.altura_del_arbol()
        print("Altura del árbol:", altura)
        
    def listar_empleados_por_fecha(self):
        fecha_str = input("Ingrese una fecha (DD/MM/YYYY): ")
        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y")#Validamos que la fecha esté en el formato correcto, caso contrario dara error
            empleados = self.arbol_empleados.listar_empleados_contratados_despues_o_en_fecha(fecha_str)
            if empleados:
                print("Lista de Empleados Contratados después o en la fecha", fecha.strftime("%d/%m/%Y"), "(Preorden):")
                for empleado in empleados:
                    print("Cédula:", empleado.cedula)
                    print("Nombre:", empleado.nombre)
                    print("Fecha de Contratación:", empleado.fecha_contratacion)
                    print("")
            else:
                print("No hay empleados contratados después o en la fecha especificada.")
        except ValueError:
            print("Fecha ingresada no válida. Utilice el formato DD/MM/YYYY.")
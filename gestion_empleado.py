from datetime import date
from pickle import dump, load
# from json import loads

class Empleado:
    def __init__(self, cedula:int, nombre:str, posicion:str, salario:float, fecha_contratacion:str):
        self.cedula = cedula
        self.nombre = nombre
        self.posicion = posicion
        self.salario = salario
        self.fecha_contratacion = fecha_contratacion
        self.izquierda = None
        self.derecha = None

class ArbolEmpleados:
#     Gestión de Empleados(5 ptos): Por cada hotel, utiliza un árbol binario para
# gestionar la información de los empleados(CRUDL) que trabajan en los diferentes hoteles
# de la cadena. Cada nodo representaría un empleado y contendría datos como el nombre, la
# posición, el salario y la fecha de contratación. Este módulo facilita la asignación de tareas y
# la gestión de recursos humanos
    def __init__(self):
        self.raiz = None

    def insertar(self, empleado:Empleado):
        if not self.raiz:
            self.raiz = empleado
        else:
            self._insertar_recursivo(self.raiz, empleado)

    def _insertar_recursivo(self, nodo_actual:Empleado, empleado:Empleado):#Por fecha de contratación
        if empleado.cedula < nodo_actual.cedula:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = empleado
            else:
                self._insertar_recursivo(nodo_actual.izquierda, empleado)
        elif empleado.cedula > nodo_actual.cedula:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = empleado
            else:
                self._insertar_recursivo(nodo_actual.derecha, empleado)
        else:
            # Si ya existe un empleado con la misma cédula, no se agrega porque ya existe
            pass

    def buscar(self, cedula:int):
        return self._buscar_recursivo(self.raiz, cedula)

    def _buscar_recursivo(self, nodo_actual:Empleado, cedula:int):
        if nodo_actual is None:
            return None
        if cedula == nodo_actual.cedula:
            return nodo_actual
        elif cedula < nodo_actual.cedula:
            return self._buscar_recursivo(nodo_actual.izquierda, cedula)
        else:
            return self._buscar_recursivo(nodo_actual.derecha, cedula)

    def eliminar(self, cedula:int):
        resultado, self.raiz = self._eliminar_recursivo(self.raiz, cedula)
        return resultado

    def _eliminar_recursivo(self, nodo_actual:Empleado, cedula:int):
        if nodo_actual is None:
            return False, nodo_actual

        if cedula < nodo_actual.cedula:
            resultado, nodo_actual.izquierda = self._eliminar_recursivo(nodo_actual.izquierda, cedula)
        elif cedula > nodo_actual.cedula:
            resultado, nodo_actual.derecha = self._eliminar_recursivo(nodo_actual.derecha, cedula)
        else:
            if nodo_actual.izquierda is None:
                return True, nodo_actual.derecha
            elif nodo_actual.derecha is None:
                return True, nodo_actual.izquierda

            nodo_actual.cedula = self._encontrar_minimo_valor(nodo_actual.derecha).cedula
            resultado, nodo_actual.derecha = self._eliminar_recursivo(nodo_actual.derecha, nodo_actual.cedula)

        return resultado, nodo_actual

    def _encontrar_minimo_valor(self, nodo_actual:Empleado):
        while nodo_actual.izquierda:
            nodo_actual = nodo_actual.izquierda
        return nodo_actual

    def listar_empleados(self):
        empleados = []
        self._inorden(self.raiz, empleados)
        return empleados

    def _inorden(self, nodo_actual:Empleado, empleados:Empleado):
        if nodo_actual:
            self._inorden(nodo_actual.izquierda, empleados)
            empleados.append(nodo_actual)
            self._inorden(nodo_actual.derecha, empleados)
            
# Listar todos los empleados existentes dado un hotel seleccionado y por fecha
# de contratación.Mostrar altura del árbol (Recorrido en preorden)
    def altura_del_arbol(self):
        return self._altura_del_arbol(self.raiz)

    def _altura_del_arbol(self, nodo_actual):
        if nodo_actual is None:
            return 0
        else:
            izquierda_altura = self._altura_del_arbol(nodo_actual.izquierda)
            derecha_altura = self._altura_del_arbol(nodo_actual.derecha)
            return max(izquierda_altura, derecha_altura) + 1


    # def cargar_empleados_desde_archivo(self, archivo_empleados):
    #     try:
    #         with open(archivo_empleados, 'r', encoding="UTF-8") as archivo:
    #             data = archivo.read()
    #             if data:
    #                 empleados = loads(data)
    #                 for empleado in empleados:
    #                     empleado_obj = Empleado(
    #                         empleado['cedula'],
    #                         empleado['nombre'],
    #                         empleado['posicion'],
    #                         empleado['salario'],
    #                         empleado['fecha_contratacion']
    #                     )
    #                     self.insertar(empleado_obj)
    #     except FileNotFoundError:
    #         pass

    # def guardar_empleados_en_archivo(self):
    #     empleados = self.listar_empleados()
    #     empleados_json = []
    #     for empleado in empleados:
    #         empleado_data = {
    #             'cedula': empleado.cedula,
    #             'nombre': empleado.nombre,
    #             'posicion': empleado.posicion,
    #             'salario': empleado.salario,
    #             'fecha_contratacion': empleado.fecha_contratacion
    #         }
    #         empleados_json.append(empleado_data)

    #     with open(self.archivo_empleados, 'w', encoding="UTF-8") as archivo:
    #         dump(empleados_json, archivo, indent=4, ensure_ascii=False)


    def mostrar_arbol(self):
        if self.raiz:
            self._mostrar_arbol(self.raiz, None, "Raíz", 0)

    def _mostrar_arbol(self, nodo_actual, padre, rama, nivel):
        if nodo_actual is not None:
            if padre is not None:
                print(f"Nivel {nivel}: Cédula: {nodo_actual.cedula} - Nombre: {nodo_actual.nombre}")
                print(f"Precede a: {padre.cedula} {padre.nombre}  - Rama: {rama}\n")
            else:
                print(f"Nivel {nivel}: Cédula: {nodo_actual.cedula} - Nombre: {nodo_actual.nombre} (Raíz)\n")

            self._mostrar_arbol(nodo_actual.izquierda, nodo_actual, "Izquierda", nivel + 1)
            self._mostrar_arbol(nodo_actual.derecha, nodo_actual, "Derecha", nivel + 1)
            
    def serializar(self, nombre_archivo: str):
        try:
            with open(nombre_archivo, 'wb') as archivo:
                dump(self.raiz, archivo)
        except Exception as e:
            print("Error al serializar el árbol:", str(e))

    @classmethod
    def deserializar(cls, nombre_archivo: str):
        try:
            with open(nombre_archivo, 'rb') as archivo:
                arbol = cls()
                arbol.raiz = load(archivo)
            return arbol
        except Exception as e:
            print("Error al deserializar el árbol:", str(e))
            return None

    def listar_empleados_contratados_despues_o_en_fecha(self, fecha):
        empleados = []
        self._preorden_fecha_contratacion(self.raiz, fecha, empleados)
        return empleados

    def _preorden_fecha_contratacion(self, nodo_actual, fecha, empleados):
        if nodo_actual:
            if self._convertir_a_date(nodo_actual.fecha_contratacion) >= self._convertir_a_date(fecha):
                empleados.append(nodo_actual)
            self._preorden_fecha_contratacion(nodo_actual.izquierda, fecha, empleados)
            self._preorden_fecha_contratacion(nodo_actual.derecha, fecha, empleados)
            
    def _convertir_a_date(self, fecha_str:str):
        dd, mm, yyyy = map(int, fecha_str.split('/'))
        fecha = date(yyyy, mm, dd)
        return fecha
    
    def mostrar_cinco_empleados_mas_antiguos(self):
        empleados = self._inorden_fecha_contratacion(self.raiz, [])
        empleados.sort(key=lambda empleado: self._convertir_a_date(empleado.fecha_contratacion))
        if len(empleados) >= 5:
            print("Los cinco empleados más antiguos:")
            for i in range(5):
                print(f"Cédula: {empleados[i].cedula} - Nombre: {empleados[i].nombre} - Fecha de Contratación: {empleados[i].fecha_contratacion}")
        else:
            print("No hay suficientes empleados registrados para mostrar cinco de los más antiguos.")

    def _inorden_fecha_contratacion(self, nodo_actual, empleados):
        if nodo_actual:
            self._inorden_fecha_contratacion(nodo_actual.izquierda, empleados)
            empleados.append(nodo_actual)
            self._inorden_fecha_contratacion(nodo_actual.derecha, empleados)
        return empleados
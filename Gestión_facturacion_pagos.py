from datetime import datetime
from pickle import dump, load

class Factura:

    # Variable de clase para mantener un contador de facturas
    contador_facturas = 1

    def __init__(self, cliente, costo_total, servicios_adicionales, metodo_pago, estado_pago):
        # Asignar la fecha y hora actual con formato de 12 horas
        self.fecha = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")

        # Generar el número de factura automáticamente
        self.numero_factura = Factura.contador_facturas
        Factura.contador_facturas += 1

        self.cliente = cliente
        self.costo_total = costo_total
        self.servicios_adicionales = servicios_adicionales
        self.metodo_pago = metodo_pago
        self.estado_pago = estado_pago

class NodoAVL:
    def __init__(self, factura):
        self.factura = factura
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class SistemaReservaciones:
    def __init__(self):
        self.raiz = None

    def altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def balance(self, nodo):
        if not nodo:
            return 0
        return self.altura(nodo.izquierda) - self.altura(nodo.derecha)

    def rotar_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha

        x.derecha = y
        y.izquierda = T2

        y.altura = 1 + max(self.altura(y.izquierda), self.altura(y.derecha))
        x.altura = 1 + max(self.altura(x.izquierda), self.altura(x.derecha))

        return x

    def rotar_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda

        y.izquierda = x
        x.derecha = T2

        x.altura = 1 + max(self.altura(x.izquierda), self.altura(x.derecha))
        y.altura = 1 + max(self.altura(y.izquierda), self.altura(y.derecha))

        return y

    def agregar(self, factura, nodo_actual=None):
        if not nodo_actual:
            return NodoAVL(factura)
        
        if factura.numero_factura < nodo_actual.factura.numero_factura:
            nodo_actual.izquierda = self.agregar(factura, nodo_actual.izquierda)
        else:
            nodo_actual.derecha = self.agregar(factura, nodo_actual.derecha)

        nodo_actual.altura = 1 + max(self.altura(nodo_actual.izquierda), self.altura(nodo_actual.derecha))

        balance = self.balance(nodo_actual)

        if balance > 1:
            if factura.numero_factura < nodo_actual.izquierda.factura.numero_factura:
                return self.rotar_derecha(nodo_actual)
            else:
                nodo_actual.izquierda = self.rotar_izquierda(nodo_actual.izquierda)
                return self.rotar_derecha(nodo_actual)

        if balance < -1:
            if factura.numero_factura > nodo_actual.derecha.factura.numero_factura:
                return self.rotar_izquierda(nodo_actual)
            else:
                nodo_actual.derecha = self.rotar_derecha(nodo_actual.derecha)
                return self.rotar_izquierda(nodo_actual)

        return nodo_actual

    def buscar(self, numero_factura, nodo_actual=None):
        if not nodo_actual:
            return None
        if numero_factura == nodo_actual.factura.numero_factura:
            return nodo_actual.factura
        if numero_factura < nodo_actual.factura.numero_factura:
            return self.buscar(numero_factura, nodo_actual.izquierda)
        return self.buscar(numero_factura, nodo_actual.derecha)

    def eliminar(self, numero_factura, nodo_actual=None):
        if not nodo_actual:
            return nodo_actual

        if numero_factura < nodo_actual.factura.numero_factura:
            nodo_actual.izquierda = self.eliminar(numero_factura, nodo_actual.izquierda)
        elif numero_factura > nodo_actual.factura.numero_factura:
            nodo_actual.derecha = self.eliminar(numero_factura, nodo_actual.derecha)
        else:
            if not nodo_actual.izquierda:
                return nodo_actual.derecha
            elif not nodo_actual.derecha:
                return nodo_actual.izquierda
            temp = self.min_value_node(nodo_actual.derecha)
            nodo_actual.factura = temp.factura
            nodo_actual.derecha = self.eliminar(temp.factura.numero_factura, nodo_actual.derecha)

        if not nodo_actual:
            return nodo_actual

        nodo_actual.altura = 1 + max(self.altura(nodo_actual.izquierda), self.altura(nodo_actual.derecha))

        balance = self.balance(nodo_actual)

        if balance > 1:
            if self.balance(nodo_actual.izquierda) >= 0:
                return self.rotar_derecha(nodo_actual)
            else:
                nodo_actual.izquierda = self.rotar_izquierda(nodo_actual.izquierda)
                return self.rotar_derecha(nodo_actual)

        if balance < -1:
            if self.balance(nodo_actual.derecha) <= 0:
                return self.rotar_izquierda(nodo_actual)
            else:
                nodo_actual.derecha = self.rotar_derecha(nodo_actual.derecha)
                return self.rotar_izquierda(nodo_actual)

        return nodo_actual

    def min_value_node(self, nodo):
        while nodo.izquierda:
            nodo = nodo.izquierda
        return nodo

    def listar_facturas(self, nodo_actual=None):
        if not nodo_actual:
            return []
        return self.listar_facturas(nodo_actual.izquierda) + [nodo_actual.factura] + self.listar_facturas(nodo_actual.derecha)
    
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

    def listar_facturas_por_metodo_pago_postorden(self, metodo_pago, nodo_actual=None):
        resultado = []

        if not nodo_actual:
            return resultado

        # Recorrido en postorden: izquierda -> derecha -> nodo actual
        resultado += self.listar_facturas_por_metodo_pago_postorden(metodo_pago, nodo_actual.izquierda)
        resultado += self.listar_facturas_por_metodo_pago_postorden(metodo_pago, nodo_actual.derecha)

        # Verificar si el nodo actual tiene el método de pago deseado
        if nodo_actual.factura.metodo_pago == metodo_pago:
            resultado.append(nodo_actual.factura)

        return resultado

    def altura_arbol(self, nodo):
        if nodo is None:
            return 0
        else:
            izquierda = self.altura_arbol(nodo.izquierda)
            derecha = self.altura_arbol(nodo.derecha)
            return max(izquierda, derecha) + 1

    def mostrar_arbol(self, nodo_actual=None, nivel=0, lado=None):
        if not nodo_actual:
            return

        # Indentar según el nivel del nodo para mostrar la estructura del árbol
        indentacion = " " * (nivel * 4)

        # Determinar si es un nodo izquierdo o derecho
        if lado is None:
            nodo_str = f"Raíz (Nivel {nivel}):"
        elif lado == "izquierda":
            nodo_str = f"Nodo Izquierdo (Nivel {nivel}):"
        else:
            nodo_str = f"Nodo Derecho (Nivel {nivel}):"

        # Imprimir información del nodo actual
        print(indentacion + nodo_str)
        print(indentacion + f"Número de Factura: {nodo_actual.factura.numero_factura}")
        print(indentacion + f"Cliente: {nodo_actual.factura.cliente}")
        print()

        # Recorrer los nodos hijos (preorden)
        self.mostrar_arbol(nodo_actual.izquierda, nivel + 1, lado="izquierda")
        self.mostrar_arbol(nodo_actual.derecha, nivel + 1, lado="derecha")
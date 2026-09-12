class Nodo:

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ColaPrioridad:

    def __init__(self):
        self.cabeza = None
        self.final = None

    def obtener_prioridad(self, solicitud):
        if solicitud["prioridad"] == "ALTA":
            return 3
        elif solicitud["prioridad"] == "MEDIA":
            return 2
        else:
            return 1

    def insertar(self, solicitud):

        nuevo_nodo = Nodo(solicitud)

        # Si la cola está vacía
        if self.cabeza == None:
            self.cabeza = nuevo_nodo
            self.final = nuevo_nodo
            return

        prioridad_nueva = self.obtener_prioridad(solicitud)
        prioridad_cabeza = self.obtener_prioridad(self.cabeza.dato)

        # Si la nueva solicitud tiene mayor prioridad
        if prioridad_nueva > prioridad_cabeza:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo
            return

        # Buscar dónde insertar la solicitud
        actual = self.cabeza

        while actual.siguiente != None:

            prioridad_siguiente = self.obtener_prioridad(
                actual.siguiente.dato
            )

            if prioridad_nueva > prioridad_siguiente:
                break

            actual = actual.siguiente

        nuevo_nodo.siguiente = actual.siguiente
        actual.siguiente = nuevo_nodo

        # Si se insertó al final
        if nuevo_nodo.siguiente == None:
            self.final = nuevo_nodo

    def atender(self):

        if self.cabeza == None:
            return None

        solicitud = self.cabeza.dato

        self.cabeza = self.cabeza.siguiente

        if self.cabeza == None:
            self.final = None

        return solicitud

    def imprimir_cola(self):

        actual = self.cabeza

        while actual:
            print(
                actual.dato["recurso"],
                "-",
                actual.dato["prioridad"]
            )

            actual = actual.siguiente

        print("Fin")


    def eliminar(self, id_solicitud):

        actual = self.cabeza
        anterior = None

        while actual != None:

            if actual.dato["id"] == id_solicitud:

                # Si es el primer nodo
                if anterior == None:
                    self.cabeza = actual.siguiente

                # Si está en medio o al final
                else:
                    anterior.siguiente = actual.siguiente

                # Si era el último nodo
                if actual == self.final:
                    self.final = anterior

                return actual.dato

            anterior = actual
            actual = actual.siguiente

        return None







if __name__ == "__main__":

    cola = ColaPrioridad()

    solicitud1 = {
    "id": 1,
    "recurso": "Proyector",
    "prioridad": "MEDIA"
    }

    solicitud2 = {
    "id": 2,
    "recurso": "Computador",
    "prioridad": "BAJA"
    }

    solicitud3 = {
    "id": 3,
    "recurso": "Tablero digital",
    "prioridad": "ALTA"
    }

    solicitud4 = {
    "id": 4,
    "recurso": "Ventilador",
    "prioridad": "MEDIA"
    }
    
    cola.insertar(solicitud1)
    cola.insertar(solicitud2)
    cola.insertar(solicitud3)
    cola.insertar(solicitud4)

    print("COLA DE PRIORIDAD:")
    cola.imprimir_cola()

    print("\nATENDIENDO:")
    solicitud_atendida = cola.atender()

    print(
        solicitud_atendida["recurso"],
        "-",
        solicitud_atendida["prioridad"]
    )

    print("\nCOLA DESPUÉS DE ATENDER:")
    cola.imprimir_cola()

    print("\nELIMINANDO PROYECTOR:")

    cola.eliminar(1)

    print("\nCOLA DESPUÉS DE ELIMINAR:")
    cola.imprimir_cola()    
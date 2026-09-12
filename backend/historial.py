import json
from pathlib import Path


class Nodo:

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Historial:

    def __init__(self):
        self.cabeza = None

    def insertar(self, dato):

        nuevo_nodo = Nodo(dato)

        nuevo_nodo.siguiente = self.cabeza

        self.cabeza = nuevo_nodo

    def guardar_en_json(self):

        archivo = Path("datos/historial.json")

        cambios = []

        actual = self.cabeza

        while actual:

            cambios.append(actual.dato)

            actual = actual.siguiente

        with open(archivo, "w", encoding="utf-8") as archivo_json:

            json.dump(
                cambios,
                archivo_json,
                indent=4,
                ensure_ascii=False
            )

    def cargar_desde_json(self):

        archivo = Path("datos/historial.json")

        if not archivo.exists():
            return

        with open(archivo, "r", encoding="utf-8") as archivo_json:
            cambios = json.load(archivo_json)

        for dato in reversed(cambios):
            self.insertar(dato)

    def imprimir_historial(self):

        actual = self.cabeza

        while actual:

            print(actual.dato)

            actual = actual.siguiente

        print("Fin")


if __name__ == "__main__":

    historial = Historial()

    historial.insertar("Solicitud creada")
    historial.insertar("Estado cambiado a EN PROCESO")
    historial.insertar("Estado cambiado a SOLUCIONADO")

    print("HISTORIAL:")

    historial.imprimir_historial()
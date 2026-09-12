from fastapi import FastAPI
from pydantic import BaseModel
from backend.prioridad import calcular_prioridad
from backend.cola_prioridad import ColaPrioridad
from backend.historial import Historial
from datetime import datetime
from typing import Optional
import json
from pathlib import Path


app = FastAPI(title="Nodex API")

cola = ColaPrioridad()
historial = Historial()
historial.cargar_desde_json()

def cargar_cola():

    archivo = Path("datos/solicitudes.json")

    with open(archivo, "r", encoding="utf-8") as archivo_json:
        solicitudes = json.load(archivo_json)

    for solicitud in solicitudes:
        if solicitud.get("estado") == "PENDIENTE":
            cola.insertar(solicitud)

cargar_cola()

def guardar_solicitud(solicitud):
    archivo = Path("datos/solicitudes.json")

    with open(archivo, "r", encoding="utf-8") as archivo_json:
        solicitudes = json.load(archivo_json)

    solicitudes.append(solicitud)

    with open(archivo, "w", encoding="utf-8") as archivo_json:
        json.dump(solicitudes, archivo_json, indent=4, ensure_ascii=False)

def calcular_minutos_espera(id_solicitud):

    actual = historial.cabeza
    fecha_creacion = None

    while actual:
        if (
            actual.dato.get("id") == id_solicitud
            and actual.dato.get("accion") == "Solicitud creada"
        ):
            fecha_creacion = actual.dato.get("fecha_hora")
            break

        actual = actual.siguiente

    if fecha_creacion is None:
        return 0

    fecha_creacion = datetime.strptime(
        fecha_creacion,
        "%d/%m/%Y %H:%M:%S"
    )

    ahora = datetime.now()

    tiempo_espera = ahora - fecha_creacion

    minutos = int(tiempo_espera.total_seconds() // 60)

    return minutos

def actualizar_prioridades_pendientes():

    archivo = Path("datos/solicitudes.json")

    if not archivo.exists():
        return

    with open(archivo, "r", encoding="utf-8") as archivo_json:
        solicitudes = json.load(archivo_json)

    for solicitud in solicitudes:

        if solicitud.get("estado") == "PENDIENTE":

            minutos_espera = calcular_minutos_espera(
                solicitud["id"]
            )

            nueva_prioridad = calcular_prioridad(
                solicitud["impacto_academico"],
                solicitud["personas_afectadas"],
                minutos_espera
            )

            solicitud["prioridad"] = nueva_prioridad

    with open(archivo, "w", encoding="utf-8") as archivo_json:
        json.dump(
            solicitudes,
            archivo_json,
            indent=4,
            ensure_ascii=False
        )

    # Reconstruir la cola con las nuevas prioridades
    cola.cabeza = None
    cola.final = None

    for solicitud in solicitudes:

        if solicitud.get("estado") == "PENDIENTE":
            cola.insertar(solicitud)


class Solicitud(BaseModel):
    id: Optional[int] = None
    recurso: str
    ubicacion: str
    descripcion: str
    impacto_academico: int
    personas_afectadas: int

class CambioEstado(BaseModel):
    estado: str

class ModificarPrioridad(BaseModel):
    impacto_academico: int
    personas_afectadas: int


@app.get("/")
def inicio():
    return {"message": "Nodex API funcionando correctamente."}



@app.post("/solicitudes")
def crear_solicitud(solicitud: Solicitud):
    archivo = Path("datos/solicitudes.json")
    
    # Cargar las solicitudes existentes para calcular el nuevo ID
    solicitudes_existentes = []
    if archivo.exists():
        with open(archivo, "r", encoding="utf-8") as archivo_json:
            try:
                solicitudes_existentes = json.load(archivo_json)
            except json.JSONDecodeError:
                solicitudes_existentes = []

    # Generar ID automático: si ya existen solicitudes, toma el max(id) + 1, si no empieza en 1
    ids = [s.get("id", 0) for s in solicitudes_existentes if isinstance(s.get("id"), int)]
    nuevo_id = max(ids) + 1 if ids else 1

    # Calcular la prioridad
    prioridad = calcular_prioridad(
        solicitud.impacto_academico,
        solicitud.personas_afectadas,
        0
    )

    nueva_solicitud = {
        "id": nuevo_id,
        "recurso": solicitud.recurso,
        "ubicacion": solicitud.ubicacion,
        "descripcion": solicitud.descripcion,
        "impacto_academico": solicitud.impacto_academico,
        "personas_afectadas": solicitud.personas_afectadas,
        "prioridad": prioridad,
        "estado": "PENDIENTE"
    }

    # Guardar en archivo JSON y estructuras de datos
    guardar_solicitud(nueva_solicitud)
    cola.insertar(nueva_solicitud)
    
    historial.insertar({
        "id": nuevo_id,
        "accion": "Solicitud creada",
        "estado_inicial": "PENDIENTE",
        "fecha_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
    historial.guardar_en_json()

    return {
        "mensaje": "Solicitud creada exitosamente",
        "solicitud": nueva_solicitud
    }

@app.get("/solicitudes/cola")
def consultar_cola():
    actualizar_prioridades_pendientes()
    solicitudes = []
    actual = cola.cabeza

    while actual:
        solicitudes.append(actual.dato)
        actual = actual.siguiente

    return {
        "cantidad": len(solicitudes),
        "cola": solicitudes
    }

@app.get("/solicitudes/todas")
def obtener_todas_las_solicitudes():
    archivo_solicitudes = Path("datos/solicitudes.json")
    archivo_historial = Path("datos/historial.json")

    # 1. Cargar solicitudes
    solicitudes = []
    if archivo_solicitudes.exists():
        with open(archivo_solicitudes, "r", encoding="utf-8") as f:
            solicitudes = json.load(f)

    # 2. Cargar historial
    historial_completo = []
    if archivo_historial.exists():
        with open(archivo_historial, "r", encoding="utf-8") as f:
            historial_completo = json.load(f)

    # 3. Vincular a cada solicitud su lista de historial correspondiente
    for solicitud in solicitudes:
        solicitud_id = solicitud.get("id")
        solicitud["historial"] = [
            h for h in historial_completo if h.get("id") == solicitud_id
        ]

    return {"solicitudes": solicitudes}



@app.get("/solicitudes/{id}/historial")
def consultar_historial_solicitud(id: int):
    cambios = []
    actual = historial.cabeza

    while actual:
        if actual.dato["id"] == id:
            cambios.append(actual.dato)

        actual = actual.siguiente

    return {
        "id_solicitud": id,
        "cantidad": len(cambios),
        "historial": cambios
    }


@app.put("/solicitudes/{id}/estado")
def cambiar_estado(id: int, cambio: CambioEstado):

    nuevo_estado = cambio.estado.upper()

    # Validar que el estado sea correcto
    estados_validos = ["PENDIENTE", "EN PROCESO", "SOLUCIONADO"]

    if nuevo_estado not in estados_validos:
        return {
            "mensaje": "Estado no válido"
        }

    

    # Leer las solicitudes guardadas
    archivo = Path("datos/solicitudes.json")

    if not archivo.exists():
        return {"mensaje": "Archivo de solicitudes no existe"}

    with open(archivo, "r", encoding="utf-8") as archivo_json:
        solicitudes = json.load(archivo_json)

    # Buscar la solicitud
    solicitud_encontrada = False
    for solicitud in solicitudes:

        if solicitud.get("id") == id:
            solicitud_encontrada = True
            estado_anterior = solicitud.get("estado", "PENDIENTE")

            # Actualizar el estado en el diccionario
            solicitud["estado"] = nuevo_estado

            # Si pasa a EN PROCESO o a SOLUCIONADO, la removemos de la cola en memoria
            if nuevo_estado in ["EN PROCESO", "SOLUCIONADO"]:
                try:
                    cola.eliminar(id)
                except Exception:
                    pass  # Si ya no estaba en la cola, continua normalmente

            # Guardar en historial (en memoria)
            historial.insertar({
                "id": id,
                "accion": f"Estado cambiado a {nuevo_estado}",
                "estado_anterior": estado_anterior,
                "estado_nuevo": nuevo_estado,
                "fecha_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            })

            # 1. Guardar historial en el JSON de historial
            historial.guardar_en_json()

            # 2. Guardar solicitudes actualizadas en datos/solicitudes.json
            with open(archivo, "w", encoding="utf-8") as archivo_json:
                json.dump(
                    solicitudes,
                    archivo_json,
                    indent=4,
                    ensure_ascii=False
                )

            return {
                "mensaje": "Estado actualizado correctamente",
                "solicitud": solicitud
            }

    if not solicitud_encontrada:
        return {
            "mensaje": "No se encontró la solicitud"
        }

@app.delete("/solicitudes/{id}")
def eliminar_solicitud(id: int):
    archivo = Path("datos/solicitudes.json")
    
    if not archivo.exists():
        return {"mensaje": "Archivo de solicitudes no existe", "eliminado": False}

    with open(archivo, "r", encoding="utf-8") as archivo_json:
        try:
            solicitudes = json.load(archivo_json)
        except json.JSONDecodeError:
            solicitudes = []

    # Buscar la solicitud para validar su estado
    solicitud = next((s for s in solicitudes if s.get("id") == id), None)

    if not solicitud:
        return {"mensaje": "Solicitud no encontrada", "eliminado": False}

    # Restricción: Solo se puede eliminar si está en estado PENDIENTE
    if solicitud.get("estado") != "PENDIENTE":
        return {
            "mensaje": f"No se puede eliminar la solicitud #{id} porque su estado es '{solicitud.get('estado')}'",
            "eliminado": False
        }

    # Filtrar para eliminar la solicitud de la lista
    solicitudes_actualizadas = [s for s in solicitudes if s.get("id") != id]

    # Guardar la lista actualizada en datos/solicitudes.json
    with open(archivo, "w", encoding="utf-8") as archivo_json:
        json.dump(solicitudes_actualizadas, archivo_json, indent=4, ensure_ascii=False)

    # Remover de la cola en memoria si estaba allí
    try:
        cola.eliminar(id)
    except Exception:
        pass

    # Registrar la cancelación/eliminación en el historial
    historial.insertar({
        "id": id,
        "accion": "Solicitud cancelada/eliminada por el usuario",
        "estado_inicial": "PENDIENTE",
        "fecha_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
    historial.guardar_en_json()

    return {"mensaje": "Solicitud eliminada exitosamente", "eliminado": True}





@app.put("/solicitudes/{id}/prioridad")
def modificar_prioridad(id: int, datos: ModificarPrioridad):
    try:
        # 1. Validar rangos (1 a 5)
        if not (1 <= datos.impacto_academico <= 5) or not (1 <= datos.personas_afectadas <= 5):
            return {"mensaje": "Valores de impacto o personas afectadas fuera de rango (1-5)", "actualizado": False}

        archivo = Path("datos/solicitudes.json")
        if not archivo.exists():
            return {"mensaje": "Archivo de solicitudes no existe", "actualizado": False}

        with open(archivo, "r", encoding="utf-8") as f:
            try:
                solicitudes = json.load(f)
            except json.JSONDecodeError:
                solicitudes = []

        # Buscar la solicitud
        solicitud = next((s for s in solicitudes if s.get("id") == id), None)

        if not solicitud:
            return {"mensaje": f"No se encontró la solicitud #{id}", "actualizado": False}

        # Solo permitir ajustar si está PENDIENTE
        if solicitud.get("estado") != "PENDIENTE":
            return {
                "mensaje": f"No se puede modificar la prioridad de la solicitud #{id} porque su estado es '{solicitud.get('estado')}'",
                "actualizado": False
            }

        # 2. Actualizar valores de impacto y personas afectadas
        solicitud["impacto_academico"] = datos.impacto_academico
        solicitud["personas_afectadas"] = datos.personas_afectadas
        
        # Calcular nueva prioridad como número entero
        nueva_prioridad = datos.impacto_academico + datos.personas_afectadas
        solicitud["prioridad"] = nueva_prioridad

        # 3. Separar pendientes y ordenarlas descendentemente garantizando comparaciones numéricas
        solicitudes_pendientes = [s for s in solicitudes if s.get("estado") == "PENDIENTE"]
        otras_solicitudes = [s for s in solicitudes if s.get("estado") != "PENDIENTE"]

        # Función auxiliar para obtener prioridad numérica segura
        def obtener_prioridad_numerica(s):
            prio = s.get("prioridad")
            if isinstance(prio, int):
                return prio
            # Si la prioridad es un string (ej: "ALTA", "MEDIA", "BAJA" o "8"), intentar convertir
            if isinstance(prio, str) and prio.isdigit():
                return int(prio)
            # Si no es numérico, recalcular basándose en impacto + personas afectadas
            imp = s.get("impacto_academico", 1)
            per = s.get("personas_afectadas", 1)
            try:
                return int(imp) + int(per)
            except (ValueError, TypeError):
                return 0

        # Asegurar que todas las solicitudes pendientes tengan su prioridad como int
        for s in solicitudes_pendientes:
            s["prioridad"] = obtener_prioridad_numerica(s)

        # Ordenar descendentemente por prioridad numérica
        solicitudes_pendientes.sort(key=obtener_prioridad_numerica, reverse=True)

        # Unir listas manteniendo pendientes ordenadas arriba
        solicitudes_actualizadas = solicitudes_pendientes + otras_solicitudes

        # Guardar cambios en el JSON
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(solicitudes_actualizadas, f, indent=4, ensure_ascii=False)

        # 4. Reconstruir la cola en memoria según los métodos existentes
        try:
            if hasattr(cola, 'cabeza'):
                cola.cabeza = None
            elif hasattr(cola, 'vaciar'):
                cola.vaciar()

            for s in solicitudes_pendientes:
                if hasattr(cola, 'insertar'):
                    cola.insertar(s)
                elif hasattr(cola, 'encolar'):
                    cola.encolar(s)
                elif hasattr(cola, 'push'):
                    cola.push(s)
        except Exception as e:
            print(f"Aviso al actualizar cola en memoria: {e}")

        # 5. Registrar evento en el historial
        try:
            historial.insertar({
                "id": id,
                "accion": f"Prioridad modificada a {nueva_prioridad} (Impacto: {datos.impacto_academico}, Personas: {datos.personas_afectadas})",
                "fecha_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            })
            historial.guardar_en_json()
        except Exception:
            pass

        return {
            "mensaje": f"Prioridad de la solicitud #{id} actualizada correctamente",
            "actualizado": True,
            "nueva_prioridad": nueva_prioridad,
            "solicitud": solicitud
        }

    except Exception as e:
        return {
            "mensaje": f"Error interno en el servidor: {str(e)}",
            "actualizado": False
        }
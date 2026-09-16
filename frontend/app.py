import streamlit as st
import requests
import textwrap


# CONFIGURACIÓN DE LA PÁGINA

st.set_page_config(
    page_title="Nodex | Sistema de Mantenimiento",
    page_icon="⚡",
    layout="wide"
)

# Inicializar estado de navegación
if "opcion" not in st.session_state:
    st.session_state.opcion = "📝 Nueva solicitud"

# ESTILOS CSS 

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3.5rem;
        max-width: 1120px;
    }

    /* ENCABEZADO SOFISTICADO & LOGO */

    .brand-header {
        display: flex;
        align-items: center;
        gap: 16px;
        padding-bottom: 20px;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 28px;
    }

    .brand-icon {
        width: 52px;
        height: 52px;
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0px 6px 16px rgba(37, 99, 235, 0.18);
    }

    .brand-title-wrap {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand-title {
        font-size: 34px;
        font-weight: 800;
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.8px;
        margin: 0;
        line-height: 1;
    }

    .brand-badge {
        background-color: #eff6ff;
        color: #2563eb;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 20px;
        border: 1px solid #bfdbfe;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .brand-subtitle {
        font-size: 14px;
        color: #64748b;
        margin-top: 4px;
        font-weight: 500;
    }

    /*  TARJETAS DE MÉTRICAS (KPIs) */

    .tarjeta {
        background-color: #ffffff;
        padding: 20px 22px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0px 2px 8px rgba(15, 23, 42, 0.03);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .tarjeta:hover {
        transform: translateY(-3px);
        box-shadow: 0px 10px 20px rgba(15, 23, 42, 0.06);
        border-color: #cbd5e1;
    }

    .tarjeta-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }

    .tarjeta-titulo {
        font-size: 12px;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    .tarjeta-numero {
        font-size: 32px;
        font-weight: 800;
        color: #0f172a;
        line-height: 1;
    }

    /* ==============================
       BOTONES DE NAVEGACIÓN
    ============================== */
    .subheading-nav {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 12px;
    }

    div[data-testid="column"] button[kind="secondary"] {
        background-color: #ffffff !important;
        color: #475569 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 12px 0px !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="column"] button[kind="secondary"]:hover {
        color: #2563eb !important;
        border-color: #93c5fd !important;
        background-color: #f8fafc !important;
    }

    div[data-testid="column"] button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 12px 0px !important;
        box-shadow: 0px 4px 12px rgba(37, 99, 235, 0.2) !important;
    }

    /* FORMULARIO Y BOTÓN CON TEXTO EN NEGRITA */
    div[data-testid="stForm"] {
        background-color: #ffffff;
        padding: 32px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #60a5fa;
        box-shadow: 0px 6px 20px rgba(15, 23, 42, 0.03);
    }

    /* Etiquetas de los campos */
    div[data-testid="stForm"] label,
    div[data-testid="stForm"] label p,
    div[data-testid="stForm"] div[data-testid="stWidgetLabel"],
    div[data-testid="stForm"] div[data-testid="stWidgetLabel"] p,
    div[data-testid="stForm"] div[data-testid="stMarkdownContainer"] p {
        font-family: 'Outfit', sans-serif !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        color: #334155 !important;
        letter-spacing: -0.1px !important;
    }

    /* Inputs de texto y textareas */
    div[data-testid="stForm"] input, 
    div[data-testid="stForm"] textarea {
        font-family: 'Outfit', sans-serif !important;
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        color: #0f172a !important;
        font-size: 14.5px !important;
        padding: 10px 14px !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stForm"] input:focus, 
    div[data-testid="stForm"] textarea:focus {
        background-color: #ffffff !important;
        border-color: #93c5fd !important;
        box-shadow: 0 0 0 3px rgba(147, 197, 253, 0.2) !important;
    }

    /* Selectbox */
    div[data-testid="stForm"] div[data-baseweb="select"] *,
    div[data-testid="stForm"] div[data-baseweb="select"] > div {
        font-family: 'Outfit', sans-serif !important;
        font-size: 14.5px !important;
    }

    div[data-testid="stForm"] div[data-baseweb="select"] > div {
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        color: #0f172a !important;
    }

    /* Botón con azul suave y TEXTO EN NEGRITA */
    div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button {
        font-family: 'Outfit', sans-serif !important;
        background: linear-gradient(135deg, #93c5fd 0%, #60a5fa 100%) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 700 !important; /* Texto en negrita */
        border: none !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0px 4px 12px rgba(96, 165, 250, 0.2) !important;
        transition: all 0.25s ease !important;
        width: 100% !important;
        margin-top: 10px !important;
        cursor: pointer !important;
    }

    div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%) !important;
        box-shadow: 0px 6px 16px rgba(59, 130, 246, 0.25) !important;
        transform: translateY(-1px) !important;
    }
</style>
""", unsafe_allow_html=True)


# ENCABEZADO CON BRANDING

st.markdown("""
<div class="brand-header">
    <div class="brand-icon">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path>
        </svg>
    </div>
    <div>
        <div class="brand-title-wrap">
            <h1 class="brand-title">Nodex</h1>
            <span class="brand-badge">Sistema v1.0</span>
        </div>
        <div class="brand-subtitle">Sistema inteligente de priorización de solicitudes de mantenimiento</div>
    </div>
</div>
""", unsafe_allow_html=True)


# MÉTRICAS (METRIC CARDS)

# Consultar todas las solicitudes registradas
try:
    respuesta_metricas = requests.get(
        "http://127.0.0.1:8000/solicitudes/todas"
    )

    if respuesta_metricas.status_code == 200:

        datos_metricas = respuesta_metricas.json()
        solicitudes_metricas = datos_metricas.get("solicitudes", [])

        # Total de solicitudes
        total_solicitudes = len(solicitudes_metricas)

        # Contadores
        prioridad_alta = 0
        prioridad_media = 0
        en_proceso = 0

        # Recorrer todas las solicitudes
        for solicitud in solicitudes_metricas:

            prioridad = solicitud.get("prioridad")
            estado = solicitud.get("estado")

            # Contar prioridad alta
            if prioridad == "ALTA" or (
                isinstance(prioridad, int) and prioridad >= 8
            ):
                prioridad_alta += 1

            # Contar prioridad media
            elif prioridad == "MEDIA" or (
                isinstance(prioridad, int) and 5 <= prioridad <= 7
            ):
                prioridad_media += 1

            # Contar solicitudes en proceso
            if estado == "EN PROCESO":
                en_proceso += 1

    else:
        total_solicitudes = 0
        prioridad_alta = 0
        prioridad_media = 0
        en_proceso = 0

except requests.exceptions.ConnectionError:

    total_solicitudes = 0
    prioridad_alta = 0
    prioridad_media = 0
    en_proceso = 0


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="tarjeta" style="border-top: 3px solid #64748b;">
        <div class="tarjeta-header">
            <span class="tarjeta-titulo">Solicitudes</span>
            <span style="font-size: 16px;">📝</span>
        </div>
        <div class="tarjeta-numero">{total_solicitudes}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="tarjeta" style="border-top: 3px solid #f87171;">
        <div class="tarjeta-header">
            <span class="tarjeta-titulo" style="color: #dc2626;">Prioridad alta</span>
            <span style="font-size: 16px;">🔴</span>
        </div>
        <div class="tarjeta-numero" style="color: #dc2626;">{prioridad_alta}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="tarjeta" style="border-top: 3px solid #fbbf24;">
        <div class="tarjeta-header">
            <span class="tarjeta-titulo" style="color: #d97706;">Prioridad media</span>
            <span style="font-size: 16px;">🟠</span>
        </div>
        <div class="tarjeta-numero" style="color: #d97706;">{prioridad_media}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="tarjeta" style="border-top: 3px solid #60a5fa;">
        <div class="tarjeta-header">
            <span class="tarjeta-titulo" style="color: #2563eb;">En proceso</span>
            <span style="font-size: 16px;">🔧</span>
        </div>
        <div class="tarjeta-numero" style="color: #2563eb;">{en_proceso}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# NAVEGACIÓN DISTRIBUIDA (3 OPCIONES)
st.markdown('<div class="subheading-nav">¿Qué deseas hacer?</div>', unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    type_btn1 = "primary" if st.session_state.opcion == "📝 Nueva solicitud" else "secondary"
    if st.button("📝 Nueva solicitud", use_container_width=True, type=type_btn1):
        st.session_state.opcion = "📝 Nueva solicitud"
        st.rerun()

with nav_col2:
    type_btn2 = "primary" if st.session_state.opcion == "📋 Solicitudes" else "secondary"
    if st.button("📋 Solicitudes", use_container_width=True, type=type_btn2):
        st.session_state.opcion = "📋 Solicitudes"
        st.rerun()

with nav_col3:
    type_btn3 = "primary" if st.session_state.opcion == "🔍 Buscar por ID" else "secondary"
    if st.button("🔍 Buscar por ID", use_container_width=True, type=type_btn3):
        st.session_state.opcion = "🔍 Buscar por ID"
        st.rerun()

st.write("")

# SECCIONES DE LA NAVEGACIÓN

opcion = st.session_state.opcion

if opcion == "📝 Nueva solicitud":
    st.subheader("Registrar Nueva Solicitud de Mantenimiento")
    st.caption("Diligencie los datos del problema. El sistema asignará un ID automático.")
    st.write("")

    # Inicializar la lista de IDs creados en la sesión del usuario
    if "mis_solicitudes_ids" not in st.session_state:
        st.session_state.mis_solicitudes_ids = []

    opciones_impacto = {
        "1 - No afecta directamente las actividades academicas": 1,
        "2 - Afecta poco la actividad academica": 2,
        "3 - Afecta parcialmente la actividad academica": 3,
        "4 - Afecta considerablemente la actividad academica": 4,
        "5 - Impide realizar la actividad academica": 5
    }

    opciones_personas = {
        "1 persona": 1,
        "2-4 personas": 2,
        "5-10 personas": 3,
        "11-20 personas": 4,
        "Más de 20 personas": 5
    }

    with st.form("form_nueva_solicitud", clear_on_submit=True):
        recurso = st.text_input("Recurso o Equipo", placeholder="Ej: Video Beam")
        ubicacion = st.text_input("Ubicación", placeholder="Ej: Casa Obando, Piso 3")
        descripcion = st.text_area("Descripción del problema", placeholder="Describa brevemente la falla...")
        
        col_imp, col_per = st.columns(2)
        with col_imp:
            impacto_texto = st.selectbox(
                "Impacto Académico",
                options=list(opciones_impacto.keys())
            )
        with col_per:
            personas_texto = st.selectbox(
                "Personas Afectadas",
                options=list(opciones_personas.keys())
            )

        boton_enviar = st.form_submit_button("🚀 Registrar Solicitud", use_container_width=True)

    # Procesamiento tras presionar el botón de envío
    if boton_enviar:
        if not recurso.strip() or not ubicacion.strip() or not descripcion.strip():
            st.warning("Por favor complete todos los campos obligatorios.")
        else:
            try:
                impacto_val = opciones_impacto[impacto_texto]
                personas_val = opciones_personas[personas_texto]

                payload = {
                    "recurso": recurso.strip(),
                    "ubicacion": ubicacion.strip(),
                    "descripcion": descripcion.strip(),
                    "impacto_academico": impacto_val,
                    "personas_afectadas": personas_val
                }

                respuesta = requests.post(
                    "http://127.0.0.1:8000/solicitudes",
                    json=payload
                )

                if respuesta.status_code in [200, 201]:
                    res_json = respuesta.json()
                    
                    # Extraer el ID (soporta si viene en {"solicitud": {"id": ...}} o en {"id": ...})
                    datos = res_json.get("solicitud", res_json)
                    id_creado = datos.get("id")

                    if id_creado is not None:
                        id_int = int(id_creado)
                        if id_int not in st.session_state.mis_solicitudes_ids:
                            st.session_state.mis_solicitudes_ids.append(id_int)

                        st.success(f"¡Solicitud #{id_creado} creada e ingresada a la cola exitosamente!")
                        st.toast(f"Solicitud #{id_creado} registrada", icon="✅")
                        st.rerun()
                    else:
                        st.warning("La solicitud fue creada pero no se pudo leer el ID devuelto.")
                else:
                    st.error(f"Error al crear la solicitud: {respuesta.text}")

            except requests.exceptions.ConnectionError:
                st.error("No se pudo conectar con el servidor Nodex. Verifica que FastAPI esté ejecutándose.")


    # SECCIÓN: LISTA DE MIS SOLICITUDES Y OPCIÓN DE CANCELAR

    st.markdown("---")
    st.subheader("📌 Mis Solicitudes Registradas")

    try:
        # Consultar TODAS las solicitudes guardadas en el JSON
        res = requests.get(
            "http://127.0.0.1:8000/solicitudes/todas"
        )

        if res.status_code == 200:
            data_backend = res.json()
            todas_solicitudes = data_backend.get("solicitudes", [])

            # Recuperar los IDs que existen actualmente en solicitudes.json
            # Esto permite que las solicitudes sigan apareciendo
            # aunque se reinicie Streamlit.
            ids_guardados = [
                int(s.get("id"))
                for s in todas_solicitudes
                if s.get("id") is not None
            ]

            # Actualizar la lista de IDs de la sesión
            st.session_state.mis_solicitudes_ids = ids_guardados

            # Si no existen solicitudes guardadas
            if not ids_guardados:
                st.info("Aún no has registrado solicitudes.")
            else:

                # Mostrar las solicitudes guardadas
                for sol in sorted(
                    todas_solicitudes,
                    key=lambda x: int(x.get("id", 0)),
                    reverse=True
                ):

                    sol_id = int(sol.get("id"))
                    estado = sol.get("estado", "PENDIENTE")
                    recurso_nom = sol.get("recurso", "N/A")
                    ubicacion_nom = sol.get("ubicacion", "N/A")
                    prioridad_val = sol.get("prioridad", "N/A")

                    with st.expander(
                        f"Solicitud #{sol_id} - {recurso_nom} ({estado})",
                        expanded=(estado == "PENDIENTE")
                    ):

                        col_info, col_accion = st.columns([3, 1])

                        with col_info:
                            st.write(f"**Ubicación:** {ubicacion_nom}")
                            st.write(
                                f"**Descripción:** {sol.get('descripcion', '')}"
                            )
                            st.write(
                                f"**Prioridad calculada:** {prioridad_val}"
                            )
                            st.write(
                                f"**Estado actual:** `{estado}`"
                            )

                        with col_accion:

                            # Solo se puede cancelar mientras esté PENDIENTE
                            if estado == "PENDIENTE":

                                if st.button(
                                    "🗑️ Cancelar",
                                    key=f"btn_del_{sol_id}",
                                    use_container_width=True
                                ):

                                    # Llamada al backend para eliminar
                                    res_del = requests.delete(
                                        f"http://127.0.0.1:8000/solicitudes/{sol_id}"
                                    )

                                    if (
                                        res_del.status_code == 200
                                        and res_del.json().get("eliminado")
                                    ):

                                        # Eliminar también el ID de la sesión
                                        st.session_state.mis_solicitudes_ids = [
                                            x
                                            for x in st.session_state.mis_solicitudes_ids
                                            if int(x) != sol_id
                                        ]

                                        st.success(
                                            f"Solicitud #{sol_id} cancelada y eliminada."
                                        )

                                        st.rerun()

                                    else:
                                        msg = res_del.json().get(
                                            "mensaje",
                                            "No se pudo eliminar la solicitud."
                                        )
                                        st.error(msg)

                            else:
                                st.caption(
                                    "🔒 *En atención o finalizada "
                                    "(No se puede cancelar)*"
                                )

    except requests.exceptions.ConnectionError:
        st.warning(
            "No se pudo conectar con el servidor para consultar "
            "el estado de tus solicitudes."
        )


elif opcion == "📋 Solicitudes":
    st.subheader("Solicitudes de mantenimiento")
    st.caption("Consulta las solicitudes registradas y gestiona su atención.")
    st.write("")

    # Mapeo de opciones para la actualización manual de prioridad
    opciones_impacto = {
        "1 - No afecta directamente las actividades académicas": 1,
        "2 - Afecta poco la actividad académica": 2,
        "3 - Afecta parcialmente la actividad académica": 3,
        "4 - Afecta considerablemente la actividad académica": 4,
        "5 - Impide realizar la actividad académica": 5
    }

    opciones_personas = {
        "1 persona": 1,
        "2-4 personas": 2,
        "5-10 personas": 3,
        "11-20 personas": 4,
        "Más de 20 personas": 5
    }

    try:
        # Traemos la cola de pendientes Y todas las solicitudes para detectar la que está EN PROCESO
        res_cola = requests.get("http://127.0.0.1:8000/solicitudes/cola")
        res_todas = requests.get("http://127.0.0.1:8000/solicitudes/todas")

        if res_cola.status_code == 200 and res_todas.status_code == 200:
            solicitudes_pendientes = res_cola.json().get("cola", [])
            todas = res_todas.json().get("solicitudes", [])

            # Filtrar si hay alguna solicitud actualmente EN PROCESO
            en_proceso = [s for s in todas if s.get("estado") == "EN PROCESO"]

            # SECCIÓN 1: SOLICITUD EN ATENCIÓN ACTUAL (EN PROCESO)

            if en_proceso:
                st.markdown("### 🛠️ En Atención Actual")
                
                for sol_activa in en_proceso:
                    id_activa = sol_activa.get("id")
                    
                    html_en_proceso = f"""
                    <div style="
                        font-family: 'Plus Jakarta Sans', sans-serif;
                        background-color: #f0f9ff;
                        border: 2px solid #0284c7;
                        border-radius: 12px;
                        padding: 16px 20px;
                        margin-bottom: 12px;
                        box-shadow: 0px 4px 10px rgba(2, 132, 199, 0.1);
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <div>
                                <span style="background: #bae6fd; color: #0369a1; font-size: 11px; font-weight: 800; padding: 2px 8px; border-radius: 4px;">ID #{id_activa}</span>
                                <strong style="font-size: 17px; color: #0369a1; margin-left: 6px;">{sol_activa.get('recurso', '')}</strong>
                            </div>
                            <span style="background: #e0f2fe; color: #0284c7; border: 1px solid #7dd3fc; padding: 3px 10px; border-radius: 12px; font-size: 11.5px; font-weight: 700;">
                                ⚙️ EN PROCESO
                            </span>
                        </div>
                        <div style="color: #64748b; font-size: 12.5px; margin-bottom: 8px;">📍 {sol_activa.get('ubicacion', '')}</div>
                        <div style="background: #ffffff; padding: 10px 14px; border-radius: 8px; border: 1px solid #bae6fd; color: #0f172a; font-size: 14px;">
                            <strong>Descripción:</strong> {sol_activa.get('descripcion', '')}
                        </div>
                    </div>
                    """
                    col_card, col_btn = st.columns([4, 1])
                    
                    with col_card:
                        st.html(html_en_proceso)
                        
                    with col_btn:
                        st.write("")
                        st.write("")
                        if st.button("✅ Finalizar", key=f"btn_fin_{id_activa}", type="primary", use_container_width=True):
                            res_fin = requests.put(
                                f"http://127.0.0.1:8000/solicitudes/{id_activa}/estado",
                                json={"estado": "SOLUCIONADO"}
                            )
                            if res_fin.status_code == 200:
                                st.toast(f"¡Solicitud #{id_activa} solucionada!", icon="🎉")
                                st.rerun()
                            else:
                                st.error("No se pudo finalizar la solicitud.")

                st.divider()

            # SECCIÓN 2: COLA DE ESPERA (PENDIENTES)

            st.markdown(f"### ⏳ Cola de Espera ({len(solicitudes_pendientes)})")

            if len(solicitudes_pendientes) == 0:
                st.info("No hay solicitudes pendientes en la cola.")
            else:
                hay_en_proceso = len(en_proceso) > 0

                for idx, solicitud in enumerate(solicitudes_pendientes):
                    solicitud_id = solicitud.get("id")
                    prioridad = solicitud.get("prioridad", "BAJA")
                    imp_val = solicitud.get("impacto_academico", 1)
                    per_val = solicitud.get("personas_afectadas", 1)

                    if prioridad == "ALTA" or (isinstance(prioridad, (int, float)) and prioridad >= 8):
                        color, fondo, borde, icono = "#dc2626", "#fef2f2", "#fecaca", "🔴"
                        prio_texto = f"ALTA" if isinstance(prioridad, int) else prioridad
                    elif prioridad == "MEDIA" or (isinstance(prioridad, (int, float)) and 4 <= prioridad < 8):
                        color, fondo, borde, icono = "#d97706", "#fffbeb", "#fde68a", "🟠"
                        prio_texto = f"MEDIA" if isinstance(prioridad, int) else prioridad
                    else:
                        color, fondo, borde, icono = "#16a34a", "#f0fdf4", "#bbf7d0", "🟢"
                        prio_texto = f"BAJA" if isinstance(prioridad, int) else prioridad

                    html_tarjeta = f"""
                    <div style="
                        font-family: 'Plus Jakarta Sans', sans-serif;
                        background-color: #ffffff;
                        border: 1px solid #e2e8f0;
                        border-left: 5px solid {color};
                        border-radius: 12px;
                        padding: 14px 18px;
                        margin-bottom: 12px;
                        box-shadow: 0px 2px 6px rgba(15, 23, 42, 0.04);
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                            <div>
                                <span style="background: #f1f5f9; color: #334155; font-size: 11px; font-weight: 800; padding: 2px 6px; border-radius: 4px;">ID #{solicitud_id}</span>
                                <strong style="font-size: 17px; color: #0f172a; margin-left: 6px;">{solicitud.get('recurso', '')}</strong>
                                <div style="color: #64748b; font-size: 12.5px; margin-top: 3px;">📍 {solicitud.get('ubicacion', '')}</div>
                            </div>
                            <span style="background-color: {fondo}; color: {color}; border: 1px solid {borde}; padding: 3px 10px; border-radius: 12px; font-size: 11.5px; font-weight: 700;">
                                {icono} {prio_texto}
                            </span>
                        </div>
                        <div style="background-color: #f8fafc; border-left: 3px solid #cbd5e1; border-radius: 0px 8px 8px 0px; padding: 10px 14px; margin-bottom: 10px;">
                            <strong style="color: #64748b; font-size: 13px; text-transform: uppercase;">Descripción:</strong>
                            <span style="color: #0f172a; font-weight: 600; font-size: 14px; margin-left: 4px;">{solicitud.get('descripcion', '')}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-size: 12px; color: #475569; background-color: #f1f5f9; padding: 3px 8px; border-radius: 6px;">
                                📊 <b>Impacto:</b> {imp_val}/5 | 👥 <b>Personas:</b> {per_val}/5
                            </div>
                            <div style="font-size: 11px; font-weight: 700; color: #2563eb; background-color: #eff6ff; border: 1px solid #bfdbfe; padding: 3px 10px; border-radius: 6px;">
                                ● ESTADO: {solicitud.get('estado', 'PENDIENTE')}
                            </div>
                        </div>
                    </div>
                    """
                    col_tarjeta, col_boton = st.columns([4, 1])

                    with col_tarjeta:
                        st.html(html_tarjeta)

                    with col_boton:
                        st.write("")
                        st.write("")
                        
                        # Botón para Atender (Deshabilitado si ya hay uno en proceso o no es el primero)
                        deshabilitado = hay_en_proceso or (idx != 0)
                        if st.button("▶️ Atender", key=f"btn_atender_{solicitud_id}", disabled=deshabilitado, use_container_width=True):
                            res_atender = requests.put(
                                f"http://127.0.0.1:8000/solicitudes/{solicitud_id}/estado",
                                json={"estado": "EN PROCESO"}
                            )
                            if res_atender.status_code == 200:
                                st.toast(f"Atendiendo solicitud #{solicitud_id}", icon="🚀")
                                st.rerun()

                        # Botón/Popover para Modificar Prioridad
                        with st.popover("⚡ Prioridad", use_container_width=True):
                            st.caption(f"**Modificar Prioridad Excepcional (ID #{solicitud_id})**")
                            
                            idx_imp = max(0, min(imp_val - 1, 4))
                            idx_per = max(0, min(per_val - 1, 4))

                            nuevo_imp_text = st.selectbox(
                                "Impacto Académico",
                                options=list(opciones_impacto.keys()),
                                index=idx_imp,
                                key=f"pop_imp_{solicitud_id}"
                            )

                            nuevo_per_text = st.selectbox(
                                "Personas Afectadas",
                                options=list(opciones_personas.keys()),
                                index=idx_per,
                                key=f"pop_per_{solicitud_id}"
                            )

                            if st.button("Guardar Cambios", key=f"pop_save_{solicitud_id}", type="primary", use_container_width=True):
                                payload_prio = {
                                    "impacto_academico": opciones_impacto[nuevo_imp_text],
                                    "personas_afectadas": opciones_personas[nuevo_per_text]
                                }
                                res_prio = requests.put(
                                    f"http://127.0.0.1:8000/solicitudes/{solicitud_id}/prioridad",
                                    json=payload_prio
                                )
                                if res_prio.status_code == 200 and res_prio.json().get("actualizado"):
                                    st.toast(f"Prioridad de Solicitud #{solicitud_id} actualizada", icon="⚡")
                                    st.rerun()
                                else:
                                    msg = res_prio.json().get("mensaje", "Error al actualizar")
                                    st.error(msg)

        else:
            st.error("No se pudieron consultar las solicitudes.")

    except requests.exceptions.ConnectionError:
        st.error("No se pudo conectar con el servidor Nodex FastAPI.")



# OPCIÓN 4: SOLICITUDES POR ID

elif opcion == "🔍 Buscar por ID":
    st.subheader("Solicitudes Registradas")
    st.caption("Visualiza todas las solicitudes registradas y consulta el historial detallado de cambios mediante su ID.")
    st.write("")

    try:
        # Cargar la lista completa desde el archivo datos/solicitudes.json
        respuesta = requests.get("http://127.0.0.1:8000/solicitudes/todas")

        if respuesta.status_code == 200:
            datos = respuesta.json()
            solicitudes_totales = datos.get("solicitudes", [])

            if not solicitudes_totales:
                st.info("No hay solicitudes registradas actualmente en `datos/solicitudes.json`.")
            else:
                # BARRA DE BÚSQUEDA Y FILTRADO POR ID

                col_search, col_info = st.columns([3, 1])
                with col_search:
                    busqueda_id = st.text_input(
                        "🔍 Buscar por ID", 
                        placeholder="Ingresa el ID de la solicitud (ej: 2, 4, 5)...",
                        label_visibility="collapsed"
                    )
                with col_info:
                    st.markdown(f"<div style='padding-top: 8px; font-weight: 600; color: #64748b; font-size: 14px;'>Total: {len(solicitudes_totales)} solicitudes</div>", unsafe_allow_html=True)

                st.write("")

                # Filtrar si el usuario escribió un ID
                busqueda_limpia = busqueda_id.strip()

                if busqueda_limpia:
                    solicitudes_filtradas = [
                        s for s in solicitudes_totales 
                        if str(s.get("id", "")) == busqueda_limpia or busqueda_limpia in str(s.get("recurso", "")).lower()
                    ]
                else:
                    solicitudes_filtradas = solicitudes_totales

                if busqueda_limpia and not solicitudes_filtradas:
                    st.warning(f"No se encontró ninguna solicitud con el ID o criterio: '{busqueda_id}'.")
                else:
                    if busqueda_limpia:
                        st.caption(f"Mostrando resultados para el ID: **'{busqueda_id}'**")

                    # LISTADO DE TARJETAS DE SOLICITUDES

                    for solicitud in solicitudes_filtradas:
                        prioridad = solicitud.get("prioridad", "BAJA")
                        solicitud_id = solicitud.get("id", "N/A")

                        if prioridad == "ALTA":
                            color = "#dc2626"
                            fondo = "#fef2f2"
                            borde = "#fecaca"
                            icono = "🔴"
                        elif prioridad == "MEDIA":
                            color = "#d97706"
                            fondo = "#fffbeb"
                            borde = "#fde68a"
                            icono = "🟠"
                        else:
                            color = "#16a34a"
                            fondo = "#f0fdf4"
                            borde = "#bbf7d0"
                            icono = "🟢"

                        # Renderizado HTML de la tarjeta principal
                        html_tarjeta = f"""
                        <div style="
                            font-family: 'Plus Jakarta Sans', sans-serif;
                            background-color: #ffffff;
                            border: 1px solid #e2e8f0;
                            border-left: 5px solid {color};
                            border-radius: 12px;
                            padding: 16px 20px;
                            margin-bottom: 8px;
                            box-shadow: 0px 2px 6px rgba(15, 23, 42, 0.04);
                        ">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                                <div>
                                    <div style="display: flex; align-items: center; gap: 8px;">
                                        <span style="
                                            background-color: #f1f5f9;
                                            color: #334155;
                                            font-size: 12px;
                                            font-weight: 800;
                                            padding: 2px 8px;
                                            border-radius: 6px;
                                            border: 1px solid #cbd5e1;
                                        ">ID #{solicitud_id}</span>
                                        <span style="font-size: 18px; font-weight: 800; color: #0f172a;">
                                            {solicitud.get('recurso', 'N/A')}
                                        </span>
                                    </div>
                                    <div style="color: #64748b; font-size: 13px; margin-top: 4px; font-weight: 500;">
                                        📍 Ubicación: {solicitud.get('ubicacion', 'N/A')}
                                    </div>
                                </div>
                                <span style="
                                    background-color: {fondo};
                                    color: {color};
                                    border: 1px solid {borde};
                                    padding: 4px 12px;
                                    border-radius: 12px;
                                    font-size: 12px;
                                    font-weight: 700;
                                    white-space: nowrap;
                                ">
                                    {icono} {prioridad}
                                </span>
                            </div>

                            <div style="
                                background-color: #f8fafc;
                                border-left: 3px solid #cbd5e1;
                                border-radius: 0px 8px 8px 0px;
                                padding: 12px 16px;
                                margin-bottom: 12px;
                            ">
                                <div style="color: #0f172a; font-size: 14px; font-weight: 600;">
                                    <strong style="color: #64748b; font-size: 12px; text-transform: uppercase;">Descripción:</strong><br>
                                    {solicitud.get('descripcion', 'Sin descripción')}
                                </div>
                            </div>

                            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #64748b;">
                                <div>
                                    📊 Impacto: <strong>{solicitud.get('impacto_academico', 'N/A')}/5</strong> | 
                                    👥 Afectados: <strong>{solicitud.get('personas_afectadas', 'N/A')}/5</strong>
                                </div>
                                <div style="
                                    font-size: 11px;
                                    font-weight: 700;
                                    color: #2563eb;
                                    background-color: #eff6ff;
                                    border: 1px solid #bfdbfe;
                                    padding: 3px 10px;
                                    border-radius: 6px;
                                    text-transform: uppercase;
                                ">
                                    ● ESTADO: {solicitud.get('estado', 'PENDIENTE')}
                                </div>
                            </div>
                        </div>
                        """
                        st.html(html_tarjeta)

                        # Botón desplegable para consultar el endpoint GET /solicitudes/{id}/historial
                        with st.expander(f"📜 Ver Historial de la Solicitud #{solicitud_id}"):
                            try:
                                res_historial = requests.get(f"http://127.0.0.1:8000/solicitudes/{solicitud_id}/historial")
                                
                                if res_historial.status_code == 200:
                                    datos_h = res_historial.json()
                                    historial_lista = datos_h.get("historial", [])

                                    if not historial_lista:
                                        st.caption("No hay eventos registrados en el historial para esta solicitud.")
                                    else:
                                        for h in historial_lista:
                                            accion = h.get("accion", "")
                                            fecha = h.get("fecha_hora", "N/A")
                                            
                                            if accion == "Solicitud creada":
                                                st.markdown(f"✨ **{accion}** — Estado inicial: `{h.get('estado_inicial', 'PENDIENTE')}` *({fecha})*")
                                            else:
                                                st.markdown(f"🔄 **{accion}** — De `{h.get('estado_anterior', '')}` ➔ `{h.get('estado_nuevo', '')}` *({fecha})*")
                                else:
                                    st.error("No se pudo obtener el historial de esta solicitud.")
                            except requests.exceptions.ConnectionError:
                                st.error("Error al conectar con el endpoint de historial.")
                        st.write("")

        else:
            st.error("No se pudieron cargar las solicitudes desde el servidor.")

    except requests.exceptions.ConnectionError:
        st.error("No se pudo conectar con Nodex. Verifica que el servidor FastAPI esté ejecutándose.")




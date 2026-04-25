import streamlit as st
from fpdf import FPDF
from datetime import datetime
import json
import os

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="SVI - ACTA 10 BIS", page_icon="👮", layout="wide")

# --- PERSISTENCIA DE DATOS ---
DB_FILE = "historial_svi_final.json"

def cargar_historial():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return []
    return []

def guardar_historial(historial):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=4)

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("### 🛠️ Desarrollo")
    st.info("**Creado por:** \n\nSubComisario Castañeda Juan")
    st.write("Sistemas de Automatización Policial")
    st.divider()
    if st.button("🗑️ Vaciar Historial"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.session_state.historial = []
        st.rerun()

# --- MAPA INSPECCIÓN 8va ---
MAPA_JURISDICCION = {
    "Pérez": {"tipo": "Ciudad", "depto": "Rosario"},
    "Funes": {"tipo": "Ciudad", "depto": "Rosario"},
    "Soldini": {"tipo": "Localidad", "depto": "Rosario"},
    "Zavalla": {"tipo": "Localidad", "depto": "Rosario"},
    "Rosario": {"tipo": "Ciudad", "depto": "Rosario"}
}

# --- INICIALIZACIÓN ---
campos_base = {
    'unidad': "G.T.M.", 'tercio': "TERCIO ALPHA", 'movil': "12.116", 'jurisdiccion': "Pérez",
    'lugar': "", 'hora_demora': datetime.now().strftime('%H:%M'), 'acta_nro': "",
    'apellido': "", 'nombre': "", 'dni': "", 'nacionalidad': "ARGENTINA",
    'est_civil': "SOLTERO/A", 'edad': "", 'nacimiento': "", 'domicilio': "", 'padres': "",
    'actuante_ap': "", 'actuante_nom': "", 'refuerzo_ap': "", 'refuerzo_nom': "",
    'testigo_datos': "", 'requisa': "PALPADO PREVENTIVO SOBRE SUS PRENDAS NO HALLANDO ELEMENTOS DE PELIGROSIDAD", 
    'secuestro': "PERTENENCIAS PERSONALES", 'estado_fisico': "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
    'motivo_unico': "EL INDIVIDUO CAMBIA BRUSCAMENTE SU SENTIDO DE MARCHA AL NOTAR LA PRESENCIA POLICIAL E INTENTA EVITAR CONTACTO, Y AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO.",
    'of_recibe': "SUBOFICIAL RODRIGUEZ (M)"
}

for k, v in campos_base.items():
    if k not in st.session_state: st.session_state[k] = v

if 'historial' not in st.session_state:
    st.session_state.historial = cargar_historial()

# --- INTERFAZ ---
st.title("👮 ACTA DE DEMORA ART 10 BIS LEY 7.395")
st.markdown("🚀 **Sistema SVI** | Versión Profesional")

tabs = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Testigo/Requisa", "✍️ Cierre y WhatsApp", "🗂️ Historial"])

with tabs[0]:
    c1, c2 = st.columns(2)
    u_opciones = ["G.T.M.", "C.R.E. ROSARIO", "B.O.U.", "P.A.T.", "OTRO"]
    u_sel = c1.selectbox("Unidad", u_opciones, index=u_opciones.index(st.session_state.unidad) if st.session_state.unidad in u_opciones else 0)
    st.session_state.unidad = c1.text_input("Especifique Unidad", value=st.session_state.unidad) if u_sel == "OTRO" else u_sel
    st.session_state.tercio = c2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    st.session_state.movil = st.text_input("Móvil / Legajo", value=st.session_state.movil)
    lista_8va = list(MAPA_JURISDICCION.keys())
    st.session_state.jurisdiccion = st.selectbox("Jurisdicción:", lista_8va, index=lista_8va.index(st.session_state.jurisdiccion) if st.session_state.jurisdiccion in lista_8va else 0)
    st.session_state.lugar = st.text_input("Lugar del procedimiento:", value=st.session_state.lugar).upper()
    st.session_state.hora_demora = st.text_input("Hora de inicio:", value=st.session_state.hora_demora)
    st.session_state.acta_nro = st.text_input("Acta Nº:", value=st.session_state.acta_nro)

with tabs[1]:
    ca, cb = st.columns(2)
    st.session_state.apellido = ca.text_input("Apellido/s:", value=st.session_state.apellido).upper()
    st.session_state.nombre = cb.text_input("Nombre/s:", value=st.session_state.nombre).upper()
    st.session_state.dni = st.text_input("DNI:", value=st.session_state.dni)
    st.session_state.nacionalidad = st.text_input("Nacionalidad:", value=st.session_state.nacionalidad).upper()
    st.session_state.est_civil = st.selectbox("Estado Civil:", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "CONCUBINATO"])
    st.session_state.edad = st.text_input("Edad:", value=st.session_state.edad)
    st.session_state.nacimiento = st.text_input("Fecha de Nacimiento:", value=st.session_state.nacimiento)
    st.session_state.domicilio = st.text_input("Domicilio Real:", value=st.session_state.domicilio).upper()
    st.session_state.padres = st.text_input("Filiación (Hijo de):", value=st.session_state.padres).upper()

with tabs[2]:
    st.session_state.actuante_ap = st.text_input("Ap. Actuante:", value=st.session_state.actuante_ap).upper()
    st.session_state.actuante_nom = st.text_input("Nom. Actuante:", value=st.session_state.actuante_nom).upper()
    st.session_state.refuerzo_ap = st.text_input("Ap. Refuerzo:", value=st.session_state.refuerzo_ap).upper()
    st.session_state.refuerzo_nom = st.text_input("Nom. Refuerzo:", value=st.session_state.refuerzo_nom).upper()
    st.session_state.testigo_datos = st.text_area("Datos de Testigos:", value=st.session_state.testigo_datos).upper()
    st.session_state.requisa = st.text_area("Resultado de Requisa:", value=st.session_state.requisa).upper()
    st.session_state.secuestro = st.text_area("Elementos Secuestrados:", value=st.session_state.secuestro).upper()

with tabs[3]:
    st.session_state.estado_fisico = st.selectbox("Estado físico:", [
        "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
        "presenta lesiones de vieja data y no requirieron atención médica",
        "presenta lesiones que motivaron su traslado previo a un centro de salud"
    ])
    st.session_state.motivo_unico = st.text_area("Motivo observado:", value=st.session_state.motivo_unico).upper()
    st.session_state.of_recibe = st.text_input("Oficial de Guardia:", value=st.session_state.of_recibe).upper()

    # --- ACCIONES ---
    c_pdf, c_save = st.columns(2)
    with c_save:
        if st.button("💾 GUARDAR EN HISTORIAL PERMANENTE", use_container_width=True):
            reg = {clave: st.session_state[clave] for clave in campos_base.keys()}
            reg['fecha_registro'] = datetime.now().strftime('%d/%m %H:%M')
            st.session_state.historial.append(reg)
            guardar_historial(st.session_state.historial)
            st.success("Guardado en disco.")

    # --- PARTE DE WHATSAPP COMPLETO ---
    st.divider()
    st.subheader("📲 Parte para WhatsApp")
    
    parte_completo = f"""*🚔 {st.session_state.unidad}* | *ACTA 10 BIS*
*HORA:* {st.session_state.hora_demora} hs.
*JURISDICCIÓN:* {st.session_state.jurisdiccion.upper()}
*LUGAR:* {st.session_state.lugar}

*👤 DEMORADO:*
*IDENTIDAD:* **{st.session_state.apellido} {st.session_state.nombre}**
*DNI:* **{st.session_state.dni}**
*NACIONALIDAD:* {st.session_state.nacionalidad}
*EDAD:* {st.session_state.edad} AÑOS
*HIJO DE:* {st.session_state.padres}
*DOMICILIO:* {st.session_state.domicilio}

*📝 PROCEDIMIENTO:*
*MOTIVO:* {st.session_state.motivo_unico}
*REQUISA:* {st.session_state.requisa}
*SECUESTRO:* **{st.session_state.secuestro}**
*ESTADO:* {st.session_state.estado_fisico.upper()}
*RECIBE:* **{st.session_state.of_recibe}**
*ACTA N°:* {st.session_state.acta_nro}

👮 *PERSONAL:* {st.session_state.actuante_ap} / {st.session_state.refuerzo_ap}"""
    
    st.code(parte_completo)

with tabs[4]:
    st.subheader("🗂️ Historial del Dispositivo")
    h_disco = cargar_historial()
    if not h_disco:
        st.info("Vacío.")
    else:
        for i, r in enumerate(reversed(h_disco)):
            with st.expander(f"📌 {r['apellido']} - {r['fecha_registro']}"):
                if st.button("Reactivar Datos", key=f"recu_{i}"):
                    for k in campos_base.keys(): st.session_state[k] = r[k]
                    st.rerun()

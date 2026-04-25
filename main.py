import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="SVI - ACTA 10 BIS", page_icon="👮", layout="wide")

# --- BARRA LATERAL (AUTORÍA) ---
with st.sidebar:
    st.markdown("### 🛠️ Desarrollo")
    st.info("**Creado por:** \n\nSubComisario Castañeda Juan")
    st.write("Sistemas de Automatización Policial")
    st.divider()
    st.caption("Versión Estable 2026.04")
    st.caption("Rosario, Santa Fe")

# --- DATA DE LA INSPECCIÓN 8va ---
MAPA_JURISDICCION = {
    "Pérez": {"tipo": "Ciudad", "depto": "Rosario"},
    "Funes": {"tipo": "Ciudad", "depto": "Rosario"},
    "Soldini": {"tipo": "Localidad", "depto": "Rosario"},
    "Zavalla": {"tipo": "Localidad", "depto": "Rosario"},
    "Rosario": {"tipo": "Ciudad", "depto": "Rosario"}
}

# --- INICIALIZACIÓN DE MEMORIA ---
campos_base = {
    'unidad': "G.T.M.", 'tercio': "TERCIO ALPHA", 'movil': "12.116", 'jurisdiccion': "Pérez",
    'lugar': "", 'hora_demora': datetime.now().strftime('%H:%M'), 'acta_nro': "",
    'apellido': "", 'nombre': "", 'dni': "", 'nacionalidad': "ARGENTINA",
    'est_civil': "SOLTERO/A", 'edad': "", 'nacimiento': "", 'domicilio': "", 'padres': "",
    'actuante_ap': "", 'actuante_nom': "", 'refuerzo_ap': "", 'refuerzo_nom': "",
    'testigo_datos': "", 'requisa': "palpado preventivo sobre sus prendas no hallando elementos de peligrosidad", 
    'secuestro': "pertenencias personales", 'estado_fisico': "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
    'motivo_unico': "", 'of_recibe': "SUBOFICIAL RODRIGUEZ (M)"
}

for clave, valor in campos_base.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor

if 'historial' not in st.session_state:
    st.session_state.historial = []

# --- INTERFAZ DE USUARIO ---
st.title("👮 ACTA DE DEMORA ART 10 BIS LEY 7.395")
st.markdown(f"🚀 **Sistema SVI** | Creado por: **SubComisario Castañeda Juan**")
st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Testigo/Requisa", "✍️ Cierre y WhatsApp", "🗂️ Historial"])

with tab1:
    c1, c2 = st.columns(2)
    u_opciones = ["G.T.M.", "C.R.E. ROSARIO", "B.O.U.", "P.A.T.", "OTRO"]
    u_sel = c1.selectbox("Unidad", u_opciones, index=u_opciones.index(st.session_state.unidad) if st.session_state.unidad in u_opciones else 0)
    st.session_state.unidad = c1.text_input("Especifique Unidad", value=st.session_state.unidad) if u_sel == "OTRO" else u_sel
    st.session_state.tercio = c2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    st.session_state.movil = st.text_input("Móvil / Legajo", value=st.session_state.movil)
    
    lista_8va = list(MAPA_JURISDICCION.keys())
    st.session_state.jurisdiccion = st.selectbox(
        "Jurisdicción de entrega (Inspección 8va):", 
        lista_8va, 
        index=lista_8va.index(st.session_state.jurisdiccion) if st.session_state.jurisdiccion in lista_8va else 0
    )
    st.session_state.lugar = st.text_input("Lugar del procedimiento", value=st.session_state.lugar)
    st.session_state.hora_demora = st.text_input("Hora de inicio", value=st.session_state.hora_demora)
    st.session_state.acta_nro = st.text_input("Acta Nº", value=st.session_state.acta_nro)

with tab2:
    ca, cb = st.columns(2)
    st.session_state.apellido = ca.text_input("Apellido/s", value=st.session_state.apellido)
    st.session_state.nombre = cb.text_input("Nombre/s", value=st.session_state.nombre)
    st.session_state.dni = st.text_input("DNI", value=st.session_state.dni)
    st.session_state.nacionalidad = st.text_input("Nacionalidad", value=st.session_state.nacionalidad)
    st.session_state.est_civil = st.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "CONCUBINATO"])
    st.session_state.edad = st.text_input("Edad", value=st.session_state.edad)
    st.session_state.nacimiento = st.text_input("Fecha de Nacimiento", value=st.session_state.nacimiento)
    st.session_state.domicilio = st.text_input("Domicilio Real", value=st.session_state.domicilio)
    st.session_state.padres = st.text_input("Hijo de (Filiación)", value=st.session_state.padres)

with tab3:
    st.session_state.actuante_ap = st.text_input("Ap. Actuante", value=st.session_state.actuante_ap)
    st.session_state.actuante_nom = st.text_input("Nom. Actuante", value=st.session_state.actuante_nom)
    st.session_state.refuerzo_ap = st.text_input("Ap. Refuerzo", value=st.session_state.refuerzo_ap)
    st.session_state.refuerzo_nom = st.text_input("Nom. Refuerzo", value=st.session_state.refuerzo_nom)
    st.session_state.testigo_datos = st.text_area("Testigos", value=st.session_state.testigo_datos)
    st.session_state.requisa = st.text_area("Resultado de la Requisa", value=st.session_state.requisa)
    st.session_state.secuestro = st.text_area("Elementos secuestrados", value=st.session_state.secuestro)

with tab4:
    st.session_state.estado_fisico = st.selectbox("Estado físico:", [
        "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
        "presenta lesiones de vieja data y no requirieron atención médica",
        "presenta lesiones que motivaron su traslado previo a un centro de salud"
    ])

    op_motivos = [
        "EL INDIVIDUO CAMBIA BRUSCAMENTE SU SENTIDO DE MARCHA AL NOTAR LA PRESENCIA POLICIAL E INTENTA EVITAR CONTACTO, Y AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO.",
        "SE DETECTA AL MASCULINO OCULTÁNDOSE DE LA VISUAL DE LA PREVENCIÓN Y, AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO.",
        "OTRO (Manual)"
    ]
    seleccion = st.selectbox("Motivo observado:", op_motivos)
    if seleccion == "OTRO (Manual)":
        st.session_state.motivo_unico = st.text_area("Redacción del motivo:", value=st.session_state.motivo_unico)
    else:
        st.session_state.motivo_unico = seleccion

    st.session_state.of_recibe = st.text_input("Oficial de Guardia que recibe", value=st.session_state.of_recibe)

    # --- PDF GENERATOR ---
    def generar_pdf():
        pdf = FPDF()
        pdf.set_margins(left=25, top=20, right=20)
        pdf.add_page()
        ahora = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(165, 8, "ACTA DE DEMORA ART 10 BIS LEY 7.395", ln=True, align='C')
        pdf.ln(3)
        pdf.set_font('Arial', '', 11)
        
        info_jur = MAPA_JURISDICCION[st.session_state.jurisdiccion]
        prefijo_lugar = info_jur["tipo"].upper()
        depto_lugar = info_jur["depto"].upper()

        cuerpo = (
            f"En la {prefijo_lugar} de {st.session_state.jurisdiccion.upper()}, departamento {depto_lugar} de la provincia de Santa Fe, a los {ahora.day} días del mes de {meses[ahora.month-1]} del año {ahora.year}, "
            f"siendo las {st.session_state.hora_demora} hs, el funcionario policial actuante {st.session_state.actuante_ap.upper()} {st.session_state.actuante_nom.upper()} "
            f"a cargo de la unidad móvil {st.session_state.movil} juntamente con el refuerzo {st.session_state.refuerzo_ap.upper()} {st.session_state.refuerzo_nom.upper()}, "
            f"ambos pertenecientes a {st.session_state.unidad} de la UR II Rosario... (texto legal completo)"
        )
        pdf.multi_cell(165, 6, cuerpo.encode('latin-1', 'replace').decode('latin-1'), align='J')
        return bytes(pdf.output())

    col_pdf, col_hist = st.columns(2)
    with col_pdf:
        if st.session_state.apellido:
            st.download_button("📄 DESCARGAR PDF", data=generar_pdf(), file_name=f"10Bis_{st.session_state.apellido}.pdf")
            
    with col_hist:
        if st.button("💾 GUARDAR EN HISTORIAL", use_container_width=True):
            # Captura forzada de todos los valores actuales
            nuevo_registro = {clave: st.session_state[clave] for clave in campos_base.keys()}
            nuevo_registro['fecha_registro'] = datetime.now().strftime('%d/%m %H:%M')
            st.session_state.historial.append(nuevo_registro)
            st.toast("✅ Registro guardado en Historial")

    # --- WHATSAPP CODE ---
    st.subheader("📲 Parte para WhatsApp")
    res_wa = f"""*🚔 {st.session_state.unidad}* | *ACTA 10 BIS*
*HORA:* {st.session_state.hora_demora} hs.
*JURISDICCIÓN:* {st.session_state.jurisdiccion.upper()}
*👤 DEMORADO:* **{st.session_state.apellido.upper()} {st.session_state.nombre.upper()}**
*DNI:* **{st.session_state.dni}**"""
    st.code(res_wa)

with tab5:
    st.subheader("🗂️ Historial de Procedimientos")
    if not st.session_state.historial:
        st.info("No hay registros guardados todavía.")
    else:
        # Mostramos los registros del más nuevo al más viejo
        for i, reg in enumerate(reversed(st.session_state.historial)):
            with st.expander(f"📌 {reg['apellido']} - {reg['fecha_registro']}"):
                st.write(f"**DNI:** {reg['dni']} | **Móvil:** {reg['movil']}")
                if st.button(f"Reactivar datos de {reg['apellido']}", key=f"btn_{i}"):
                    for k in campos_base.keys():
                        st.session_state[k] = reg[k]
                    st.rerun()

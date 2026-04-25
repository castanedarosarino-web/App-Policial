import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SVI - ACTA 10 BIS", page_icon="👮", layout="wide")

# --- INICIALIZACIÓN DE VARIABLES ---
if 'historial' not in st.session_state:
    st.session_state.historial = []

campos_base = {
    'unidad': "B.O.U.", 'movil': "12.116", 'jurisdiccion': "SUB 18",
    'lugar': "", 'hora_demora': datetime.now().strftime('%H:%M'), 'acta_nro': "",
    'apellido': "", 'nombre': "", 'dni': "", 'nacionalidad': "ARGENTINA",
    'est_civil': "SOLTERO/A", 'edad': "", 'nacimiento': "", 'domicilio': "", 'padres': "",
    'actuante_ap': "CASTAÑEDA", 'actuante_nom': "JUAN", 'refuerzo_ap': "GOMEZ", 'refuerzo_nom': "RICARDO",
    'testigo_datos': "", 'requisa': "PALPADO PREVENTIVO SOBRE SUS PRENDAS NO HALLANDO ELEMENTOS DE PELIGROSIDAD", 
    'secuestro': "PERTENENCIAS PERSONALES", 
    'estado_fisico': "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
    'motivo_unico': "", 'of_recibe': "SUBOFICIAL RODRIGUEZ"
}

for clave, valor in campos_base.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor

# --- CABECERA PERSONALIZADA ---
st.markdown(f"""
    <div style='text-align: center; background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: 2px solid #1E3A8A;'>
        <h2 style='margin-bottom: 0; color: #1E3A8A;'>ACTA DE DEMORA ART 10 BIS LEY 7.395</h2>
        <p style='font-size: 1.1em; font-weight: bold; color: #1E3A8A;'>Creado por: Sub Crio. CASTAÑEDA JUAN</p>
    </div>
    """, unsafe_allow_html=True)

tabs = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Testigo/Requisa", "✍️ Cierre y WhatsApp", "🗂️ Historial"])

with tabs[0]:
    c1, c2 = st.columns(2)
    st.session_state.unidad = c1.text_input("Unidad Policial", value=st.session_state.unidad)
    st.session_state.movil = c2.text_input("Móvil / Legajo", value=st.session_state.movil)
    st.session_state.lugar = st.text_input("Lugar del procedimiento", value=st.session_state.lugar)
    st.session_state.hora_demora = c1.text_input("Hora de inicio", value=st.session_state.hora_demora)
    st.session_state.acta_nro = c2.text_input("Acta N°", value=st.session_state.acta_nro)

with tabs[1]:
    ca, cb = st.columns(2)
    st.session_state.apellido = ca.text_input("Apellido/s", value=st.session_state.apellido)
    st.session_state.nombre = cb.text_input("Nombre/s", value=st.session_state.nombre)
    st.session_state.dni = ca.text_input("DNI", value=st.session_state.dni)
    st.session_state.nacimiento = cb.text_input("Fecha de Nacimiento", value=st.session_state.nacimiento)
    st.session_state.padres = st.text_input("Filiación (Hijo de...)", value=st.session_state.padres)
    st.session_state.domicilio = st.text_input("Domicilio Real", value=st.session_state.domicilio)

with tabs[2]:
    st.session_state.testigo_datos = st.text_area("Datos del Testigo", value=st.session_state.testigo_datos)
    st.session_state.requisa = st.text_area("Resultado Requisa", value=st.session_state.requisa)
    st.session_state.secuestro = st.text_area("Elementos en depósito", value=st.session_state.secuestro)

with tabs[3]:
    # Motivo predefinido según acta oficial
    motivo_doc = "SE DETECTA AL MASCULINO OCULTÁNDOSE DE LA VISUAL DE LA PREVENCIÓN Y, AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO."
    st.session_state.motivo_unico = st.text_area("Motivo de la demora", value=motivo_doc if not st.session_state.motivo_unico else st.session_state.motivo_unico)
    st.session_state.of_recibe = st.text_input("Oficial que recibe", value=st.session_state.of_recibe)

    # --- GENERADOR DE PDF ---
    def crear_pdf():
        pdf = FPDF()
        pdf.set_margins(30, 30, 20)
        pdf.add_page()
        ahora = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "ACTA DE DEMORA ART 10 BIS LEY 7.395", align='C', ln=1)
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 11)
        # Redacción espejo del Word oficial
        cuerpo = (
            f"En la ciudad de ROSARIO, departamento Rosario de la provincia de Santa Fe, a los {ahora.day} días del mes de {meses[ahora.month-1]} del año {ahora.year}, "
            f"siendo las {st.session_state.hora_demora} hs, el funcionario policial actuante {st.session_state.actuante_ap.upper()} {st.session_state.actuante_nom.upper()} "
            f"a cargo de la unidad móvil {st.session_state.movil} juntamente con el refuerzo {st.session_state.refuerzo_ap.upper()} {st.session_state.refuerzo_nom.upper()}, "
            f"ambos pertenecientes a {st.session_state.unidad.upper()} de la UR II Rosario, SE HACE CONSTAR: Que de conformidad a lo establecido en el "
            f"Art. 10 bis de la Ley Orgánica de Policial de la Provincia de Santa Fe N° 7395 se procede a DEMORAR a las {st.session_state.hora_demora} horas, "
            f"desde calle {st.session_state.lugar.upper()} al cual manifiesta ser {st.session_state.apellido.upper()} {st.session_state.nombre.upper()}, "
            f"DNI {st.session_state.dni}, de nacionalidad {st.session_state.nacionalidad.upper()}, nacido el {st.session_state.nacimiento}, "
            f"hijo de {st.session_state.padres.upper()}, con domicilio real en la calle {st.session_state.domicilio.upper()}. "
            f"Motivo: {st.session_state.motivo_unico.upper()}. Derechos y garantías: a) traslado a dependencia; b) demora máx 6 horas; "
            f"c) no incomunicado; d) llamada telefónica; e) no alojamiento con detenidos comunes; f) ante testigos: {st.session_state.testigo_datos.upper()}. "
            f"Requisa: {st.session_state.requisa.upper()}. Secuestro: {st.session_state.secuestro.upper()}. "
            f"Estado físico: {st.session_state.estado_fisico.upper()}. Oficial que recibe: {st.session_state.of_recibe.upper()}."
        )
        pdf.multi_cell(0, 7, cuerpo, align='J')
        
        pdf.ln(20)
        pdf.cell(53, 10, "________________", align='C')
        pdf.cell(53, 10, "________________", align='C')
        pdf.cell(53, 10, "________________", align='C', ln=1)
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(53, 5, "PERSONAL ACTUANTE", align='C')
        pdf.cell(53, 5, "DEMORADO", align='C')
        pdf.cell(53, 5, "OF. GUARDIA", align='C')
        
        return pdf.output(dest='S').encode('latin-1')

    # BOTONES
    st.write("---")
    st.download_button("📄 DESCARGAR PDF OFICIAL", data=crear_pdf(), file_name=f"Acta_10Bis_{st.session_state.apellido}.pdf", mime="application/pdf")
    
    if st.button("💾 GUARDAR REGISTRO"):
        st.session_state.historial.append({k: st.session_state[k] for k in campos_base.keys()})
        st.success("Guardado en historial.")

    # --- COPIA WHATSAPP ---
    st.subheader("📲 Copia para WhatsApp")
    res_wa = f"""*🚔 {st.session_state.unidad.upper()}* | *ACTA 10 BIS*
*HORA:* {st.session_state.hora_demora} hs.
*DEMORADO:* **{st.session_state.apellido.upper()} {st.session_state.nombre.upper()}**
*DNI:* {st.session_state.dni}
*LUGAR:* {st.session_state.lugar.upper()}
*MOTIVO:* {st.session_state.motivo_unico.upper()}
*SECUESTRO:* {st.session_state.secuestro.upper()}
*RECIBE:* {st.session_state.of_recibe.upper()}"""
    st.code(res_wa)

with tabs[4]:
    st.subheader("Historial de Actas")
    for i, reg in enumerate(reversed(st.session_state.historial)):
        if st.button(f"Cargar: {reg['apellido']} ({reg['hora_demora']} hs)", key=f"h_{i}"):
            for k in campos_base.keys(): st.session_state[k] = reg[k]
            st.rerun()

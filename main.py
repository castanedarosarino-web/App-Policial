import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="ACTA DE DEMORA ART 10 BIS LEY 7.395", page_icon="👮", layout="wide")

# --- INICIALIZACIÓN DE MEMORIA (SESSION STATE) ---
# Esto asegura que el "espejo" funcione siempre
campos_base = {
    'unidad': "G.T.M.", 'tercio': "TERCIO ALPHA", 'movil': "12.116", 'jurisdiccion': "SUB 18",
    'lugar': "", 'hora_demora': datetime.now().strftime('%H:%M'), 'acta_nro': "",
    'apellido': "", 'nombre': "", 'dni': "", 'nacionalidad': "ARGENTINA",
    'est_civil': "SOLTERO/A", 'edad': "", 'nacimiento': "", 'domicilio': "", 'padres': "",
    'actuante_ap': "CASTAÑEDA", 'actuante_nom': "JUAN", 'refuerzo_ap': "", 'refuerzo_nom': "",
    'testigo_datos': "SIENDO EL MISMO EL PERSONAL ACTUANTE ANTE LA URGENCIA Y FALTA DE COLABORACIÓN DE TERCEROS", 
    'requisa': "palpado preventivo sobre sus prendas no hallando elementos de peligrosidad", 
    'secuestro': "pertenencias personales", 
    'estado_fisico': "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
    'motivo_final': "", 'of_recibe': "SUBOFICIAL RODRIGUEZ (M)"
}

for clave, valor in campos_base.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor

# --- TÍTULO Y AUTORÍA ---
st.title("👮 ACTA DE DEMORA ART 10 BIS LEY 7.395")
st.markdown("### **Creado por: Sub Comisario CASTAÑEDA JUAN**")

tab1, tab2, tab3, tab4 = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Procedimiento", "📄 Salida y WhatsApp"])

with tab1:
    col1, col2 = st.columns(2)
    st.session_state.unidad = col1.selectbox("Unidad", ["G.T.M.", "C.R.E. ROSARIO", "B.O.U.", "P.A.T.", "OTRO"], index=0)
    st.session_state.tercio = col2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    st.session_state.movil = st.text_input("Móvil / Legajo", value=st.session_state.movil)
    st.session_state.lugar = st.text_input("Lugar del procedimiento", value=st.session_state.lugar)
    st.session_state.hora_demora = st.text_input("Hora de inicio", value=st.session_state.hora_demora)
    st.session_state.acta_nro = st.text_input("Acta Nº", value=st.session_state.acta_nro)

with tab2:
    ca, cb = st.columns(2)
    st.session_state.apellido = ca.text_input("Apellido/s", value=st.session_state.apellido)
    st.session_state.nombre = cb.text_input("Nombre/s", value=st.session_state.nombre)
    st.session_state.dni = st.text_input("DNI", value=st.session_state.dni)
    st.session_state.domicilio = st.text_input("Domicilio Real", value=st.session_state.domicilio)
    st.session_state.nacimiento = st.text_input("Fecha de Nacimiento", value=st.session_state.nacimiento)
    st.session_state.padres = st.text_input("Filiación (Hijo de)", value=st.session_state.padres)

with tab3:
    st.session_state.actuante_ap = st.text_input("Ap. Actuante", value=st.session_state.actuante_ap)
    st.session_state.refuerzo_ap = st.text_input("Ap. Refuerzo", value=st.session_state.refuerzo_ap)
    st.session_state.requisa = st.text_area("Resultado Requisa", value=st.session_state.requisa)
    st.session_state.secuestro = st.text_area("Elementos secuestrados", value=st.session_state.secuestro)
    
    motivo_sel = st.selectbox("Motivo observado:", [
        "EL INDIVIDUO CAMBIA BRUSCAMENTE SU SENTIDO DE MARCHA AL NOTAR LA PRESENCIA POLICIAL E INTENTA EVITAR CONTACTO, Y AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO.",
        "SE DETECTA AL MASCULINO OCULTÁNDOSE DE LA VISUAL DE LA PREVENCIÓN Y, AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO.",
        "OTRO (Manual)"
    ])
    if motivo_sel == "OTRO (Manual)":
        st.session_state.motivo_final = st.text_area("Redacción personalizada:")
    else:
        st.session_state.motivo_final = motivo_sel

with tab4:
    # --- MOTOR PDF CORREGIDO ---
    def generar_pdf_bytes():
        pdf = FPDF()
        pdf.set_margins(left=30, top=30, right=20)
        pdf.add_page()
        ahora = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(160, 10, "ACTA DE DEMORA ART 10 BIS LEY 7.395", ln=True, align='C')
        pdf.set_font('Arial', 'I', 8)
        pdf.cell(160, 5, "SVI - Creado por: Sub Comisario CASTAÑEDA JUAN", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 11)
        # Usamos st.session_state para que el PDF siempre tenga lo último escrito
        cuerpo = (
            f"En la ciudad de ROSARIO, a los {ahora.day} días del mes de {meses[ahora.month-1]} del año {ahora.year}, "
            f"siendo las {st.session_state.hora_demora} hs, el funcionario actuante {st.session_state.actuante_ap.upper()} "
            f"con móvil {st.session_state.movil} y refuerzo {st.session_state.refuerzo_ap.upper()}, "
            f"pertenecientes a {st.session_state.unidad}, SE HACE CONSTAR: Que bajo Art. 10 bis Ley 7395 "
            f"se procede a DEMORAR a {st.session_state.apellido.upper()} {st.session_state.nombre.upper()}, DNI {st.session_state.dni}, "
            f"con domicilio en {st.session_state.domicilio.upper()}. Motivo: {st.session_state.motivo_final.upper()}. "
            f"Derechos: Traslado a dependencia, no exceder 6 horas, llamada telefónica. Requisa: {st.session_state.requisa.upper()}. "
            f"Secuestro: {st.session_state.secuestro.upper()}. Estado físico: {st.session_state.estado_fisico.upper()}."
        )
        pdf.multi_cell(160, 7, cuerpo.encode('latin-1', 'replace').decode('latin-1'), align='J')
        
        # Retornamos como bytes para evitar el StreamlitAPIException
        return pdf.output(dest='S').encode('latin-1')

    # Botón de Descarga
    if st.session_state.apellido:
        btn_data = generar_pdf_bytes()
        st.download_button(
            label="📄 DESCARGAR ACTA PDF",
            data=btn_data,
            file_name=f"10Bis_{st.session_state.apellido}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Complete el apellido para habilitar el PDF.")

    st.divider()
    
    # --- ESPEJO WHATSAPP AUTOMÁTICO ---
    st.subheader("📲 Espejo para WhatsApp")
    res_wa = f"""*🚔 {st.session_state.unidad}* | *ACTA 10 BIS*
*HORA:* {st.session_state.hora_demora} hs.
*LUGAR:* {st.session_state.lugar.upper()}

*👤 DEMORADO:*
*IDENTIDAD:* **{st.session_state.apellido.upper()} {st.session_state.nombre.upper()}**
*DNI:* **{st.session_state.dni}**

*📝 PROCEDIMIENTO:*
*MOTIVO:* {st.session_state.motivo_final.upper()}
*SECUESTRO:* **{st.session_state.secuestro.upper()}**
*Acta N• {st.session_state.acta_nro}*

👮 *PERSONAL:* {st.session_state.actuante_ap.upper()}"""
    st.code(res_wa)

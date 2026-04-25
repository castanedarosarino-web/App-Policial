import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="ACTA DE DEMORA ART 10 BIS", page_icon="👮", layout="wide")

# --- MEMORIA DE LA APP (SESSION STATE) ---
if 'unidad' not in st.session_state:
    st.session_state.unidad = "G.T.M."
if 'actuante_ap' not in st.session_state:
    st.session_state.actuante_ap = "CASTAÑEDA"
if 'movil' not in st.session_state:
    st.session_state.movil = "12.116"

# --- TÍTULO ---
st.title("👮 ACTA DE DEMORA ART 10 BIS LEY 7.395")
st.caption("Creado por: Sub Comisario CASTAÑEDA JUAN")

tab1, tab2, tab3, tab4 = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Procedimiento", "📄 Salida y WhatsApp"])

with tab1:
    col1, col2 = st.columns(2)
    u_op = ["G.T.M.", "C.R.E. ROSARIO", "B.O.U.", "P.A.T.", "OTRO"]
    unidad = col1.selectbox("Unidad", u_op, index=0)
    tercio = col2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    movil = st.text_input("Móvil / Legajo", value=st.session_state.movil)
    lugar = st.text_input("Lugar del procedimiento")
    hora_demora = st.text_input("Hora de inicio", value=datetime.now().strftime('%H:%M'))
    acta_nro = st.text_input("Acta Nº")

with tab2:
    ca, cb = st.columns(2)
    apellido = ca.text_input("Apellido/s")
    nombre = cb.text_input("Nombre/s")
    dni = st.text_input("DNI")
    domicilio = st.text_input("Domicilio Real")
    nacimiento = st.text_input("Fecha de Nacimiento")
    padres = st.text_input("Hijo de (Filiación)")

with tab3:
    actuante_ap = st.text_input("Ap. Actuante", value=st.session_state.actuante_ap)
    refuerzo_ap = st.text_input("Ap. Refuerzo")
    requisa = st.text_area("Resultado Requisa", value="palpado preventivo sobre sus prendas no hallando elementos de peligrosidad")
    secuestro = st.text_area("Elementos secuestrados", value="pertenencias personales")
    
    motivo_op = [
        "EL INDIVIDUO CAMBIA BRUSCAMENTE SU SENTIDO DE MARCHA AL NOTAR LA PRESENCIA POLICIAL E INTENTA EVITAR CONTACTO, Y AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO.",
        "SE DETECTA AL MASCULINO OCULTÁNDOSE DE LA VISUAL DE LA PREVENCIÓN Y, AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO.",
        "OTRO (Manual)"
    ]
    motivo_sel = st.selectbox("Motivo observado:", motivo_op)
    if motivo_sel == "OTRO (Manual)":
        motivo_final = st.text_area("Redacción personalizada:")
    else:
        motivo_final = motivo_sel

with tab4:
    # --- FUNCIÓN GENERADORA (LA QUE FUNCIONABA) ---
    def crear_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(left=30, top=30, right=20)
        ahora = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        
        # Encabezado
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "ACTA DE DEMORA ART 10 BIS LEY 7.395", ln=True, align='C')
        pdf.set_font('Arial', 'I', 8)
        pdf.cell(0, 5, "Creado por: Sub Comisario CASTAÑEDA JUAN", ln=True, align='C')
        pdf.ln(10)
        
        # Texto Justificado (Sin negritas para evitar errores)
        pdf.set_font('Arial', '', 11)
        texto = (
            f"En la ciudad de ROSARIO, a los {ahora.day} dias del mes de {meses[ahora.month-1]} del año {ahora.year}, "
            f"siendo las {hora_demora} hs, el funcionario actuante {actuante_ap.upper()} "
            f"con movil {movil} y refuerzo {refuerzo_ap.upper()}, pertenecientes a {unidad}, "
            f"SE HACE CONSTAR: Que bajo Art. 10 bis Ley 7395 se procede a DEMORAR a "
            f"{apellido.upper()} {nombre.upper()}, DNI {dni}, con domicilio en {domicilio.upper()}. "
            f"Motivo: {motivo_final.upper()}. Se le comunica que la demora no excedera las SEIS (6) HORAS. "
            f"Requisa: {requisa.upper()}. Secuestro: {secuestro.upper()}. Con lo que se da por finalizado el acto."
        )
        pdf.multi_cell(0, 7, texto.encode('latin-1', 'replace').decode('latin-1'), align='J')
        
        pdf.ln(20)
        pdf.cell(0, 10, "HORA DE CESE: __________ hs.", ln=True)
        return pdf.output(dest='S').encode('latin-1')

    # BOTÓN DE DESCARGA
    if apellido:
        st.download_button(
            label="📄 DESCARGAR PDF JUSTIFICADO",
            data=crear_pdf(),
            file_name=f"10Bis_{apellido}.pdf",
            mime="application/pdf"
        )
    else:
        st.info("Complete los datos para generar el PDF.")

    st.divider()
    
    # ESPEJO WHATSAPP (AQUÍ SE REFLEJA TODO)
    st.subheader("📲 Espejo para WhatsApp")
    res_wa = f"""*🚔 {unidad}* | *ACTA 10 BIS*
*HORA:* {hora_demora} hs.
*LUGAR:* {lugar.upper()}

*👤 DEMORADO:*
*IDENTIDAD:* **{apellido.upper()} {nombre.upper()}**
*DNI:* **{dni}**

*📝 PROCEDIMIENTO:*
*MOTIVO:* {motivo_final.upper()}
*SECUESTRO:* **{secuestro.upper()}**
*Acta N• {acta_nro}*

👮 *PERSONAL:* {actuante_ap.upper()}"""
    st.code(res_wa)

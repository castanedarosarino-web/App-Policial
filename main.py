import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuración técnica para dispositivos móviles
st.set_page_config(page_title="Gestión Operativa URII", page_icon="👮")

st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3.5em; font-weight: bold; background-color: #182c54; color: white; border-radius: 10px; }
    .stTextInput>div>div>input { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

st.title("👮 Sistema de Actas URII")

# --- PESTAÑAS DE CARGA ---
tab1, tab2, tab3 = st.tabs(["🚔 Intervención", "👤 Demorado", "✍️ Relato y Cierre"])

with tab1:
    col1, col2 = st.columns(2)
    unidad = col1.selectbox("Unidad", ["C.R.E. ROSARIO", "G.T.M.", "B.O.U.", "P.A.T.", "OTRA"])
    tercio = col2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    movil = st.text_input("Móvil / Legajo", value="2308")
    lugar = st.text_input("Lugar de la demora (Calle y Altura)")
    dependencia = st.text_input("Dependencia de traslado", value="SUB CRIA 18")

with tab2:
    apellido = st.text_input("Apellido/s")
    nombre = st.text_input("Nombre/s")
    dni = st.text_input("DNI", value="No recuerda")
    nacionalidad = st.text_input("Nacionalidad", value="Argentina")
    padres = st.text_input("Hijo de (Padre y Madre)")
    nacimiento = st.text_input("Fecha de Nac. / Edad")
    domicilio = st.text_input("Domicilio Real")

with tab3:
    # Menú desplegable con tus motivos técnicos
    opciones_motivos = [
        "Se detecta al masculino ocultándose de la visual de la prevención. Al requerir su identificación, responde con evasivas y manifiesta no poseer documentación.",
        "El individuo, ante la proximidad del personal, cambia bruscamente su sentido de marcha e intenta ocultar su rostro, no aportando datos filiatorios fehacientes.",
        "Se observa al masculino apostado de forma prolongada. Al ser abordado, manifiesta versiones contradictorias y carece de acreditación de identidad.",
        "Se detecta al sujeto realizando un seguimiento cercano a terceros. Al notar la presencia policial, adopta conducta esquiva y se niega a brindar datos.",
        "El causante observaba objetivos en la zona, retirándose presurosamente al advertir el móvil. Tras ser alcanzado, no posee DNI para su identificación.",
        "OTRO (Redactar manualmente)"
    ]
    
    seleccion = st.selectbox("Motivo de la demora (Art. 10 Bis):", opciones_motivos)
    
    if seleccion == "OTRO (Redactar manualmente)":
        motivo_final = st.text_area("Escriba la circunstancia específica:")
    else:
        motivo_final = seleccion

    st.divider()
    redacto = st.text_input("Suscrito (Grado y Apellido)")
    refuerzo = st.text_input("Refuerzo (Grado y Apellido)")

# --- CONSTRUCCIÓN DEL PDF (MODELO CORRECTOR) ---
class ActaURII(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(190, 10, "ACTA DE PROCEDIMIENTO - ARTÍCULO 10 BIS LEY 7.395", ln=True, align='C')
        self.ln(5)

def generar_acta_oficial():
    pdf = ActaURII()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)
    
    # Fecha y Hora automáticas
    ahora = datetime.now()
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    fecha_texto = f"{ahora.day} de {meses[ahora.month-1]} de {ahora.year}"
    
    # Cuerpo del Acta (Siguiendo el modelo PDF oficial)
    intro = (f"En la ciudad de ROSARIO, departamento Rosario de la provincia de Santa Fe, a los {ahora.day} días del mes de {meses[ahora.month-1]} "
             f"del año {ahora.year}, siendo las {ahora.strftime('%H:%M')} hs, el funcionario policial actuante {redacto.upper()} "
             f"juntamente como refuerzo {refuerzo.upper()}, ambos pertenecientes a {unidad} de la UR II Rosario, a los fines legales que diera a lugar "
             f"se hace CONSTAR: Que de conformidad a lo establecido en el Art. 10 bis de la Ley Orgánica de Policial de la Provincia de Santa Fe N° 7395 "
             f"se procede a DEMORAR en calle {lugar.upper()} al ciudadano quien manifiesta ser {apellido.upper()}, {nombre.upper()}, "
             f"de nacionalidad {nacionalidad.upper()}, DNI {dni}, domiciliado en {domicilio.upper()}, hijo de {padres.upper()}, "
             f"nacido el/con edad de {nacimiento}.")
    
    pdf.multi_cell(190, 6, intro)
    pdf.ln(5)
    
    # Motivo (Recuadro)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(190, 7, "Adoptándose esta medida por el motivo de que ante la presencia policial:", ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(190, 7, f" {motivo_final}", border=1)
    pdf.ln(5)
    
    # Base Legal y Derechos (Copiado fiel del modelo corrector)
    pdf.set_font('Arial', '', 9)
    legal = ("Razón para lo cual y para la constancia de su identidad con el registro policial en los términos y alcances del Art. 10 Bis Ley 7395/75, "
             "introducida por Ley 11.516/97 y Resol. 0745/16. A continuación se imponen al demorado sus derechos y garantías: "
             "a) Que será demorado en el lugar y trasladado a dependencia; b) Que la demora podrá prolongarse hasta constatar su identificación "
             "sin que esta supere las SEIS (6) HORAS; c) Que en ningún momento ha de ser incomunicado; d) Que tiene derecho a efectuar una llamada telefónica; "
             "e) Que no será alojado con detenidos por delitos; f) Que se procede a labrar acta ad-hoc con testigos.")
    pdf.multi_cell(190, 5, legal)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(190, 6, f"Se hace constar que se traslada el procedimiento a {dependencia.upper()} para su correspondiente registro.")

    # Firmas (3 columnas como el modelo)
    pdf.ln(30)
    pdf.cell(63, 5, "____________________", 0, 0, 'C')
    pdf.cell(63, 5, "____________________", 0, 0, 'C')
    pdf.cell(63, 5, "____________________", 0, 1, 'C')
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(63, 5, "PERSONAL ACTUANTE", 0, 0, 'C')
    pdf.cell(63, 5, "DEMORADO", 0, 0, 'C')
    pdf.cell(63, 5, "TESTIGO / OF. GUARDIA", 0, 1, 'C')

    return pdf.output(dest='S').encode('latin-1')

# Botón de acción
if st.button("📄 GENERAR ACTA 10 BIS"):
    if apellido and redacto:
        pdf_out = generar_acta_oficial()
        st.download_button("⬇️ DESCARGAR PDF OFICIAL", data=pdf_out, file_name=f"10Bis_{apellido}.pdf", mime="application/pdf")
        st.success("Acta generada siguiendo el protocolo URII.")
    else:
        st.error("Faltan datos obligatorios (Apellido y Funcionario).")

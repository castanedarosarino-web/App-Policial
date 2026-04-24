import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuración de la App
st.set_page_config(page_title="Sistema de Actas URII", page_icon="👮")

st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3.5em; font-weight: bold; background-color: #182c54; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("👮 Sistema de Actas URII")

# --- PESTAÑAS OPERATIVAS ---
tab1, tab2, tab3, tab4 = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Testigo/Requisa", "✍️ Cierre y WhatsApp"])

with tab1:
    col1, col2 = st.columns(2)
    unidad = col1.selectbox("Unidad", ["G.T.M.", "C.R.E. ROSARIO", "B.O.U.", "P.A.T."])
    tercio = col2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    movil = st.text_input("Móvil / Legajo", value="12.116")
    jurisdiccion = st.text_input("Jurisdicción", value="SUB 18")
    lugar = st.text_input("Lugar (Calle e intersección)", placeholder="Ej: LOS TORDOS 317")
    acta_nro = st.text_input("Acta Nº", placeholder="Ej: 192 / 2026")

with tab2:
    apellido = st.text_input("Apellido/s")
    nombre = st.text_input("Nombre/s")
    dni = st.text_input("DNI", value="")
    nacionalidad = st.text_input("Nacionalidad", value="Argentina")
    est_civil = st.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "CONCUBINATO"])
    edad = st.text_input("Edad")
    nacimiento = st.text_input("Fecha de Nacimiento")
    domicilio = st.text_input("Domicilio Real")
    padres = st.text_input("Hijo de (Padre y Madre)")

with tab3:
    personal_completo = st.text_area("Personal Actuante (Grados y Nombres)", placeholder="SUBOFICIAL FERNANDEZ DANTE\nSUBOFICIAL GAUNA RODRIGO")
    testigo_datos = st.text_area("Datos del Testigo", placeholder="Apellido y Nombres, Edad, Identidad...")
    requisa = st.text_area("Resultado de la Requisa:", value="NEGATIVO (No se hallan elementos de peligrosidad)")
    secuestro = st.text_area("Se le secuestra en carácter de depósito:", placeholder="Ej: (01) Celular Samsung, llaves...")

with tab4:
    opciones = [
        "Se detecta al masculino ocultándose de la visual de la prevención.",
        "El individuo cambia bruscamente su sentido de marcha e intenta evitar contacto.",
        "Se observa al mismo apostado de forma prolongada, brindando versiones contradictorias.",
        "Se encontraba observando objetivos, retirándose presurosamente al notar el móvil.",
        "OTRO (Manual)"
    ]
    seleccion = st.selectbox("Motivo de la demora:", opciones)
    motivo_final = st.text_area("Detalle:", value=seleccion if seleccion != "OTRO (Manual)" else "")
    
    redacto = st.text_input("Redactó (Grado y Apellido)")
    of_recibe = st.text_input("Oficial de Guardia que recibe", value="suboficial Rodriguez (M)")
    hora_cese = st.text_input("Hora de Cese", placeholder="Ej: 19:30")

# --- LÓGICA DE PDF ESPEJO ---
def generar_pdf_espejo():
    pdf = FPDF()
    pdf.add_page()
    ahora = datetime.now()
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(190, 10, "ACTA DE PROCEDIMIENTO - ARTICULO 10 BIS LEY 7.395", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 10)
    # Párrafo 1: Encabezado
    texto_1 = (f"En la ciudad de ROSARIO, departamento Rosario de la provincia de Santa Fe, a los {ahora.day} días del mes de {meses[ahora.month-1]} del año {ahora.year}, "
               f"siendo las {ahora.strftime('%H:%M')} hs, el funcionario policial actuante {redacto.upper()} a cargo de la unidad móvil {movil} juntamente como refuerzo {personal_completo.upper()}, "
               f"ambos pertenecientes a {unidad} de la UR II Rosario, a los fines legales que diera a lugar se hace CONSTAR: Que de conformidad a lo establecido en el Art. 10 bis de la "
               f"Ley Orgánica de Policial de la Provincia de Santa Fe N° 7395 se procede a DEMORAR a las {ahora.strftime('%H:%M')} horas, desde calle {lugar.upper()} al cual manifiesta ser "
               f"{apellido.upper()} {nombre.upper()}, de nacionalidad {nacionalidad.upper()}, DNI {dni}, domicilio en la calle {domicilio.upper()} de esta ciudad, hijo de {padres.upper()}, "
               f"fecha de nacimiento {nacimiento} contando con {edad} años de edad.")
    pdf.multi_cell(190, 6, texto_1)
    pdf.ln(4)

    # Motivo
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(190, 7, "Adoptándose esta medida por el motivo de que ante la presencia policial:", ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(190, 6, f"X {motivo_final}", border=1)
    pdf.ln(4)

    # Base Legal y Derechos
    legal_text = ("Razón para lo cual y para la constancia de su identidad con el registro policial en los términos y alcances del Art. 10 Bis Ley 7395/75, introducida por Ley 11.516/97 y Resol. 0745/16. "
                  "A continuación se imponen al demorado, sus derechos y garantías establecidos por Ley a saber: a) Que será demorado en el lugar y trasladado a dependencia; b) Que la demora podrá "
                  "prolongarse hasta constatar su identificación con el registro policial, sin que esta supere las SEIS (6) HORAS corridas contadas desde el inicio de la medida; c) Que en ningún momento "
                  "ha de ser incomunicado; d) Que tiene derecho a efectuar una llamada telefónica tendiente a plantear su situación y a fin de colaborar en su individualización e identidad personal; "
                  "e) Que en caso de ser trasladado a dependencia policial no será alojado con detenidos por delitos o contravenciones; f) Que se procede a labrar acta ad-hoc con testigos del procedimiento. "
                  f"Siendo estos los llamados: {testigo_datos.upper()}.")
    pdf.multi_cell(190, 5, legal_text)
    pdf.ln(4)

    # Requisa y Secuestro
    pdf.multi_cell(190, 6, f"Se procede a la requisa del demorado, con el siguiente resultado: {requisa.upper()}", border=1)
    pdf.ln(2)
    pdf.multi_cell(190, 6, f"Se le secuestra en carácter de depósito: {secuestro.upper()}", border=1)
    pdf.ln(4)

    # Cierre
    cierre_text = (f"Se hace constar que se labra la presente en recibiendo de conformidad {of_recibe.upper()} en carácter de oficial de guardia. "
                   "Con lo que no siendo para más se da por finalizado el presente acto del cual firman los testigos, demorado y el personal actuante para su debida constancia.")
    pdf.multi_cell(190, 6, cierre_text)
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(190, 10, f"HORA DE CESE: {hora_cese} hs. :-", ln=True)

    # Firmas
    pdf.ln(15)
    pdf.cell(63, 5, "________________", 0, 0, 'C'); pdf.cell(63, 5, "________________", 0, 0, 'C'); pdf.cell(63, 5, "________________", 0, 1, 'C')
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(63, 5, "ACTUANTE", 0, 0, 'C'); pdf.cell(63, 5, "DEMORADO", 0, 0, 'C'); pdf.cell(63, 5, "TESTIGO / OF. GUARDIA", 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- PARTE WHATSAPP (ESPEJO) ---
fecha_wa = ahora.strftime("%d/%m/%Y")
resumen_wa = f"""*{unidad} - {tercio}*
*PARTE DEMORA ART 10 BIS*

*FECHA:* {fecha_wa}.-
*HORA:* {ahora.strftime('%H:%M')}.-
*Lugar :* {lugar.upper()} .-
*Jurisdicción:* {jurisdiccion.upper()} .-

*PERSONAL:* {personal_completo.upper()} .-
*Móvil:* {movil}

*DEMORADO:* {apellido.upper()} {nombre.upper()} .-
*ESTADO CIVIL:* {est_civil}.-
*EDAD:* {edad}
*DNI:* {dni}
*DOMICILIO:* {domicilio.upper()}.-

*ENTREGADO EN CRIA:* {jurisdiccion.upper()}, Sin lesiones visibles y no refieren dolencias.-

*Recibe:* {of_recibe}.-

*Acta N• {acta_nro}.-*

*redacto:* {redacto}"""

# --- BOTONES ---
st.divider()
if st.button("📄 GENERAR PDF (MODELO ESPEJO)"):
    if apellido and redacto:
        st.download_button("⬇️ DESCARGAR ACTA OFICIAL", data=generar_pdf_espejo(), file_name=f"Acta_10Bis_{apellido}.pdf")

st.subheader("📲 Parte para WhatsApp")
st.code(resumen_wa, language="text")

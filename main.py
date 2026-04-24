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

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Testigo/Requisa", "✍️ Cierre y WhatsApp"])

with tab1:
    col1, col2 = st.columns(2)
    unidad = col1.selectbox("Unidad", ["G.T.M.", "C.R.E. ROSARIO", "B.O.U.", "P.A.T."])
    tercio = col2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    movil = st.text_input("Móvil / Legajo", value="12.116")
    jurisdiccion = st.text_input("Jurisdicción", value="SUB 18")
    lugar = st.text_input("Lugar de la demora", placeholder="Ej: LOS TORDOS 317")
    hora_demora = st.text_input("Hora de la demora", value=datetime.now().strftime('%H:%M'))
    acta_nro = st.text_input("Acta Nº", placeholder="Ej: 192 / 2026")

with tab2:
    col_a, col_b = st.columns(2)
    apellido = col_a.text_input("Apellido/s")
    nombre = col_b.text_input("Nombre/s")
    dni = st.text_input("DNI", value="")
    nacionalidad = st.text_input("Nacionalidad", value="Argentina")
    est_civil = st.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "CONCUBINATO"])
    edad = st.text_input("Edad")
    nacimiento = st.text_input("Fecha de Nacimiento")
    domicilio = st.text_input("Domicilio Real")
    padres = st.text_input("Hijo de (Padre y Madre)")

with tab3:
    actuante = st.text_input("Funcionario Actuante (Grado y Apellido)")
    refuerzo = st.text_input("Funcionario Refuerzo (Grado y Apellido)")
    testigo_datos = st.text_area("Datos del Testigo", placeholder="Apellido y Nombres, Edad, Identidad...")
    requisa = st.text_area("Resultado de la Requisa:", value="NEGATIVO (No se hallan elementos de peligrosidad)")
    secuestro = st.text_area("Se le secuestra en carácter de depósito:", placeholder="Ej: (01) Celular Samsung, llaves...")

with tab4:
    opciones_fisicas = [
        "Se deja constancia que el demorado NO PRESENTA LESIONES VISIBLES, GOLPES NI MANIFIESTA DOLENCIAS al momento de ingresar a la dependencia.",
        "PRESENTA LESIONES DE VIEJA DATA Y NO REQUIRIERON ATENCION MEDICA.",
        "PRESENTA LESIONES QUE MOTIVARON SU TRASLADO PREVIO A UN CENTRO DE SALUD PARA LO CUAL SE ANEXA CERTIFICADO MEDICO."
    ]
    estado_fisico = st.selectbox("Estado físico del demorado:", opciones_fisicas)
    
    opciones_motivos = [
        "Se detecta al masculino ocultándose de la visual de la prevención.",
        "El individuo cambia bruscamente su sentido de marcha e intenta evitar contacto.",
        "Se observa al mismo apostado de forma prolongada, brindando versiones contradictorias.",
        "OTRO (Manual)"
    ]
    seleccion_motivo = st.selectbox("Motivo de la demora:", opciones_motivos)
    motivo_final = st.text_area("Detalle del motivo:", value=seleccion_motivo if seleccion_motivo != "OTRO (Manual)" else "")
    
    of_recibe = st.text_input("Oficial de Guardia que recibe", value="suboficial Rodriguez (M)")
    redacta_wa = st.text_input("Redactó (Solo para WhatsApp)", value=f"SubOf. {actuante.split()[-1] if actuante else ''}")

# --- LÓGICA DE PDF ---
def generar_pdf_espejo():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    ahora = datetime.now()
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(190, 10, "ACTA DE PROCEDIMIENTO - ARTÍCULO 10 BIS LEY 7.395", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 11)
    
    # Texto Justificado y Fluido
    intro = (f"En la ciudad de ROSARIO, departamento Rosario de la provincia de Santa Fe, a los {ahora.day} días del mes de {meses[ahora.month-1]} del año {ahora.year}, "
             f"siendo las {hora_demora} hs, el funcionario policial actuante {actuante.upper()} a cargo de la unidad móvil {movil} juntamente como refuerzo {refuerzo.upper()}, "
             f"ambos pertenecientes a {unidad} de la UR II Rosario, a los fines legales que diera a lugar se hace CONSTAR: Que de conformidad a lo establecido en el Art. 10 bis de la "
             f"Ley Orgánica de Policial de la Provincia de Santa Fe N° 7395 se procede a DEMORAR a las {hora_demora} horas, desde calle {lugar.upper()} al cual manifiesta ser "
             f"{apellido.upper()} {nombre.upper()}, de nacionalidad {nacionalidad.upper()}, DNI {dni}, domicilio en la calle {domicilio.upper()} de esta ciudad, hijo de {padres.upper()}, "
             f"fecha de nacimiento {nacimiento} contando con {edad} años de edad.")
    
    pdf.multi_cell(190, 6, intro, align='J')
    pdf.ln(4)

    pdf.set_font('Arial', 'B', 11)
    pdf.multi_cell(190, 6, "Adoptándose esta medida por el motivo de que ante la presencia policial:", align='J')
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(190, 6, f" {motivo_final.upper()}", border=1, align='J')
    pdf.ln(4)
    
    legal = ("Razón para lo cual y para la constancia de su identidad con el registro policial en los términos y alcances del Art. 10 Bis Ley 7395/75, introducida por Ley 11.516/97 y Resol. 0745/16. "
             "A continuación se imponen al demorado, sus derechos y garantías establecidos por Ley a saber: a) Que será demorado en el lugar y trasladado a dependencia; b) Que la demora podrá prolongarse "
             "hasta constatar su identificación con el registro policial, sin que esta supere las SEIS (6) HORAS corridas contadas desde el inicio de la medida; c) Que en ningún momento ha de ser incomunicado; "
             "d) Que tiene derecho a efectuar una llamada telefónica tendiente a plantear su situación y a fin de colaborar en su individualización e identidad personal; e) Que en caso de ser trasladado a dependencia "
             "policial no será alojado con detenidos por delitos o contravenciones; f) Que se procede a labrar acta ad-hoc con testigos del procedimiento. Siendo estos los llamados: " + testigo_datos.upper() + ".")
    pdf.multi_cell(190, 5, legal, align='J')
    pdf.ln(4)
    
    pdf.multi_cell(190, 6, f"REQUISA: {requisa.upper()}", border=1, align='J')
    pdf.multi_cell(190, 6, f"SECUESTRO EN DEPÓSITO: {secuestro.upper()}", border=1, align='J')
    pdf.ln(4)
    
    # Inclusión del estado físico
    pdf.multi_cell(190, 6, f"{estado_fisico.upper()}", align='J')
    pdf.ln(2)
    
    pdf.multi_cell(190, 6, f"Se hace constar que se labra la presente en recibiendo de conformidad {of_recibe.upper()} en carácter de oficial de guardia. Con lo que no siendo para más se da por finalizado el presente acto del cual firman los testigos, demorado y el personal actuante para su debida constancia.", align='J')
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(190, 10, "HORA DE CESE: _________ hs. :-", ln=True)

    # Firmas
    pdf.ln(15)
    col_width = 190/3
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(col_width, 5, "________________", 0, 0, 'C')
    pdf.cell(col_width, 5, "________________", 0, 0, 'C')
    pdf.cell(col_width, 5, "________________", 0, 1, 'C')
    pdf.cell(col_width, 5, "PERSONAL ACTUANTE", 0, 0, 'C')
    pdf.cell(col_width, 5, "DEMORADO", 0, 0, 'C')
    pdf.cell(col_width, 5, "TESTIGO / OF. GUARDIA", 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- PARTE WHATSAPP ---
resumen_wa = f"""*{unidad} - {tercio}*
*PARTE DEMORA ART 10 BIS*

*FECHA:* {datetime.now().strftime('%d/%m/%Y')}.-
*HORA:* {hora_demora}.-
*Lugar :* {lugar.upper()} .-
*Jurisdicción:* {jurisdiccion.upper()} .-

*PERSONAL:* {actuante.upper()} .-
{refuerzo.upper()} .-
*Móvil:* {movil}

*DEMORADO:* {apellido.upper()} {nombre.upper()} .-
*ESTADO CIVIL:* {est_civil}.-
*EDAD:* {edad}
*DNI:* {dni}
*DOMICILIO:* {domicilio.upper()}.-

*ENTREGADO EN CRIA:* {jurisdiccion.upper()}, Sin lesiones visibles y no refieren dolencias.-

*Recibe:* {of_recibe}.-

*Acta N• {acta_nro}.-*

*redacto:* {redacta_wa}"""

st.divider()
if st.button("📄 GENERAR PDF"):
    if apellido and actuante:
        st.download_button("⬇️ DESCARGAR ACTA", data=generar_pdf_espejo(), file_name=f"10Bis_{apellido}.pdf")

st.subheader("📲 Parte WhatsApp")
st.code(resumen_wa, language="text")

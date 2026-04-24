import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuración de la App
st.set_page_config(page_title="ACTA DE DEMORA ART 10 BIS LEY 7.395", page_icon="👮")

# Estilos personalizados
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3.5em; font-weight: bold; background-color: #182c54; color: white; border-radius: 10px; }
    .autor-text { font-size: 11px; color: #777; margin-top: -20px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("👮 ACTA DE DEMORA ART 10 BIS LEY 7.395")
st.markdown('<p class="autor-text">creado: Sub Crio Castañeda Juan</p>', unsafe_allow_html=True)

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Testigo/Requisa", "✍️ Cierre y WhatsApp"])

with tab1:
    col1, col2 = st.columns(2)
    lista_unidades = ["G.T.M.", "C.R.E. ROSARIO", "B.O.U.", "P.A.T.", "OTRO"]
    seleccion_u = col1.selectbox("Unidad", lista_unidades)
    unidad = col1.text_input("Especifique Unidad", value=seleccion_u) if seleccion_u == "OTRO" else seleccion_u
        
    tercio = col2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    movil = st.text_input("Móvil / Legajo", value="12.116")
    jurisdiccion = st.text_input("Jurisdicción de entrega", value="SUB 18")
    lugar = st.text_input("Lugar de la demora", placeholder="Ej: LOS TORDOS 317")
    hora_demora = st.text_input("Hora de la demora", value=datetime.now().strftime('%H:%M'))
    acta_nro = st.text_input("Acta Nº", placeholder="Ej: 192 / 2026")

with tab2:
    col_a, col_b = st.columns(2)
    apellido = col_a.text_input("Apellido/s del demorado")
    nombre = col_b.text_input("Nombre/s del demorado")
    dni = st.text_input("DNI", value="")
    nacionalidad = st.text_input("Nacionalidad", value="Argentina")
    est_civil = st.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "CONCUBINATO"])
    edad = st.text_input("Edad")
    nacimiento = st.text_input("Fecha de Nacimiento")
    domicilio = st.text_input("Domicilio Real")
    padres = st.text_input("Hijo de (Padre y Madre)")

with tab3:
    actuante_ap = st.text_input("Apellido Funcionario Actuante")
    actuante_nom = st.text_input("Nombre Funcionario Actuante")
    refuerzo_ap = st.text_input("Apellido Funcionario Refuerzo")
    refuerzo_nom = st.text_input("Nombre Funcionario Refuerzo")
    testigo_datos = st.text_area("Datos del Testigo", placeholder="Apellido y Nombres, Edad, Identidad...")
    requisa = st.text_area("Resultado de la Requisa:", value="NEGATIVO (No se hallan elementos de peligrosidad)")
    secuestro = st.text_area("Se le secuestra en carácter de depósito:", placeholder="Ej: (01) Celular Samsung, llaves...")

with tab4:
    opciones_fisicas = [
        "No presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia.",
        "Presenta lesiones de vieja data y no requirieron atención médica.",
        "Presenta lesiones que motivaron su traslado previo a un centro de salud para lo cual se anexa certificado médico."
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
    redacta_wa = st.text_input("Redactó (Solo para WhatsApp)", value=f"SubOf. {actuante_ap}")

# --- LÓGICA DE PDF ---
def generar_pdf_espejo():
    # Márgenes de 3 cm (30mm) superior e izquierdo
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=30, top=30, right=15)
    pdf.add_page()
    
    ahora = datetime.now()
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    
    # Título actualizado en el PDF
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(165, 10, "ACTA DE DEMORA ART 10 BIS LEY 7.395", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    
    # Párrafo principal con interlineado 1.5 (height=9)
    intro_txt = (f"En la ciudad de ROSARIO, departamento Rosario de la provincia de Santa Fe, a los {ahora.day} días del mes de {meses[ahora.month-1]} del año {ahora.year}, "
                 f"siendo las {hora_demora} hs, el funcionario policial actuante {actuante_ap.upper()} {actuante_nom.upper()} a cargo de la unidad móvil {movil} juntamente como refuerzo {refuerzo_ap.upper()} {refuerzo_nom.upper()}, "
                 f"ambos pertenecientes a {unidad} de la UR II Rosario, a los fines legales que diera a lugar se hace CONSTAR: Que de conformidad a lo establecido en el Art. 10 bis de la "
                 f"Ley Orgánica de Policial de la Provincia de Santa Fe N° 7395 se procede a DEMORAR a las {hora_demora} horas, desde calle {lugar.upper()} al cual manifiesta ser "
                 f"{apellido.upper()} {nombre.upper()}, DNI {dni}, de nacionalidad {nacionalidad.upper()}, domicilio en la calle {domicilio.upper()} de esta ciudad, hijo de {padres.upper()}, "
                 f"fecha de nacimiento {nacimiento} contando con {edad} años de edad. Adoptándose esta medida por el motivo de que ante la presencia policial: {motivo_final.upper()}.")

    pdf.multi_cell(165, 9, intro_txt, align='J')
    pdf.ln(4)

    legal_text = ("Razón para lo cual y para la constancia de su identidad con el registro policial en los términos y alcances del Art. 10 Bis Ley 7395/75, introducida por Ley 11.516/97 y Resol. 0745/16. "
                  "A continuación se imponen al demorado, sus derechos y garantías establecidos por Ley a saber: a) Que será demorado en el lugar y trasladado a dependencia; b) Que la demora podrá prolongarse "
                  "hasta constatar su identificación con el registro policial, sin que esta supere las SEIS (6) HORAS corridas contadas desde el inicio de la medida; c) Que en ningún momento ha de ser incomunicado; "
                  "d) Que tiene derecho a efectuar una llamada telefónica tendiente a plantear su situación y a fin de colaborar en su individualización e identidad personal; e) Que en caso de ser trasladado a dependencia "
                  "policial no será alojado con detenidos por delitos o contravenciones; f) Que se procede a labrar acta ad-hoc con testigos del procedimiento. Siendo estos los llamados: " + testigo_datos.upper() + ".")
    pdf.multi_cell(165, 9, legal_text, align='J')
    pdf.ln(4)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.multi_cell(165, 9, f"REQUISA: {requisa.upper()}", border=1, align='J')
    pdf.multi_cell(165, 9, f"SECUESTRO EN DEPÓSITO: {secuestro.upper()}", border=1, align='J')
    pdf.set_font('Arial', '', 12)
    pdf.ln(4)
    
    pdf.multi_cell(165, 9, f"Se deja constancia que el demorado {estado_fisico.lower()}", align='J')
    pdf.ln(4)
    
    pdf.multi_cell(165, 9, f"Se hace constar que se labra la presente en recibiendo de conformidad {of_recibe.upper()} en carácter de oficial de guardia. Con lo que no siendo para más se da por finalizado el presente acto del cual firman los testigos, demorado y el personal actuante para su debida constancia.", align='J')
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(165, 10, "HORA DE CESE: _________ hs. :-", ln=True)

    # Bloque de Firmas
    pdf.ln(15)
    w = 165/3
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(w, 5, "________________", 0, 0, 'C')
    pdf.cell(w, 5, "________________", 0, 0, 'C')
    pdf.cell(w, 5, "________________", 0, 1, 'C')
    pdf.cell(w, 5, "ACTUANTE", 0, 0, 'C')
    pdf.cell(w, 5, "DEMORADO", 0, 0, 'C')
    pdf.cell(w, 5, "TESTIGO/GUARDIA", 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- PARTE WHATSAPP DINÁMICO ---
resumen_wa = f"""*{unidad} - {tercio}*
*ACTA DE DEMORA ART 10 BIS LEY 7.395*

*FECHA:* {datetime.now().strftime('%d/%m/%Y')}.-
*HORA:* {hora_demora}.-
*Lugar :* {lugar.upper()} .-
*Jurisdicción:* {jurisdiccion.upper()} .-

*PERSONAL:* {actuante_ap.upper()} {actuante_nom.upper()} .-
{refuerzo_ap.upper()} {refuerzo_nom.upper()} .-
*Móvil:* {movil}

*DEMORADO:* {apellido.upper()} {nombre.upper()} .-
*ESTADO CIVIL:* {est_civil}.-
*EDAD:* {edad}
*DNI:* {dni}
*DOMICILIO:* {domicilio.upper()}.-

*ENTREGADO EN CRIA:* {jurisdiccion.upper()}, {estado_fisico}.-

*Recibe:* {of_recibe}.-

*Acta N• {acta_nro}.-*

*redacto:* {redacta_wa}"""

st.divider()
if st.button("📄 GENERAR ACTA PDF"):
    if apellido and actuante_ap:
        st.download_button("⬇️ DESCARGAR ARCHIVO", data=generar_pdf_espejo(), file_name=f"10Bis_{apellido}.pdf")

st.subheader("📲 Parte WhatsApp")
st.code(resumen_wa, language="text")

import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuración de la App
st.set_page_config(page_title="ACTA DE DEMORA ART 10 BIS LEY 7.395", page_icon="👮")

# --- MEMORIA DEL SISTEMA (Session State) ---
# Esto evita que los datos se borren al tocar botones
campos = [
    'unidad', 'tercio', 'movil', 'jurisdiccion', 'lugar', 'hora_demora', 'acta_nro',
    'apellido', 'nombre', 'dni', 'nacionalidad', 'est_civil', 'edad', 'nacimiento', 
    'domicilio', 'padres', 'actuante_ap', 'actuante_nom', 'refuerzo_ap', 'refuerzo_nom',
    'testigo_datos', 'requisa', 'secuestro', 'estado_fisico', 'motivo_final', 'of_recibe', 'redacta_wa'
]

for campo in campos:
    if campo not in st.session_state:
        st.session_state[campo] = ""

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
    if seleccion_u == "OTRO":
        st.session_state.unidad = col1.text_input("Especifique Unidad", value=st.session_state.unidad)
    else:
        st.session_state.unidad = seleccion_u
        
    st.session_state.tercio = col2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    st.session_state.movil = st.text_input("Móvil / Legajo", value=st.session_state.movil if st.session_state.movil else "12.116")
    st.session_state.jurisdiccion = st.text_input("Jurisdicción de entrega", value=st.session_state.jurisdiccion if st.session_state.jurisdiccion else "SUB 18")
    st.session_state.lugar = st.text_input("Lugar de la demora", value=st.session_state.lugar)
    st.session_state.hora_demora = st.text_input("Hora de la demora", value=st.session_state.hora_demora if st.session_state.hora_demora else datetime.now().strftime('%H:%M'))
    st.session_state.acta_nro = st.text_input("Acta Nº", value=st.session_state.acta_nro)

with tab2:
    col_a, col_b = st.columns(2)
    st.session_state.apellido = col_a.text_input("Apellido/s del demorado", value=st.session_state.apellido)
    st.session_state.nombre = col_b.text_input("Nombre/s del demorado", value=st.session_state.nombre)
    st.session_state.dni = st.text_input("DNI", value=st.session_state.dni)
    st.session_state.nacionalidad = st.text_input("Nacionalidad", value=st.session_state.nacionalidad if st.session_state.nacionalidad else "Argentina")
    st.session_state.est_civil = st.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "CONCUBINATO"])
    st.session_state.edad = st.text_input("Edad", value=st.session_state.edad)
    st.session_state.nacimiento = st.text_input("Fecha de Nacimiento", value=st.session_state.nacimiento)
    st.session_state.domicilio = st.text_input("Domicilio Real", value=st.session_state.domicilio)
    st.session_state.padres = st.text_input("Hijo de (Padre y Madre)", value=st.session_state.padres)

with tab3:
    st.session_state.actuante_ap = st.text_input("Apellido Funcionario Actuante", value=st.session_state.actuante_ap)
    st.session_state.actuante_nom = st.text_input("Nombre Funcionario Actuante", value=st.session_state.actuante_nom)
    st.session_state.refuerzo_ap = st.text_input("Apellido Funcionario Refuerzo", value=st.session_state.refuerzo_ap)
    st.session_state.refuerzo_nom = st.text_input("Nombre Funcionario Refuerzo", value=st.session_state.refuerzo_nom)
    st.session_state.testigo_datos = st.text_area("Datos del Testigo", value=st.session_state.testigo_datos)
    st.session_state.requisa = st.text_area("Resultado de la Requisa:", value=st.session_state.requisa if st.session_state.requisa else "NEGATIVO (No se hallan elementos de peligrosidad)")
    st.session_state.secuestro = st.text_area("Se le secuestra en carácter de depósito:", value=st.session_state.secuestro)

with tab4:
    opciones_fisicas = [
        "No presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia.",
        "Presenta lesiones de vieja data y no requirieron atención médica.",
        "Presenta lesiones que motivaron su traslado previo a un centro de salud para lo cual se anexa certificado médico."
    ]
    st.session_state.estado_fisico = st.selectbox("Estado físico del demorado:", opciones_fisicas)
    
    opciones_motivos = [
        "Se detecta al masculino ocultándose de la visual de la prevención.",
        "El individuo cambia bruscamente su sentido de marcha e intenta evitar contacto.",
        "Se observa al mismo apostado de forma prolongada, brindando versiones contradictorias.",
        "OTRO (Manual)"
    ]
    seleccion_motivo = st.selectbox("Motivo de la demora:", opciones_motivos)
    if seleccion_motivo == "OTRO (Manual)":
        st.session_state.motivo_final = st.text_area("Detalle el motivo manualmente:", value=st.session_state.motivo_final)
    else:
        st.session_state.motivo_final = seleccion_motivo
    
    st.session_state.of_recibe = st.text_input("Oficial de Guardia que recibe", value=st.session_state.of_recibe if st.session_state.of_recibe else "suboficial Rodriguez (M)")
    st.session_state.redacta_wa = st.text_input("Redactó (Solo para WhatsApp)", value=f"SubOf. {st.session_state.actuante_ap}")

# --- LÓGICA DE PDF ---
def generar_pdf_espejo():
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=30, top=30, right=15)
    pdf.add_page()
    
    ahora = datetime.now()
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(165, 10, "ACTA DE DEMORA ART 10 BIS LEY 7.395", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    
    intro_txt = (f"En la ciudad de ROSARIO, departamento Rosario de la provincia de Santa Fe, a los {ahora.day} días del mes de {meses[ahora.month-1]} del año {ahora.year}, "
                 f"siendo las {st.session_state.hora_demora} hs, el funcionario policial actuante {st.session_state.actuante_ap.upper()} {st.session_state.actuante_nom.upper()} a cargo de la unidad móvil {st.session_state.movil} juntamente como refuerzo {st.session_state.refuerzo_ap.upper()} {st.session_state.refuerzo_nom.upper()}, "
                 f"ambos pertenecientes a {st.session_state.unidad} de la UR II Rosario, a los fines legales que diera a lugar se hace CONSTAR: Que de conformidad a lo establecido en el Art. 10 bis de la "
                 f"Ley Orgánica de Policial de la Provincia de Santa Fe N° 7395 se procede a DEMORAR a las {st.session_state.hora_demora} horas, desde calle {st.session_state.lugar.upper()} al cual manifiesta ser "
                 f"{st.session_state.apellido.upper()} {st.session_state.nombre.upper()}, DNI {st.session_state.dni}, de nacionalidad {st.session_state.nacionalidad.upper()}, domicilio en la calle {st.session_state.domicilio.upper()} de esta ciudad, hijo de {st.session_state.padres.upper()}, "
                 f"fecha de nacimiento {st.session_state.nacimiento} contando con {st.session_state.edad} años de edad. Adoptándose esta medida por el motivo de que ante la presencia policial: {st.session_state.motivo_final.upper()}.")

    pdf.multi_cell(165, 9, intro_txt, align='J')
    pdf.ln(4)

    legal_text = ("Razón para lo cual y para la constancia de su identidad con el registro policial en los términos y alcances del Art. 10 Bis Ley 7395/75, introducida por Ley 11.516/97 y Resol. 0745/16. "
                  "A continuación se imponen al demorado, sus derechos y garantías establecidos por Ley a saber: a) Que será demorado en el lugar y trasladado a dependencia; b) Que la demora podrá prolongarse "
                  "hasta constatar su identificación con el registro policial, sin que esta supere las SEIS (6) HORAS corridas contadas desde el inicio de la medida; c) Que en ningún momento ha de ser incomunicado; "
                  "d) Que tiene derecho a efectuar una llamada telefónica tendiente a plantear su situación y a fin de colaborar en su individualización e identidad personal; e) Que en caso de ser trasladado a dependencia "
                  "policial no será alojado con detenidos por delitos o contravenciones; f) Que se procede a labrar acta ad-hoc con testigos del procedimiento. Siendo estos los llamados: " + st.session_state.testigo_datos.upper() + ".")
    pdf.multi_cell(165, 9, legal_text, align='J')
    pdf.ln(4)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.multi_cell(165, 9, f"REQUISA: {st.session_state.requisa.upper()}", border=1, align='J')
    pdf.multi_cell(165, 9, f"SECUESTRO EN DEPÓSITO: {st.session_state.secuestro.upper()}", border=1, align='J')
    pdf.set_font('Arial', '', 12)
    pdf.ln(4)
    
    pdf.multi_cell(165, 9, f"Se deja constancia que el demorado {st.session_state.estado_fisico.lower()}", align='J')
    pdf.ln(4)
    
    pdf.multi_cell(165, 9, f"Se hace constar que se labra la presente en recibiendo de conformidad {st.session_state.of_recibe.upper()} en carácter de oficial de guardia. Con lo que no siendo para más se da por finalizado el presente acto del cual firman los testigos, demorado y el personal actuante para su debida constancia.", align='J')
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(165, 10, "HORA DE CESE: _________ hs. :-", ln=True)

    # Firmas
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

# --- PARTE WHATSAPP ---
resumen_wa = f"""*{st.session_state.unidad} - {st.session_state.tercio}*
*ACTA DE DEMORA ART 10 BIS LEY 7.395*

*FECHA:* {datetime.now().strftime('%d/%m/%Y')}.-
*HORA:* {st.session_state.hora_demora}.-
*Lugar :* {st.session_state.lugar.upper()} .-
*Jurisdicción:* {st.session_state.jurisdiccion.upper()} .-

*PERSONAL:* {st.session_state.actuante_ap.upper()} {st.session_state.actuante_nom.upper()} .-
{st.session_state.refuerzo_ap.upper()} {st.session_state.refuerzo_nom.upper()} .-
*Móvil:* {st.session_state.movil}

*DEMORADO:* {st.session_state.apellido.upper()} {st.session_state.nombre.upper()} .-
*ESTADO CIVIL:* {st.session_state.est_civil}.-
*EDAD:* {st.session_state.edad}
*DNI:* {st.session_state.dni}
*DOMICILIO:* {st.session_state.domicilio.upper()}.-

*ENTREGADO EN CRIA:* {st.session_state.jurisdiccion.upper()}, {st.session_state.estado_fisico}.-

*Recibe:* {st.session_state.of_recibe}.-

*Acta N• {st.session_state.acta_nro}.-*

*redacto:* {st.session_state.redacta_wa}"""

st.divider()
if st.button("📄 GENERAR ACTA PDF"):
    if st.session_state.apellido and st.session_state.actuante_ap:
        st.download_button("⬇️ DESCARGAR ARCHIVO", data=generar_pdf_espejo(), file_name=f"10Bis_{st.session_state.apellido}.pdf")

st.subheader("📲 Parte WhatsApp")
st.code(resumen_wa, language="text")

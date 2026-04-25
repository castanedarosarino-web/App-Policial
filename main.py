import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="ACTA DE DEMORA ART 10 BIS LEY 7.395", page_icon="👮", layout="wide")

# --- INICIALIZACIÓN DE MEMORIA ---
if 'historial' not in st.session_state:
    st.session_state.historial = []

# --- FORMULARIO PRINCIPAL ---
st.title("👮 ACTA DE DEMORA ART 10 BIS LEY 7.395")
st.subheader("Creado por: Sub Comisario CASTAÑEDA JUAN")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Testigo/Requisa", "📄 Generar y WhatsApp", "🗂️ Historial"])

with tab1:
    col1, col2 = st.columns(2)
    unidad = col1.selectbox("Unidad", ["G.T.M.", "C.R.E. ROSARIO", "B.O.U.", "P.A.T.", "OTRO"])
    tercio = col2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    movil = st.text_input("Móvil / Legajo", value="12.116")
    jurisdiccion = st.text_input("Jurisdicción de entrega", value="SUB 18")
    lugar = st.text_input("Lugar del procedimiento")
    hora_demora = st.text_input("Hora de inicio", value=datetime.now().strftime('%H:%M'))
    acta_nro = st.text_input("Acta Nº")

with tab2:
    ca, cb = st.columns(2)
    apellido = ca.text_input("Apellido/s")
    nombre = cb.text_input("Nombre/s")
    dni = st.text_input("DNI")
    nacionalidad = st.text_input("Nacionalidad", value="ARGENTINA")
    est_civil = st.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "CONCUBINATO"])
    edad = st.text_input("Edad")
    nacimiento = st.text_input("Fecha de Nacimiento")
    domicilio = st.text_input("Domicilio Real")
    padres = st.text_input("Hijo de (Filiación)")

with tab3:
    actuante_ap = st.text_input("Ap. Actuante", value="CASTAÑEDA")
    actuante_nom = st.text_input("Nom. Actuante", value="JUAN")
    refuerzo_ap = st.text_input("Ap. Refuerzo")
    refuerzo_nom = st.text_input("Nom. Refuerzo")
    testigo_datos = st.text_area("Testigos", value="SIENDO EL MISMO EL PERSONAL ACTUANTE ANTE LA URGENCIA Y FALTA DE COLABORACIÓN DE TERCEROS")
    requisa = st.text_area("Resultado de la Requisa", value="palpado preventivo sobre sus prendas no hallando elementos de peligrosidad")
    secuestro = st.text_area("Elementos secuestrados", value="pertenencias personales")

with tab4:
    estado_fisico = st.selectbox("Estado físico:", [
        "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
        "presenta lesiones de vieja data y no requirieron atención médica",
        "presenta lesiones que motivaron su traslado previo a un centro de salud"
    ])
    
    motivo_opciones = [
        "EL INDIVIDUO CAMBIA BRUSCAMENTE SU SENTIDO DE MARCHA AL NOTAR LA PRESENCIA POLICIAL E INTENTA EVITAR CONTACTO, Y AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO.",
        "SE DETECTA AL MASCULINO OCULTÁNDOSE DE LA VISUAL DE LA PREVENCIÓN Y, AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO.",
        "OTRO (Manual)"
    ]
    motivo_sel = st.selectbox("Motivo observado:", motivo_opciones)
    if motivo_sel == "OTRO (Manual)":
        motivo_final = st.text_area("Redacción del motivo:")
    else:
        motivo_final = motivo_sel

    of_recibe = st.text_input("Oficial de Guardia que recibe", value="SUBOFICIAL RODRIGUEZ (M)")

    # --- LÓGICA DE PDF ---
    def generar_pdf():
        pdf = FPDF()
        pdf.set_margins(left=30, top=30, right=20)
        pdf.add_page()
        ahora = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(160, 10, "ACTA DE DEMORA ART 10 BIS LEY 7.395", ln=True, align='C')
        pdf.set_font('Arial', 'I', 8)
        pdf.cell(160, 5, "Creado por: Sub Comisario CASTAÑEDA JUAN", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 11)
        cuerpo = (
            f"En la ciudad de ROSARIO, departamento Rosario de la provincia de Santa Fe, a los {ahora.day} días del mes de {meses[ahora.month-1]} del año {ahora.year}, "
            f"siendo las {hora_demora} hs, el funcionario policial actuante {actuante_ap.upper()} {actuante_nom.upper()} "
            f"a cargo de la unidad móvil {movil} juntamente con el refuerzo {refuerzo_ap.upper()} {refuerzo_nom.upper()}, "
            f"ambos pertenecientes a {unidad} de la UR II Rosario, SE HACE CONSTAR: Que de conformidad a lo establecido en el "
            f"Art. 10 bis de la Ley Orgánica de Policial de la Provincia de Santa Fe N° 7395 se procede a DEMORAR a las {hora_demora} horas, "
            f"desde calle {lugar.upper()} al cual manifiesta ser {apellido.upper()} {nombre.upper()}, "
            f"DNI {dni}, de nacionalidad {nacionalidad.upper()}, estado civil {est_civil}, nacido el {nacimiento}, "
            f"contando con {edad} años de edad, hijo de {padres.upper()}, con domicilio real en la calle {domicilio.upper()} "
            f"de esta ciudad. Adoptándose esta medida por el motivo de que ante la presencia policial: {motivo_final.upper()}. "
            f"A continuación se le imponen al demorado sus derechos y garantías: a) será trasladado a la dependencia; b) la demora no superará las SEIS (6) HORAS; "
            f"c) no será incomunicado; d) tiene derecho a realizar una llamada telefónica; e) no será alojado con detenidos comunes; f) se labra la presente acta ante los testigos: "
            f"{testigo_datos.upper()}. Se hace constar que de la requisa efectuada sobre el demorado la misma arrojó resultado {requisa.upper()}. "
            f"Es dable hacer mención que se le secuestra en carácter de depósito para su resguardo: {secuestro.upper()}. "
            f"Se deja constancia que el demorado {estado_fisico}. Se hace constar que se labra la presente en recibiendo de conformidad "
            f"{of_recibe.upper()} en carácter de oficial de guardia. Con lo que no siendo para más se da por finalizado el presente acto."
        )
        pdf.multi_cell(160, 7, cuerpo.encode('latin-1', 'replace').decode('latin-1'), align='J')
        pdf.ln(15)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(160, 10, "HORA DE CESE: __________ hs.", ln=True)
        return pdf.output(dest='S')

    st.divider()
    if apellido:
        st.download_button("📄 DESCARGAR ACTA PDF", data=generar_pdf(), file_name=f"10Bis_{apellido}.pdf", mime="application/pdf")
    
    # --- ESPEJO WHATSAPP ---
    st.subheader("📲 Espejo para WhatsApp")
    res_wa = f"""*🚔 {unidad}* | *ACTA 10 BIS*
*HORA:* {hora_demora} hs.
*LUGAR:* {lugar.upper()}

*👤 DEMORADO:*
*IDENTIDAD:* **{apellido.upper()} {nombre.upper()}**
*DNI:* **{dni}**
*DOMICILIO:* {domicilio.upper()}

*📝 PROCEDIMIENTO:*
*MOTIVO:* {motivo_final.upper()}
*SECUESTRO:* **{secuestro.upper()}**
*RECIBE:* **{of_recibe.upper()}**
*Acta N• {acta_nro}*

👮 *PERSONAL:* {actuante_ap.upper()}"""
    st.code(res_wa)

with tab5:
    st.write("Registros guardados en esta sesión.")

import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="ACTA DE DEMORA ART 10 BIS LEY 7.395", page_icon="👮", layout="wide")

# --- INICIALIZACIÓN DE MEMORIA ---
campos_base = {
    'unidad': "G.T.M.", 'tercio': "TERCIO ALPHA", 'movil': "12.116", 'jurisdiccion': "SUB 18",
    'lugar': "", 'hora_demora': datetime.now().strftime('%H:%M'), 'acta_nro': "",
    'apellido': "", 'nombre': "", 'dni': "", 'nacionalidad': "ARGENTINA",
    'est_civil': "SOLTERO/A", 'edad': "", 'nacimiento': "", 'domicilio': "", 'padres': "",
    'actuante_ap': "CASTAÑEDA", 'actuante_nom': "JUAN", 'refuerzo_ap': "", 'refuerzo_nom': "",
    'testigo_datos': "", 'requisa': "PALPADO PREVENTIVO SOBRE SUS PRENDAS NO HALLANDO ELEMENTOS DE PELIGROSIDAD", 
    'secuestro': "PERTENENCIAS PERSONALES", 
    'estado_fisico': "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
    'motivo_unico': "", 'of_recibe': "SUBOFICIAL RODRIGUEZ (M)"
}

for clave, valor in campos_base.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor

if 'historial' not in st.session_state:
    st.session_state.historial = []

# --- CABECERA ---
st.markdown(f"""
    <div style='text-align: center; background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: 2px solid #1E3A8A;'>
        <h1 style='margin-bottom: 0; color: #1E3A8A;'>ACTA DE DEMORA ART 10 BIS LEY 7.395</h1>
        <p style='font-size: 1.2em; font-weight: bold; color: #1E3A8A; margin-top: 5px;'>Creado por: Sub Comisario CASTAÑEDA JUAN</p>
    </div>
    """, unsafe_allow_html=True)

tabs = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Testigo/Requisa", "✍️ Cierre y WhatsApp", "🗂️ Historial"])

with tabs[0]:
    c1, c2 = st.columns(2)
    st.session_state.unidad = c1.text_input("Unidad Policial", value=st.session_state.unidad)
    st.session_state.tercio = c2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    st.session_state.movil = c1.text_input("Móvil / Legajo", value=st.session_state.movil)
    st.session_state.jurisdiccion = c2.text_input("Dependencia de entrega", value=st.session_state.jurisdiccion)
    st.session_state.lugar = st.text_input("Lugar del procedimiento", value=st.session_state.lugar)
    st.session_state.hora_demora = st.text_input("Hora de inicio", value=st.session_state.hora_demora)
    st.session_state.acta_nro = st.text_input("Acta Nº", value=st.session_state.acta_nro)

with tabs[1]:
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

with tabs[2]:
    st.session_state.actuante_ap = st.text_input("Ap. Actuante", value=st.session_state.actuante_ap)
    st.session_state.actuante_nom = st.text_input("Nom. Actuante", value=st.session_state.actuante_nom)
    st.session_state.refuerzo_ap = st.text_input("Ap. Refuerzo", value=st.session_state.refuerzo_ap)
    st.session_state.refuerzo_nom = st.text_input("Nom. Refuerzo", value=st.session_state.refuerzo_nom)
    st.session_state.testigo_datos = st.text_area("Testigos (Nombre, DNI, Domicilio)", value=st.session_state.testigo_datos)
    st.session_state.requisa = st.text_area("Resultado de la Requisa", value=st.session_state.requisa)
    st.session_state.secuestro = st.text_area("Elementos en depósito", value=st.session_state.secuestro)

with tabs[3]:
    st.session_state.estado_fisico = st.selectbox("Estado físico:", [
        "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
        "presenta lesiones de vieja data y no requirieron atención médica",
        "presenta lesiones que motivaron su traslado previo a un centro de salud"
    ])

    st.session_state.motivo_unico = st.text_area("Motivo de la demora:", value=st.session_state.motivo_unico)
    st.session_state.of_recibe = st.text_input("Oficial que recibe", value=st.session_state.of_recibe)

    # --- FUNCIÓN GENERADORA DE PDF ---
    def generar_pdf_oficial():
        pdf = FPDF()
        pdf.set_margins(left=30, top=30, right=20)
        pdf.add_page()
        ahora = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(0, 10, "ACTA DE DEMORA ART 10 BIS LEY 7.395", align='C', ln=1)
        pdf.ln(5)

        pdf.set_font('helvetica', '', 11)
        cuerpo = (
            f"En la ciudad de ROSARIO, departamento Rosario de la provincia de Santa Fe, a los {ahora.day} días del mes de {meses[ahora.month-1]} del año {ahora.year}, "
            f"siendo las {st.session_state.hora_demora} hs, el funcionario policial actuante {st.session_state.actuante_ap.upper()} {st.session_state.actuante_nom.upper()} "
            f"a cargo de la unidad móvil {st.session_state.movil} juntamente con el refuerzo {st.session_state.refuerzo_ap.upper()} {st.session_state.refuerzo_nom.upper()}, "
            f"ambos pertenecientes a {st.session_state.unidad.upper()} de la UR II Rosario, SE HACE CONSTAR: Que de conformidad a lo establecido en el "
            f"Art. 10 bis de la Ley Orgánica de Policial de la Provincia de Santa Fe N° 7395 se procede a DEMORAR a las {st.session_state.hora_demora} horas, "
            f"desde calle {st.session_state.lugar.upper()} al cual manifiesta ser {st.session_state.apellido.upper()} {st.session_state.nombre.upper()}, "
            f"DNI {st.session_state.dni}, de nacionalidad {st.session_state.nacionalidad.upper()}, estado civil {st.session_state.est_civil}, nacido el {st.session_state.nacimiento}, "
            f"contando con {st.session_state.edad} años de edad, hijo de {st.session_state.padres.upper()}, con domicilio real en la calle {st.session_state.domicilio.upper()} "
            f"de esta ciudad. Adoptándose esta medida por el motivo de que ante la presencia policial: {st.session_state.motivo_unico.upper()}. "
            f"A continuación se le imponen al demorado sus derechos y garantías: a) será trasladado a la dependencia; b) la demora no superará las SEIS (6) HORAS; "
            f"c) no será incomunicado; d) tiene derecho a realizar una llamada

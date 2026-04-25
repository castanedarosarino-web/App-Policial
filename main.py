import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="ACTA DE DEMORA ART 10 BIS LEY 7.395", page_icon="👮", layout="wide")

# --- INICIALIZACIÓN DE VARIABLES ---
if 'historial' not in st.session_state:
    st.session_state.historial = []

campos_iniciales = {
    'unidad': "G.T.M.", 'movil': "12.116", 'jurisdiccion': "SUB 18",
    'lugar': "", 'hora_demora': datetime.now().strftime('%H:%M'), 'acta_nro': "",
    'apellido': "", 'nombre': "", 'dni': "", 'nacionalidad': "ARGENTINA",
    'est_civil': "SOLTERO/A", 'edad': "", 'nacimiento': "", 'domicilio': "", 'padres': "",
    'actuante_ap': "CASTAÑEDA", 'actuante_nom': "JUAN", 'refuerzo_ap': "", 'refuerzo_nom': "",
    'testigo_datos': "", 'requisa': "PALPADO PREVENTIVO SOBRE SUS PRENDAS NO HALLANDO ELEMENTOS DE PELIGROSIDAD", 
    'secuestro': "PERTENENCIAS PERSONALES", 'estado_fisico': "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
    'motivo_unico': "", 'of_recibe': "SUBOFICIAL RODRIGUEZ (M)"
}

for clave, valor in campos_iniciales.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor

# --- CABECERA ---
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='margin-bottom: 0;'>ACTA DE DEMORA ART 10 BIS LEY 7.395</h1>
        <p style='font-size: 1.2em; font-weight: bold; color: #1E3A8A; margin-top: 5px;'>Creado por: Sub Comisario CASTAÑEDA JUAN</p>
    </div>
    """, unsafe_allow_html=True)

tabs = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Testigo/Requisa", "✍️ Cierre", "🗂️ Historial"])

with tabs[0]:
    c1, c2 = st.columns(2)
    st.session_state.unidad = c1.text_input("Unidad", value=st.session_state.unidad)
    st.session_state.movil = c2.text_input("Móvil / Legajo", value=st.session_state.movil)
    st.session_state.jurisdiccion = c1.text_input("Jurisdicción de entrega", value=st.session_state.jurisdiccion)
    st.session_state.lugar = c2.text_input("Lugar del procedimiento", value=st.session_state.lugar)
    st.session_state.hora_demora = c1.text_input("Hora de Inicio", value=st.session_state.hora_demora)
    st.session_state.acta_nro = c2.text_input("Acta N°", value=st.session_state.acta_nro)

with tabs[1]:
    st.session_state.apellido = st.text_input("Apellido/s", value=st.session_state.apellido)
    st.session_state.nombre = st.text_input("Nombre/s", value=st.session_state.nombre)
    c3, c4 = st.columns(2)
    st.session_state.dni = c3.text_input("DNI", value=st.session_state.dni)
    st.session_state.nacionalidad = c4.text_input("Nacionalidad", value=st.session_state.nacionalidad)
    st.session_state.nacimiento = c3.text_input("Fecha de Nacimiento", value=st.session_state.nacimiento)
    st.session_state.edad = c4.text_input("Edad", value=st.session_state.edad)
    st.session_state.domicilio = st.text_input("Domicilio Real", value=st.session_state.domicilio)
    st.session_state.padres = st.text_input("Filiación (Hijo de...)", value=st.session_state.padres)

with tabs[2]:
    c5, c6 = st.columns(2)
    st.session_state.actuante_ap = c5.text_input("Ap. Actuante", value=st.session_state.actuante_ap)
    st.session_state.actuante_nom = c6.text_input("Nom. Actuante", value=st.session_state.actuante_nom)
    st.session_state.refuerzo_ap = c5.text_input("Ap. Refuerzo", value=st.session_state.refuerzo_ap)
    st.session_state.refuerzo_nom = c6.text_input("Nom. Refuerzo", value=st.session_state.refuerzo_nom)
    st.session_state.testigo_datos = st.text_area("Datos de los Testigos", value=st.session_state.testigo_datos)
    st.session_state.requisa = st.text_area("Resultado de la Requisa", value=st.session_state.requisa)
    st.session_state.secuestro = st.text_area("Elementos en Depósito/Secuestro", value=st.session_state.secuestro)

with tabs[3]:
    st.session_state.estado_fisico = st.selectbox("Estado físico del demorado:", [
        "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
        "presenta lesiones de vieja data y no requirieron atención médica",
        "presenta lesiones que motivaron su traslado previo a un centro de salud"
    ])
    st.session_state.motivo_unico = st.text_area("Motivo observado de la demora", value=st.session_state.motivo_unico)
    st.session_state.of_recibe = st.text_input("Oficial de Guardia que recibe", value=st.session_state.of_recibe)

    def generar_acta_pdf():
        pdf = FPDF()
        pdf.set_margins(left=30, top=30, right=20)
        pdf.add_page()
        ahora = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(0, 10, "ACTA DE DEMORA ART 10 BIS LEY 7.395", align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

        pdf.set_font('helvetica', '', 11)
        # Redacción formal espejo del modelo legal
        texto_acta = (
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
            f"c) no será incomunicado; d) tiene derecho a realizar una llamada telefónica; e) no será alojado con detenidos comunes; f) se labra la presente acta ante los testigos: "
            f"{st.session_state.testigo_datos.upper()}. Se hace constar que de la requisa efectuada sobre el demorado la misma arrojó resultado {st.session_state.requisa.upper()}. "
            f"Es dable hacer mención que se le secuestra en carácter de depósito para su resguardo: {st.session_state.secuestro.upper()}. "
            f"Se deja constancia que el demorado {st.session_state.estado_fisico}. Se hace constar que se labra la presente en recibiendo de conformidad "
            f"{st.session_state.of_recibe.upper()} en carácter de oficial de guardia. Con lo que no siendo para más se da por finalizado el presente acto del cual "
            f"firman los testigos, demorado y el personal actuante para su debida constancia."
        )

        pdf.multi_cell(0, 7, texto_acta, align='J')

        pdf.ln(20)
        pdf.cell(0, 10, "____________________                 _____________________               ___________________", align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(60, 5, "PERSONAL ACTUANTE", align='C')
        pdf.cell(60, 5, "DEMORADO", align='C')
        pdf.cell(60, 5, "OF. GUARDIA", align='C')
        
        return bytes(pdf.output())

    # Descarga del PDF corregido para evitar errores de Streamlit
    pdf_bytes = generar_acta_pdf()
    st.download_button(
        label="📄 DESCARGAR ACTA PDF",
        data=pdf_bytes,
        file_name=f"Acta_10Bis_{st.session_state.apellido}.pdf",
        mime="application/pdf"
    )

    if st.button("💾 Guardar Registro"):
        st.session_state.historial.append({k: st.session_state[k] for k in campos_iniciales.keys()})
        st.success("Registro guardado con éxito.")

with tabs[4]:
    st.subheader("Historial de la sesión")
    if not st.session_state.historial:
        st.info("No hay registros en esta sesión.")
    else:
        for i, reg in enumerate(reversed(st.session_state.historial)):
            if st.button(f"Cargar Acta: {reg['apellido']} - {reg['acta_nro']}", key=i):
                for k in campos_iniciales.keys(): st.session_state[k] = reg[k]
                st.rerun()

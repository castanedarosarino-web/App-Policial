import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuración de la App
st.set_page_config(page_title="ACTA DE DEMORA ART 10 BIS LEY 7.395", page_icon="👮", layout="wide")

# --- INICIALIZACIÓN DE MEMORIA (Session State) ---
campos_base = {
    'unidad': "G.T.M.", 'tercio': "TERCIO ALPHA", 'movil': "12.116", 'jurisdiccion': "SUB 18",
    'lugar': "", 'hora_demora': datetime.now().strftime('%H:%M'), 'acta_nro': "",
    'apellido': "", 'nombre': "", 'dni': "", 'nacionalidad': "Argentina",
    'est_civil': "SOLTERO/A", 'edad': "", 'nacimiento': "", 'domicilio': "", 'padres': "",
    'actuante_ap': "", 'actuante_nom': "", 'refuerzo_ap': "", 'refuerzo_nom': "",
    'testigo_datos': "", 'requisa': "NEGATIVO (No se hallan elementos de peligrosidad)", 
    'secuestro': "", 'estado_fisico': "No presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia.",
    'motivo_final': "", 'of_recibe': "suboficial Rodriguez (M)", 'redacta_wa': ""
}

for clave, valor in campos_base.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor

if 'historial' not in st.session_state:
    st.session_state.historial = []

# --- FUNCIONES ---
def guardar_en_historial():
    registro = {clave: st.session_state[clave] for clave in campos_base.keys()}
    registro['fecha_registro'] = datetime.now().strftime('%H:%M:%S')
    st.session_state.historial.append(registro)
    st.success(f"✅ Datos de {st.session_state.apellido} guardados.")

def recuperar_registro(index):
    registro = st.session_state.historial[index]
    for clave in campos_base.keys():
        st.session_state[clave] = registro[clave]
    st.rerun()

# --- ESTILOS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; font-weight: bold; border-radius: 10px; height: 3em; background-color: #f0f2f6; }
    .autor-text { font-size: 11px; color: #777; margin-top: -20px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("👮 ACTA DE DEMORA ART 10 BIS LEY 7.395")
st.markdown('<p class="autor-text">creado: Sub Crio Castañeda Juan</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Testigo/Requisa", "✍️ Cierre y WhatsApp", "🗂️ Historial"])

with tab1:
    col1, col2 = st.columns(2)
    u_opciones = ["G.T.M.", "C.R.E. ROSARIO", "B.O.U.", "P.A.T.", "OTRO"]
    idx_u = u_opciones.index(st.session_state.unidad) if st.session_state.unidad in u_opciones else 4
    u_sel = col1.selectbox("Unidad", u_opciones, index=idx_u)
    if u_sel == "OTRO":
        st.session_state.unidad = col1.text_input("Especifique Unidad", value=st.session_state.unidad)
    else:
        st.session_state.unidad = u_sel
    st.session_state.tercio = col2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    st.session_state.movil = st.text_input("Móvil / Legajo", value=st.session_state.movil)
    st.session_state.jurisdiccion = st.text_input("Jurisdicción de entrega", value=st.session_state.jurisdiccion)
    st.session_state.lugar = st.text_input("Lugar de la demora", value=st.session_state.lugar)
    st.session_state.hora_demora = st.text_input("Hora de inicio", value=st.session_state.hora_demora)
    st.session_state.acta_nro = st.text_input("Acta Nº", value=st.session_state.acta_nro)

with tab2:
    col_a, col_b = st.columns(2)
    st.session_state.apellido = col_a.text_input("Apellido/s", value=st.session_state.apellido)
    st.session_state.nombre = col_b.text_input("Nombre/s", value=st.session_state.nombre)
    st.session_state.dni = st.text_input("DNI", value=st.session_state.dni)
    st.session_state.nacionalidad = st.text_input("Nacionalidad", value=st.session_state.nacionalidad)
    st.session_state.est_civil = st.selectbox("Estado Civil", ["SOLTERO/A", "CASADO/A", "DIVORCIADO/A", "CONCUBINATO"])
    st.session_state.edad = st.text_input("Edad", value=st.session_state.edad)
    st.session_state.nacimiento = st.text_input("Fecha Nacimiento", value=st.session_state.nacimiento)
    st.session_state.domicilio = st.text_input("Domicilio Real", value=st.session_state.domicilio)
    st.session_state.padres = st.text_input("Hijo de", value=st.session_state.padres)

with tab3:
    st.session_state.actuante_ap = st.text_input("Ap. Actuante", value=st.session_state.actuante_ap)
    st.session_state.actuante_nom = st.text_input("Nom. Actuante", value=st.session_state.actuante_nom)
    st.session_state.refuerzo_ap = st.text_input("Ap. Refuerzo", value=st.session_state.refuerzo_ap)
    st.session_state.refuerzo_nom = st.text_input("Nom. Refuerzo", value=st.session_state.refuerzo_nom)
    st.session_state.testigo_datos = st.text_area("Datos del Testigo", value=st.session_state.testigo_datos)
    st.session_state.requisa = st.text_area("Resultado Requisa", value=st.session_state.requisa)
    st.session_state.secuestro = st.text_area("Elementos en Depósito", value=st.session_state.secuestro)

with tab4:
    # --- OPCIONES DE CIERRE ---
    st.session_state.estado_fisico = st.selectbox("Estado físico:", [
        "No presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia.",
        "Presenta lesiones de vieja data y no requirieron atención médica.",
        "Presenta lesiones que motivaron su traslado previo a un centro de salud para lo cual se anexa certificado médico."
    ])
    st.session_state.motivo_final = st.text_area("Motivo de la demora", value=st.session_state.motivo_final)
    st.session_state.of_recibe = st.text_input("Oficial de Guardia que recibe", value=st.session_state.of_recibe)
    st.session_state.redacta_wa = st.text_input("Firma WhatsApp", value=f"SubOf. {st.session_state.actuante_ap}")

    c1, c2 = st.columns(2)
    if c1.button("💾 GUARDAR EN HISTORIAL"): guardar_en_historial()
    if c2.button("🧹 LIMPIAR FORMULARIO"):
        for k, v in campos_base.items(): st.session_state[k] = v
        st.rerun()

    st.divider()
    
    # --- BOTÓN DE PDF (AHORA SIEMPRE VISIBLE) ---
    def generar_pdf():
        pdf = FPDF()
        pdf.set_margins(left=30, top=30, right=15)
        pdf.add_page()
        ahora = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(165, 10, "ACTA DE DEMORA ART 10 BIS LEY 7.395", ln=True, align='C')
        pdf.ln(5)
        pdf.set_font('Arial', '', 12)
        
        cuerpo = (f"En la ciudad de ROSARIO, departamento Rosario de la provincia de Santa Fe, a los {ahora.day} días del mes de {meses[ahora.month-1]} del año {ahora.year}, "
                  f"siendo las {st.session_state.hora_demora} hs, el funcionario policial actuante {st.session_state.actuante_ap.upper()} {st.session_state.actuante_nom.upper()} a cargo de la unidad móvil {st.session_state.movil} juntamente como refuerzo {st.session_state.refuerzo_ap.upper()} {st.session_state.refuerzo_nom.upper()}, "
                  f"ambos pertenecientes a {st.session_state.unidad} de la UR II Rosario, se hace CONSTAR: Que de conformidad a lo establecido en el Art. 10 bis de la "
                  f"Ley Orgánica de Policial de la Provincia de Santa Fe N° 7395 se procede a DEMORAR a las {st.session_state.hora_demora} horas, desde calle {st.session_state.lugar.upper()} al cual manifiesta ser "
                  f"{st.session_state.apellido.upper()} {st.session_state.nombre.upper()}, DNI {st.session_state.dni}, de nacionalidad {st.session_state.nacionalidad.upper()}, domicilio en la calle {st.session_state.domicilio.upper()} de esta ciudad, hijo de {st.session_state.padres.upper()}, "
                  f"fecha de nacimiento {st.session_state.nacimiento} contando con {st.session_state.edad} años de edad. Adoptándose esta medida por el motivo de que ante la presencia policial: {st.session_state.motivo_final.upper()}.")
        pdf.multi_cell(165, 9, cuerpo, align='J')
        pdf.ln(4)
        pdf.multi_cell(165, 9, ("A continuación se imponen al demorado sus derechos y garantías: a) será trasladado a dependencia; b) la demora no superará las SEIS (6) HORAS; c) no será incomunicado; d) derecho a una llamada; e) no será alojado con detenidos; f) testigos: " + st.session_state.testigo_datos.upper() + "."), align='J')
        pdf.ln(4)
        pdf.set_font('Arial', 'B', 12)
        pdf.multi_cell(165, 9, f"REQUISA: {st.session_state.requisa.upper()}", border=1)
        pdf.multi_cell(165, 9, f"SECUESTRO EN DEPÓSITO: {st.session_state.secuestro.upper()}", border=1)
        pdf.set_font('Arial', '', 12)
        pdf.ln(4)
        pdf.multi_cell(165, 9, f"Se deja constancia que el demorado {st.session_state.estado_fisico.lower()}")
        pdf.ln(10)
        pdf.cell(165, 10, "HORA DE CESE: _________ hs.", ln=True)
        return pdf.output(dest='S').encode('latin-1')

    # El botón ahora está fuera de condiciones complicadas
    st.download_button(
        label="📄 DESCARGAR ACTA EN PDF",
        data=generar_pdf(),
        file_name=f"10Bis_{st.session_state.apellido if st.session_state.apellido else 'DOC'}.pdf",
        mime="application/pdf"
    )

    st.subheader("📲 Parte WhatsApp")
    res_wa = f"""*{st.session_state.unidad} - {st.session_state.tercio}*
*ACTA DE DEMORA ART 10 BIS LEY 7.395*

*FECHA:* {datetime.now().strftime('%d/%m/%Y')}
*HORA:* {st.session_state.hora_demora}
*Lugar:* {st.session_state.lugar.upper()}
*Jurisdicción:* {st.session_state.jurisdiccion.upper()}

*PERSONAL:* {st.session_state.actuante_ap.upper()} / {st.session_state.refuerzo_ap.upper()}
*Móvil:* {st.session_state.movil}

*DEMORADO:* {st.session_state.apellido.upper()} {st.session_state.nombre.upper()}
*DNI:* {st.session_state.dni}
*DOMICILIO:* {st.session_state.domicilio.upper()}

*ENTREGADO EN CRIA:* {st.session_state.jurisdiccion.upper()}, {st.session_state.estado_fisico}

*Recibe:* {st.session_state.of_recibe}
*Acta N• {st.session_state.acta_nro}
*Redactó:* {st.session_state.redacta_wa}"""
    st.code(res_wa)

with tab5:
    st.subheader("🗂️ Historial")
    if not st.session_state.historial:
        st.write("No hay registros.")
    else:
        for i, reg in enumerate(reversed(st.session_state.historial)):
            real_idx = len(st.session_state.historial) - 1 - i
            c_h1, c_h2 = st.columns([4, 1])
            c_h1.write(f"📌 **{reg['apellido']}** ({reg['fecha_registro']} hs)")
            if c_h2.button("🔄 Recuperar", key=f"rec_{real_idx}"): recuperar_registro(real_idx)

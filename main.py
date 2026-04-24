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

# Crear los campos en la memoria si no existen
for clave, valor in campos_base.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor

if 'historial' not in st.session_state:
    st.session_state.historial = []

# --- FUNCIONES DE CONTROL ---
def guardar_en_historial():
    registro = {clave: st.session_state[clave] for clave in campos_base.keys()}
    registro['fecha_registro'] = datetime.now().strftime('%H:%M:%S')
    st.session_state.historial.append(registro)
    st.success(f"✅ Acta de {st.session_state.apellido} guardada en el historial.")

def recuperar_registro(index):
    registro = st.session_state.historial[index]
    for clave in campos_base.keys():
        st.session_state[clave] = registro[clave]
    st.info(f"🔄 Datos de {registro['apellido']} cargados en el formulario.")

def limpiar_formulario():
    for clave, valor in campos_base.items():
        st.session_state[clave] = valor
    st.rerun()

# --- INTERFAZ ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; font-weight: bold; border-radius: 10px; }
    .btn-guardar { background-color: #28a745; color: white; }
    .autor-text { font-size: 11px; color: #777; margin-top: -20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("👮 ACTA DE DEMORA ART 10 BIS LEY 7.395")
st.markdown('<p class="autor-text">creado: Sub Crio Castañeda Juan</p>', unsafe_allow_html=True)

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Testigo/Requisa", "✍️ Cierre y WhatsApp", "🗂️ Historial"])

with tab1:
    col1, col2 = st.columns(2)
    st.session_state.unidad = col1.selectbox("Unidad", ["G.T.M.", "C.R.E. ROSARIO", "B.O.U.", "P.A.T.", "OTRO"], index=0)
    st.session_state.tercio = col2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    st.session_state.movil = st.text_input("Móvil / Legajo", value=st.session_state.movil)
    st.session_state.jurisdiccion = st.text_input("Jurisdicción de entrega", value=st.session_state.jurisdiccion)
    st.session_state.lugar = st.text_input("Lugar de la demora", value=st.session_state.lugar)
    st.session_state.hora_demora = st.text_input("Hora", value=st.session_state.hora_demora)
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
    st.session_state.domicilio = st.text_input("Domicilio", value=st.session_state.domicilio)
    st.session_state.padres = st.text_input("Hijo de", value=st.session_state.padres)

with tab3:
    st.session_state.actuante_ap = st.text_input("Ap. Actuante", value=st.session_state.actuante_ap)
    st.session_state.actuante_nom = st.text_input("Nom. Actuante", value=st.session_state.actuante_nom)
    st.session_state.refuerzo_ap = st.text_input("Ap. Refuerzo", value=st.session_state.refuerzo_ap)
    st.session_state.refuerzo_nom = st.text_input("Nom. Refuerzo", value=st.session_state.refuerzo_nom)
    st.session_state.testigo_datos = st.text_area("Testigo", value=st.session_state.testigo_datos)
    st.session_state.requisa = st.text_area("Requisa", value=st.session_state.requisa)
    st.session_state.secuestro = st.text_area("Secuestro", value=st.session_state.secuestro)

with tab4:
    st.session_state.estado_fisico = st.selectbox("Estado físico:", [
        "No presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia.",
        "Presenta lesiones de vieja data y no requirieron atención médica.",
        "Presenta lesiones que motivaron su traslado previo a un centro de salud para lo cual se anexa certificado médico."
    ])
    st.session_state.motivo_final = st.text_area("Motivo de demora", value=st.session_state.motivo_final)
    st.session_state.of_recibe = st.text_input("Oficial recibe", value=st.session_state.of_recibe)
    st.session_state.redacta_wa = st.text_input("Redactó WA", value=f"SubOf. {st.session_state.actuante_ap}")

    # BOTONES DE ACCIÓN
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    if col_btn1.button("💾 GUARDAR EN HISTORIAL"):
        guardar_en_historial()
    
    if col_btn2.button("🧹 LIMPIAR TODO"):
        limpiar_formulario()

    # --- PDF GENERATOR ---
    def generar_pdf():
        pdf = FPDF()
        pdf.set_margins(left=30, top=30, right=15)
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(165, 10, "ACTA DE DEMORA ART 10 BIS LEY 7.395", ln=True, align='C')
        pdf.ln(5)
        pdf.set_font('Arial', '', 12)
        
        cuerpo = (f"En la ciudad de ROSARIO, a los {datetime.now().day} días del mes de {datetime.now().month}, "
                  f"siendo las {st.session_state.hora_demora} hs, el funcionario policial actuante {st.session_state.actuante_ap.upper()} {st.session_state.actuante_nom.upper()} "
                  f"en móvil {st.session_state.movil} con refuerzo {st.session_state.refuerzo_ap.upper()} {st.session_state.refuerzo_nom.upper()}, "
                  f"pertenecientes a {st.session_state.unidad}, procede a DEMORAR a {st.session_state.apellido.upper()} {st.session_state.nombre.upper()}, "
                  f"DNI {st.session_state.dni}, domiciliado en {st.session_state.domicilio.upper()}. Motivo: {st.session_state.motivo_final.upper()}.")
        
        pdf.multi_cell(165, 9, cuerpo, align='J')
        return pdf.output(dest='S').encode('latin-1')

    if st.session_state.apellido:
        st.download_button("📄 DESCARGAR PDF", data=generar_pdf(), file_name=f"Acta_{st.session_state.apellido}.pdf")

    st.subheader("📲 WhatsApp")
    resumen_wa = f"*ACTA 10 BIS* \n*DEMORADO:* {st.session_state.apellido} \n*DNI:* {st.session_state.dni} \n*ESTADO:* {st.session_state.estado_fisico}"
    st.code(resumen_wa)

with tab5:
    st.subheader("📚 Actas Cargadas en esta Sesión")
    if not st.session_state.historial:
        st.write("No hay actas guardadas todavía.")
    else:
        for i, reg in enumerate(reversed(st.session_state.historial)):
            idx_real = len(st.session_state.historial) - 1 - i
            col_hist1, col_hist2 = st.columns([3, 1])
            col_hist1.write(f"**{reg['apellido']}** - {reg['fecha_registro']} hs (DNI: {reg['dni']})")
            if col_hist2.button(f"Recuperar ##{idx_real}", key=f"btn_{idx_real}"):
                recuperar_registro(idx_real)
                st.rerun()

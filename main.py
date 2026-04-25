import streamlit as st
from docx import Document
from docx.shared import Pt, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
import io

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="ACTA DE DEMORA ART 10 BIS LEY 7.395", page_icon="👮", layout="wide")

# --- INICIALIZACIÓN DE MEMORIA ---
campos_base = {
    'unidad': "G.T.M.", 'movil': "12.116", 'lugar': "", 
    'hora_demora': datetime.now().strftime('%H:%M'),
    'apellido': "", 'nombre': "", 'dni': "", 'nacionalidad': "ARGENTINA",
    'est_civil': "SOLTERO/A", 'edad': "", 'nacimiento': "", 'domicilio': "", 'padres': "",
    'actuante_ap': "CASTANEDA", 'actuante_nom': "JUAN", 
    'refuerzo_ap': "", 'refuerzo_nom': "",
    'testigo_datos': "", 'requisa': "PALPADO PREVENTIVO SOBRE SUS PRENDAS NO HALLANDO ELEMENTOS DE PELIGROSIDAD", 
    'secuestro': "PERTENENCIAS PERSONALES", 
    'estado_fisico': "no presenta lesiones visibles, golpes ni manifiesta dolencias",
    'motivo_unico': "", 'of_recibe': "SUBOFICIAL RODRIGUEZ (M)"
}

for clave, valor in campos_base.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor

if 'historial' not in st.session_state:
    st.session_state.historial = []

# --- MOTOR DE GENERACIÓN WORD ---
def generar_word():
    doc = Document()
    section = doc.sections[0]
    section.left_margin, section.right_margin = Mm(30), Mm(20)
    section.top_margin, section.bottom_margin = Mm(25), Mm(25)

    titulo = doc.add_paragraph()
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t = titulo.add_run("ACTA DE DEMORA ART 10 BIS LEY 7.395")
    run_t.bold = True
    run_t.font.size, run_t.font.name = Pt(13), 'Arial'

    ahora = datetime.now()
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY 
    
    def agregar(texto, negrita=False):
        run = p.add_run(texto)
        run.bold = negrita
        run.font.name, run.font.size = 'Arial', Pt(11)

    agregar(f"En la ciudad de ROSARIO, a los {ahora.day} días del mes de {meses[ahora.month-1]} del año {ahora.year}, siendo las ")
    agregar(f"{st.session_state.hora_demora} hs", True)
    agregar(", el funcionario policial actuante ")
    agregar(f"{st.session_state.actuante_ap.upper()} {st.session_state.actuante_nom.upper()}", True)
    agregar(f" a cargo de la unidad móvil {st.session_state.movil} juntamente con el refuerzo ")
    agregar(f"{st.session_state.refuerzo_ap.upper()} {st.session_state.refuerzo_nom.upper()}", True)
    agregar(f", ambos pertenecientes a {st.session_state.unidad}, ")
    agregar("SE HACE CONSTAR: ", True)
    agregar("Que de conformidad a lo establecido en el ")
    agregar("Art. 10 bis de la Ley Orgánica de Policial de la Provincia de Santa Fe N° 7395", True)
    agregar(f" se procede a DEMORAR a las {st.session_state.hora_demora} horas, desde calle ")
    agregar(f"{st.session_state.lugar.upper()}", True)
    agregar(" al cual manifiesta ser ")
    agregar(f"{st.session_state.apellido.upper()} {st.session_state.nombre.upper()}, DNI {st.session_state.dni}", True)
    agregar(f", de nacionalidad {st.session_state.nacionalidad.upper()}, nacido el {st.session_state.nacimiento}, hijo de {st.session_state.padres.upper()}, con domicilio en {st.session_state.domicilio.upper()}. ")
    agregar("Motivo: ")
    agregar(f"{st.session_state.motivo_unico.upper()}. ", True)
    agregar("Derechos y garantías: a) traslado a dependencia; ")
    agregar("b) la demora no superará las SEIS (6) HORAS; ", True)
    agregar(f"c) no incomunicación; d) llamada telefónica; e) no alojamiento con detenidos comunes; f) testigos: {st.session_state.testigo_datos.upper()}. ")
    agregar("Requisa: ")
    agregar(f"{st.session_state.requisa.upper()}. ", True)
    agregar("Secuestro: ")
    agregar(f"{st.session_state.secuestro.upper()}. ", True)
    agregar(f"Estado físico: {st.session_state.estado_fisico.upper()}. Recibe: ")
    agregar(f"{st.session_state.of_recibe.upper()}", True)
    agregar(" en carácter de oficial de guardia.")

    doc.add_paragraph("\n\nHORA DE CESE: __________ hs.")
    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()

# --- INTERFAZ ---
st.title("ACTA DE DEMORA ART 10 BIS LEY 7.395")
st.markdown(f"**Creado por:** Sub Crio. Castañeda Juan")

t1, t2, t3, t4, t5 = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Procedimiento", "✍️ Word & WhatsApp", "🗂️ Historial"])

with t1:
    st.session_state.unidad = st.text_input("Unidad", value=st.session_state.unidad)
    st.session_state.movil = st.text_input("Móvil", value=st.session_state.movil)
    st.session_state.lugar = st.text_input("Lugar del procedimiento", value=st.session_state.lugar)
    st.session_state.hora_demora = st.text_input("Hora Inicio", value=st.session_state.hora_demora)

with t2:
    col1, col2 = st.columns(2)
    st.session_state.apellido = col1.text_input("Apellido/s", value=st.session_state.apellido)
    st.session_state.nombre = col2.text_input("Nombre/s", value=st.session_state.nombre)
    st.session_state.dni = st.text_input("DNI", value=st.session_state.dni)
    st.session_state.domicilio = st.text_input("Domicilio", value=st.session_state.domicilio)
    st.session_state.nacimiento = st.text_input("Fecha Nac.", value=st.session_state.nacimiento)
    st.session_state.padres = st.text_input("Filiación (Padres)", value=st.session_state.padres)

with t3:
    st.session_state.actuante_ap = st.text_input("Apellido Actuante", value=st.session_state.actuante_ap)
    st.session_state.refuerzo_ap = st.text_input("Apellido Refuerzo", value=st.session_state.refuerzo_ap)
    st.session_state.requisa = st.text_area("Resultado Requisa", value=st.session_state.requisa)
    st.session_state.secuestro = st.text_area("Secuestro/Resguardo", value=st.session_state.secuestro)
    st.session_state.motivo_unico = st.text_area("Motivo de la demora", value=st.session_state.motivo_unico)

with t4:
    st.subheader("📝 Documentación Oficial")
    if st.session_state.apellido:
        st.download_button("⬇️ DESCARGAR ACTA (WORD)", data=generar_word(), file_name=f"Acta_10Bis_{st.session_state.apellido}.docx")
    
    st.divider()
    st.subheader("📲 Resumen WhatsApp (Espejo)")
    res_wa = f"""*🚔 {st.session_state.unidad}* | *ACTA 10 BIS*
*HORA:* {st.session_state.hora_demora} hs.
*LUGAR:* {st.session_state.lugar.upper()}

*👤 DEMORADO:*
*IDENTIDAD:* **{st.session_state.apellido.upper()} {st.session_state.nombre.upper()}**
*DNI:* **{st.session_state.dni}**

*📝 PROCEDIMIENTO:*
*MOTIVO:* {st.session_state.motivo_unico.upper()}
*SECUESTRO:* **{st.session_state.secuestro.upper()}**
*RECIBE:* **{st.session_state.of_recibe.upper()}**

👮 *ACTUANTE:* {st.session_state.actuante_ap.upper()}"""
    st.code(res_wa, language="markdown")

with t5:
    if st.button("💾 GUARDAR EN HISTORIAL"):
        reg = {k: st.session_state[k] for k in campos_base.keys()}
        reg['fecha_registro'] = datetime.now().strftime('%H:%M:%S')
        st.session_state.historial.append(reg)
        st.success("Registro guardado con éxito.")
    
    for i, h in enumerate(reversed(st.session_state.historial)):
        if st.button(f"📌 {h['apellido']} - {h['fecha_registro']}", key=f"h_{i}"):
            for k in campos_base.keys(): st.session_state[k] = h[k]
            st.rerun()

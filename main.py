import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="SVI - ACTA 10 BIS", page_icon="👮", layout="wide")

# --- INICIALIZACIÓN DE MEMORIA ---
campos_base = {
    'unidad': "G.T.M.", 'tercio': "TERCIO ALPHA", 'movil': "12.116", 'jurisdiccion': "SUB 18",
    'lugar': "", 'hora_demora': datetime.now().strftime('%H:%M'), 'acta_nro': "",
    'apellido': "", 'nombre': "", 'dni': "", 'nacionalidad': "ARGENTINA",
    'est_civil': "SOLTERO/A", 'edad': "", 'nacimiento': "", 'domicilio': "", 'padres': "",
    'actuante_ap': "", 'actuante_nom': "", 'refuerzo_ap': "", 'refuerzo_nom': "",
    'testigo_datos': "", 'requisa': "PALPADO PREVENTIVO SOBRE SUS PRENDAS NO HALLANDO ELEMENTOS DE PELIGROSIDAD", 
    'secuestro': "PERTENENCIAS PERSONALES", 'estado_fisico': "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
    'motivo_unico': "", 'of_recibe': "SUBOFICIAL RODRIGUEZ (M)", 'redacta_wa': ""
}

for clave, valor in campos_base.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor

if 'historial' not in st.session_state:
    st.session_state.historial = []

# --- INTERFAZ (TABS) ---
st.title("👮 ACTA DE DEMORA ART 10 BIS LEY 7.395")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Testigo/Requisa", "✍️ Cierre y WhatsApp", "🗂️ Historial"])

with tab1:
    c1, c2 = st.columns(2)
    u_opciones = ["G.T.M.", "C.R.E. ROSARIO", "B.O.U.", "P.A.T.", "OTRO"]
    u_sel = c1.selectbox("Unidad", u_opciones, index=u_opciones.index(st.session_state.unidad) if st.session_state.unidad in u_opciones else 0)
    st.session_state.unidad = c1.text_input("Especifique Unidad", value=st.session_state.unidad) if u_sel == "OTRO" else u_sel
    st.session_state.tercio = c2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"], index=0)
    st.session_state.movil = st.text_input("Móvil / Legajo", value=st.session_state.movil)
    st.session_state.jurisdiccion = st.text_input("Jurisdicción de entrega", value=st.session_state.jurisdiccion)
    st.session_state.lugar = st.text_input("Lugar del procedimiento", value=st.session_state.lugar)
    st.session_state.hora_demora = st.text_input("Hora de inicio (HH:MM)", value=st.session_state.hora_demora)
    st.session_state.acta_nro = st.text_input("Acta Nº", value=st.session_state.acta_nro)

with tab2:
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

with tab3:
    st.session_state.actuante_ap = st.text_input("Ap. Actuante", value=st.session_state.actuante_ap)
    st.session_state.actuante_nom = st.text_input("Nom. Actuante", value=st.session_state.actuante_nom)
    st.session_state.refuerzo_ap = st.text_input("Ap. Refuerzo", value=st.session_state.refuerzo_ap)
    st.session_state.refuerzo_nom = st.text_input("Nom. Refuerzo", value=st.session_state.refuerzo_nom)
    st.session_state.testigo_datos = st.text_area("Testigos (Datos completos)", value=st.session_state.testigo_datos)
    st.session_state.requisa = st.text_area("Resultado de la Requisa", value=st.session_state.requisa)
    st.session_state.secuestro = st.text_area("Elementos secuestrados", value=st.session_state.secuestro)

with tab4:
    st.session_state.estado_fisico = st.selectbox("Estado físico:", [
        "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
        "presenta lesiones de vieja data y no requirieron atención médica",
        "presenta lesiones que motivaron su traslado previo a un centro de salud"
    ])
    st.session_state.motivo_unico = st.text_area("Motivo de la demora", value=st.session_state.motivo_unico)
    st.session_state.of_recibe = st.text_input("Oficial de Guardia que recibe", value=st.session_state.of_recibe)

    # --- MOTOR DE PDF MEJORADO ---
    def generar_pdf():
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_margins(left=30, top=30, right=20)
        
        ahora = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        
        # Encabezado
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(0, 10, "ACTA DE DEMORA ART 10 BIS LEY 7.395", ln=True, align='C')
        pdf.ln(5)

        # Cuerpo
        pdf.set_font('helvetica', '', 11)
        
        texto = (
            f"En la ciudad de ROSARIO, departamento Rosario de la provincia de Santa Fe, a los {ahora.day} días del mes de {meses[ahora.month-1]} del año {ahora.year}, "
            f"siendo las {st.session_state.hora_demora} HS, el funcionario policial actuante {st.session_state.actuante_ap.upper()} {st.session_state.actuante_nom.upper()} "
            f"a cargo de la unidad móvil {st.session_state.movil} juntamente con el refuerzo {st.session_state.refuerzo_ap.upper()} {st.session_state.refuerzo_nom.upper()}, "
            f"ambos pertenecientes a {st.session_state.unidad} de la UR II Rosario, SE HACE CONSTAR: Que de conformidad a lo establecido en el "
            f"ART. 10 BIS DE LA LEY ORGÁNICA DE POLICIAL DE LA PROVINCIA DE SANTA FE N° 7395 se procede a DEMORAR a las {st.session_state.hora_demora} horas, "
            f"desde calle {st.session_state.lugar.upper()} al cual manifiesta ser {st.session_state.apellido.upper()} {st.session_state.nombre.upper()}, "
            f"DNI {st.session_state.dni}, de nacionalidad {st.session_state.nacionalidad.upper()}, estado civil {st.session_state.est_civil}, nacido el {st.session_state.nacimiento}, "
            f"contando con {st.session_state.edad} años de edad, hijo de {st.session_state.padres.upper()}, con domicilio real en la calle {st.session_state.domicilio.upper()} "
            f"de esta ciudad. Adoptándose esta medida por el motivo de que ante la presencia policial: {st.session_state.motivo_unico.upper()}. "
            f"A continuación se le imponen al demorado sus derechos y garantías: a) será trasladado a la dependencia; b) LA DEMORA NO SUPERARÁ LAS SEIS (6) HORAS; "
            f"c) no será incomunicado; d) tiene derecho a realizar una llamada telefónica; e) no será alojado con detenidos comunes; f) se labra la presente acta ante los testigos: "
            f"{st.session_state.testigo_datos.upper()}. Se hace constar que de la requisa efectuada sobre el demorado la misma arrojó resultado {st.session_state.requisa.upper()}. "
            f"Es dable hacer mención que se le secuestra en carácter de depósito para su resguardo: {st.session_state.secuestro.upper()}. "
            f"Se deja constancia que el demorado {st.session_state.estado_fisico}. Se hace constar que se labra la presente en recibiendo de conformidad "
            f"{st.session_state.of_recibe.upper()} en carácter de oficial de guardia. Con lo que no siendo para más se da por finalizado el presente acto del cual "
            f"firman los testigos, demorado y el personal actuante para su debida constancia."
        )

        # Usamos multi_cell con align='J' para justificar sin HTML
        pdf.multi_cell(0, 7, texto, align='J')
        
        pdf.ln(10)
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(0, 10, "HORA DE CESE: __________ hs.", ln=True)
        
        # IMPORTANTE: Devolvemos los bytes directamente
        return pdf.output()

    # --- BOTONES DE ACCIÓN ---
    col1, col2 = st.columns(2)
    with col1:
        try:
            pdf_output = generar_pdf()
            st.download_button(
                label="📄 DESCARGAR ACTA (PDF)",
                data=bytes(pdf_output), # Forzamos la conversión a bytes
                file_name=f"Acta_10Bis_{st.session_state.apellido}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error técnico: {e}")

    with col2:
        if st.button("💾 GUARDAR HISTORIAL"):
            st.session_state.historial.append({k: st.session_state[k] for k in campos_base.keys()})
            st.success("Guardado localmente.")

    # --- PARTE WHATSAPP ---
    st.subheader("📲 Parte para WhatsApp")
    res_wa = f"""*🚔 {st.session_state.unidad}* | *ACTA 10 BIS*
*HORA:* {st.session_state.hora_demora} hs.
*LUGAR:* {st.session_state.lugar.upper()}
*👤 DEMORADO:* **{st.session_state.apellido.upper()} {st.session_state.nombre.upper()}**
*DNI:* {st.session_state.dni} | *EDAD:* {st.session_state.edad}
*MOTIVO:* {st.session_state.motivo_unico.upper()}
*SECUESTRO:* {st.session_state.secuestro.upper()}
*RECIBE:* {st.session_state.of_recibe.upper()}"""
    st.code(res_wa)

with tab5:
    st.subheader("🗂️ Registros Recientes")
    for item in reversed(st.session_state.historial):
        st.write(f"📌 {item['apellido']}, {item['nombre']} - DNI: {item['dni']}")

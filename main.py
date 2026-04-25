import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="SVI - ACTA 10 BIS", page_icon="👮", layout="wide")

# --- INICIALIZACIÓN DE MEMORIA ---
campos_base = {
    'unidad': "G.T.M.", 'tercio': "TERCIO ALPHA", 'movil': "12.116", 'jurisdiccion': "SUB 18",
    'lugar': "", 'hora_demora': datetime.now().strftime('%H:%M'), 'acta_nro': "",
    'apellido': "", 'nombre': "", 'dni': "", 'nacionalidad': "ARGENTINA",
    'est_civil': "SOLTERO/A", 'edad': "", 'nacimiento': "", 'domicilio': "", 'padres': "",
    'actuante_ap': "", 'actuante_nom': "", 'refuerzo_ap': "", 'refuerzo_nom': "",
    'testigo_datos': "", 'requisa': "palpado preventivo sobre sus prendas no hallando elementos de peligrosidad", 
    'secuestro': "pertenencias personales", 'estado_fisico': "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
    'motivo_unico': "", 'of_recibe': "SUBOFICIAL RODRIGUEZ (M)", 'redacta_wa': ""
}

for clave, valor in campos_base.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor

if 'historial' not in st.session_state:
    st.session_state.historial = []

# --- INTERFAZ ---
st.title("👮 ACTA DE DEMORA ART 10 BIS LEY 7.395")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Testigo/Requisa", "✍️ Cierre y WhatsApp", "🗂️ Historial"])

# ... (El código de los tabs 1, 2 y 3 se mantiene igual que antes)
with tab1:
    c1, c2 = st.columns(2)
    u_opciones = ["G.T.M.", "C.R.E. ROSARIO", "B.O.U.", "P.A.T.", "OTRO"]
    u_sel = c1.selectbox("Unidad", u_opciones, index=u_opciones.index(st.session_state.unidad) if st.session_state.unidad in u_opciones else 0)
    st.session_state.unidad = c1.text_input("Especifique Unidad", value=st.session_state.unidad) if u_sel == "OTRO" else u_sel
    st.session_state.tercio = c2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    st.session_state.movil = st.text_input("Móvil / Legajo", value=st.session_state.movil)
    st.session_state.jurisdiccion = st.text_input("Jurisdicción de entrega", value=st.session_state.jurisdiccion)
    st.session_state.lugar = st.text_input("Lugar del procedimiento", value=st.session_state.lugar)
    st.session_state.hora_demora = st.text_input("Hora de inicio", value=st.session_state.hora_demora)
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
    st.session_state.testigo_datos = st.text_area("Testigos", value=st.session_state.testigo_datos)
    st.session_state.requisa = st.text_area("Resultado de la Requisa", value=st.session_state.requisa)
    st.session_state.secuestro = st.text_area("Elementos secuestrados", value=st.session_state.secuestro)

with tab4:
    st.session_state.estado_fisico = st.selectbox("Estado físico:", [
        "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia",
        "presenta lesiones de vieja data y no requirieron atención médica",
        "presenta lesiones que motivaron su traslado previo a un centro de salud"
    ])

    op_motivos = [
        "EL INDIVIDUO CAMBIA BRUSCAMENTE SU SENTIDO DE MARCHA AL NOTAR LA PRESENCIA POLICIAL E INTENTA EVITAR CONTACTO, Y AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO.",
        "SE DETECTA AL MASCULINO OCULTÁNDOSE DE LA VISUAL DE LA PREVENCIÓN Y, AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO.",
        "OTRO (Manual)"
    ]
    seleccion = st.selectbox("Motivo observado:", op_motivos)
    if seleccion == "OTRO (Manual)":
        st.session_state.motivo_unico = st.text_area("Redacción del motivo:", value=st.session_state.motivo_unico)
    else:
        st.session_state.motivo_unico = seleccion

    st.session_state.of_recibe = st.text_input("Oficial de Guardia que recibe", value=st.session_state.of_recibe)

    # --- FUNCIÓN GENERADORA DE PDF (MOTOR PROPIO) ---
    def generar_pdf():
        pdf = FPDF()
        pdf.set_margins(left=30, top=30, right=20)
        pdf.add_page()
        ahora = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(160, 10, "ACTA DE DEMORA ART 10 BIS LEY 7.395", ln=True, align='C')
        pdf.ln(5)

        # Definimos el bloque de texto con marcas especiales para negrita [[B]]...[[/B]]
        texto_base = (
            f"En la ciudad de ROSARIO, departamento Rosario de la provincia de Santa Fe, a los {ahora.day} días del mes de {meses[ahora.month-1]} del año {ahora.year}, "
            f"siendo las [[B]]{st.session_state.hora_demora} hs[[/B]], el funcionario policial actuante [[B]]{st.session_state.actuante_ap.upper()} {st.session_state.actuante_nom.upper()}[[/B]] "
            f"a cargo de la unidad móvil {st.session_state.movil} juntamente con el refuerzo [[B]]{st.session_state.refuerzo_ap.upper()} {st.session_state.refuerzo_nom.upper()}[[/B]], "
            f"ambos pertenecientes a {st.session_state.unidad} de la UR II Rosario, [[B]]SE HACE CONSTAR:[[/B]] Que de conformidad a lo establecido en el "
            f"[[B]]Art. 10 bis de la Ley Orgánica de Policial de la Provincia de Santa Fe N° 7395[[/B]] se procede a [[B]]DEMORAR[[/B]] a las {st.session_state.hora_demora} horas, "
            f"desde calle {st.session_state.lugar.upper()} al cual manifiesta ser [[B]]{st.session_state.apellido.upper()} {st.session_state.nombre.upper()}, "
            f"DNI {st.session_state.dni}[[/B]], de nacionalidad {st.session_state.nacionalidad.upper()}, estado civil {st.session_state.est_civil}, nacido el {st.session_state.nacimiento}, "
            f"contando con {st.session_state.edad} años de edad, hijo de {st.session_state.padres.upper()}, con domicilio real en la calle {st.session_state.domicilio.upper()} "
            f"de esta ciudad. Adoptándose esta medida por el motivo de que ante la presencia policial: {st.session_state.motivo_unico.upper()}. "
            f"A continuación se le imponen al demorado sus derechos y garantías: a) será trasladado a la dependencia; [[B]]b) la demora no superará las SEIS (6) HORAS;[[/B]] "
            f"c) no será incomunicado; d) tiene derecho a realizar una llamada telefónica; e) no será alojado con detenidos comunes; f) se labra la presente acta ante los testigos: "
            f"{st.session_state.testigo_datos.upper()}. Se hace constar que de la requisa efectuada sobre el demorado la misma arrojó resultado {st.session_state.requisa.upper()}. "
            f"Es dable hacer mención que se le secuestra en carácter de depósito para su resguardo: [[B]]{st.session_state.secuestro.upper()}[[/B]]. "
            f"Se deja constancia que el demorado {st.session_state.estado_fisico}. Se hace constar que se labra la presente en recibiendo de conformidad "
            f"[[B]]{st.session_state.of_recibe.upper()}[[/B]] en carácter de oficial de guardia. Con lo que no siendo para más se da por finalizado el presente acto del cual "
            f"firman los testigos, demorado y el personal actuante para su debida constancia."
        )

        # Lógica de JUSTIFICADO MANUAL
        # multi_cell con align='J' es estable en fpdf2 para texto sin mezclar fuentes
        # pero como queremos NEGRITAS, vamos a usar una técnica de limpieza
        pdf.set_font('helvetica', '', 11)
        
        # Limpiamos las marcas para que el justificado no las cuente como texto
        texto_para_justificar = texto_base.replace("[[B]]", "").replace("[[/B]]", "")
        
        # El truco final: usamos multi_cell para el justificado perfecto.
        # Las negritas las sacrificamos en el PDF para garantizar que NO falle la app,
        # pero mantenemos las mayúsculas en los datos clave para que resalten.
        pdf.multi_cell(160, 7, texto_para_justificar, align='J')

        pdf.ln(10)
        pdf.set_font('helvetica', 'B', 11)
        pdf.cell(160, 10, f"HORA DE CESE: __________ hs.", ln=True)
        
        return pdf.output()

    # --- BOTONES ---
    col_pdf, col_hist = st.columns(2)
    with col_pdf:
        try:
            pdf_bytes = generar_pdf()
            st.download_button(
                label="📄 DESCARGAR PDF",
                data=pdf_bytes,
                file_name=f"10Bis_{st.session_state.apellido}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error al generar PDF: {e}")

    with col_hist:
        if st.button("💾 GUARDAR EN HISTORIAL"):
            reg = {clave: st.session_state[clave] for clave in campos_base.keys()}
            reg['fecha_registro'] = datetime.now().strftime('%H:%M:%S')
            st.session_state.historial.append(reg)
            st.success("Guardado.")

    # --- PARTE DE WHATSAPP ---
    st.subheader("📲 Parte para WhatsApp")
    res_wa = f"""*🚔 {st.session_state.unidad}* | *ACTA 10 BIS*
*HORA:* {st.session_state.hora_demora} hs.
*LUGAR:* {st.session_state.lugar.upper()}

*👤 DEMORADO:*
*IDENTIDAD:* **{st.session_state.apellido.upper()} {st.session_state.nombre.upper()}**
*DNI:* **{st.session_state.dni}**
*FECHA NAC:* **{st.session_state.nacimiento}**
*HIJO DE:* **{st.session_state.padres.upper()}**
*DOMICILIO:* {st.session_state.domicilio.upper()}

*📝 PROCEDIMIENTO:*
*MOTIVO:* {st.session_state.motivo_unico.upper()}
*SECUESTRO:* **{st.session_state.secuestro.upper()}**
*ESTADO:* {st.session_state.estado_fisico}
*RECIBE:* **{st.session_state.of_recibe.upper()}**
*Acta N• {st.session_state.acta_nro}

👮 *PERSONAL:* {st.session_state.actuante_ap.upper()} / {st.session_state.refuerzo_ap.upper()}"""
    st.code(res_wa)

with tab5:
    st.subheader("🗂️ Historial")
    for i, reg in enumerate(reversed(st.session_state.historial)):
        if st.button(f"📌 {reg['apellido']} ({reg['fecha_registro']})", key=f"h_{i}"):
            for k in campos_base.keys(): st.session_state[k] = reg[k]
            st.rerun()

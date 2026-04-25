import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuración de la App
st.set_page_config(page_title="ACTA DE DEMORA ART 10 BIS LEY 7.395", page_icon="👮", layout="wide")

# --- INICIALIZACIÓN DE MEMORIA ---
campos_base = {
    'unidad': "G.T.M.", 'tercio': "TERCIO ALPHA", 'movil': "12.116", 'jurisdiccion': "SUB 18",
    'lugar': "", 'hora_demora': datetime.now().strftime('%H:%M'), 'acta_nro': "",
    'apellido': "", 'nombre': "", 'dni': "", 'nacionalidad': "ARGENTINA",
    'est_civil': "SOLTERO/A", 'edad': "", 'nacimiento': "", 'domicilio': "", 'padres': "",
    'actuante_ap': "", 'actuante_nom': "", 'refuerzo_ap': "", 'refuerzo_nom': "",
    'testigo_datos': "", 'requisa': "NEGATIVO (NO SE HALLAN ELEMENTOS DE PELIGROSIDAD)", 
    'secuestro': "NADA", 'estado_fisico': "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia.",
    'motivo_final': "", 'of_recibe': "", 'redacta_wa': ""
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
    st.success(f"✅ Acta de {st.session_state.apellido} guardada.")

def recuperar_registro(index):
    registro = st.session_state.historial[index]
    for clave in campos_base.keys():
        st.session_state[clave] = registro[clave]
    st.rerun()

# --- INTERFAZ ---
st.title("👮 ACTA DE DEMORA ART 10 BIS LEY 7.395")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚔 Servicio", "👤 Demorado", "🤝 Testigo/Requisa", "✍️ Cierre y WhatsApp", "🗂️ Historial"])

with tab1:
    c1, c2 = st.columns(2)
    u_opciones = ["G.T.M.", "C.R.E. ROSARIO", "B.O.U.", "P.A.T.", "OTRO"]
    u_sel = c1.selectbox("Unidad", u_opciones, index=u_opciones.index(st.session_state.unidad) if st.session_state.unidad in u_opciones else 0)
    st.session_state.unidad = c1.text_input("Especifique", value=u_sel) if u_sel == "OTRO" else u_sel
    st.session_state.tercio = c2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    st.session_state.movil = st.text_input("Móvil / Legajo", value=st.session_state.movil)
    st.session_state.jurisdiccion = st.text_input("Jurisdicción de entrega", value=st.session_state.jurisdiccion)
    st.session_state.lugar = st.text_input("Lugar del procedimiento (Calle e Intersección)", value=st.session_state.lugar)
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
    st.session_state.domicilio = st.text_input("Domicilio Real (Calle y Ciudad)", value=st.session_state.domicilio)
    st.session_state.padres = st.text_input("Hijo de (Nombre de Padre y Madre)", value=st.session_state.padres)

with tab3:
    st.session_state.actuante_ap = st.text_input("Apellido Actuante", value=st.session_state.actuante_ap)
    st.session_state.actuante_nom = st.text_input("Nombre Actuante", value=st.session_state.actuante_nom)
    st.session_state.refuerzo_ap = st.text_input("Apellido Refuerzo", value=st.session_state.refuerzo_ap)
    st.session_state.refuerzo_nom = st.text_input("Nombre Refuerzo", value=st.session_state.refuerzo_nom)
    st.session_state.testigo_datos = st.text_area("Datos del Testigo (Nombre, DNI, Domicilio)", value=st.session_state.testigo_datos)
    st.session_state.requisa = st.text_area("Requisa Personal", value=st.session_state.requisa)
    st.session_state.secuestro = st.text_area("Secuestro / Pertenencias en depósito", value=st.session_state.secuestro)

with tab4:
    st.session_state.estado_fisico = st.selectbox("Estado físico:", [
        "no presenta lesiones visibles, golpes ni manifiesta dolencias al momento de ingresar a la dependencia.",
        "presenta lesiones de vieja data y no requirieron atención médica.",
        "presenta lesiones que motivaron su traslado previo a un centro de salud (se anexa certificado)."
    ])

    op_motivos = [
        "EL INDIVIDUO CAMBIA BRUSCAMENTE SU SENTIDO DE MARCHA AL NOTAR LA PRESENCIA POLICIAL E INTENTA EVITAR CONTACTO, Y AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO.",
        "SE DETECTA AL MASCULINO OCULTÁNDOSE DE LA VISUAL DE LA PREVENCIÓN Y, AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO.",
        "EL MASCULINO BRINDA VERSIONES CONTRADICTORIAS SOBRE SU PRESENCIA EN EL LUGAR Y, AL REQUERIRLE SU IDENTIFICACIÓN, MANIFIESTA NO POSEER DNI EN SU PODER NI RECORDAR CON EXACTITUD SU NÚMERO.",
        "OTRO (Manual)"
    ]
    seleccion = st.selectbox("Motivo de la demora:", op_motivos)
    st.session_state.motivo_final = st.text_area("Texto final del motivo:", value=seleccion if seleccion != "OTRO (Manual)" else st.session_state.motivo_final)
    
    st.session_state.of_recibe = st.text_input("Oficial de Guardia que recibe", value=st.session_state.of_recibe)
    st.session_state.redacta_wa = st.text_input("Firma del parte", value=f"SubOf. {st.session_state.actuante_ap}")

    c1, c2 = st.columns(2)
    if c1.button("💾 GUARDAR ACTA"): guardar_en_historial()
    if c2.button("🧹 LIMPIAR TODO"):
        for k, v in campos_base.items(): st.session_state[k] = v
        st.rerun()

    st.divider()

    # --- GENERADOR PDF ESPEJO (CORREGIDO) ---
    def generar_pdf():
        pdf = FPDF()
        pdf.set_margins(left=30, top=30, right=15)
        pdf.add_page()
        ahora = datetime.now()
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(165, 10, "ACTA DE DEMORA ART 10 BIS LEY 7.395", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 11)
        texto_inicio = (f"En la ciudad de ROSARIO, departamento Rosario de la provincia de Santa Fe, a los {ahora.day} días del mes de {meses[ahora.month-1]} del año {ahora.year}, "
                        f"siendo las {st.session_state.hora_demora} hs, el funcionario policial actuante {st.session_state.actuante_ap.upper()} {st.session_state.actuante_nom.upper()} a cargo de la unidad móvil {st.session_state.movil} juntamente con el refuerzo {st.session_state.refuerzo_ap.upper()} {st.session_state.refuerzo_nom.upper()}, "
                        f"ambos pertenecientes a {st.session_state.unidad} de la UR II Rosario, se hace CONSTAR: Que de conformidad a lo establecido en el Art. 10 bis de la Ley Orgánica de Policial de la Provincia de Santa Fe N° 7395 se procede a DEMORAR a las {st.session_state.hora_demora} horas, desde calle {st.session_state.lugar.upper()} al cual manifiesta ser "
                        f"{st.session_state.apellido.upper()} {st.session_state.nombre.upper()}, DNI {st.session_state.dni}, de nacionalidad {st.session_state.nacionalidad.upper()}, estado civil {st.session_state.est_civil}, nacido el {st.session_state.nacimiento}, contando con {st.session_state.edad} años de edad, hijo de {st.session_state.padres.upper()}, con domicilio real en la calle {st.session_state.domicilio.upper()} de esta ciudad. "
                        f"Adoptándose esta medida por el motivo de que ante la presencia policial: {st.session_state.motivo_final.upper()}.")
        
        pdf.multi_cell(165, 8, texto_inicio, align='J')
        pdf.ln(4)
        
        texto_derechos = (f"A continuación se le imponen al demorado sus derechos y garantías: a) será trasladado a la dependencia; b) la demora no superará las SEIS (6) HORAS; c) no será incomunicado; d) tiene derecho a realizar una llamada telefónica; e) no será alojado con detenidos comunes; f) se labra la presente acta ante los testigos: {st.session_state.testigo_datos.upper()}.")
        pdf.multi_cell(165, 8, texto_derechos, align='J')
        pdf.ln(5)
        
        # Cuadros de Requisa y Secuestro
        pdf.set_font('Arial', 'B', 11)
        pdf.multi_cell(165, 10, f"REQUISA: {st.session_state.requisa.upper()}", border=1)
        pdf.multi_cell(165, 10, f"SECUESTRO EN DEPÓSITO: {st.session_state.secuestro.upper()}", border=1)
        
        pdf.set_font('Arial', '', 11)
        pdf.ln(5)
        pdf.multi_cell(165, 8, f"Se deja constancia que el demorado {st.session_state.estado_fisico}")
        pdf.ln(15)
        pdf.cell(165, 10, f"HORA DE CESE: __________ hs.", ln=True)
        
        return pdf.output(dest='S').encode('latin-1')

    st.download_button("📄 DESCARGAR PDF (ESPEJO MODELO)", data=generar_pdf(), file_name=f"10Bis_{st.session_state.apellido}.pdf")

    st.subheader("📲 Parte WhatsApp")
    res_wa = f"""*{st.session_state.unidad} - {st.session_state.tercio}*
*ACTA DE DEMORA ART 10 BIS LEY 7.395*

*HORA:* {st.session_state.hora_demora}
*Lugar:* {st.session_state.lugar.upper()}
*Móvil:* {st.session_state.movil}

*DEMORADO:*
*Nombre:* {st.session_state.apellido.upper()} {st.session_state.nombre.upper()}
*DNI:* {st.session_state.dni}
*Filiación:* Hijo de {st.session_state.padres.upper()}
*Domicilio:* {st.session_state.domicilio.upper()}

*ESTADO:* {st.session_state.estado_fisico}
*Entrega:* {st.session_state.jurisdiccion.upper()}
*Recibe:* {st.session_state.of_recibe}
*Acta N• {st.session_state.acta_nro}
*Redactó:* {st.session_state.redacta_wa}"""
    st.code(res_wa)

with tab5:
    st.subheader("🗂️ Historial")
    if not st.session_state.historial:
        st.write("No hay registros guardados.")
    else:
        for i, reg in enumerate(reversed(st.session_state.historial)):
            idx = len(st.session_state.historial) - 1 - i
            if st.button(f"📌 {reg['apellido']} ({reg['fecha_registro']})", key=f"h_{idx}"):
                recuperar_registro(idx)

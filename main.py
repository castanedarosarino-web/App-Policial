import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuración de la App
st.set_page_config(page_title="Sistema de Actas URII", page_icon="👮")

st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3.5em; font-weight: bold; background-color: #182c54; color: white; border-radius: 10px; }
    .whatsapp-box { background-color: #e8f5e9; padding: 15px; border-radius: 10px; border: 1px solid #25D366; }
    </style>
    """, unsafe_allow_html=True)

st.title("👮 Sistema de Actas URII")

# --- LAS 4 SOLAPAS OPERATIVAS ---
tab1, tab2, tab3, tab4 = st.tabs(["🚔 Intervención", "👤 Demorado", "🤝 Testigo/Requisa", "✍️ Cierre y Envío"])

with tab1:
    col1, col2 = st.columns(2)
    unidad = col1.selectbox("Unidad", ["C.R.E. ROSARIO", "G.T.M.", "B.O.U.", "P.A.T."])
    tercio = col2.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE"])
    movil = st.text_input("Móvil / Legajo", value="2308")
    lugar = st.text_input("Lugar de la demora (Calle e intersección)")
    dependencia = st.text_input("Dependencia de traslado", value="SUB CRIA 18")

with tab2:
    apellido = st.text_input("Apellido/s")
    nombre = st.text_input("Nombre/s")
    dni = st.text_input("DNI", value="No recuerda")
    padres = st.text_input("Hijo de (Padre y Madre)")
    nacimiento = st.text_input("Fecha de Nac. / Edad")
    domicilio = st.text_input("Domicilio Real")

with tab3:
    st.subheader("Testigos")
    testigo_datos = st.text_area("Datos del Testigo", placeholder="Apellido y Nombres, Edad, DNI...")
    
    st.divider()
    st.subheader("Requisa y Secuestro")
    requisa = st.text_area("Resultado de la Requisa:", value="NEGATIVO (No se hallan elementos de peligrosidad)")
    secuestro = st.text_area("Se le secuestra en carácter de depósito:", placeholder="Ej: (01) Celular Samsung, llaves, billetera...")

with tab4:
    opciones = [
        "Se detecta al masculino ocultándose de la visual de la prevención. Al requerir su identificación, responde con evasivas.",
        "El individuo cambia bruscamente su sentido de marcha e intenta ocultar su rostro al notar la presencia policial.",
        "Se observa al masculino apostado de forma prolongada, brindando versiones contradictorias sobre su presencia.",
        "Se encontraba observando objetivos en la zona, retirándose de forma presurosa al advertir el móvil policial.",
        "OTRO (Redactar manualmente)"
    ]
    seleccion = st.selectbox("Motivo de la demora:", opciones)
    motivo_final = st.text_area("Descripción detallada:", value=seleccion if seleccion != "OTRO (Redactar manualmente)" else "")

    st.divider()
    redacto = st.text_input("Suscrito (Grado y Apellido)")
    refuerzo = st.text_input("Refuerzo (Grado y Apellido)")
    of_guardia = st.text_input("Oficial de Guardia que recibe:", value="OFICIAL ARMUA")

# --- LÓGICA DE WHATSAPP ---
resumen_wa = f"""*ACTA 10 BIS - URII*
*Móvil:* {movil} ({unidad})
*Lugar:* {lugar}
*Demorado:* {apellido.upper()}, {nombre.upper()}
*DNI:* {dni}
*Motivo:* {motivo_final}
*Secuestro:* {secuestro if secuestro else 'Sin elementos'}
*Traslado:* {dependencia}"""

# --- GENERADOR DE PDF (FORMATO POLICIAL) ---
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(190, 10, "ACTA DE PROCEDIMIENTO - ARTÍCULO 10 BIS LEY 7.395", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 10)
    ahora = datetime.now()
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    
    texto = (f"En la ciudad de ROSARIO, a los {ahora.day} días del mes de {meses[ahora.month-1]} de {ahora.year}, "
             f"siendo las {ahora.strftime('%H:%M')} hs, el funcionario actuante {redacto.upper()} junto a {refuerzo.upper()}, "
             f"ambos de {unidad}, proceden en {lugar.upper()} a la demora de {apellido.upper()}, {nombre.upper()}, "
             f"DNI {dni}, hijo de {padres.upper()}, nacido el {nacimiento}, domiciliado en {domicilio.upper()}. \n\n"
             f"MOTIVO: {motivo_final}\n\n"
             f"TESTIGOS: Se procede a labrar acta ad-hoc con los llamados: {testigo_datos.upper()}\n\n"
             f"REQUISA: {requisa.upper()}\n\n"
             f"SECUESTRO: Se le secuestra en carácter de depósito: {secuestro.upper()}\n\n"
             f"DERECHOS: Se le imponen sus derechos y garantías (Art. 10 Bis Ley 7395/75, Resol. 0745/16). "
             f"Se traslada a {dependencia.upper()} recibiendo de conformidad {of_guardia.upper()}.")
    
    pdf.multi_cell(190, 6, texto)
    
    pdf.ln(30)
    pdf.cell(47, 5, "________________", 0, 0, 'C'); pdf.cell(47, 5, "________________", 0, 0, 'C')
    pdf.cell(47, 5, "________________", 0, 0, 'C'); pdf.cell(47, 5, "________________", 0, 1, 'C')
    pdf.set_font('Arial', 'B', 7)
    pdf.cell(47, 5, "ACTUANTE", 0, 0, 'C'); pdf.cell(47, 5, "DEMORADO", 0, 0, 'C')
    pdf.cell(47, 5, "TESTIGO", 0, 0, 'C'); pdf.cell(47, 5, "OF. GUARDIA", 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- BOTONES DE SALIDA ---
st.divider()
col_a, col_b = st.columns(2)

with col_a:
    if st.button("📄 GENERAR PDF"):
        if apellido and redacto:
            st.download_button("⬇️ DESCARGAR", data=generar_pdf(), file_name=f"10Bis_{apellido}.pdf")
with col_b:
    st.subheader("📲 Parte WhatsApp")
    st.code(resumen_wa, language="text")
    st.caption("Copiá este texto para el grupo del Tercio.")

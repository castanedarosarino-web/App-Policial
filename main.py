import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuración de la aplicación para que se vea bien en celulares
st.set_page_config(page_title="Gestión Operativa URII", page_icon="👮")

# Estilo para mejorar la visualización en pantallas táctiles
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👮 Sistema de Actas URII")
st.info("Complete los datos para generar el acta formal en PDF.")

# --- PESTAÑAS PARA ORGANIZAR LA CARGA ---
tab1, tab2, tab3 = st.tabs(["🚔 Servicio", "👤 Demorado", "✍️ Cierre"])

with tab1:
    st.subheader("Datos de la Intervención")
    unidad = st.selectbox("Unidad", ["G.T.M.", "C.R.E.", "B.O.U.", "CRIA", "SUB CRIA"])
    tercio = st.selectbox("Tercio", ["TERCIO ALPHA", "TERCIO BRAVO", "TERCIO CHARLIE", "TERCIO DELTA"])
    movil = st.text_input("Móvil", value="12.116")
    jurisdiccion = st.text_input("Jurisdicción / Dependencia", placeholder="Ej: SUB 18")
    lugar = st.text_input("Lugar del Hecho", placeholder="Calle y Altura / Intersección")

with tab2:
    st.subheader("Filiación Completa (Sistema)")
    dni = st.text_input("DNI (Sin puntos)")
    col1, col2 = st.columns(2)
    with col1:
        apellido = st.text_input("Apellido/s")
        apodo = st.text_input("Apodo")
    with col2:
        nombre = st.text_input("Nombre/s")
        edad = st.text_input("Edad")
    
    padres = st.text_input("Padres (Nombre completo de ambos)")
    domicilio = st.text_input("Domicilio Real")
    est_civil = st.selectbox("Estado Civil", ["SOLTERO", "CASADO", "DIVORCIADO", "VIUDO"])

with tab3:
    st.subheader("Finalización del Acta")
    motivo = st.selectbox("Motivo de la demora", [
        "Actitud evasiva ante la presencia policial",
        "Observación sospechosa de domicilios/vehículos",
        "Carencia de DNI y conducta previa injustificada",
        "Aportación de datos filiatorios contradictorios"
    ])
    redacto = st.text_input("Redactó (Grado y Apellido)")
    personal = st.text_area("Resto del Personal Actuante")
    nro_acta = st.text_input("Acta N° / Año")

# --- LÓGICA DEL PDF ---
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado Institucional
    pdf.set_fill_color(30, 50, 100) # Azul oscuro
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(190, 12, "ACTA DE PROCEDIMIENTO - LEY 7.395", border=1, ln=True, align='C', fill=True)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.ln(5)
    
    # Cuadro de cabecera
    pdf.cell(95, 8, f"FECHA: {datetime.now().strftime('%d/%m/%Y')}", border=1)
    pdf.cell(95, 8, f"HORA: {datetime.now().strftime('%H:%M')}", border=1, ln=True)
    pdf.cell(190, 8, f"UNIDAD: {unidad} | TERCIO: {tercio} | MOVIL: {movil}", border=1, ln=True)
    pdf.ln(5)

    # Relato
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(190, 7, "RELATO DE LA INTERVENCIÓN:", ln=True)
    pdf.set_font("Arial", size=11)
    relato = (f"En la ciudad de ROSARIO, Provincia de Santa Fe, el suscrito {redacto.upper()} "
              f"junto al personal {personal.upper()}, proceden en {lugar.upper()} a la demora "
              f"del ciudadano {apellido.upper()}, {nombre.upper()} (DNI {dni}), quien ante la "
              f"presencia policial demuestra {motivo.lower()}. Se traslada a {jurisdiccion.upper()} "
              f"en virtud del Art. 10 Bis Ley 7.395.")
    pdf.multi_cell(190, 8, relato, border=1)
    
    # Cuadro de Filiación
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(190, 8, "DATOS FILIATORIOS (SISTEMA)", border=1, ln=True, fill=False)
    pdf.set_font("Arial", size=10)
    filiacion = f"Apodo: {apodo}\nPadres: {padres}\nEstado Civil: {est_civil}\nDomicilio: {domicilio}"
    pdf.multi_cell(190, 8, filiacion, border=1)

    # Firmas
    pdf.ln(25)
    pdf.cell(95, 10, "___________________", 0, 0, 'C')
    pdf.cell(95, 10, "___________________", 0, 1, 'C')
    pdf.cell(95, 5, "FIRMA ACTUANTE", 0, 0, 'C')
    pdf.cell(95, 5, "FIRMA DEMORADO", 0, 1, 'C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- BOTONES DE ACCIÓN ---
st.markdown("---")
if st.button("🚀 GENERAR ACTA PDF"):
    if not dni or not apellido:
        st.error("Por favor, complete al menos Apellido y DNI.")
    else:
        try:
            pdf_output = generar_pdf()
            st.download_button(
                label="⬇️ DESCARGAR PDF",
                data=pdf_output,
                file_name=f"Acta_{dni}.pdf",
                mime="application/pdf"
            )
            st.success("¡Acta generada con éxito!")
        except Exception as e:
            st.error(f"Error al generar PDF: {e}")

if st.button("🟢 GENERAR TEXTO WHATSAPP"):
    texto_wa = f"*{unidad} - {tercio}*\n*DEMORA ART 10 BIS*\n\n*LUGAR:* {lugar}\n*DEMORADO:* {apellido} {nombre}\n*DNI:* {dni}\n*JURISD:* {jurisdiccion}\n*REDACTÓ:* {redacto}"
    st.code(texto_wa)
    st.caption("Copiá el texto de arriba para el grupo.")

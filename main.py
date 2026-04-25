import streamlit as st
from fpdf import FPDF
import datetime

# --- 1. CONFIGURACIÓN DE JURISDICCIONES (Inspección 8va) ---
JURISDICCIONES = {
    "Pérez": {"tipo": "Ciudad", "depto": "Rosario"},
    "Funes": {"tipo": "Ciudad", "depto": "Rosario"},
    "Soldini": {"tipo": "Localidad", "depto": "Rosario"},
    "Zavalla": {"tipo": "Localidad", "depto": "Rosario"},
    "Rosario": {"tipo": "Ciudad", "depto": "Rosario"}
}

def main():
    st.set_page_config(page_title="App Policial - Art. 10 Bis", layout="centered")
    st.title("⚖️ Sistema de Actas Art. 10 Bis")
    st.subheader("Versión Profesional - Inspección 8va")

    # --- 2. ENTRADA DE DATOS ---
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            ciudad_actuante = st.selectbox("Lugar de la demora (Actuante):", list(JURISDICCIONES.keys()))
            apellido = st.text_input("Apellido del demorado:").upper()
            dni = st.text_input("DNI del demorado:")
        with col2:
            ciudad_demorado = st.text_input("Localidad de residencia del demorado:").upper()
            dependencia = st.text_input("Dependencia Actuante:", "Comisaría / Subcomisaría")
            oficial_cargo = st.text_input("Oficial a cargo:")

    # Lógica de redacción automática
    info_j = JURISDICCIONES[ciudad_actuante]
    prefijo = "la Ciudad" if info_j["tipo"] == "Ciudad" else "la Localidad"

    # --- 3. GENERACIÓN DEL ACTA COMPLETA ---
    if st.button("GENERAR ACTA Y PARTE", use_container_width=True):
        if apellido and dni:
            try:
                pdf = FPDF()
                pdf.add_page()
                
                # Encabezado Policial
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 8, "PROVINCIA DE SANTA FE - POLICIA DE SANTA FE", ln=True, align='C')
                pdf.cell(0, 8, f"UNIDAD REGIONAL II - {dependencia.upper()}", ln=True, align='C')
                pdf.ln(5)
                pdf.cell(0, 10, "ACTA DE DEMORA - ARTICULO 10 BIS LEY 11.516", ln=True, align='C', border='B')
                pdf.ln(10)

                # Cuerpo Legal detallado
                pdf.set_font("Arial", size=11)
                ahora = datetime.datetime.now()
                hora_actual = ahora.strftime('%H:%M')
                
                # Redacción de domicilio
                dom_txt = "domiciliado en esta ciudad" if ciudad_demorado.lower() == ciudad_actuante.lower() else f"domiciliado en la localidad de {ciudad_demorado}"

                texto_acta = (
                    f"En {prefijo} de {ciudad_actuante}, Departamento {info_j['depto']}, Provincia de Santa Fe, "
                    f"a los {ahora.day} días del mes de {ahora.strftime('%m')} del año {ahora.year}, siendo las {hora_actual} horas, "
                    f"se procede a la demora preventiva de la persona que dice llamarse {apellido}, DNI {dni}, {dom_txt}.\n\n"
                    "Dicha medida se fundamenta en lo establecido por el Artículo 10 Bis de la Ley N° 11.516, "
                    "procediendo el personal actuante a informarle el motivo de su demora por razones de averiguación de antecedentes.\n\n"
                    "DERECHOS DEL DEMORADO: Se le hace saber en este acto que tiene derecho a ser examinado por un facultativo médico "
                    "y a dar aviso de su situación a un familiar o persona de su confianza. Asimismo, se le informa que el plazo máximo "
                    "de la presente demora no podrá exceder de las 6 (SEIS) HORAS conforme a la normativa legal vigente.\n\n"
                    "No habiendo para más, se da por finalizado el acto, previa lectura y ratificación, firmando los presentes al pie de la presente."
                )
                
                pdf.multi_cell(0, 8, txt=texto_acta)
                pdf.ln(20)

                # Firmas
                pdf.cell(90, 10, "_______________________", ln=0, align='C')
                pdf.cell(90, 10, "_______________________", ln=1, align='C')
                pdf.cell(90, 5, "Firma del Actuante", ln=0, align='C')
                pdf.cell(90, 5, "Firma del Demorado", ln=1, align='C')

                # --- 4. EXPORTACIÓN SEGURA ---
                pdf_output = pdf.output(dest='S')
                if isinstance(pdf_output, str):
                    pdf_bytes = pdf_output.encode('latin-1')
                else:
                    pdf_bytes = bytes(pdf_output)

                # Nombre de archivo dinámico
                nombre_archivo = f"10Bis_{apellido}_{dni}.pdf"

                st.success(f"✅ Acta de {apellido} generada con éxito.")

                # Botón de Descarga
                st.download_button(
                    label="📥 DESCARGAR PDF PARA WHATSAPP",
                    data=pdf_bytes,
                    file_name=nombre_archivo,
                    mime="application/pdf",
                    use_container_width=True
                )

                # Parte para WhatsApp
                st.divider()
                parte_wa = (
                    f"*PARTE PREVENTIVO*\n"
                    f"*Motivo:* Demora Art. 10 Bis\n"
                    f"*Jurisdicción:* {ciudad_actuante} ({dependencia})\n"
                    f"*Causante:* {apellido}\n"
                    f"*DNI:* {dni}\n"
                    f"*Hora:* {hora_actual} hs."
                )
                st.text_area("Copia el parte para el grupo:", value=parte_wa, height=150)

            except Exception as e:
                st.error(f"Error técnico: {e}")
        else:
            st.warning("⚠️ Debes completar Apellido y DNI para generar el documento.")

if __name__ == "__main__":
    main()

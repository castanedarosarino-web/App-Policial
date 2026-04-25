import streamlit as st
from fpdf import FPDF
import datetime

# --- 1. JURISDICCIONES INSPECCIÓN 8va ---
JURISDICCIONES = {
    "Pérez": {"tipo": "Ciudad", "depto": "Rosario"},
    "Funes": {"tipo": "Ciudad", "depto": "Rosario"},
    "Soldini": {"tipo": "Localidad", "depto": "Rosario"},
    "Zavalla": {"tipo": "Localidad", "depto": "Rosario"},
    "Rosario": {"tipo": "Ciudad", "depto": "Rosario"}
}

def main():
    st.set_page_config(page_title="Acta Art. 10 Bis", layout="centered")
    st.title("⚖️ Acta de Demora Art. 10 Bis")
    st.info("Configurado para la Inspección 8va (Pérez, Funes, Soldini, Zavalla)")

    # --- 2. ENTRADA DE DATOS ---
    col1, col2 = st.columns(2)
    with col1:
        ciudad_actuante = st.selectbox("Lugar de la demora:", list(JURISDICCIONES.keys()))
        apellido = st.text_input("Apellido del demorado:").upper()
    with col2:
        dni = st.text_input("DNI del demorado:")
        ciudad_demorado = st.text_input("Ciudad de residencia del demorado:").upper()

    info_j = JURISDICCIONES[ciudad_actuante]
    prefijo = "la Ciudad" if info_j["tipo"] == "Ciudad" else "la Localidad"

    # --- 3. GENERACIÓN ---
    if st.button("GENERAR ACTA Y PARTE", use_container_width=True):
        if apellido and dni:
            try:
                pdf = FPDF()
                pdf.add_page()
                
                # Título Profesional
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "ACTA DE DEMORA - ART. 10 BIS LEY 11.516", ln=True, align='C')
                pdf.ln(5)

                # Cuerpo del Acta (Recuperando el texto legal)
                pdf.set_font("Arial", size=11)
                ahora = datetime.datetime.now()
                
                # Lógica de domicilio
                if ciudad_demorado.lower() == ciudad_actuante.lower():
                    domicilio_txt = "domiciliado en esta ciudad"
                else:
                    domicilio_txt = f"domiciliado en la localidad de {ciudad_demorado}"

                cuerpo_legal = (
                    f"En {prefijo} de {ciudad_actuante}, Departamento {info_j['depto']}, "
                    f"Provincia de Santa Fe, a los {ahora.day} días del mes de {ahora.strftime('%m')} "
                    f"del año {ahora.year}, siendo las {ahora.strftime('%H:%M')} horas, se procede a la "
                    f"demora de quien dice llamarse {apellido}, DNI {dni}, {domicilio_txt}. "
                    "\n\nSe le hace saber el motivo de su demora en virtud del Art. 10 Bis, "
                    "haciéndole conocer los derechos que le asisten, informándole que el plazo "
                    "máximo de demora es de 6 (seis) horas según la normativa vigente."
                )
                pdf.multi_cell(0, 8, txt=cuerpo_legal)
                pdf.ln(10)
                
                # Espacios para firmas
                pdf.cell(0, 10, "_________________________          _________________________", ln=True, align='C')
                pdf.cell(0, 5, "Firma del Actuante                      Firma del Demorado", ln=True, align='C')

                # --- 4. EXPORTACIÓN SEGURA ---
                pdf_output = pdf.output(dest='S')
                # Forzamos conversión a bytes para evitar el error anterior
                if isinstance(pdf_output, str):
                    pdf_bytes = pdf_output.encode('latin-1')
                else:
                    pdf_bytes = bytes(pdf_output)

                nombre_archivo = f"10Bis_{apellido}_{dni}.pdf"

                st.success(f"✅ Acta de {apellido} generada correctamente.")

                # Botón de Descarga
                st.download_button(
                    label="📥 DESCARGAR PDF PARA WHATSAPP",
                    data=pdf_bytes,
                    file_name=nombre_archivo,
                    mime="application/pdf",
                    use_container_width=True
                )

                # Parte para copiar
                st.divider()
                parte_txt = f"*PARTE PREVENTIVO*\n*Demora Art. 10 Bis*\n*Lugar:* {ciudad_actuante}\n*Causante:* {apellido}\n*DNI:* {dni}"
                st.text_area("Copia este parte:", value=parte_txt, height=120)

            except Exception as e:
                st.error(f"Error al procesar: {e}")
        else:
            st.warning("Completá los datos antes de generar.")

if __name__ == "__main__":
    main()

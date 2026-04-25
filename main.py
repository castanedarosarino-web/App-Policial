import streamlit as st
from fpdf import FPDF
import datetime

def main():
    st.set_page_config(page_title="App Policial - Art. 10 Bis", layout="centered")
    st.title("Sistema de Actas Art. 10 Bis")

    # --- CAMPOS DE ENTRADA ORIGINALES ---
    ciudad_actuante = st.text_input("Ciudad/Localidad donde se labra el acta:", "Rosario")
    dependencia = st.text_input("Dependencia Policial:", "Comisaría / Subcomisaría")
    
    col1, col2 = st.columns(2)
    with col1:
        apellido = st.text_input("Apellido del demorado:").upper()
        dni = st.text_input("DNI del demorado:")
    with col2:
        domicilio = st.text_input("Domicilio declarado:")

    if st.button("GENERAR ACTA Y PARTE", use_container_width=True):
        if apellido and dni:
            try:
                # 1. Configuración del PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                
                # Encabezado
                pdf.cell(0, 10, "POLICIA DE SANTA FE - UNIDAD REGIONAL II", ln=True, align='C')
                pdf.cell(0, 10, f"{dependencia.upper()}", ln=True, align='C')
                pdf.ln(5)
                pdf.cell(0, 10, "ACTA DE DEMORA - ART. 10 BIS LEY 11.516", ln=True, align='C', border='B')
                pdf.ln(10)

                # Cuerpo Legal
                pdf.set_font("Arial", size=12)
                ahora = datetime.datetime.now()
                fecha_actual = ahora.strftime('%d/%m/%Y')
                hora_actual = ahora.strftime('%H:%M')

                cuerpo_texto = (
                    f"En la ciudad de {ciudad_actuante}, Provincia de Santa Fe, a los {ahora.day} días "
                    f"del mes de {ahora.month} del año {ahora.year}, siendo las {hora_actual} horas, "
                    f"se procede a la demora preventiva de {apellido}, DNI {dni}, domiciliado en {domicilio}. "
                    f"\n\nSe le hace saber el motivo de la presente medida en virtud del Art. 10 Bis de la Ley 11.516. "
                    f"Se le informa que cuenta con el derecho de dar aviso a un familiar y que el plazo máximo "
                    f"de demora no podrá exceder las 6 (seis) horas."
                )
                
                pdf.multi_cell(0, 10, txt=cuerpo_texto)
                pdf.ln(20)
                
                # Firmas
                pdf.cell(90, 10, "_______________________", ln=0, align='C')
                pdf.cell(90, 10, "_______________________", ln=1, align='C')
                pdf.cell(90, 5, "Firma Actuante", ln=0, align='C')
                pdf.cell(90, 5, "Firma Demorado", ln=1, align='C')

                # 2. Manejo de la salida de datos (Protección contra errores)
                pdf_output = pdf.output(dest='S')
                if isinstance(pdf_output, str):
                    pdf_bytes = pdf_output.encode('latin-1')
                else:
                    pdf_bytes = bytes(pdf_output)

                # 3. Resultados en pantalla
                st.success(f"✅ Acta de {apellido} generada con éxito.")

                st.download_button(
                    label="📥 DESCARGAR PDF PARA WHATSAPP",
                    data=pdf_bytes,
                    file_name=f"Acta_10Bis_{apellido}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

                # Parte de texto
                st.divider()
                parte_wa = (
                    f"*PARTE PREVENTIVO*\n"
                    f"*Demora Art. 10 Bis*\n"
                    f"*Lugar:* {ciudad_actuante}\n"
                    f"*Causante:* {apellido}\n"
                    f"*DNI:* {dni}\n"
                    f"*Hora:* {hora_actual} hs."
                )
                st.text_area("Copiar texto para WhatsApp:", value=parte_wa, height=150)

            except Exception as e:
                st.error(f"Error técnico: {e}")
        else:
            st.warning("⚠️ Completá Apellido y DNI.")

if __name__ == "__main__":
    main()

import streamlit as st
from fpdf import FPDF
import datetime

def main():
    st.set_page_config(page_title="App Policial", layout="centered")
    st.title("Sistema de Actas Art. 10 Bis")

    # --- CAMPOS DE CARGA ---
    ciudad_actuante = st.text_input("En la ciudad de:", "Rosario")
    
    col1, col2 = st.columns(2)
    with col1:
        apellido = st.text_input("Apellido del demorado:").upper()
        dni = st.text_input("DNI del demorado:")
    with col2:
        domicilio = st.text_input("Domiciliado en:")
        dependencia = st.text_input("Dependencia Policial:")

    if st.button("GENERAR ACTA Y PARTE", use_container_width=True):
        if apellido and dni:
            try:
                # 1. GENERACIÓN DEL PDF
                pdf = FPDF()
                pdf.add_page()
                
                # Encabezado
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "POLICIA DE SANTA FE", ln=True, align='C')
                pdf.cell(0, 10, f"UNIDAD REGIONAL II - {dependencia.upper()}", ln=True, align='C')
                pdf.ln(5)
                pdf.cell(0, 10, "ACTA DE PROCEDIMIENTO - ART. 10 BIS LEY 11.516", ln=True, align='C', border='B')
                pdf.ln(10)

                # Cuerpo del Acta
                pdf.set_font("Arial", size=12)
                ahora = datetime.datetime.now()
                hora_actual = ahora.strftime('%H:%M')
                
                cuerpo = (
                    f"En la ciudad de {ciudad_actuante}, Provincia de Santa Fe, a los {ahora.day} días "
                    f"del mes de {ahora.month} del año {ahora.year}, siendo las {hora_actual} horas, "
                    f"se procede a la demora de quien dice llamarse {apellido}, DNI {dni}, "
                    f"domiciliado en {domicilio}. \n\n"
                    "Se le hace saber el motivo de su demora en virtud del Art. 10 Bis de la Ley N° 11.516, "
                    "haciéndole conocer los derechos que le asisten y que el plazo máximo de la presente "
                    "medida no podrá exceder de las 6 (seis) horas conforme a la normativa vigente."
                )
                
                pdf.multi_cell(0, 10, txt=cuerpo)
                pdf.ln(20)
                
                # Firmas
                pdf.cell(90, 10, "_______________________", ln=0, align='C')
                pdf.cell(90, 10, "_______________________", ln=1, align='C')
                pdf.cell(90, 5, "Firma del Actuante", ln=0, align='C')
                pdf.cell(90, 5, "Firma del Demorado", ln=1, align='C')

                # 2. CONVERSIÓN BINARIA SEGURA (Para que no falle la descarga)
                pdf_output = pdf.output(dest='S')
                if isinstance(pdf_output, str):
                    pdf_bytes = pdf_output.encode('latin-1')
                else:
                    pdf_bytes = bytes(pdf_output)

                # 3. INTERFAZ DE SALIDA
                st.success(f"Acta de {apellido} generada con éxito.")
                
                st.download_button(
                    label="📥 DESCARGAR PDF PARA WHATSAPP",
                    data=pdf_bytes,
                    file_name=f"Acta_10Bis_{apellido}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

                st.divider()
                # Parte de WhatsApp
                parte_wa = (
                    f"*PARTE PREVENTIVO*\n"
                    f"*Demora:* Art. 10 Bis\n"
                    f"*Lugar:* {ciudad_actuante}\n"
                    f"*Causante:* {apellido}\n"
                    f"*DNI:* {dni}\n"
                    f"*Hora:* {hora_actual} hs."
                )
                st.text_area("Texto para WhatsApp:", value=parte_wa, height=150)

            except Exception as e:
                st.error(f"Error técnico: {e}")
        else:
            st.warning("Completá los datos obligatorios.")

if __name__ == "__main__":
    main()

import streamlit as st
from fpdf import FPDF
import datetime

# --- 1. CONFIGURACIÓN DE JURISDICCIONES ---
JURISDICCIONES = {
    "Pérez": {"tipo": "Ciudad", "depto": "Rosario"},
    "Funes": {"tipo": "Ciudad", "depto": "Rosario"},
    "Soldini": {"tipo": "Localidad", "depto": "Rosario"},
    "Zavalla": {"tipo": "Localidad", "depto": "Rosario"},
    "Rosario": {"tipo": "Ciudad", "depto": "Rosario"}
}

def main():
    st.title("Sistema de Actas Art. 10 Bis")
    
    # --- 2. ENTRADA DE DATOS ---
    col1, col2 = st.columns(2)
    with col1:
        ciudad_actuante = st.selectbox("Lugar de la demora:", list(JURISDICCIONES.keys()))
        apellido = st.text_input("Apellido del demorado:").upper()
    with col2:
        dni = st.text_input("DNI:")
        domicilio_ciudad = st.text_input("Ciudad/Localidad del demorado:")

    # Lógica de redacción automática
    info = JURISDICCIONES[ciudad_actuante]
    prefijo = "la Ciudad" if info["tipo"] == "Ciudad" else "la Localidad"
    
    # --- 3. PROCESAMIENTO ---
    if st.button("Generar Acta y Parte"):
        if apellido and dni:
            try:
                # Crear el PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, txt="ACTA DE DEMORA ART. 10 BIS", ln=True, align='C')
                
                pdf.set_font("Arial", size=12)
                fecha_texto = datetime.datetime.now().strftime('%d/%m/%Y a las %H:%M')
                cuerpo = f"En {prefijo} de {ciudad_actuante}, Departamento {info['depto']}, siendo fecha {fecha_texto}..."
                pdf.multi_cell(0, 10, txt=cuerpo)
                
                # --- SOLUCIÓN AL ERROR DE SALIDA ---
                # Usamos bytearray para asegurar compatibilidad total
                pdf_bytes = pdf.output(dest='S')
                if isinstance(pdf_bytes, str):
                    pdf_bytes = pdf_bytes.encode('latin-1')
                
                # --- 4. NOMBRE DE ARCHIVO Y DESCARGA ---
                hora_proc = datetime.datetime.now().strftime("%H%M")
                nombre_archivo = f"10Bis_{apellido}_{dni}_{hora_proc}.pdf"

                st.success(f"✅ Acta de {apellido} generada")

                st.download_button(
                    label="📥 DESCARGAR PDF PARA WHATSAPP",
                    data=pdf_bytes,
                    file_name=nombre_archivo,
                    mime="application/pdf"
                )

                # Parte de texto
                parte_wa = f"*PARTE PREVENTIVO*\n*Demora Art. 10 Bis*\n*Lugar:* {ciudad_actuante}\n*Causante:* {apellido}, DNI {dni}"
                st.text_area("Copiar para WhatsApp:", value=parte_wa, height=100)

            except Exception as e:
                st.error(f"Error técnico al generar el archivo: {e}")
        else:
            st.error("Faltan datos críticos (Apellido o DNI).")

if __name__ == "__main__":
    main()

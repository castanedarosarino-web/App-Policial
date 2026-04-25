import streamlit as st
from fpdf import FPDF
import datetime
import base64

# --- 1. CONFIGURACIÓN DE JURISDICCIONES (INSPECCIÓN 8va) ---
JURISDICCIONES = {
    "Pérez": {"tipo": "Ciudad", "depto": "Rosario"},
    "Funes": {"tipo": "Ciudad", "depto": "Rosario"},
    "Soldini": {"tipo": "Localidad", "depto": "Rosario"},
    "Zavalla": {"tipo": "Localidad", "depto": "Rosario"},
    "Rosario": {"tipo": "Ciudad", "depto": "Rosario"}
}

def main():
    st.title("Sistema de Actas Art. 10 Bis")
    st.subheader("Jurisdicción Inspección 8va")

    # --- 2. ENTRADA DE DATOS (Lo que ya tenías funcionando) ---
    col1, col2 = st.columns(2)
    with col1:
        ciudad_actuante = st.selectbox("Lugar de la demora:", list(JURISDICCIONES.keys()))
        apellido = st.text_input("Apellido del demorado:").upper()
    with col2:
        dni = st.text_input("DNI:")
        domicilio_ciudad = st.text_input("Ciudad/Localidad del demorado:")

    # Lógica de redacción automática según el tipo de lugar
    info = JURISDICCIONES[ciudad_actuante]
    prefijo = "la Ciudad" if info["tipo"] == "Ciudad" else "la Localidad"
    
    # --- 3. GENERACIÓN DEL PDF (Estructura protegida) ---
    if st.button("Generar Acta y Parte"):
        if apellido and dni:
            # Crear el PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            
            # Encabezado dinámico
            pdf.cell(200, 10, txt=f"ACTA DE DEMORA ART. 10 BIS", ln=True, align='C')
            pdf.set_font("Arial", size=12)
            
            # El texto legal que ya pulimos
            cuerpo_acta = f"En {prefijo} de {ciudad_actuante}, Departamento {info['depto']}, a los {datetime.datetime.now().strftime('%d')} días..."
            pdf.multi_cell(0, 10, txt=cuerpo_acta)
            
            # Guardar PDF en memoria
            pdf_output = pdf.output(dest='S').encode('latin-1')
            
            # --- 4. NOMBRE DE ARCHIVO INTELIGENTE ---
            hora_proc = datetime.datetime.now().strftime("%H%M")
            nombre_archivo = f"10Bis_{apellido}_{dni}_{hora_proc}.pdf"

            # --- 5. INTERFAZ DE SALIDA (Para el policía de calle) ---
            st.success("✅ Acta generada correctamente")

            # Botón de Descarga con el nombre específico
            st.download_button(
                label="📥 DESCARGAR PDF PARA WHATSAPP",
                data=pdf_output,
                file_name=nombre_archivo,
                mime="application/pdf"
            )

            # Parte de WhatsApp para copiar
            parte_wa = f"*PARTE PREVENTIVO*\n*Demora Art. 10 Bis*\n*Lugar:* {ciudad_actuante}\n*Causante:* {apellido}, DNI {dni}"
            st.text_area("Copiar este texto para WhatsApp:", value=parte_wa, height=100)
            
            st.info("💡 Al descargar, el archivo tendrá el apellido del demorado para que lo encuentres rápido al adjuntar en WhatsApp.")
        else:
            st.error("Por favor, completa Apellido y DNI.")

if __name__ == "__main__":
    main()

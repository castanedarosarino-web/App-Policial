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
    # Configuración de página para móviles
    st.set_page_config(page_title="App Policial - Art. 10 Bis", layout="centered")
    
    st.title("⚖️ Acta de Demora Art. 10 Bis")
    st.info("Configurado para la Inspección 8va (Pérez, Funes, Soldini, Zavalla)")

    # --- 2. ENTRADA DE DATOS ---
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            ciudad_actuante = st.selectbox("Lugar de la demora (Actuante):", list(JURISDICCIONES.keys()))
            apellido = st.text_input("Apellido del demorado:").upper()
        with col2:
            dni = st.text_input("DNI del demorado:")
            ciudad_demorado = st.text_input("Ciudad/Localidad de residencia del demorado:").upper()

    # Lógica de redacción automática según el rango del lugar
    info_juris = JURISDICCIONES[ciudad_actuante]
    prefijo_actuante = "la Ciudad" if info_juris["tipo"] == "Ciudad" else "la Localidad"

    # --- 3. PROCESAMIENTO Y GENERACIÓN ---
    if st.button("GENERAR ACTA Y PARTE", use_container_width=True):
        if apellido and dni:
            try:
                # Inicializar PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 14)
                
                # Título del acta
                pdf.cell(0, 10, txt="ACTA DE DEMORA - ARTICULO 10 BIS LEY 11.516", ln=True, align='C')
                pdf.ln(5)
                
                # Cuerpo del Acta
                pdf.set_font("Arial", size=12)
                ahora = datetime.datetime.now()
                fecha_hoy = ahora.strftime('%d/%m/%Y')
                hora_hoy = ahora.strftime('%H:%M')
                
                # Determinamos la redacción del domicilio del demorado
                texto_domicilio = f"domiciliado en esta ciudad" if ciudad_demorado.lower() == ciudad_actuante.lower() else f"domiciliado en la localidad de {ciudad_demorado}"

                texto_cuerpo = (
                    f"En {prefijo_actuante} de {ciudad_actuante}, Departamento {info_juris['depto']}, "
                    f"Provincia de Santa Fe, a los {ahora.day} días del mes de {ahora.strftime('%B')} "
                    f"del año {ahora.year}, siendo las {hora_hoy} horas, se procede a la demora de "
                    f"quien dice llamarse {apellido}, DNI {dni}, {texto_domicilio}..."
                )
                
                pdf.multi_cell(0, 10, txt=texto_cuerpo)
                
                # --- SOLUCIÓN BINARIA (Bytes puros para Streamlit) ---
                pdf_output = pdf.output(dest='S')
                if isinstance(pdf_output, str):
                    pdf_bytes = bytes(pdf_output, 'latin-1')
                else:
                    pdf_bytes = bytes(pdf_output)
                
                # --- 4. NOMBRE DE ARCHIVO DINÁMICO ---
                # Esto es lo que permite encontrarlo rápido en WhatsApp
                nombre_archivo = f"10Bis_{apellido}_{dni}_{ahora.strftime('%H%M')}.pdf"

                st.success(f"✅ Acta de {apellido} lista para enviar")

                # Botón de Descarga
                st.download_button(
                    label="📥 DESCARGAR PDF PARA WHATSAPP",
                    data=pdf_bytes,
                    file_name=nombre_archivo,
                    mime="application/pdf",
                    use_container_width=True
                )

                # Parte para copiar y pegar
                st.divider()
                st.subheader("Parte de WhatsApp")
                parte_wa = (
                    f"*PARTE PREVENTIVO*\n"
                    f"*Procedimiento:* Demora Art. 10 Bis\n"
                    f"*Lugar:* {ciudad_actuante} ({prefijo_actuante})\n"
                    f"*Causante:* {apellido}\n"
                    f"*DNI:* {dni}\n"
                    f"*Fecha/Hora:* {fecha_hoy} - {hora_hoy}hs"
                )
                st.text_area("Copiá este texto:", value=parte_wa, height=150)
                st.info("💡 Consejo: Al tocar 'Adjuntar' en WhatsApp, buscá el archivo que empieza con el Apellido del demorado.")

            except Exception as e:
                st.error(f"Error técnico: {e}")
        else:
            st.warning("⚠️ Falta completar Apellido o DNI para generar el documento.")

if __name__ == "__main__":
    main()

// --- 1. VARIABLES DE CONFIGURACIÓN DE JURISDICCIÓN (Inspección 8va) ---
const jurisdicciones = {
    "Perez": { tipo: "Ciudad", depto: "Rosario" },
    "Funes": { tipo: "Ciudad", depto: "Rosario" },
    "Soldini": { tipo: "Localidad", depto: "Rosario" },
    "Zavalla": { tipo: "Localidad", depto: "Rosario" },
    "Rosario": { tipo: "Ciudad", depto: "Rosario" }
};

// --- 2. FUNCIÓN PARA GENERAR EL NOMBRE DEL ARCHIVO ---
function generarNombreArchivo(apellido, dni) {
    const ahora = new Date();
    const hora = ahora.getHours() + "" + ahora.getMinutes();
    // Limpiamos espacios para evitar errores en el sistema de archivos
    return `10Bis_${apellido.trim().toUpperCase()}_${dni.trim()}_${hora}.pdf`;
}

// --- 3. FUNCIÓN MAESTRA: GENERAR Y COMPARTIR ---
// Esta es la función que debés vincular al botón "FINALIZAR"
async function finalizarYCompartir() {
    try {
        // A. Captura de datos del formulario (manteniendo tus IDs actuales)
        const apellido = document.getElementById('apellido_demorado').value;
        const dni = document.getElementById('dni_demorado').value;
        const lugarActuacion = document.getElementById('lista_ciudades').value;
        
        // Determinamos si es Ciudad o Localidad según la Inspección 8va
        const infoLugar = jurisdicciones[lugarActuacion] || { tipo: "Ciudad", depto: "Rosario" };
        const prefijoLugar = infoLugar.tipo === "Localidad" ? "la Localidad de" : "la Ciudad de";

        // B. GENERACIÓN DEL PDF 
        // (Aquí el programa ejecuta tu lógica de jsPDF que ya funciona)
        const doc = generarEstructuraPDF(prefijoLugar); // Tu función actual de dibujo
        
        const pdfBlob = doc.output('blob');
        const nombreArchivo = generarNombreArchivo(apellido, dni);
        const file = new File([pdfBlob], nombreArchivo, { type: 'application/pdf' });

        // C. LÓGICA DE WHATSAPP (PARTE TEXTUAL)
        const textoWhatsApp = generarParteWhatsApp(); // Tu función actual de texto
        navigator.clipboard.writeText(textoWhatsApp);

        // D. SISTEMA DE COMPARTIR (WEB SHARE API)
        if (navigator.canShare && navigator.canShare({ files: [file] })) {
            await navigator.share({
                files: [file],
                title: 'Acta de Demora Art. 10 Bis',
                text: 'Se adjunta acta y se copió el parte al portapapeles.'
            });
        } else {
            // Backup por si el navegador es viejo: Descarga tradicional
            const link = document.createElement('a');
            link.href = URL.createObjectURL(pdfBlob);
            link.download = nombreArchivo;
            link.click();
            alert("El archivo se descargó en la carpeta 'Descargas'. El parte de texto ya está copiado.");
        }

    } catch (error) {
        console.error("Error en el proceso:", error);
        alert("Hubo un problema al generar. Revisar conexión.");
    }
}

// Configuración de colores para el tema híbrido de la aplicación
export const temaHibrido = {
  backgroundColor: 'rgba(30, 41, 55, 0.8)',  // Fondo semi-transparente oscuro
  gridColor: 'rgba(55, 65, 81, 0.6)',        // Color de la cuadrícula
  textColor: '#d1d5db',                       // Color del texto (gris claro)
  chartColor: '#06b6d4',                      // Color principal para gráficos (cyan)
  successColor: '#10b981',                    // Verde para éxito/aprobado
  warningColor: '#f59e0b',                    // Amarillo para advertencias
  errorColor: '#ef4444'                       // Rojo para errores/no aprobado
};

// Función para exportar gráficos como imagen PNG
export function exportarImagen(canvas, nombrePrueba) {
  // Crear enlace temporal para descarga
  const link = document.createElement("a");

  // Configurar nombre del archivo (reemplazar espacios con guiones bajos)
  link.download = `${nombrePrueba.replace(/\s+/g, "_")}_hibrido.png`;

  // Convertir canvas a imagen PNG de alta calidad
  link.href = canvas.toDataURL("image/png", 1.0);

  // Simular click para iniciar descarga
  link.click();
}
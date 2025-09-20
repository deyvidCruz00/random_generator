import { temaHibrido } from '../utils.js';

export function obtenerConfiguracionChiCuadrado(prueba) {
    /**
     * Genera configuración para Chart.js que visualiza los resultados 
     * de la prueba chi-cuadrado como gráfico de barras + línea
     * 
     * @param {Object} prueba - Objeto JSON con resultados del test chi-cuadrado
     * @returns {Object} Configuración completa para Chart.js
     */

    // PASO 1: Extraer datos de los intervalos
    // Crear etiquetas para cada intervalo mostrando su rango [inicio, fin)
    const etiquetas = prueba.intervals_data.map(intervalo =>
        `[${intervalo.inicio.toFixed(3)}, ${intervalo.fin.toFixed(3)})`
    );

    // Extraer frecuencias observadas de cada intervalo
    const frecuenciasObservadas = prueba.intervals_data.map(intervalo => intervalo.frecuencia_obt);

    // PASO 2: Calcular frecuencia esperada uniforme
    const n = prueba.n;           // Total de datos
    const k = prueba.intervals;   // Número de intervalos
    const frecuenciaEsperada = n / k;  // Para distribución uniforme: cada intervalo debería tener n/k datos

    // PASO 3: Configurar Chart.js
    return {
        type: 'bar',  // Tipo principal: gráfico de barras
        data: {
            labels: etiquetas,  // Etiquetas del eje X
            datasets: [
                // Dataset 1: Barras para frecuencias observadas
                {
                    label: 'Frecuencia Observada',
                    data: frecuenciasObservadas,
                    backgroundColor: 'rgba(6, 182, 212, 0.7)',  // Azul cyan semi-transparente
                    borderColor: '#06b6d4',                     // Borde azul cyan
                    borderWidth: 1
                },
                // Dataset 2: Línea horizontal para frecuencia esperada
                {
                    label: `Frecuencia Esperada (${frecuenciaEsperada.toFixed(2)})`,
                    data: Array(etiquetas.length).fill(frecuenciaEsperada),  // Array con mismo valor repetido
                    type: 'line',              // Superponer línea sobre barras
                    borderColor: '#ef4444',    // Rojo para contraste
                    borderWidth: 2,
                    borderDash: [6, 4],        // Línea punteada (6px línea, 4px espacio)
                    fill: false,               // Sin relleno bajo la línea
                    pointRadius: 0,            // Sin puntos en los vértices
                    tension: 0                 // Línea recta (sin curvas)
                }
            ]
        },
        options: {
            // CONFIGURACIÓN GENERAL
            responsive: true,
            maintainAspectRatio: false,  // Permite redimensionar libremente

            plugins: {
                // LEYENDA
                legend: {
                    display: true,
                    labels: { color: temaHibrido.textColor }  // Color del texto según tema
                },

                // TÍTULO
                title: {
                    display: true,
                    // Título dinámico con estadísticos clave
                    text: `Prueba Chi-Cuadrado - χ² = ${prueba.statistics.chi2_total.toFixed(3)} (Crítico: ${prueba.statistics.chi2_critico.toFixed(3)})`,
                    color: temaHibrido.textColor,
                    font: { size: 16, weight: 'bold' }
                },

                // TOOLTIPS (información al hacer hover)
                tooltip: {
                    enabled: true,
                    backgroundColor: 'rgba(30, 41, 55, 0.9)',  // Fondo oscuro semi-transparente
                    titleColor: temaHibrido.textColor,
                    bodyColor: temaHibrido.textColor,
                    borderColor: temaHibrido.chartColor,
                    borderWidth: 1
                }
            },

            // CONFIGURACIÓN DE EJES
            scales: {
                // EJE X (horizontal)
                x: {
                    title: {
                        display: true,
                        text: 'Intervalos',
                        color: temaHibrido.textColor
                    },
                    grid: { color: temaHibrido.gridColor },     // Color de líneas de cuadrícula
                    ticks: { color: temaHibrido.textColor }     // Color de etiquetas
                },
                // EJE Y (vertical)
                y: {
                    title: {
                        display: true,
                        text: 'Frecuencia',
                        color: temaHibrido.textColor
                    },
                    grid: { color: temaHibrido.gridColor },
                    ticks: { color: temaHibrido.textColor }
                }
            }
        }
    };
}

/**
 * ¿QUÉ VISUALIZA ESTE GRÁFICO?
 * 
 * INTERPRETACIÓN VISUAL:
 * 1. BARRAS AZULES: Frecuencias realmente observadas en cada intervalo
 * 2. LÍNEA ROJA PUNTEADA: Frecuencia que se esperaría si los datos fueran perfectamente uniformes
 * 
 * CÓMO LEER EL GRÁFICO:
 * - Si las barras están CERCA de la línea roja → distribución uniforme (BUENO)
 * - Si las barras están MUY ARRIBA o MUY ABAJO de la línea → no uniforme (MALO)
 * - Cuanto más "planas" las barras, mejor es la uniformidad
 * 
 * ELEMENTOS CLAVE:
 * - Título incluye χ² calculado vs crítico para decisión rápida
 * - Tooltips muestran valores exactos al hacer hover
 * - Tema híbrido para consistencia visual con la aplicación
 * 
 * EJEMPLO DE INTERPRETACIÓN:
 * Si χ² calculado = 5.2 y crítico = 12.6:
 * - Las barras deberían estar relativamente cerca de la línea roja
 * - El test pasa (5.2 < 12.6), confirmando uniformidad
 * 
 * Si χ² calculado = 18.3 y crítico = 12.6:
 * - Habrá barras muy altas o muy bajas comparadas con la línea
 * - El test falla (18.3 > 12.6), rechazando uniformidad
 */
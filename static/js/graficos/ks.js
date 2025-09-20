import { temaHibrido } from '../utils.js';

// Configuración para la prueba de Kolmogorov-Smirnov
export function obtenerConfiguracionKolmogorov(prueba) {
    /**
     * Genera configuración para Chart.js que visualiza los resultados 
     * de la prueba de Kolmogorov-Smirnov comparando distribuciones acumuladas
     * 
     * @param {Object} prueba - Objeto JSON con resultados del test KS
     * @returns {Object} Configuración completa para Chart.js
     */

    // PASO 1: Extraer datos de los intervalos
    // Crear etiquetas para cada intervalo mostrando su rango [inicial, final)
    const etiquetas = prueba.intervals_data.map(intervalo =>
        `[${intervalo.Inicial.toFixed(3)}, ${intervalo.Final.toFixed(3)})`
    );

    // PASO 2: Extraer probabilidades acumuladas
    // P_Obt = proporción acumulada observada hasta este intervalo
    const probabilidadesObtenidas = prueba.intervals_data.map(intervalo => intervalo.P_Obt);
    // P_Esp_A = proporción acumulada esperada (distribución uniforme perfecta)
    const probabilidadesEsperadas = prueba.intervals_data.map(intervalo => intervalo.P_Esp_A);

    return {
        type: 'bar',  // Gráfico de barras agrupadas
        data: {
            labels: etiquetas,
            datasets: [
                // Dataset 1: Distribución esperada (uniforme)
                {
                    label: 'Probabilidad Esperada Acumulada',
                    data: probabilidadesEsperadas,
                    backgroundColor: 'rgba(6, 182, 212, 0.7)',  // Azul cyan semi-transparente
                    borderColor: '#06b6d4',
                    borderWidth: 2,
                    order: 2  // Se dibuja segundo (detrás)
                },
                // Dataset 2: Distribución observada
                {
                    label: 'Probabilidad Obtenida Acumulada',
                    data: probabilidadesObtenidas,
                    backgroundColor: 'rgba(16, 185, 129, 0.7)',  // Verde esmeralda semi-transparente
                    borderColor: '#10b981',
                    borderWidth: 2,
                    order: 1  // Se dibuja primero (al frente)
                }
            ]
        },
        options: {
            // CONFIGURACIÓN GENERAL
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                // LEYENDA
                legend: {
                    display: true,
                    labels: {
                        color: temaHibrido.textColor,
                        usePointStyle: true  // Usa puntos en lugar de rectángulos
                    }
                },

                // TÍTULO con estadísticos clave del test KS
                title: {
                    display: true,
                    text: `Prueba Kolmogorov-Smirnov - D_máx = ${prueba.statistics.max_difference.toFixed(5)} (Crítico: ${prueba.statistics.critical_value.toFixed(5)})`,
                    color: temaHibrido.textColor,
                    font: { size: 16, weight: 'bold' }
                },

                // TOOLTIPS personalizados
                tooltip: {
                    enabled: true,
                    backgroundColor: 'rgba(30, 41, 55, 0.9)',
                    titleColor: temaHibrido.textColor,
                    bodyColor: temaHibrido.textColor,
                    borderColor: temaHibrido.chartColor,
                    borderWidth: 1,
                    callbacks: {
                        // Personalizar título del tooltip
                        title: function (context) {
                            return `Intervalo: ${context[0].label}`;
                        },
                        // Personalizar contenido del tooltip
                        label: function (context) {
                            const datasetLabel = context.dataset.label;
                            const value = context.parsed.y;
                            return `${datasetLabel}: ${value.toFixed(4)}`;
                        }
                    }
                }
            },

            // CONFIGURACIÓN DE EJES
            scales: {
                // EJE X (intervalos)
                x: {
                    title: {
                        display: true,
                        text: 'Intervalos',
                        color: temaHibrido.textColor,
                        font: { size: 14 }
                    },
                    grid: { color: temaHibrido.gridColor },
                    ticks: {
                        color: temaHibrido.textColor,
                        maxRotation: 45,  // Rotar etiquetas si son muy largas
                        font: { size: 10 }
                    }
                },
                // EJE Y (probabilidades acumuladas 0-1)
                y: {
                    title: {
                        display: true,
                        text: 'Probabilidad Acumulada',
                        color: temaHibrido.textColor,
                        font: { size: 14 }
                    },
                    grid: { color: temaHibrido.gridColor },
                    ticks: {
                        color: temaHibrido.textColor,
                        callback: function (value) {
                            return value.toFixed(2);  // Mostrar 2 decimales
                        }
                    },
                    min: 0,    // Las probabilidades van de 0
                    max: 1.1   // a 1, con margen para mejor visualización
                }
            },

            // CONFIGURACIÓN DE INTERACCIÓN
            interaction: {
                intersect: false,  // No necesita intersección exacta para activar
                mode: 'index'      // Muestra info de ambas barras al mismo tiempo
            },
            hover: {
                mode: 'index',
                intersect: false
            }
        }
    };
}

/**
 * ¿QUÉ VISUALIZA ESTE GRÁFICO?
 * 
 * CONCEPTO CLAVE - FUNCIONES DE DISTRIBUCIÓN ACUMULADA (CDF):
 * - El test KS compara dos curvas de distribución acumulada
 * - Una curva es la esperada (uniforme perfecta)
 * - Otra curva es la observada (datos reales)
 * 
 * INTERPRETACIÓN VISUAL:
 * 1. BARRAS AZULES: Distribución acumulada esperada (escalones uniformes)
 *    - Debería crecer de forma constante: 0.1, 0.2, 0.3... 1.0
 * 
 * 2. BARRAS VERDES: Distribución acumulada observada (escalones reales)
 *    - Crece según los datos reales, puede ser irregular
 * 
 * 3. DIFERENCIAS ENTRE BARRAS: 
 *    - Pequeñas diferencias = distribución uniforme (BUENO)
 *    - Grandes diferencias = no uniforme (MALO)
 * 
 * CÓMO LEER EL GRÁFICO:
 * - Si las barras verdes y azules están MUY CERCA → datos uniformes ✅
 * - Si hay GRANDES SEPARACIONES entre barras → no uniformes ❌
 * - El test busca la MÁXIMA diferencia entre las dos distribuciones
 */
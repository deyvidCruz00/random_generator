import { temaHibrido } from '../utils.js';

// Configuración para la Prueba de Rachas con muestreo automático
export function obtenerConfiguracionRachas(prueba) {
    /**
     * Genera configuración para Chart.js que visualiza la evolución
     * de las rachas acumuladas comparando observadas vs esperadas
     * 
     * @param {Object} prueba - Objeto JSON con resultados del test de rachas
     * @returns {Object} Configuración completa para Chart.js
     */

    // PASO 1: Extraer estadísticos clave del test
    const n = prueba.Total;                 // Número total de observaciones
    const esperadas = prueba.UR;           // Número esperado de rachas
    const varianza = prueba.Varianza;      // Varianza de las rachas
    const desv = Math.sqrt(varianza);      // Desviación estándar

    // PASO 2: OPTIMIZACIÓN DE RENDIMIENTO
    // Límite máximo de puntos para evitar problemas de renderizado
    const maxPoints = 2000;
    const step = Math.max(1, Math.ceil(n / maxPoints));

    // PASO 3: Función auxiliar para muestreo inteligente
    function reducirDatos(generator) {
        const datos = [];
        // Generar puntos con muestreo uniforme
        for (let i = 1; i <= n; i += step) {
            datos.push(generator(i));
        }
        // Asegurar que el último punto siempre aparezca (importante para la tendencia final)
        if (datos[datos.length - 1].x !== n) {
            datos.push(generator(n));
        }
        return datos;
    }

    // PASO 4: Construcción de datasets con datos muestreados

    // Dataset 1: Rachas acumuladas observadas (pendiente real)
    const datosObservados = reducirDatos(i => ({
        x: i,                              // Posición en la secuencia
        y: (prueba.Rachas / n) * i        // Proyección lineal de rachas observadas
    }));

    // Dataset 2: Rachas acumuladas esperadas (pendiente teórica)
    const datosEsperados = reducirDatos(i => ({
        x: i,
        y: (esperadas / n) * i            // Proyección lineal de rachas esperadas
    }));

    // Dataset 3: Límite superior del intervalo de confianza
    const datosSup = reducirDatos(i => {
        const media = (esperadas / n) * i;
        const margen = 1.96 * (desv / Math.sqrt(n)) * (i / n);  // Margen de error 95%
        return { x: i, y: media + margen };
    });

    // Dataset 4: Límite inferior del intervalo de confianza
    const datosInf = reducirDatos(i => {
        const media = (esperadas / n) * i;
        const margen = 1.96 * (desv / Math.sqrt(n)) * (i / n);
        return { x: i, y: media - margen };
    });

    return {
        type: 'line',  // Gráfico de líneas para mostrar evolución temporal
        data: {
            datasets: [
                // Dataset 1: Línea principal - Rachas observadas
                {
                    label: 'Rachas acumuladas (observadas)',
                    data: datosObservados,
                    borderColor: 'rgba(6, 182, 212, 0.9)',   // Azul cyan destacado
                    backgroundColor: 'rgba(6, 182, 212, 0.5)',
                    borderWidth: 3,                           // Línea gruesa para destacar
                    borderDash: [4, 2],                       // Punteada para diferenciarse
                    fill: false,
                    tension: 0,                               // Línea recta (sin curvas)
                    pointRadius: n <= 200 ? 3 : 0,           // Puntos solo si hay pocos datos
                    order: 2                                  // Se dibuja encima de la esperada
                },
                // Dataset 2: Línea de referencia - Rachas esperadas
                {
                    label: 'Rachas esperadas',
                    data: datosEsperados,
                    borderColor: '#ef4444',                   // Rojo para contraste
                    borderDash: [6, 4],                       // Patrón diferente de línea punteada
                    fill: false,
                    borderWidth: 2,
                    tension: 0,
                    pointRadius: 0                            // Sin puntos visibles
                },
                // Dataset 3: Área de confianza (combinando límites superior e inferior)
                {
                    label: 'Intervalo de confianza 95%',
                    data: [...datosSup, ...datosInf.reverse()],  // Concatena superior + inferior invertido
                    backgroundColor: 'rgba(148, 163, 184, 0.4)', // Gris semi-transparente
                    borderColor: 'transparent',                   // Sin borde visible
                    fill: true,                                   // Rellena el área entre los límites
                    pointRadius: 0
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
                    labels: {
                        color: temaHibrido.textColor,
                        usePointStyle: true
                    }
                },
                // TÍTULO
                title: {
                    display: true,
                    text: `Evolución de las Rachas (n=${n})`,
                    color: temaHibrido.textColor,
                    font: { size: 16, weight: 'bold' }
                }
            },

            // CONFIGURACIÓN DE EJES
            scales: {
                // EJE X (progreso en la secuencia)
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'Número de observaciones',
                        color: temaHibrido.textColor
                    },
                    grid: { color: temaHibrido.gridColor },
                    ticks: { color: temaHibrido.textColor }
                },
                // EJE Y (rachas acumuladas)
                y: {
                    title: {
                        display: true,
                        text: 'Rachas acumuladas',
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
 * CONCEPTO PRINCIPAL:
 * Muestra cómo evolucionan las rachas a medida que se procesan más números,
 * comparando la tendencia real vs la esperada teóricamente.
 * 
 * ELEMENTOS VISUALES:
 * 
 * 1. 📈 LÍNEA AZUL PUNTEADA (gruesa): Rachas acumuladas observadas
 *    - Pendiente real de acumulación de rachas en los datos
 * 
 * 2. 📈 LÍNEA ROJA PUNTEADA: Rachas esperadas 
 *    - Pendiente teórica si los datos fueran perfectamente aleatorios
 * 
 * 3. 🔘 ÁREA GRIS: Intervalo de confianza del 95%
 *    - Zona donde la línea azul "debería" estar si es aleatoria
 * 
 * INTERPRETACIÓN:
 * 
 * ✅ SECUENCIA ALEATORIA:
 * - Línea azul PARALELA y CERCA de la línea roja
 * - Línea azul DENTRO del área gris
 * - Ambas líneas tienen pendientes similares
 * 
 * ❌ SECUENCIA NO ALEATORIA:
 * - Línea azul MUY SEPARADA de la línea roja
 * - Línea azul FUERA del área gris
 * - Pendientes muy diferentes
 * 
 * CASOS ESPECÍFICOS:
 * 
 * 🔽 LÍNEA AZUL POR DEBAJO (muy pocas rachas):
 * - Los números tienden a agruparse
 * - Ejemplo: muchos bajos seguidos, luego muchos altos
 * - Posible tendencia o patrón en el generador
 * 
 * 🔼 LÍNEA AZUL POR ENCIMA (demasiadas rachas):
 * - Los números alternan excesivamente
 * - Ejemplo: bajo-alto-bajo-alto repetitivamente
 * - Posible oscilación artificial
 */
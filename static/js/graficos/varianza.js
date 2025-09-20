import { temaHibrido } from '../utils.js';

export function obtenerConfiguracionVarianza(prueba) {
    /**
     * Genera configuración para Chart.js que visualiza el test de varianza
     * mostrando la distribución chi-cuadrado teórica y dónde cae el valor calculado
     * 
     * @param {Object} prueba - Objeto JSON con resultados del test de varianza
     * @returns {Object} Configuración completa para Chart.js
     */

    // PASO 1: Configurar parámetros estadísticos
    const gl = prueba.n - 1; // Grados de libertad = n - 1

    // Generar la curva de distribución chi-cuadrado teórica
    const datosChiCuadrado = generarDistribucionChiCuadrado(gl);

    // PASO 2: Crear área de aceptación (región entre límites críticos)
    // Filtrar solo los puntos que están dentro de los límites críticos
    const datosArea = datosChiCuadrado.filter(p =>
        p.x >= prueba.Xi1 && p.x <= prueba.Xi2
    );

    // Crear un polígono cerrado para rellenar el área
    // Agregar puntos en y=0 para cerrar la forma
    const areaCompleta = [
        { x: prueba.Xi1, y: 0 },    // Punto inicial en el eje X
        ...datosArea,               // Puntos de la curva
        { x: prueba.Xi2, y: 0 }     // Punto final en el eje X
    ];

    // PASO 3: Obtener valor chi-cuadrado calculado
    const chi2calc = prueba.chi2;   // Estadístico calculado del test

    return {
        type: 'line',  // Gráfico de líneas para mostrar la distribución continua
        data: {
            datasets: [
                // Dataset 1: Curva de distribución chi-cuadrado teórica
                {
                    label: 'Distribución χ² teórica',
                    data: datosChiCuadrado,
                    borderColor: temaHibrido.chartColor,     // Color principal del tema
                    backgroundColor: 'transparent',          // Sin relleno
                    fill: false,
                    tension: 0.4,                           // Curva suave
                    pointRadius: 0,                         // Sin puntos visibles
                    borderWidth: 3                          // Línea gruesa para destacar
                },
                // Dataset 2: Área de aceptación (región válida)
                {
                    label: 'Región de aceptación',
                    data: areaCompleta,
                    borderColor: 'transparent',              // Sin borde
                    backgroundColor: 'rgba(16, 185, 129, 0.3)', // Verde semi-transparente
                    fill: true,                              // Rellenar área
                    pointRadius: 0,
                    tension: 0.4
                },
                // Dataset 3: Línea vertical del valor calculado
                {
                    label: `χ² calculado = ${chi2calc.toFixed(3)}`,
                    data: [
                        { x: chi2calc, y: 0 },               // Base de la línea
                        { x: chi2calc, y: Math.max(...datosChiCuadrado.map(d => d.y)) } // Pico de la línea
                    ],
                    borderColor: temaHibrido.errorColor,     // Color de error/alerta
                    borderWidth: 2,
                    borderDash: [6, 4],                      // Línea punteada
                    pointRadius: 0,
                    showLine: true,                          // Conectar puntos con línea
                    fill: false
                },
                // Dataset 4: Línea vertical del límite inferior
                {
                    label: `LI = ${prueba.Xi1.toFixed(3)}`,
                    data: [
                        { x: prueba.Xi1, y: 0 },
                        { x: prueba.Xi1, y: Math.max(...datosChiCuadrado.map(d => d.y)) }
                    ],
                    borderColor: temaHibrido.warningColor,   // Color de advertencia
                    borderWidth: 2,
                    borderDash: [5, 5],                      // Patrón diferente de línea punteada
                    pointRadius: 0,
                    showLine: true,
                    fill: false
                },
                // Dataset 5: Línea vertical del límite superior
                {
                    label: `LS = ${prueba.Xi2.toFixed(3)}`,
                    data: [
                        { x: prueba.Xi2, y: 0 },
                        { x: prueba.Xi2, y: Math.max(...datosChiCuadrado.map(d => d.y)) }
                    ],
                    borderColor: temaHibrido.warningColor,
                    borderWidth: 2,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    showLine: true,
                    fill: false
                }
            ]
        },
        options: {
            // CONFIGURACIÓN GENERAL
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                tooltip: { enabled: false },                 // Sin tooltips (evita interferencia visual)
                legend: { labels: { color: temaHibrido.textColor } },
                title: {
                    display: true,
                    // Título con información clave del test
                    text: `Prueba de Varianza: σ² = ${prueba.varianza_muestral.toFixed(4)} (gl = ${gl})`,
                    color: temaHibrido.textColor,
                    font: { size: 14 }
                }
            },

            // CONFIGURACIÓN DE EJES
            scales: {
                // EJE X (valores de chi-cuadrado)
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'Valor χ²',
                        color: temaHibrido.textColor
                    },
                    grid: { color: temaHibrido.gridColor },
                    ticks: { color: temaHibrido.textColor }
                },
                // EJE Y (densidad de probabilidad)
                y: {
                    title: {
                        display: true,
                        text: 'Densidad de Probabilidad',
                        color: temaHibrido.textColor
                    },
                    grid: { color: temaHibrido.gridColor },
                    ticks: { color: temaHibrido.textColor }
                }
            }
        }
    };
}

// Generar distribución Chi-cuadrado con jStat
function generarDistribucionChiCuadrado(gl, puntos = 200) {
    /**
     * Genera puntos para dibujar la curva de distribución chi-cuadrado
     * 
     * @param {number} gl - Grados de libertad
     * @param {number} puntos - Número de puntos para la curva
     * @returns {Array} Array de objetos {x, y} para la curva
     */
    const datos = [];

    // PASO 1: Calcular rango apropiado para la visualización
    // Usar aproximaciones estadísticas para determinar límites visuales
    const min = Math.max(0, gl - 5 * Math.sqrt(2 * gl));      // Límite inferior
    const max = gl + 5 * Math.sqrt(2 * gl);                   // Límite superior
    const paso = (max - min) / puntos;                        // Incremento entre puntos

    // PASO 2: Generar puntos de la curva
    for (let i = min; i <= max; i += paso) {
        // Calcular densidad de probabilidad usando jStat
        const y = jStat.chisquare.pdf(i, gl);                 // Función de densidad chi²
        datos.push({ x: i, y: y });
    }

    return datos;
}

/**
 * ¿QUÉ VISUALIZA ESTE GRÁFICO?
 * 
 * CONCEPTO PRINCIPAL:
 * Muestra la distribución teórica chi-cuadrado y dónde cae el estadístico
 * calculado del test de varianza, permitiendo evaluación visual del resultado.
 * 
 * ELEMENTOS VISUALES:
 * 
 * 1. 📈 CURVA PRINCIPAL (color del tema): Distribución χ² teórica
 *    - Forma característica de campana asimétrica
 *    - Depende de los grados de libertad (n-1)
 * 
 * 2. 🟢 ÁREA VERDE: Región de aceptación
 *    - Zona donde el estadístico debe caer para pasar el test
 *    - Entre los límites críticos LI y LS
 * 
 * 3. 🔴 LÍNEA ROJA PUNTEADA: χ² calculado
 *    - Valor del estadístico obtenido del test
 *    - Su posición determina si pasa o no la prueba
 * 
 * 4. 🟡 LÍNEAS AMARILLAS: Límites críticos (LI y LS)
 *    - Definen los bordes de la región de aceptación
 *    - Valores de la tabla chi-cuadrado para α dado
 * 
 * INTERPRETACIÓN:
 * 
 * ✅ VARIANZA ACEPTABLE:
 * - Línea roja DENTRO del área verde
 * - El estadístico cae entre LI y LS
 * - La varianza observada es consistente con distribución uniforme
 * 
 * ❌ VARIANZA PROBLEMÁTICA:
 * - Línea roja FUERA del área verde
 * - Estadístico < LI: varianza muy baja (números muy concentrados)
 * - Estadístico > LS: varianza muy alta (números muy dispersos)
 * 
 * DEPENDENCIA DE JSTAT:
 * La función requiere la librería jStat para calcular la densidad
 * de probabilidad chi-cuadrado (jStat.chisquare.pdf).
 */
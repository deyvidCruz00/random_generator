import { temaHibrido } from '../utils.js';

export function obtenerConfiguracionMedias(prueba, nums) {
  /**
   * Genera configuración para Chart.js que visualiza el test de medias
   * mostrando todos los números individuales y las líneas de límites
   * 
   * @param {Object} prueba - Objeto JSON con resultados del test de medias
   * @param {Array} nums - Array original de números a graficar
   * @returns {Object} Configuración completa para Chart.js
   */

  // PASO 1: OPTIMIZACIÓN DE RENDIMIENTO
  // Límite máximo de puntos para evitar problemas de rendimiento
  const maxPoints = 2000;
  const step = Math.max(1, Math.ceil(nums.length / maxPoints));

  // PASO 2: PREPARAR DATOS CON MUESTREO INTELIGENTE
  // Crear puntos de datos con información de si están dentro del rango aceptable
  const datos = nums
    .map((valor, i) => ({
      x: i + 1,  // Índice empezando en 1
      y: valor,  // Valor del número
      enRango: valor >= prueba.limite_inferior && valor <= prueba.limite_superior
    }))
    .filter((_, i) => i % step === 0); // Muestreo: tomar cada "step" elementos

  // PASO 3: SEPARAR DATOS POR CATEGORÍAS
  const dentro = datos.filter(d => d.enRango);    // Números dentro del rango aceptable
  const fuera = datos.filter(d => !d.enRango);    // Números fuera del rango (problemáticos)

  return {
    type: 'scatter',  // Gráfico de dispersión para mostrar puntos individuales
    data: {
      datasets: [
        // Dataset 1: Puntos DENTRO del rango aceptable
        {
          label: `En rango [${prueba.limite_inferior.toFixed(2)}, ${prueba.limite_superior.toFixed(2)}]`,
          data: dentro.map(d => ({ x: d.x, y: d.y })),
          backgroundColor: 'red',  // Color rojo para los puntos válidos
          pointRadius: nums.length > 5000 ? 2 : 5  // Puntos más pequeños si hay muchos datos
        },
        // Dataset 2: Puntos FUERA del rango aceptable
        {
          label: 'Fuera del rango',
          data: fuera.map(d => ({ x: d.x, y: d.y })),
          backgroundColor: 'gray',  // Color gris para puntos problemáticos
          pointRadius: nums.length > 5000 ? 2 : 5
        },
        // Dataset 3: Línea de límite inferior
        {
          label: `Límite inferior = ${prueba.limite_inferior.toFixed(3)}`,
          data: [
            { x: 0, y: prueba.limite_inferior },         // Punto inicial
            { x: prueba.n, y: prueba.limite_inferior }   // Punto final
          ],
          borderColor: 'blue',
          borderDash: [6, 4],    // Línea punteada (6px línea, 4px espacio)
          borderWidth: 2,
          showLine: true,        // Conectar puntos con línea
          fill: false,           // Sin relleno
          pointRadius: 0         // Sin puntos visibles en los extremos
        },
        // Dataset 4: Línea de límite superior  
        {
          label: `Límite superior = ${prueba.limite_superior.toFixed(3)}`,
          data: [
            { x: 0, y: prueba.limite_superior },
            { x: prueba.n, y: prueba.limite_superior }
          ],
          borderColor: 'blue',
          borderDash: [6, 4],
          borderWidth: 2,
          showLine: true,
          fill: false,
          pointRadius: 0
        },
        // Dataset 5: Línea de media observada
        {
          label: `Media muestral = ${prueba.media_muestra.toFixed(3)}`,
          data: [
            { x: 0, y: prueba.media_muestra },
            { x: prueba.n, y: prueba.media_muestra }
          ],
          borderColor: '#f59e0b',  // Color ámbar/naranja
          borderWidth: 2,
          borderDash: [4, 2],      // Patrón diferente de línea punteada
          showLine: true,
          fill: false,
          pointRadius: 0
        },
        // Dataset 6: Línea de media teórica (0.5)
        {
          label: `Media teórica = ${prueba.mu_esperada.toFixed(3)}`,
          data: [
            { x: 0, y: prueba.mu_esperada },
            { x: prueba.n, y: prueba.mu_esperada }
          ],
          borderColor: '#10b981',  // Color verde esmeralda
          borderWidth: 2,
          borderDash: [4, 4],      // Patrón de línea punteada diferente
          showLine: true,
          fill: false,
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
            usePointStyle: true  // Usar estilos de punto en lugar de rectángulos
          }
        },
        // TÍTULO con información de muestreo
        title: {
          display: true,
          text: `Valores Ri y rango de aceptación (n=${prueba.n}, graficados ${datos.length})`,
          color: temaHibrido.textColor,
          font: { size: 16, weight: 'bold' }
        }
      },

      // CONFIGURACIÓN DE EJES
      scales: {
        // EJE X (índice de la muestra)
        x: {
          title: {
            display: true,
            text: 'Índice de muestra',  // Posición de cada número en la secuencia
            color: temaHibrido.textColor
          },
          grid: { color: temaHibrido.gridColor },
          ticks: { color: temaHibrido.textColor }
        },
        // EJE Y (valores de 0 a 1)
        y: {
          min: 0,    // Mínimo fijo en 0
          max: 1,    // Máximo fijo en 1 (rango típico de números pseudoaleatorios)
          title: {
            display: true,
            text: 'Ri',  // Valores de los números aleatorios
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
 * Muestra TODOS los números individuales de la secuencia y si sus valores
 * están dentro del rango estadísticamente aceptable para una distribución uniforme.
 * 
 * ELEMENTOS VISUALES:
 * 
 * 1. 🔴 PUNTOS ROJOS: Números dentro del rango aceptable (BUENOS)
 * 2. ⚫ PUNTOS GRISES: Números fuera del rango aceptable (PROBLEMÁTICOS)
 * 3. 🔵 LÍNEAS AZULES PUNTEADAS: Límites del intervalo de confianza
 * 4. 🟡 LÍNEA ÁMBAR: Media observada de los datos
 * 5. 🟢 LÍNEA VERDE: Media teórica esperada (0.5)
 * 
 * INTERPRETACIÓN:
 * 
 * ✅ DISTRIBUCIÓN BUENA:
 * - Mayoría de puntos son ROJOS (dentro del rango)
 * - Línea ámbar (media observada) está CERCA de la verde (0.5)
 * - Línea ámbar está ENTRE las líneas azules (límites)
 * - Los puntos se distribuyen uniformemente entre 0 y 1
 * 
 * ❌ DISTRIBUCIÓN PROBLEMÁTICA:
 * - Muchos puntos GRISES (fuera del rango)
 * - Línea ámbar MUY LEJOS de la línea verde
 * - Línea ámbar FUERA de las líneas azules
 * - Agrupamientos obvios de puntos (no uniformes)
 */
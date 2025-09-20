// MÓDULO DE ESTADÍSTICOS DESCRIPTIVOS
// Calcula y renderiza estadísticas básicas de un conjunto de números

export function calcularEstadisticos(nums) {
  /**
   * Calcula estadísticos descriptivos básicos de un array de números
   * 
   * @param {Array<number>} nums - Array de números a analizar
   * @returns {Object} Objeto con todos los estadísticos calculados
   * 
   * Retorna: { media, mediana, modas, max, min, rango, maxFrecuencia }
   */

  // CASO EDGE: Array vacío
  if (!nums.length) {
    return { media: 0, mediana: 0, modas: [], max: 0, min: 0, rango: 0, maxFrecuencia: 0 };
  }

  // PASO 1: Calcular estadísticos básicos en un solo recorrido (eficiente)
  let suma = 0, max = -Infinity, min = Infinity;
  const freq = new Map();        // Para contar frecuencias de cada valor
  let maxFrecuencia = 0;         // Mayor frecuencia encontrada

  // Recorrido único para múltiples cálculos simultáneos
  for (let v of nums) {
    suma += v;                 // Para la media
    if (v > max) max = v;      // Para el máximo
    if (v < min) min = v;      // Para el mínimo

    // Contar frecuencias para la moda
    const f = (freq.get(v) || 0) + 1;
    freq.set(v, f);
    if (f > maxFrecuencia) maxFrecuencia = f;
  }

  // PASO 2: Calcular media
  const media = suma / nums.length;

  // PASO 3: Calcular mediana (requiere ordenamiento)
  const ordenados = [...nums].sort((a, b) => a - b);  // Copia para no mutar original
  const mitad = Math.floor(nums.length / 2);

  // Mediana depende si hay cantidad par o impar de elementos
  const mediana = nums.length % 2
    ? ordenados[mitad]                                    // Impar: elemento central
    : (ordenados[mitad - 1] + ordenados[mitad]) / 2;      // Par: promedio de los dos centrales

  // PASO 4: Encontrar modas (valores con mayor frecuencia)
  let modas = [];
  if (maxFrecuencia > 1) {  // Solo si hay repeticiones
    for (const [valor, f] of freq.entries()) {
      if (f === maxFrecuencia) {
        modas.push({ valor: Number(valor), frecuencia: f });
      }
    }
    // Ordenar modas por valor para presentación consistente
    modas.sort((a, b) => a.valor - b.valor);
  }
  // Si maxFrecuencia = 1, todos los valores son únicos (no hay moda)

  return {
    media,
    mediana,
    modas,
    max,
    min,
    rango: max - min,     // Diferencia entre máximo y mínimo
    maxFrecuencia
  };
}

export function renderEstadisticos(nums) {
  /**
   * Renderiza los estadísticos calculados en el DOM como tarjetas visuales
   * 
   * @param {Array<number>} nums - Array de números para calcular estadísticos
   * 
   * Efectos secundarios:
   * - Modifica el DOM insertando/reemplazando elemento con clase 'stats-grid'
   * - Se posiciona después del elemento con id 'resumenPruebas'
   */

  // PASO 1: Calcular todos los estadísticos
  const stats = calcularEstadisticos(nums);

  // PASO 2: Generar HTML para las modas (caso especial)
  let modasHtml = "";

  if (stats.maxFrecuencia <= 1) {
    // Caso: no hay repeticiones (todos los valores son únicos)
    modasHtml = `<div class="stat-value" style="font-size:14px; color:#94a3b8;">Todos son diferentes (no hay moda)</div>`;
  } else {
    // Caso: hay modas (valores repetidos)

    // OPTIMIZACIÓN: Limitar visualización para evitar sobrecarga del DOM
    const limite = 50;
    const total = stats.modas.length;
    const mostrar = stats.modas.slice(0, limite);

    // Crear contenedor scrolleable con las modas
    modasHtml = `<div class="moda-scroll">` +
      // Mostrar cada moda como un chip con valor y frecuencia
      mostrar.map(m => `<span class="moda-item">${m.valor} (${m.frecuencia})</span>`).join("") +
      // Indicador si hay más modas que no se muestran
      (total > limite ? `<span class="moda-item">+${total - limite} más</span>` : "") +
      `</div>`;
  }

  // PASO 3: Crear estructura HTML con tarjetas de estadísticos
  const contenedor = document.createElement("div");
  contenedor.className = "stats-grid";
  contenedor.innerHTML = `
      <div class="stat-card">
        <div class="stat-label">Media</div>
        <div class="stat-value">${stats.media.toFixed(5)}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Mediana</div>
        <div class="stat-value">${stats.mediana.toFixed(5)}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Moda</div>
        ${modasHtml}
      </div>
      <div class="stat-card">
        <div class="stat-label">Máximo</div>
        <div class="stat-value">${stats.max.toFixed(5)}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Mínimo</div>
        <div class="stat-value">${stats.min.toFixed(5)}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Rango</div>
        <div class="stat-value">${stats.rango.toFixed(5)}</div>
      </div>
    `;

  // PASO 4: Insertar/reemplazar en el DOM
  const resumenDiv = document.getElementById("resumenPruebas");
  const existing = resumenDiv.nextElementSibling;

  // Si ya existe un stats-grid, reemplazarlo; si no, insertarlo
  if (existing && existing.classList.contains('stats-grid')) {
    existing.replaceWith(contenedor);
  } else {
    resumenDiv.insertAdjacentElement("afterend", contenedor);
  }
}
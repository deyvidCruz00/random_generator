// MÓDULO DE COMUNICACIÓN CON API
// Funciones para interactuar con el backend que maneja las pruebas estadísticas

export async function fetchNumeros() {
  /**
   * Obtiene todos los números almacenados en el servidor
   * 
   * @returns {Promise<Array>} Array de números almacenados
   * @throws {Error} Si la petición falla
   * 
   * Endpoint: GET /all
   * Propósito: Recuperar números previamente guardados para análisis
   */
  const response = await fetch('/all');

  // Verificar si la respuesta es exitosa (status 200-299)
  if (!response.ok) {
    throw new Error("Error al obtener los números");
  }

  // Parsear respuesta JSON y retornar
  return response.json();
}

export async function postSet(numeros) {
  /**
   * Envía un conjunto de números al servidor para almacenamiento
   * 
   * @param {Array} numeros - Array de números a guardar en el servidor
   * @throws {Error} Si la petición falla
   * 
   * Endpoint: POST /set
   * Propósito: Guardar números generados/importados para análisis posterior
   * 
   * NOTA: Esta función no retorna datos, solo confirma el almacenamiento
   */
  const response = await fetch("/set", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"     // Especifica formato JSON
    },
    body: JSON.stringify(numeros)              // Convierte array a JSON string
  });

  // Verificar éxito - lanza error si falla
  if (!response.ok) {
    throw new Error("Error en /set");
  }

  // No retorna datos - solo confirma que se guardó correctamente
}

export async function postEvaluar(datos) {
  /**
   * Solicita al servidor ejecutar pruebas estadísticas sobre los datos
   * 
   * @param {Object} datos - Configuración de las pruebas a ejecutar
   * @param {Array} datos.numeros - Números a analizar (opcional si ya están en servidor)
   * @param {Object} datos.pruebas - Configuración de qué pruebas ejecutar
   * @param {number} datos.alpha - Nivel de significancia (ej: 0.05)
   * @returns {Promise<Object>} Resultados de todas las pruebas ejecutadas
   * @throws {Error} Si la petición falla
   * 
   * Endpoint: POST /evaluar
   * Propósito: Ejecutar múltiples pruebas estadísticas y obtener resultados
   */
  const response = await fetch("/evaluar", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(datos)                // Envía configuración completa
  });

  // Verificar éxito de la petición
  if (!response.ok) {
    throw new Error("Error en /evaluar");
  }

  // Parsear y retornar resultados de las pruebas
  return response.json();
}
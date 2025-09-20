// Importar todas las funciones de configuración específicas para cada tipo de prueba
import { obtenerConfiguracionMedias } from './media.js';
import { obtenerConfiguracionVarianza } from './varianza.js';
import { obtenerConfiguracionChiCuadrado } from './chi2.js';
import { obtenerConfiguracionKolmogorov } from './ks.js';
import { obtenerConfiguracionRachas } from './racha.js';

export function obtenerConfiguracionGrafico(prueba, nums) {
    /**
     * PATRÓN FACTORY - Función factory que selecciona la configuración
     * de gráfico apropiada según el tipo de prueba estadística
     * 
     * @param {Object} prueba - Objeto JSON con resultados del test estadístico
     * @param {Array} nums - Array de números originales (solo usado para prueba de medias)
     * @returns {Object|null} Configuración de Chart.js o null si no se reconoce el test
     * 
     * VENTAJAS DEL PATRÓN FACTORY:
     * 1. Centralización: Un solo punto de entrada para todas las configuraciones
     * 2. Extensibilidad: Fácil agregar nuevos tipos de prueba
     * 3. Mantenibilidad: Cada configuración está en su propio archivo
     * 4. Consistencia: Interfaz uniforme para el cliente
     */

    // Switch basado en el campo 'test_name' del resultado de la prueba
    switch (prueba.test_name) {

        // PRUEBA DE MEDIAS
        case "Prueba de Medias":
            // Requiere tanto el resultado de la prueba como los números originales
            // para graficar cada punto individual con sus límites de aceptación
            return obtenerConfiguracionMedias(prueba, nums);

        // PRUEBA KOLMOGOROV-SMIRNOV  
        case "Prueba KS":
            // Solo necesita el resultado de la prueba (contiene intervals_data)
            // para comparar distribuciones acumuladas observadas vs esperadas
            return obtenerConfiguracionKolmogorov(prueba);

        // PRUEBA DE VARIANZA
        case "Prueba de Varianza":
            // Genera la distribución chi-cuadrado teórica y muestra dónde
            // cae el estadístico calculado respecto a los límites críticos
            return obtenerConfiguracionVarianza(prueba);

        // PRUEBA CHI-CUADRADO
        case "Prueba Chi-Cuadrado":
            // Compara frecuencias observadas vs esperadas por intervalos
            // usando gráfico de barras + línea de referencia
            return obtenerConfiguracionChiCuadrado(prueba);

        // PRUEBA DE RACHAS
        case "Prueba de Rachas":
            // Muestra evolución temporal de rachas acumuladas
            // comparando tendencia observada vs esperada con intervalo de confianza
            return obtenerConfiguracionRachas(prueba);

        // CASO DEFAULT - Tipo de prueba no reconocido
        default:
            // Retorna null para indicar que no hay configuración disponible
            // El cliente debe manejar este caso (ej: mostrar mensaje de error)
            return null;
    }
}

/**
 * ¿CÓMO FUNCIONA ESTE SISTEMA?
 * 
 * FLUJO DE EJECUCIÓN:
 * 1. El cliente tiene resultados de un test estadístico
 * 2. Llama a obtenerConfiguracionGrafico(prueba, nums)
 * 3. La función examina prueba.test_name para identificar el tipo
 * 4. Delega a la función específica correspondiente
 * 5. Retorna configuración completa de Chart.js lista para usar
 * 
 * TIPOS DE VISUALIZACIÓN POR PRUEBA:
 * 
 * 📊 MEDIAS: Scatter plot con todos los puntos individuales + límites
 * 📈 KOLMOGOROV: Barras agrupadas comparando distribuciones acumuladas  
 * 📉 VARIANZA: Curva de distribución chi² + región de aceptación
 * 📊 CHI-CUADRADO: Barras de frecuencias + línea de expectativa uniforme
 * 📈 RACHAS: Líneas de evolución temporal + área de confianza
 * 
 * EXTENSIBILIDAD:
 * Para agregar una nueva prueba (ej: "Prueba de Anderson-Darling"):
 * 1. Crear archivo anderson.js con obtenerConfiguracionAnderson()
 * 2. Importar la función al inicio de este archivo
 * 3. Agregar case "Prueba de Anderson-Darling" al switch
 * 
 * MANEJO DE ERRORES:
 * - Si test_name no coincide con ningún case → retorna null
 * - El cliente debe verificar el resultado y manejar el caso null apropiadamente
 * - Cada función específica debe manejar sus propios errores internos
 * 
 * DEPENDENCIAS:
 * - Cada función específica maneja sus propias dependencias (ej: jStat para varianza)
 * - Todas usan temaHibrido desde utils.js para consistencia visual
 * - Configuraciones optimizadas para Chart.js con opciones avanzadas
 */
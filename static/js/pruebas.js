// Importar array de números y funciones de API
import { numeros } from './numeros.js';
import { postSet, postEvaluar } from './api.js';

// Función para obtener qué pruebas seleccionó el usuario
export function getPruebasSeleccionadas() {
  const chiChecked = document.getElementById("pruebaChi").checked;
  const kolChecked = document.getElementById("pruebaKolmogorov").checked;

  let chiK = null, kolK = null;

  // Si seleccionó Chi-cuadrado, validar el valor K
  if (chiChecked) {
    chiK = parseInt(document.getElementById("chiK").value, 10);
    if (isNaN(chiK) || chiK < 2) {
      alert("El valor de K para Chi-cuadrado debe ser un entero >= 2.");
      return null;
    }
  }

  // Si seleccionó Kolmogorov, validar el valor K
  if (kolChecked) {
    kolK = parseInt(document.getElementById("kolmogorovK").value, 10);
    if (isNaN(kolK) || kolK < 1) {
      alert("El valor de K para Kolmogorov–Smirnov debe ser un entero >= 1.");
      return null;
    }
  }

  // Retornar objeto con todas las pruebas seleccionadas
  return {
    medias: document.getElementById("pruebaMedias").checked,
    varianza: document.getElementById("pruebaVarianza").checked,
    chi: chiChecked ? { k: chiK } : false,
    kolmogorov: kolChecked ? { k: kolK } : false,
    poker: document.getElementById("pruebaPoker").checked,
    rachas: document.getElementById("pruebaRachas").checked
  };
}

// Función principal para ejecutar las pruebas estadísticas
export async function generarPruebas() {
  // Obtener pruebas seleccionadas
  const pruebasSeleccionadas = getPruebasSeleccionadas();
  if (!pruebasSeleccionadas) return;

  // Obtener valor de alpha (nivel de significancia)
  const alpha = parseFloat(document.getElementById("alphaInput").value);

  // Verificar que hay números para analizar
  if (numeros.length === 0) {
    alert("Debes agregar al menos un número antes de generar las pruebas.");
    return;
  }

  // Preparar datos para enviar al servidor
  const datos = { numeros, pruebasSeleccionadas, alpha };

  try {
    // Enviar números al servidor
    await postSet(numeros);

    // Ejecutar las pruebas en el servidor
    const resultado = await postEvaluar(datos);

    // Guardar resultados y redirigir a página de resultados
    sessionStorage.setItem("resultadosPruebas", JSON.stringify(resultado));
    window.location.href = "/resultados";
  } catch (error) {
    console.error(error);
    alert("Ocurrió un error al ejecutar las pruebas.");
  }
}
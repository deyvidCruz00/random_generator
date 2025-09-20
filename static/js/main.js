import { fetchNumeros } from './api.js';
import { renderResumenPruebas } from './resumen.js';
import { renderEstadisticos } from './estadisticos.js';
import { renderResultados } from './render.js';

let resultados = JSON.parse(sessionStorage.getItem("resultadosPruebas"));
let nums = [];

fetchNumeros()
  .then(data => {
    nums = data;
    renderResumenPruebas(resultados);
    renderEstadisticos(nums);
    renderResultados(resultados, nums);
  })
  .catch(err => console.error("Error al cargar los datos:", err));

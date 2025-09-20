// Importar funciones de otros archivos
import { agregarNumero, importarCSV } from './numeros.js';
import { generarPruebas } from './pruebas.js';

// Botón para agregar números
document.getElementById("btnAgregar").addEventListener("click", agregarNumero);

// Input para seleccionar archivo CSV
document.getElementById("csvFileInput").addEventListener("change", importarCSV);

// Botón para generar pruebas estadísticas
document.getElementById("btnGenerar").addEventListener("click", generarPruebas);

// Mostrar/ocultar input de K para prueba Chi-cuadrado
document.getElementById("pruebaChi").addEventListener("change", () => {
  document.getElementById("kChi").style.display =
    document.getElementById("pruebaChi").checked ? "flex" : "none";
});

// Mostrar/ocultar input de K para prueba Kolmogorov-Smirnov
document.getElementById("pruebaKolmogorov").addEventListener("change", () => {
  document.getElementById("kKolmogorov").style.display =
    document.getElementById("pruebaKolmogorov").checked ? "flex" : "none";
});
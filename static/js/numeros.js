// Array para guardar todos los números
export let numeros = [];

// Función para agregar un número desde el input
export function agregarNumero() {
  const input = document.getElementById("numeroInput");
  const valor = parseFloat(input.value);

  // Si el valor es un número válido
  if (!isNaN(valor)) {
    numeros.push(valor);           // Agregar al array
    mostrarNumeros();              // Actualizar la lista en pantalla
    input.value = "";              // Limpiar el input
    input.focus();                 // Enfocar el input para seguir escribiendo
  } else {
    alert("Por favor, ingresa un número válido.");
  }
}

// Función para mostrar los números en pantalla
export function mostrarNumeros() {
  const lista = document.getElementById("listaNumeros");

  if (numeros.length > 0) {
    // Mostrar números separados por comas
    lista.innerHTML = numeros.join(", ");
  } else {
    // Mensaje cuando no hay números
    lista.innerHTML = "Tus números aparecerán aquí...";
  }
}

// Función para importar números desde archivo CSV
export function importarCSV(event) {
  const file = event.target.files[0];
  if (!file) return;

  // Verificar que sea archivo CSV
  if (!file.name.endsWith('.csv')) {
    alert('Por favor, selecciona un archivo con extensión .csv');
    return;
  }

  // Leer el archivo
  const reader = new FileReader();
  reader.onload = function (e) {
    const text = e.target.result;

    // Separar texto por saltos de línea y comas
    const potentialNumbers = text.split(/[\r\n,]+/).filter(Boolean);

    // Convertir a números y filtrar valores válidos
    const importedNumbers = potentialNumbers.map(val => parseFloat(val.trim())).filter(num => !isNaN(num));

    if (importedNumbers.length > 0) {
      // Agregar números importados al array principal
      numeros = numeros.concat(importedNumbers);
      mostrarNumeros();
    } else {
      alert('No se encontraron números válidos en el archivo CSV.');
    }

    // Limpiar el input de archivo
    event.target.value = '';
  };

  // Manejar errores de lectura
  reader.onerror = () => alert('Ocurrió un error al leer el archivo.');

  // Iniciar lectura del archivo como texto
  reader.readAsText(file);
}
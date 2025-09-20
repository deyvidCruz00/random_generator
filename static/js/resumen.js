// Función para mostrar un resumen visual de todas las pruebas
export function renderResumenPruebas(resultados) {
    // Obtener contenedor del resumen y limpiarlo
    const contenedor = document.getElementById("resumenPruebas");
    contenedor.innerHTML = "";

    // Orden específico para mostrar las pruebas
    const orden = [
        "Prueba de Medias",
        "Prueba de Varianza",
        "Prueba Chi-Cuadrado",
        "Prueba KS",
        "Prueba de Poker",
        "Prueba de Rachas"
    ];

    // Recorrer cada prueba en el orden establecido
    orden.forEach(nombre => {
        // Buscar la prueba específica en los resultados
        const prueba = Object.values(resultados)
            .map(r => JSON.parse(r))           // Convertir de JSON a objeto
            .find(p => p.test_name === nombre); // Encontrar por nombre

        // Si la prueba existe en los resultados
        if (prueba) {
            // Verificar si la prueba fue aprobada
            const aprobado = prueba.isApproved === "True";

            // Crear elemento visual para la prueba
            const div = document.createElement("div");
            div.className = `resumen-item ${aprobado ? "success" : "fail"}`;

            // Mostrar icono y nombre según el resultado
            div.innerHTML = aprobado
                ? `✅ ${nombre}`    // Checkmark verde si pasó
                : `❌ ${nombre}`;   // X roja si no pasó

            // Agregar al contenedor
            contenedor.appendChild(div);
        }
    });
}
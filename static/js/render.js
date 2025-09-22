// Importar configuración de gráficos y utilidades
import { obtenerConfiguracionGrafico } from './graficos/config.js';
import { exportarImagen, temaHibrido } from './utils.js';

// Array para guardar todos los gráficos creados
let charts = [];

// Función principal para mostrar los resultados de las pruebas
export function renderResultados(resultados, nums) {
    // Obtener contenedor principal y limpiarlo
    const contenedor = document.getElementById("pruebasResultados");
    contenedor.innerHTML = '';
    charts = [];

    // Recorrer cada prueba en los resultados
    Object.keys(resultados).forEach(pruebaKey => {
        // Convertir resultado de JSON a objeto
        const prueba = JSON.parse(resultados[pruebaKey]);

        // Crear tarjeta para la prueba
        const card = document.createElement("div");
        card.className = "prueba-card";

        // Agregar título de la prueba
        const title = document.createElement("h2");
        title.textContent = `${prueba.test_name}`;
        card.appendChild(title);

        // Agregar resumen del resultado con color según pase o no
        const resumen = document.createElement("p");
        resumen.textContent = "→ " + prueba.decision;
        resumen.style.color = prueba.decision.includes("Pasa") ||
            prueba.decision.includes("No se rechaza") ?
            temaHibrido.successColor : temaHibrido.errorColor;
        card.appendChild(resumen);

        let chartContainer = null;
        let canvas = null;

        // Crear contenedor de gráfico para todas las pruebas excepto Poker
        if (prueba.test_name !== "Prueba de Poker") {
            chartContainer = document.createElement("div");
            chartContainer.className = "chart-container";
            chartContainer.style.height = "400px";

            canvas = document.createElement("canvas");
            chartContainer.appendChild(canvas);
            card.appendChild(chartContainer);
        }

        // Crear sección de estadísticas detalladas
        const stats = document.createElement("div");
        stats.className = "stats-info";

        // Mostrar información específica según el tipo de prueba
        if (prueba.test_name === "Prueba de Medias") {
            // Estadísticas para prueba de medias
            stats.innerHTML = `
                <div class="stat-item"><strong>n:</strong> ${prueba.n}</div>
                <div class="stat-item"><strong>Media esperada (μ₀):</strong> ${prueba.mu_esperada}</div>
                <div class="stat-item"><strong>Media muestral (x̄):</strong> ${prueba.media_muestra.toFixed(5)}</div>
                <div class="stat-item"><strong>Estadístico Z:</strong> ${prueba.z.toFixed(5)}</div>
                <div class="stat-item"><strong>Intervalo de confianza:</strong> [${prueba.limite_inferior.toFixed(5)}, ${prueba.limite_superior.toFixed(5)}]</div>
            `;
        } else if (prueba.test_name === "Prueba KS") {
            // Crear tabla para prueba Kolmogorov-Smirnov
            stats.innerHTML = "";

            const tabla = document.createElement("table");
            tabla.style.width = "100%";
            tabla.style.borderCollapse = "collapse";
            tabla.style.marginTop = "10px";
            tabla.style.fontFamily = "'Roboto Mono', monospace";
            tabla.style.fontSize = "13px";
            tabla.style.color = "#e2e8f0";

            // Crear encabezados de la tabla
            const encabezados = [
                "No", "Inicial", "Final",
                "Frec.Obt", "F.Obt.A", "P.Obt",
                "F.Esp.A", "P.Esp.A", "Dif"
            ];
            const thead = document.createElement("thead");
            const trHead = document.createElement("tr");
            encabezados.forEach(h => {
                const th = document.createElement("th");
                th.textContent = h;
                th.style.borderBottom = "2px solid #06b6d4";
                th.style.padding = "6px";
                th.style.textAlign = "center";
                trHead.appendChild(th);
            });
            thead.appendChild(trHead);
            tabla.appendChild(thead);

            // Agregar filas de datos
            const tbody = document.createElement("tbody");
            prueba.intervals_data.forEach(row => {
                const tr = document.createElement("tr");

                [
                    row.No,
                    row.Inicial.toFixed(5),
                    row.Final.toFixed(5),
                    row.frecuencia_obt,
                    row.frecuencia_obt_acu,
                    row.P_Obt.toFixed(3),
                    row.frecuencia_esp_acu.toFixed(2),
                    row.P_Esp_A.toFixed(2),
                    row.Dif.toFixed(4)
                ].forEach(val => {
                    const td = document.createElement("td");
                    td.textContent = val;
                    td.style.padding = "6px";
                    td.style.borderBottom = "1px solid #1e293b";
                    td.style.textAlign = "center";
                    tr.appendChild(td);
                });

                tbody.appendChild(tr);
            });
            tabla.appendChild(tbody);

            // Agregar resumen al final de la tabla
            const tfoot = document.createElement("tfoot");
            [
                ["DMAX", prueba.statistics.max_difference.toFixed(5)],
                ["Crítico", prueba.statistics.critical_value.toFixed(5)],
                ["Decisión", prueba.decision]
            ].forEach(([label, val]) => {
                const tr = document.createElement("tr");

                const tdLabel = document.createElement("td");
                tdLabel.colSpan = 8;
                tdLabel.textContent = label;
                tdLabel.style.textAlign = "right";
                tdLabel.style.fontWeight = "bold";
                tdLabel.style.padding = "6px";
                tdLabel.style.borderTop = "2px solid #06b6d4";

                const tdVal = document.createElement("td");
                tdVal.textContent = val;
                tdVal.style.textAlign = "center";
                tdVal.style.fontWeight = "bold";
                tdVal.style.padding = "6px";
                tdVal.style.borderTop = "2px solid #06b6d4";

                tr.appendChild(tdLabel);
                tr.appendChild(tdVal);
                tfoot.appendChild(tr);
            });
            tabla.appendChild(tfoot);

            stats.appendChild(tabla);
        } else if (prueba.test_name === "Prueba de Poker") {
            // Crear tabla para prueba de Poker
            const tabla = document.createElement("table");
            tabla.style.width = "100%";
            tabla.style.marginTop = "15px";
            tabla.style.borderCollapse = "collapse";
            tabla.style.fontFamily = "'Roboto Mono', monospace";
            tabla.style.fontSize = "13px";
            tabla.style.color = "#e2e8f0";

            // Encabezados de tabla Poker
            const encabezados = ["Cat", "Oi", "Prob", "Ei", "(Oi-Ei)²/Ei"];
            const thead = document.createElement("thead");
            const trHead = document.createElement("tr");
            encabezados.forEach(h => {
                const th = document.createElement("th");
                th.textContent = h;
                th.style.borderBottom = "2px solid #06b6d4";
                th.style.padding = "6px";
                th.style.textAlign = "center";
                trHead.appendChild(th);
            });
            thead.appendChild(trHead);
            tabla.appendChild(thead);

            // Filas con datos de Poker
            const tbody = document.createElement("tbody");
            prueba.intervals_data.forEach(row => {
                const tr = document.createElement("tr");

                [
                    row.Cat,
                    row.Oi,
                    row.Prob.toFixed(4),
                    row.Ei.toFixed(2),
                    row["(Oi-Ei)^2/Ei"].toFixed(5)
                ].forEach(val => {
                    const td = document.createElement("td");
                    td.textContent = val;
                    td.style.padding = "6px";
                    td.style.borderBottom = "1px solid #1e293b";
                    td.style.textAlign = "center";
                    tr.appendChild(td);
                });

                tbody.appendChild(tr);
            });
            tabla.appendChild(tbody);

            card.appendChild(tabla);

            // Estadísticas adicionales de Poker
            stats.innerHTML = `
                <div class="stat-item"><strong>Suma Oi:</strong> ${prueba.statistics.Suma_Oi}</div>
                <div class="stat-item"><strong>χ² calculado:</strong> ${prueba.statistics.Chi2_calculado.toFixed(5)}</div>
                <div class="stat-item"><strong>χ² crítico:</strong> ${prueba.statistics.critical_value.toFixed(5)}</div>
                <div class="stat-item"><strong>Resultado:</strong> ${prueba.decision}</div>
            `;
        } else if (prueba.test_name === "Prueba de Varianza") {
            // Estadísticas para prueba de varianza
            stats.innerHTML = `
                <div class="stat-item"><strong>n:</strong> ${prueba.n}</div>  
                <div class="stat-item"><strong>media_muestral:</strong> ${prueba.media_muestral.toFixed(5)}</div> 
                <div class="stat-item"><strong>Varianza muestral (s²):</strong> ${prueba.varianza_muestral.toFixed(5)}</div>
                <div class="stat-item"><strong>chi-2:</strong> ${prueba.chi2.toFixed(5)}</div>
                <div class="stat-item"><strong>Intervalo de confianza chi-2:</strong> [${prueba.Xi1.toFixed(5)}, ${prueba.Xi2.toFixed(5)}]</div>    
            `;
        } else if (prueba.test_name === "Prueba Chi-Cuadrado") {
            // Crear tabla para prueba Chi-Cuadrado
            stats.innerHTML = "";

            const tabla = document.createElement("table");
            tabla.style.width = "100%";
            tabla.style.borderCollapse = "collapse";
            tabla.style.marginTop = "10px";
            tabla.style.fontFamily = "'Roboto Mono', monospace";
            tabla.style.fontSize = "13px";
            tabla.style.color = "#e2e8f0";

            // Encabezados Chi-Cuadrado
            const encabezados = ["No", "Inicial", "Final", "Frec.Obt", "Frec.Esp", "Chi²"];
            const thead = document.createElement("thead");
            const trHead = document.createElement("tr");
            encabezados.forEach(h => {
                const th = document.createElement("th");
                th.textContent = h;
                th.style.borderBottom = "2px solid #06b6d4";
                th.style.padding = "6px";
                th.style.textAlign = "center";
                trHead.appendChild(th);
            });
            thead.appendChild(trHead);
            tabla.appendChild(thead);

            // Filas con intervalos Chi-Cuadrado
            const tbody = document.createElement("tbody");
            prueba.intervals_data.forEach(row => {
                const tr = document.createElement("tr");

                [
                    row.no,
                    row.inicio.toFixed(5),
                    row.fin.toFixed(5),
                    row.frecuencia_obt,
                    row.frecuencia_esp.toFixed(2),
                    row.chi2.toFixed(5)
                ].forEach(val => {
                    const td = document.createElement("td");
                    td.textContent = val;
                    td.style.padding = "6px";
                    td.style.borderBottom = "1px solid #1e293b";
                    td.style.textAlign = "center";
                    tr.appendChild(td);
                });

                tbody.appendChild(tr);
            });
            tabla.appendChild(tbody);

            // Fila de totales
            const trTotal = document.createElement("tr");

            const tdLabel = document.createElement("td");
            tdLabel.colSpan = 3;
            tdLabel.textContent = "Total";
            tdLabel.style.fontWeight = "bold";
            tdLabel.style.textAlign = "center";
            tdLabel.style.padding = "6px";
            tdLabel.style.borderTop = "2px solid #06b6d4";

            const tdFrecObt = document.createElement("td");
            tdFrecObt.textContent = prueba.statistics.frecuencia_obt_total;
            tdFrecObt.style.fontWeight = "bold";
            tdFrecObt.style.textAlign = "center";
            tdFrecObt.style.borderTop = "2px solid #06b6d4";

            const tdFrecEsp = document.createElement("td");
            tdFrecEsp.textContent = prueba.statistics.frecuencia_esp_total;
            tdFrecEsp.style.fontWeight = "bold";
            tdFrecEsp.style.textAlign = "center";
            tdFrecEsp.style.borderTop = "2px solid #06b6d4";

            const tdChi2 = document.createElement("td");
            tdChi2.textContent = prueba.statistics.chi2_total.toFixed(3);
            tdChi2.style.fontWeight = "bold";
            tdChi2.style.textAlign = "center";
            tdChi2.style.borderTop = "2px solid #06b6d4";

            trTotal.appendChild(tdLabel);
            trTotal.appendChild(tdFrecObt);
            trTotal.appendChild(tdFrecEsp);
            trTotal.appendChild(tdChi2);
            tabla.appendChild(trTotal);

            stats.appendChild(tabla);

            // Resumen debajo de la tabla
            const resumen = document.createElement("div");
            resumen.style.marginTop = "10px";
            resumen.style.fontSize = "14px";
            resumen.innerHTML = `
                <strong>χ² crítico:</strong> ${prueba.statistics.chi2_critico.toFixed(5)}<br>
                <strong>Decisión:</strong> ${prueba.decision}
            `;
            stats.appendChild(resumen);
        } else if (prueba.test_name === "Prueba de Rachas") {
            // Estadísticas para prueba de rachas
            stats.innerHTML = `
                <div class="stat-item"><strong>Mediana muestral:</strong> ${prueba.Mediana_muestral}</div>
                <div class="stat-item"><strong>Mediana teórica:</strong> ${prueba.Mediana_teorica}</div>
                
                <div class="stat-item"><strong>Rachas observadas:</strong> ${prueba.Rachas}</div>
                <div class="stat-item"><strong>Total "+" :</strong> ${prueba.Total_may}</div>
                <div class="stat-item"><strong>Total "-" :</strong> ${prueba.Total_min}</div>
                <div class="stat-item"><strong>Total:</strong> ${prueba.Total}</div>
                
                <div class="stat-item"><strong>UR (esperado):</strong> ${prueba.UR.toFixed(5)}</div>
                <div class="stat-item"><strong>Varianza:</strong> ${prueba.Varianza.toFixed(5)}</div>
                <div class="stat-item"><strong>Z:</strong> ${prueba.Z}</div>
                <div class="stat-item"><strong>Rango crítico (95%):</strong> [${prueba.Rango_min}, ${prueba.Rango_max}]</div>
            `;
        }

        // Agregar sección de estadísticas a la tarjeta
        card.appendChild(stats);

        // Crear botón para exportar imagen
        const btnExportar = document.createElement("button");
        btnExportar.className = "export-btn";
        btnExportar.textContent = "📊 Exportar PNG";
        btnExportar.onclick = () => exportarImagen(canvas, prueba.test_name);
        card.appendChild(btnExportar);

        // Agregar tarjeta al contenedor principal
        contenedor.appendChild(card);

        // Generar y mostrar el gráfico
        const configuracion = obtenerConfiguracionGrafico(prueba, nums);
        if (configuracion) {
            const chart = new Chart(canvas, configuracion);
            charts.push(chart);
        }
    });
}
# Generador de Números Pseudoaleatorios

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

Una aplicación web  para la generación, análisis y validación de números pseudoaleatorios, implementando múltiples algoritmos clásicos con interfaz intuitiva y herramientas de visualización.

##  Características

### **Generación de Números**
- **Múltiples algoritmos** implementados con precisión matemática
- **Entrada flexible** de semillas (manual o desde archivos CSV/TXT)
- **Control granular** del número de iteraciones
- **Exportación** de resultados en formato CSV

### **Análisis y Visualización**
- **Gráficos de series temporales** para análisis secuencial
- **Histogramas de distribución** para análisis estadístico
- **Tablas detalladas** con valores Xi, Ri y Ni
- **Visualizaciones interactivas** con matplotlib

### **Validación Estadística**
- **Suite completa** de pruebas de aleatoriedad
- **Evaluación automática** de calidad estadística
- **Interpretación clara** de resultados
- **Comparación** entre diferentes métodos

### **Arquitectura Modular**
- **Código reutilizable** para integración en otros proyectos
- **Separación clara** de responsabilidades
- **Documentación completa** del código
- **Fácil extensión** para nuevos métodos

## Métodos Implementados

### **Generadores Base**

#### **Cuadrados Medios**
```python
# Método clásico de von Neumann
Xi+1 = extraer_digitos_medios(Xi²)
```
- Implementación con manejo de degeneración
- Extracción inteligente de dígitos medios
- Validación automática de semillas

#### **Congruencia Lineal**
```python
# Generador congruencial lineal
Xi+1 = (a × Xi + c) mod m
```
- Parámetros: a = 1 + 2k, m = 2^g
- Período completo garantizado
- Hull-Dobell conditions

#### **Congruencia Multiplicativa**
```python
# Generador congruencial multiplicativo
Xi+1 = (a × Xi) mod m
```
- Parámetros: a = 8t + 3, m = 2^g
- Optimizado para eficiencia
- Período máximo teórico

### **Distribuciones Transformadas**

#### **Distribución Normal**
- **Método Box-Muller** para transformación
- Parámetros configurables (μ, σ)
- Validación estadística automática

#### **Distribución Uniforme**
- **Transformación lineal** X = a + (b-a)×U
- Rango personalizable [a, b]
- Preservación de propiedades estadísticas

## Instalación

### **Prerrequisitos**
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### **Paso 1: Clonar el repositorio**
```bash
git clone https://github.com/deyvidCruz00/random_generator.git
cd random_generator
```

### **Paso 2: Crear entorno virtual (Recomendado)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### **Paso 3: Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **Paso 4: Ejecutar la aplicación**
```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 📚 Uso

### **Inicio Rápido**

1. **Acceder a la aplicación** en tu navegador
2. **Seleccionar método** de generación desde el menú principal
3. **Configurar parámetros** según el método elegido
4. **Generar números** y visualizar resultados
5. **Exportar datos** en formato CSV si es necesario

### **Configuración de Parámetros**

#### **Cuadrados Medios**
```
Semilla (X₀): Número de 4 dígitos
Cantidad: Número de valores a generar
Rango [a,b]: Para distribución uniforme (opcional)
```

#### **Congruencia Lineal**
```
Semilla (X₀): Valor inicial
k: Parámetro multiplicativo
c: Constante aditiva
g: Exponente del módulo (m = 2^g)
n: Cantidad de números
```

#### **Congruencia Multiplicativa**
```
Semilla (X₀): Valor inicial impar
t: Parámetro (a = 8t + 3)
g: Exponente del módulo (m = 2^g)
n: Cantidad de números
```

### **Carga de Semillas desde Archivo**

Crea un archivo CSV con el formato:
```csv
semilla
1234
5678
9012
```

## 📁 Estructura del Proyecto

```
random_generator/
├── 📄 app.py                          # Aplicación Flask principal
├── 📄 requirements.txt                # Dependencias Python
├── 📄 README.md                       # Documentación
├── 📁 modules/                        # Módulos principales
│   ├── 📁 generadores/                # Algoritmos de generación
│   │   ├── minimos_cuadrados.py       # Método cuadrados medios
│   │   ├── congruencia_lineal.py      # Congruencia lineal
│   │   ├── congruencia_multi.py       # Congruencia multiplicativa
│   │   ├── distribucion_normal.py     # Distribución normal
│   │   └── distribucion_uniforme.py   # Distribución uniforme
│   └── 📁 pruebas/                    # Suite de pruebas estadísticas
│       ├── dispatcher.py              # Coordinador de pruebas
│       ├── prueba_chi2_2.py           # Chi-cuadrado
│       ├── prueba_de_medias.py        # Prueba de medias
│       ├── prueba_de_varianza.py      # Prueba de varianza
│       ├── ks.py                      # Kolmogorov-Smirnov
│       ├── poker.py                   # Prueba de póker
│       └── rachas.py                  # Prueba de rachas
├── 📁 templates/                      # Plantillas HTML
│   ├── base.html                      # Plantilla base
│   ├── index.html                     # Página principal
│   ├── cuadrados.html                 # Interfaz cuadrados medios
│   ├── lineal.html                    # Interfaz congruencia lineal
│   ├── multiplicativo.html            # Interfaz multiplicativa
│   ├── distribucion_normal.html       # Interfaz distribución normal
│   ├── distribucion_uniforme.html     # Interfaz distribución uniforme
│   └── pruebas.html                   # Interfaz de pruebas
├── 📁 static/                         # Recursos estáticos
│   ├── css/                           # Hojas de estilo
│   ├── js/                            # Scripts JavaScript
│   └── images/                        # Imágenes
└── 📁 outputs/                        # Archivos de salida
```

##  Pruebas Estadísticas
### **Suite de Validación Automática**

La aplicación incluye un conjunto completo de pruebas estadísticas para validar la calidad de los números generados:

#### **Pruebas Implementadas**

| Prueba | Objetivo | Hipótesis |
|--------|----------|-----------|
| **Chi-cuadrado** | Uniformidad de distribución | H₀: Distribución uniforme |
| **Kolmogorov-Smirnov** | Bondad de ajuste | H₀: F(x) = x |
| **Prueba de Medias** | Media teórica | H₀: μ = 0.5 |
| **Prueba de Varianza** | Varianza teórica | H₀: σ² = 1/12 |
| **Prueba de Póker** | Independencia | H₀: Patrones independientes |
| **Prueba de Rachas** | Aleatoriedad secuencial | H₀: Secuencia aleatoria |



## Especificaciones Técnicas

### **Dependencias Principales**
- **Flask 2.3.3**: Framework web
- **pandas 2.1.1**: Manipulación de datos
- **numpy 1.24.3**: Cálculos numéricos
- **matplotlib 3.7.2**: Visualizaciones
- **scipy 1.11.2**: Funciones estadísticas

### **Compatibilidad**
- **Python**: 3.8, 3.9, 3.10, 3.11
- **SO**: Windows, Linux, macOS
- **Navegadores**: Chrome, Firefox, Safari, Edge

## Autores

- **Deyvid Cruz** - *Desarrollo principal* - [@deyvidCruz00](https://github.com/deyvidCruz00)
- **Julián Bayona** - *Desarrollo principal* - [@julianbayona](https://github.com/deyvidCruz00)


---


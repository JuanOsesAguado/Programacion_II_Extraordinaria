Programacion_II_Extraordinaria

https://github.com/JuanOsesAguado/Programacion_II_Extraordinaria.git

# mi_simulador_celeste

Este proyecto implementa un simulador de sistemas planetarios simplificado en Python, haciendo uso de los principios de la mecánica newtoniana y la programación orientada a objetos (POO). Permite modelar la interacción gravitatoria entre cuerpos celestes sin una interfaz gráfica, utilizando la consola para la interacción.

## Caracteristicas

- **Listado de Cuerpos Celestes**: Muestra información detallada de todos los cuerpos registrados.
- **Registro de Nuevos Cuerpos**: Permite añadir planetas, asteroides o satélites con sus propiedades iniciales.
- **Cálculo de Fuerzas Gravitatorias**: Calcula la fuerza neta sobre cada cuerpo debido a la atracción de los demás.
- **Evolución Temporal (Integración)**: Simula el movimiento de los cuerpos a lo largo del tiempo utilizando el método de Euler explícito.
- **Cálculo de Energía y Momento**: En cada paso de la simulación, calcula y muestra la energía cinética total, la energía potencial gravitatoria y el momento lineal total del sistema.
- **Persistencia en Archivo**: Guarda y carga el estado completo del sistema en formato JSON o CSV.

## Estructura del proyecto

mi_simulador_celeste/
├── src/
│   └── celeste/
│       ├── init.py      # Marca el directorio como un paquete Python
│       ├── vector3d.py      # Implementación de la clase Vector3D
│       ├── cuerpo.py        # Implementación de la clase CuerpoCeleste
│       ├── simulador.py     # Implementación de la clase Simulador
│       └── main.py          # Script principal con un menú de CLI (opcional)
├── tests/
│   ├── init.py
│   ├── test_vector3d.py     # Pruebas unitarias para Vector3D
│   ├── test_cuerpo.py       # Pruebas unitarias para CuerpoCeleste
│   └── test_simulador.py    # Pruebas unitarias para Simulador
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Este archivo

## Guía para la ejecución

Sigue estos pasos para configurar y ejecutar el simulador:

1.  **Clonar el repositorio** (si aplica) o crear la estructura de directorios manualmente.

2.  **Crear y activar un entorno virtual** (recomendado):

    ```bash
    python -m venv venv
    # En Windows
    .\venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instalar las dependencias** (pytest para las pruebas):

    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar el simulador**:

    Puedes interactuar con el simulador a través del menú de línea de comandos:

    ```bash
    python src/celeste/main.py
    ```

    O puedes importar las clases y usarlas en un REPL de Python o en otro script:

    ```python
    # Desde la raíz del proyecto, con el entorno virtual activado
    # python
    # >>> from src.celeste.simulador import Simulador
    # >>> from src.celeste.vector3d import Vector3D
    # >>> sim = Simulador()
    # >>> sim.agregar_cuerpo("Sol", 1.989e30, Vector3D(0,0,0), Vector3D(0,0,0))
    # >>> sim.agregar_cuerpo("Tierra", 5.972e24, Vector3D(1.5e11,0,0), Vector3D(0,2.978e4,0))
    # >>> sim.listar_cuerpos()
    # >>> sim.paso_simulacion(dt=3600, current_time=0) # Un paso de 1 hora
    # >>> sim.guardar("mi_sistema.json")
    ```

5.  **Ejecutar las pruebas unitarias**:

    Asegúrate de estar en la raíz del proyecto (donde se encuentra `tests/` y `requirements.txt`) y con el entorno virtual activado:

    ```bash
    pytest -v
    ```

    Esto ejecutará todas las pruebas definidas en el directorio `tests/` y mostrará los resultados detallados.
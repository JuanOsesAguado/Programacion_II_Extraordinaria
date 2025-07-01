## Estructura del Proyecto# Programacion_II_Extraordinaria

https://github.com/JuanOsesAguado/Programacion_II_Extraordinaria.git

# mi_simulador_celeste

Este proyecto implementa un simulador de sistemas planetarios simplificado en Python, haciendo uso de los principios de la mecánica newtoniana y la programación orientada a objetos (POO). Permite modelar la interacción gravitatoria entre cuerpos celestes sin una interfaz gráfica, utilizando la consola para la interacción.

## Características

- **Listado de Cuerpos Celestes**: Muestra información detallada de todos los cuerpos registrados.
- **Registro de Nuevos Cuerpos**: Permite añadir planetas, asteroides o satélites con sus propiedades iniciales.
- **Cálculo de Fuerzas Gravitatorias**: Calcula la fuerza neta sobre cada cuerpo debido a la atracción de los demás.
- **Evolución Temporal (Integración)**: Simula el movimiento de los cuerpos a lo largo del tiempo utilizando el método de Euler explícito.
- **Cálculo de Energía y Momento**: En cada paso de la simulación, calcula y muestra la energía cinética total, la energía potencial gravitatoria y el momento lineal total del sistema.
- **Persistencia en Archivo**: Guarda y carga el estado completo del sistema en formato JSON o CSV.

## Estructura del Proyecto

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
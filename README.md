# AlgebraPro1

Calculadora simbólica con interfaz Tk para analizar funciones de una variable (x): dominio, intersecciones con ejes, evaluación en un punto, rango aproximado y gráfico.

## Requisitos

- Python 3.11+ (probado en Windows)
- Paquetes: ver `requirements.txt`

## Instalación

1) Crear entorno virtual (opcional pero recomendado)
2) Instalar dependencias

## Uso

Ejecuta la app desde el punto de entrada:

- `main.py` abre la ventana.
- Ingresa la función (usa `**` para potencias) y un valor opcional para x.
- Botones: “analizar función” y “graficar función”.

## Arquitectura

- `main.py`: punto de entrada.
- `interfaz/`: UI Tk (`InterfazGrafica`).
- `funciones/`: lógica de análisis (parseo, dominio, rango, intersecciones, evaluación y gráfico).

## Limitaciones

- Rango es aproximado (basado en límites en ±∞ y el gráfico).
- Solo se admite la variable `x`.

## Créditos y licencia

Proyecto académico. Uso educativo.

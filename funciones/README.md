Estructura de Archivos

evaluar_punto.py: Parseo de función.
calcular_dominio.py: Cálculo de dominio.
calcular_rango.py: Cálculo de recorrido.
calcular_intersecciones.py: Intersecciones con ejes.
evaluar_punto.py: Evaluación de punto.
graficar_funcion.py: Generación de gráfico.



1. evaluar_punto.py - Función: evaluar_punto(expr_str)
Propósito: Parsea y valida el input de la función como string, convirtiéndola en expresión simbólica con SymPy. Maneja polinómicas (e.g., "x2 + 1") y racionales (e.g., "(x+1)/(x-2)") detectando '/' para fracciones. Asegura input limpio y lanza error si inválido.

 - Inputs: expr_str (string, e.g., "2*x2 + 2*x").
 - Outputs: Tupla (expr, x) donde expr es la expresión simbólica y x es el símbolo.

Justificación Computacional: Usa sympify para interpretación simbólica segura; split para racionales. Cumple con "ingreso limpio con SymPy" (rúbrica: 3 pts). Manejo errores: SympifyError para inválidos.
Ejemplo: "1/x" → expr = 1/x.




2. calcular_dominio.py - Función: calcular_dominio(expr, x)
Propósito: Calcula el dominio excluyendo puntos donde el denominador es cero en funciones racionales (e.g., asintotas verticales). Para polinómicas, es todo $\mathbb{R}$. Imprime justificación.

 - Inputs: expr (expresión simbólica), x (símbolo).
 - Outputs: String describiendo dominio (e.g., "R \ {0}").

Justificación Computacional: Usa fraction y together de SymPy para extraer denominador, luego solve para ceros reales. Imprime pasos (denominador y ceros). Cumple con "determina dominio" y "desarrollo paso a paso" (rúbrica: 3 pts). Manejo errores: Try-except para casos complejos.

- Ejemplo: Para $ f(x) = \frac{1}{x} $, dominio = "R \ {0}", justificación: "Denominador = x, ceros en x = [0]".





3. calcular_rango.py - Función: calcular_rango(expr, x)
Propósito: Aproxima el recorrido (rango) analizando límites en $ \pm \infty $ para identificar asintotas horizontales o 
comportamiento. Para casos complejos, sugiere consultar gráfico (simbólico exacto es avanzado). Imprime justificación.

 - Inputs: expr (expresión simbólica), x (símbolo).
 - Outputs: String aproximado (e.g., "[0, ∞)" o "Difícil simbólicamente; ver gráfico").

Justificación Computacional: Usa limit de SymPy para evaluar límites. Si iguales, asume rango basado en asintota. Imprime pasos (límites). Cumple con "determina recorrido" y justificación (rúbrica: 3 pts). Limitado a aproximación básica para 
concisión.

- Ejemplo: Para $ f(x) = x^2 $, límites ∞, recorrido "[0, ∞)"; justificación: "Límite x→-∞: ∞, x→∞: ∞".



4. calcular_intersecciones.py - Función: calcular_intersecciones(expr, x)
Propósito: Calcula intersecciones con ejes: X (raíces donde f(x)=0), Y (f(0)). Solo raíces reales. Imprime justificación.

 - Inputs: expr (expresión simbólica), x (símbolo).
 - Outputs: Tupla (x_int, y_int) donde x_int es lista de floats (raíces), y_int es float o None.

Justificación Computacional: Usa solve de SymPy para raíces, subs para y-intersección. Imprime pasos (raíces y f(0)). Cumple con "calcula intersecciones" (rúbrica: 3 pts). Manejo errores: Try-except.

-Ejemplo: Para $ f(x) = x^2 - 1 $, x_int = [-1.0, 1.0], y_int = -1.0; justificación: "Raíces: [-1, 1], y-int: -1".



5. evaluar_punto.py - Función: evaluar_punto(expr, x_val, x)
Propósito: Evalúa f(x) en un punto dado, mostrando pasos detallados de sustitución y cálculo. Retorna par ordenado para gráfico.

 - Inputs: expr (expresión simbólica), x_val (float), x (símbolo).
 - Outputs: Tupla (x_val, result) (par ordenado).

Justificación Computacional: Usa subs para sustituir, evalf para numérico. Imprime pasos (1: Sustituir, 2: Expresión, 3: Resultado). Cumple con "evaluar punto paso a paso" y "remarca en gráfica" (rúbrica: 3 pts). Manejo errores: ValueError para inválido (e.g., /0).

 - Ejemplo: f(x)=x^2, x=3 → "Paso 1: ...", resultado (3, 9).





6. graficar_funcion.py - Función: graficar_funcion(expr, x, x_int, y_int, eval_point=None, domain="Todo R")
Propósito: Genera gráfico profesional de la función, marcando intersecciones (verde/orange) y punto evaluado (rojo, sin alterar original). Incluye dominio/recorrido visible vía rango plot (-10 a 10, ajustable).

 - Inputs: expr (expresión), x (símbolo), x_int (lista), y_int (float), eval_point (tupla opcional), domain (string).
 - Outputs: Gráfico popup con Matplotlib (títulos, etiquetas, leyenda, grid, ejes).

Justificación Computacional: Usa linspace para puntos, plot/scatter para elementos. No altera original (solo añade markers). Cumple con "gráfica clara con títulos/etiquetas/colores" (rúbrica: 6-8 pts).

 - Ejemplo: Muestra curva azul, puntos verdes/orange/rojo, legend "f(x)", "X-intersecciones", etc.





7. main.py - Función: main()
Propósito: Coordina el flujo: Obtiene inputs, llama funciones secuencialmente, maneja errores globales y genera salida completa. Interfaz CLI interactiva.

 - Inputs: Ninguno (usa input() para usuario).
 - Outputs: Impresiones en consola + gráfico.

Justificación Computacional: Imports modulares, try-except global. Flujo: Parse → Análisis → Eval opcional → Plot. Cumple con "interfaz intuitiva" y "desarrollo computacional" (rúbrica: 6-8 pts para interfaz).

 - Ejemplo: Prompt "Ingresa función: ", procesa y muestra todo.
def evaluar_punto(expr, x_val, x):
    try:
        print(f"Paso 1: Sustituir x={x_val} en {expr}")
        expr_sustituida = expr.subs(x, x_val)
        print(f"Paso 2: Expresión: {expr_sustituida}")
        resultado = float(expr_sustituida.evalf())
        print(f"Paso 3: Resultado: f({x_val}) = {resultado}")
        return (x_val, resultado)
    except:
        raise ValueError("Evaluación inválida (por ejemplo, división por cero).")
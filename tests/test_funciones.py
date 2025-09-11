import sympy as sp
import pytest

from funciones.analizar_funcion import analizar_funcion
from funciones.calcular_dominio import calcular_dominio
from funciones.calcular_intersecciones import calcular_intersecciones
from funciones.evaluar_punto import evaluar_punto
from funciones.calcular_rango import calcular_rango


def test_analizar_funcion_basico():
    expr, x = analizar_funcion("x**2 - 4")
    assert str(expr) == "x**2 - 4"
    assert x.name == "x"


def test_dominio_polinomica_todo_R():
    x = sp.symbols("x")
    expr = x**2 - 4
    assert calcular_dominio(expr, x) == "Todo R"


def test_dominio_racional_exclusion():
    expr, x = analizar_funcion("(x+1)/(x-2)")
    dominio = calcular_dominio(expr, x)
    assert "2" in dominio  # excluye x=2


def test_intersecciones_reales():
    x = sp.symbols("x")
    expr = x**2 - 4
    xs, y0 = calcular_intersecciones(expr, x)
    assert sorted(xs) == [-2.0, 2.0]
    assert y0 == -4.0


def test_evaluar_punto():
    x = sp.symbols("x")
    expr = x**2
    xv, yv = evaluar_punto(expr, 3, x)
    assert (xv, round(yv, 3)) == (3, 9.0)


def test_rango_aproximado():
    expr, x = analizar_funcion("x**2")
    r = calcular_rango(expr, x)
    assert isinstance(r, str)

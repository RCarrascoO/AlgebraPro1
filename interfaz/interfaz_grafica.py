import tkinter as tk
from tkinter import messagebox
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InterfazGrafica:
    def __init__(self,root):
        self.root = root
        self.root.title("Calculadora Simbólica")
        self.func_str = tk.StringVar()
        self.x_value = tk.DoubleVar()
        self.create_widgets()
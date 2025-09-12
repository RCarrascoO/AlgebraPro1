import os
import sys

# Asegurar importaciones de paquetes locales al ejecutar directamente
CURRENT_DIR = os.path.dirname(__file__)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from interfaz.interfaz_grafica import InterfazGrafica
import customtkinter as ctk


def main():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = InterfazGrafica(root)
    root.mainloop()


if __name__ == "__main__":
    main()

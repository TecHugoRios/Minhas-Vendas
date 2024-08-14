import tkinter as tk
from tkinter import *
import pandas as pd
import GUI
import VerificacaoXlsx


def main():
    VerificacaoXlsx.XlsxExiste()
    GUI.menu_principal.mainloop()


main()

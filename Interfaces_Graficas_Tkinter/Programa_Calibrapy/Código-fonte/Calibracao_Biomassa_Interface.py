## ALGORITMO PARA CONSTRUÇÃO DA CURVA DE CALIBRAÇÃO PARA BIOMASSA:

## Bibliotecas científicas
import numpy as np 
import pandas as pd 
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
from scipy.optimize import leastsq
import math
import scipy.stats as sc
import time
import tkinter as tk
from tkinter import *
from tkinter import Label, Button
from tkinter.filedialog import askopenfilename # caixa externa - explorar files no computador
import os # divisão de strings
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from prettytable import PrettyTable
from PIL import Image, ImageTk
from tkinter.ttk import Combobox
from tkinter.filedialog import asksaveasfilename
from tkinter.commondialog import Dialog
from tkinter import colorchooser
import winsound
from tkinter import ttk
from tkinter import filedialog

# Criação da interface:
interface = Tk()
interface.title("CalibraPy")
interface.geometry("900x650")
interface.configure(bg = "gray75")
titulo = Label(interface, text="CURVA DE CALIBRAÇÃO PARA BIOMASSA", font="times 14 bold", fg="black", bg = "gray70", borderwidth=4, relief="sunken").grid(row = 0, column = 0, columnspan=1)
interface.resizable(0,0)

# Template Excel:
load = Image.open("Excel_template.png")
render = ImageTk.PhotoImage(load)
img = Label(interface, image = render, border = 0, borderwidth = 2, relief = "solid")
img.image = render
img.grid(row = 2, column = 4, padx = 6)
Button(interface, text = "Baixe nosso template", font = "arial 7 bold", fg = "black", bg = "white", borderwidth = 2, relief = "raised").grid(row = 3, column = 4, padx = 10)

# Seleção da ação desejada:
Label(interface, text = "SELECIONE A AÇÃO DESEJADA:", font = "times 10 bold italic", bg = "gray75").grid(row = 2, column = 2, sticky=W+S)
v = ("CONSTRUIR CURVA DE CALIBRAÇÃO", "UTILIZAR CURVA PRÉ-EXISTENTE")
combo = Combobox(interface, values = v, width = 39, font = "arial 10")
combo.set("-----------------------ESCOLHA-----------------------")
combo.grid(row = 3, column = 2)

# Separação variáveis de entrada:
Label(interface, width = 49, height = 32, borderwidth = 4, relief = "sunken", bg = "grey85").grid(row = 5, column = 0, pady = 10)
teste = Label(interface, width = 45, height = 23, borderwidth = 4, relief = "sunken",bg = "grey95")
teste.grid(row = 5, column = 0, pady = 108, sticky=N)

# Entradas - Primeira Opção Combobox:
tex_num_amos = Label(interface, text = "Leituras do Ensaio",  borderwidth = 4, relief = "sunken", fg = "black", bg = "grey95")
tex_num_amos.grid(row = 5, column = 0, padx = 52, pady = 140, sticky=N+W)

# Saída para o gráfico:
Label(interface, width = 68, height = 26, borderwidth = 4, relief = "sunken", bg = "grey85").place(x = 395, y = 223)

def printar_val():
    val_selec = combo.get() 
    print(val_selec)
    if val_selec == "CONSTRUIR CURVA DE CALIBRAÇÃO":
        #Label(interface, width = 45, height = 12, borderwidth = 4, relief = "sunken",bg = "white").grid(row = 5, column = 0, pady = 100, sticky=N)
        #teste.configure(bg = "red")
        tex_num_amos.configure(fg = "pink", relief = "groove")
    if val_selec == "UTILIZAR CURVA PRÉ-EXISTENTE":  
        Label(interface, width = 45, height = 10, borderwidth = 4, relief = "sunken",bg = "white").grid(row = 5, column = 0, pady = 30, sticky=S)
Button(interface, text = "AVANÇAR", font = "batang 7 bold", fg = "white", bg = "black", borderwidth=4, relief="flat", command = printar_val).grid(row = 3, column = 3, padx = 2)

# Explorador para carregar o arquivo de entrada:
def explorador():
    explorador = askopenfilename()
    nome_arquivo = os.path.basename(explorador)
    Label(interface,text=nome_arquivo,font="arial 8 bold italic", fg="black", borderwidth=2, relief="ridge", justify = "center", bg = "gray95",  width = 40).grid(row = 5, column = 0, pady = 58, sticky=N)
    # Captura dos dados de entrada - formato dataframe:
    #excel_entrada = pd.read_excel(nome_arquivo)
    #excel_entrada_np = excel_entrada.values
Button(interface, text = "Carregar Arquivo", font = "batang 10 bold", fg = "white", bg = "black", borderwidth=2, relief="groove", command = explorador).grid(row = 5, column = 0, padx = 32, pady = 30, sticky=N+W)


interface.mainloop()



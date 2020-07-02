# Importação das bibliotecas e pacotes:
## Módulos propriamente construídos
import Modulos_Monod
import Modulos_Contois
import Modulos_Andrews
import Modulos_Aiba_et_al
import Modulos_Moser
import Modulos_Hope__Hansford
import Modulos_Wu_et_al
import Modulos_Levenspiel
import Modulos_Lee_et_al
import Modulos_mi_constante
import Modulo_peso_limite_AG
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
janela = Tk()
janela.title("Processos Fermentativos em Batelada - Simulação")
janela.geometry("600x300")
#janela.configure(bg = "grey")
titulo = Label(janela, text="MODELOS CINÉTICOS NÃO ESTRUTURADOS", font="times 16 bold", fg="BLACK", borderwidth=2, relief="groove").place(x=430,y=0)

# Carregar a imagem do logo:
load = Image.open("Logo.png")
render = ImageTk.PhotoImage(load)
img = Label(janela, image = render, border = 0)
img.image = render
img.place(x = 45, y = 16)

# Criação do notebook - abas seleção simulação ou modelagem
notebook = ttk.Notebook(janela)
notebook.grid(row=3, column =3, sticky=tk.E + tk.W + tk.N + tk.S, padx=30, pady=110)
frame1 = ttk.Frame(notebook, width = 1300, height = 510, borderwidth = 5, relief = tk.SUNKEN)
notebook.add(frame1, text = 'SIMULAÇÃO')
frame2 = ttk.Frame(notebook, width = 1300, height = 510, borderwidth = 5, relief = tk.SUNKEN)
notebook.add(frame2, text = 'MODELAGEM')

#****
# Definição combobox - seleção da cinética:

## Simulação:
# Caixas de separação:
Label(frame1, text="", width = 53, height = 33, borderwidth = 3,  relief = "sunken", bg = "grey75").place(x = 10, y = 2)
ttk.Label(frame1, text = "SELECIONE A CINÉTICA DE REAÇÃO:", font = "times 12 bold").place(x = 16, y = 10)
v_1 = ("AUSÊNCIA DE INIBIÇÃO", "INIBIÇÃO PELO SUBSTRATO", "INIBIÇÃO PELO PRODUTO", "INIBIÇÃO PELA BIOMASSA", "CINÉTICA CONSTANTE")
combo_1 = Combobox(frame1, values = v_1, width = 39, font = "arial 10")
combo_1.set("-----------------------ESCOLHA-----------------------")
combo_1.place(x = 15, y = 32)
def print_me_1():
    value_1 = combo_1.get()
    print(value_1)
Button(frame1, text="Pronto", bg = "black", fg="white", font="batang 12", command = print_me_1).place(x = 315, y = 29)

## MODELAGEM ##
# Caixas de separação:
Label(frame2, text="", width = 53, height = 33, borderwidth = 3,  relief = "sunken", bg = "grey85").place(x = 10, y = 2)
ttk.Label(frame2, text = "SELECIONE A CINÉTICA DE REAÇÃO:", font = "times 12 bold").place(x = 16, y = 10)
# Combobox:
v_2 = ("AUSÊNCIA DE INIBIÇÃO", "INIBIÇÃO PELO SUBSTRATO", "INIBIÇÃO PELO PRODUTO", "INIBIÇÃO PELA BIOMASSA", "CINÉTICA CONSTANTE")
combo_2 = Combobox(frame2, values = v_2, width = 39, font = "arial 10")
combo_2.set("-----------------------ESCOLHA-----------------------")
combo_2.place(x = 15, y = 32)
def print_me_2():
    value_2 = combo_2.get()
    print(value_2)
Button(frame2, text="Pronto", bg = "black", fg="white", font="batang 12", command = print_me_2).place(x = 315, y = 29)
# Saídas:
Label(frame2, text="", width = 52, height = 33, borderwidth = 3,  relief = "sunken", bg = "grey85").place(x = 914, y = 2)
Label(frame2, text="", width = 50, height = 18, borderwidth = 3,  relief = "sunken", bg = "grey").place(x = 921, y = 185)
load = Image.open("Tabela_6_gl.png")
render = ImageTk.PhotoImage(load)
img = Label(frame2, image = render, border = 0)
img.image = render
img.place(x = 930, y = 205)
load = Image.open("Tabela_6_gl.png")
render = ImageTk.PhotoImage(load)
img = Label(frame2, image = render, border = 0)
img.image = render
img.place(x = 930, y = 366.2)
Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
Label(frame2, text = "b", font = "times 42", fg = "grey40", bg = "grey40", width = 3,borderwidth=4, relief ='sunken').place(x = 1160, y = 288.2)
Label(frame2, text = "F. Obj:", font = "broadway 11", fg = "white", bg = "black", justify = "center",  borderwidth=4, relief ='sunken').place(x = 1095, y = 297.2)
Label(frame2, text = u"R\u00b2:", font = "broadway 11", fg = "white", bg = "black", justify = "center",  borderwidth=4, relief ='sunken').place(x = 1124, y = 327.2)
load = Image.open("Cronometro.png")
render = ImageTk.PhotoImage(load)
img = Label(frame2, image = render, border = 0)
img.image = render
img.place(x = 932, y = 296) 
# Documentos excel - acesso:
## Escrita do template excel para entrada dos dados:
def excel_template():
    df_t = pd.DataFrame({'Tempo(t)':[]})
    df_Cx = pd.DataFrame({'Cx(m/v)':[]})
    df_Cs = pd.DataFrame({'Cs(m/v)':[]})
    df_Cp = pd.DataFrame({'Cp(m/v)':[]})
    df_dad_exp = pd.concat([df_t, df_Cx, df_Cs, df_Cp], axis=1)
    with pd.ExcelWriter('Template_Entrada_Dados.xlsx') as writer:
        df_dad_exp.to_excel(writer, sheet_name="C_t_exp")
        writer.save()
    os.system("start EXCEL Template_Entrada_Dados.xlsx")           
load = Image.open("Excel_template.png")
render = ImageTk.PhotoImage(load)
img = Label(frame2, image = render, border = 0, borderwidth = 2, relief = "solid")
img.image = render
img.place(x = 960, y = 41)
Button(frame2, text = "Baixe nosso template", font = "arial 7 bold", fg = "black", bg = "white", borderwidth = 2, relief = "raised", command = excel_template).place(x = 923, y = 100)
Label(frame2, text = "", borderwidth=3, relief="groove", width = 33, height = 7, bg = "gray45").place(x = 1030, y = 7)
Label(frame2, text = "Acessar Arquivos", font = "arial 8 bold", fg = "white", bg = "black", borderwidth=4, relief="sunken").place(x = 1036, y = 13)












janela.mainloop()
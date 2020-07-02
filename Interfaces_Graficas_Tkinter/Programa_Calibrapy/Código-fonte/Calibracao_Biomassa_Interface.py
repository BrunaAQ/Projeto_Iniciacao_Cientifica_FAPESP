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
teste = Label(interface, width = 45, height = 23, borderwidth = 4, relief = "sunken",bg = "grey70")
teste.grid(row = 5, column = 0, pady = 108, sticky=N)
Label(interface, width = 40, height = 12, borderwidth = 4, relief = "sunken",bg = "grey70").grid(row = 5, column = 0, pady = 145, sticky=N)

# Separação saída:
Label(interface, width = 33, height = 4, borderwidth = 4, relief = "sunken", bg = "grey65").place(x = 620, y = 150)
tit_equa_sai = Label(interface, text = "Regressão Linear", font = "times 10 bold", fg = "black", bg = "white", borderwidth = 3, relief = "sunken").place(x = 610, y = 142)
sai_equa = Label(interface, text = "Cx =                   * D.O. +                    ", font = "times 9 bold", fg = "black", bg = "gray90", borderwidth = 3, relief = "sunken").place(x = 625, y = 170)
sai_r2 = Label(interface, text = "R² =                   ", font = "times 9 bold", fg = "black", bg = "gray90", borderwidth = 3, relief = "sunken").place(x = 625, y = 193)

# Saída para o gráfico:
Label(interface, width = 68, height = 26, borderwidth = 4, relief = "sunken", bg = "grey85").place(x = 395, y = 223)

# Programação da apresentação inicial da interface - tudo sem função, apenas demonstrativa:
botao_explor = Button(interface, text = "Carregar Arquivo", font = "batang 10 bold", fg = "gray30", bg = "gray70", borderwidth=2, relief="sunken")
botao_explor.grid(row = 5, column = 0, padx = 32, pady = 30, sticky=N+W)
tit_criar_curva = Label(interface, text = "Calibrar",font = "times 11 italic",  borderwidth = 2, relief = "sunken", fg = "black", bg = "gray95")
tit_criar_curva.grid(row = 5, column = 0, padx = 48, pady = 134, sticky=N+W)
tit_num_leit = Label(interface, text = "Quantidade de Leituras",font = "times 10",  borderwidth = 3, relief = "groove", fg = "gray30", bg = "gray70")
tit_num_leit.grid(row = 5, column = 0, padx = 64, pady = 170, sticky=N+W)
botao_unic = Button(interface, text = "ÚNICA", font = "arial 8 bold", fg = "gray30", bg = "gray70", borderwidth=2, relief="sunken")
botao_unic.grid(row = 5, column = 0, padx = 64, pady = 200, sticky=N+W)
botao_dupl = Button(interface, text = "DUPLICATA", font = "arial 8 bold", fg = "gray30", bg = "gray70", borderwidth=2, relief="sunken")
botao_dupl.grid(row = 5, column = 0, padx = 114, pady = 200, sticky=N+W)
botao_tripl = Button(interface, text = "TRIPLICATA", font = "arial 8 bold", fg = "gray30", bg = "gray70", borderwidth=2, relief="sunken")
botao_tripl.grid(row = 5, column = 0, padx = 135, pady = 200, sticky=N+E)
botao_outra = Button(interface, text = "OUTRA", font = "arial 8 bold", fg = "gray30", bg = "gray70", borderwidth=2, relief="sunken")
botao_outra.grid(row = 5, column = 0, padx = 80, pady = 200, sticky=N+E)
tit_coef_ang = Label(interface, text = "Coeficiente Angular:",font = "times 8 italic bold",  borderwidth = 3, relief = "sunken", fg = "gray30", bg = "gray70")
tit_coef_ang.grid(row = 5, column = 0, padx = 64, pady = 262, sticky=N+W)
sai_coef_ang = Label(interface, width = 10, text = "I", font = "batang 10", fg = "gray70", bg = "gray70", borderwidth = 3, relief = "sunken")
sai_coef_ang.grid(row = 5, column = 0, padx = 64, pady = 260, sticky=S+W)
tit_coef_lin = Label(interface, text = "Coeficiente Linear:",font = "times 8 italic bold",  borderwidth = 3, relief = "sunken", fg = "gray30", bg = "gray70")
tit_coef_lin.grid(row = 5, column = 0, padx = 130, pady = 262, sticky=N+E)
sai_coef_lin = Label(interface, width = 10, text = "I", font = "batang 10", fg = "gray70", bg = "gray70", borderwidth = 3, relief = "sunken")
sai_coef_lin.grid(row = 5, column = 0, padx = 139, pady = 260, sticky=S+E)
botao_ok_calib = Button(interface, text = "PRONTO", font = "batang 8 bold", fg = "gray30", bg = "gray70", borderwidth=2, relief="sunken")
botao_ok_calib.grid(row = 5, column = 0, padx = 62, pady = 240, sticky=S+E)
sai_r2 = Label(interface, text = "I", font = "batang 9", width = 7, fg = "grey90", bg = "grey90")
sai_r2.place(x = 650, y = 196.5)
sai_a = Label(interface, text = "I", font = "batang 9", width = 7, fg = "grey90", bg = "grey90")
sai_a.place(x = 655, y = 173.5)
sai_b = Label(interface, text = "I", font = "batang 9", width = 7, fg = "grey90", bg = "grey90")
sai_b.place(x = 755, y = 173.5)
## Parte funcional do código:

# Explorador para carregar o arquivo de entrada:
def explorador():
    explorador = askopenfilename()
    nome_arquivo = os.path.basename(explorador)
    Label(interface,text=nome_arquivo,font="arial 8 bold italic", fg="black", borderwidth=2, relief="ridge", justify = "center", bg = "gray85",  width = 40).grid(row = 5, column = 0, pady = 68, sticky=N)
    # Captura dos dados de entrada - formato dataframe:
    excel_entrada = pd.read_excel(nome_arquivo)
    global excel_entrada_np
    excel_entrada_np = excel_entrada.values
    print(excel_entrada_np)

# Captura da ação desejada pelo operador:   
def printar_val():
    val_selec = combo.get() 
    print(val_selec)
    if val_selec == "CONSTRUIR CURVA DE CALIBRAÇÃO":
        botao_explor.configure(fg = "white", bg = "black", relief = "groove", command = explorador)
        tit_criar_curva.configure(relief = "raised")
        tit_num_leit.config(font = "times 10 bold", fg = "black", bg = "gray70")
        botao_unic.config(fg = "white", bg = "grey40", relief = "raised", command = unica, activebackground="lightgreen")
        botao_dupl.config(fg = "white", bg = "grey40", relief = "raised", activebackground="lightgreen")
        botao_tripl.config(fg = "white", bg = "grey40", relief = "raised", activebackground="lightgreen")
        botao_outra.config(fg = "white", bg = "grey40", relief = "raised", command = entr_leit, activebackground="lightgreen")
        botao_ok_calib.config(fg = "white", bg = "black")
        
    if val_selec == "UTILIZAR CURVA PRÉ-EXISTENTE":  
        #Label(interface, width = 45, height = 10, borderwidth = 4, relief = "sunken",bg = "white").grid(row = 5, column = 0, pady = 30, sticky=S)
        botao_explor.configure(command = explorador)
        
# Função para entradas de leituras acima de triplicata:    
def entr_leit():
    global num_leit_entr
    num_leit_entr = tk.Entry(interface, width = 4, borderwidth = 2, relief = "sunken", font = "batang 12 bold", bg = "white", fg = "black")
    num_leit_entr.grid(row = 5, column = 0, padx = 80, pady = 230, sticky=N+E)
    tex_qual = Label(interface, text = "Qual?",font = "times 10", fg = "black", bg = "gray70")
    tex_qual.grid(row = 5, column = 0, padx = 125, pady = 231, sticky=N+E)
    
# Leitura única:
def unica():
    global cont_leit
    cont_leit = 1
    print(cont_leit)
    global do_exp, cx_exp
    do_exp = excel_entrada_np[:,0] #eixo x
    cx_exp = excel_entrada_np[:,1] #eixo y
    print(do_exp)
    print(cx_exp)
    botao_unic.config(bg = "black")
    
# Comando, considerando conceitos estatísticos, para a construção da curva de calibração:
def calibra():
    pl=np.polyfit(do_exp,cx_exp,1)                     
    cx_model=pl[0]*do_exp+pl[1]                        
    cx_rest=cx_exp-cx_model
    SQrest=sum(pow(cx_rest,2))
    SQtotal=len(cx_exp)*np.var(cx_exp)
    R2=1-(SQrest/SQtotal)
    print(pl[0].round(4))
    print(pl[1].round(4))
    tit_coef_ang.config(fg = "white", bg = "gray20")
    tit_coef_lin.config(fg = "white", bg = "gray20")
    
    # Criação do gráfico:
    f = plt.figure(figsize=(8.53,7), dpi = 56) 
    plot = f.add_subplot(111)      
    plt.plot(do_exp,cx_exp,'o',markersize=14,color='grey',markeredgecolor='black') 
    plt.plot(do_exp,np.polyval(pl,do_exp),'g',linewidth=2)                          
    plt.xlabel("Densidade Óptica", weight='bold')                               
    plt.ylabel("Concentração de células (g/L)", weight='bold')                    
    plt.annotate(u'Linha de tendência modelo', xy=(3.7, 1.8), xytext=(1.8, 2.1), arrowprops=dict(facecolor='m',shrink=0.05), size=15)    
    plt.grid(True)                                                                                                                                                                     
    f.patch.set_facecolor('white')                                                   
    plt.style.use('default')   
    canvas = FigureCanvasTkAgg(f, interface)
    a = canvas.get_tk_widget().place(x = 400, y = 228)
    
    # Saída - valores coeficientes:
    sai_coef_ang.config(text = pl[0].round(4), font = "batang 10", fg = "black")
    sai_coef_lin.config(text = pl[1].round(4), font = "batang 10", fg = "black")
    sai_a.config(text = pl[0].round(4), fg = "black")
    sai_b.config(text = pl[1].round(4), fg = "black")
    sai_r2.config(text = R2.round(5), fg = "black")

# Passando o comando para o botão -  lançamento dos resultados:    
botao_ok_calib.config(command = calibra)



Button(interface, text = "AVANÇAR", font = "batang 7 bold", fg = "white", bg = "black", borderwidth=4, relief="flat", command = printar_val).grid(row = 3, column = 3, padx = 2)

interface.mainloop()



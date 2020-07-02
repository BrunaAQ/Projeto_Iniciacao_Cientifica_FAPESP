# Importação das bibliotecas e pacotes:
## Módulos propriamente construídos
import Modulos_Monod
import Modulos_Contois
import Modulos_Andrews
import Modulos_Aiba_et_al
import Modulos_Moser
import Modulos_Hope__Hansford
import Modulos_Hope_Hansford
import Modulos_Wu_et_al
import Modulos_Levenspiel
import Modulos_Lee_et_al
import Modulos_mi_constante
import Modulo_peso_limite_AG
import Modulo_documentacao
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
#janela.configure(bg = "white")
titulo = Label(janela, text="MODELOS CINÉTICOS NÃO ESTRUTURADOS", font="times 16 bold", fg="BLACK", borderwidth=2, relief="groove").place(x=430,y=0)

# Função para impressão de imagens:
def image(imagem, num_frame, x, y):
    load = Image.open(imagem)
    render = ImageTk.PhotoImage(load)
    img_contois = Label(num_frame, image = render, border = 0)
    img_contois.image = render
    img_contois.place(x = x, y = y)

def image_dif(imagem, num_frame, x, y):
    load = Image.open(imagem)
    render = ImageTk.PhotoImage(load)
    img_contois = Label(num_frame, image = render, border = 0, borderwidth = 2, relief = "sunken")
    img_contois.image = render
    img_contois.place(x = x, y = y)

# Carregar a imagem do logo:
load = Image.open("Logo_mod.png")
render = ImageTk.PhotoImage(load)
img = Label(janela, image = render, border = 0, borderwidth = 3, relief = "sunken")
img.image = render
img.place(x = 45, y = 16)

# Função para tabela parâmetros cinéticos:
def tab_fun_cin():
    load = Image.open("Tabela.png")
    render = ImageTk.PhotoImage(load)
    img = Label(frame2, image = render, border = 0)
    img.image = render
    img.place(x = 930, y = 205)

# Função para saídas:
def func_sai():
    Label(frame2, text = "b", font = "times 100", fg = "grey", borderwidth=2.3, relief="ridge", width = 14, bg = "grey", justify = "center").place(x = 150, y = 540)
    Label(frame2, text = "b", font = "times 14", fg = "grey", bg = "grey", borderwidth=3, relief="flat", width = 18).place(x = 140, y = 260)
    Label(frame2, text = "b", font = "times 14", fg = "grey", bg = "grey", borderwidth=3, relief="flat", width = 18).place(x = 140, y = 340)
    Label(frame2, text = "b", font = "times 14", fg = "grey", bg = "grey", borderwidth=3, relief="flat", width = 18).place(x = 140, y = 420)

# Criação do notebook - abas seleção simulação ou modelagem
notebook = ttk.Notebook(janela)
notebook.grid(row=3, column =3, sticky=tk.E + tk.W + tk.N + tk.S, padx=30, pady=110)
frame1 = ttk.Frame(notebook, width = 1300, height = 510, borderwidth = 5, relief = tk.SUNKEN)
notebook.add(frame1, text = 'SIMULAÇÃO')
frame2 = ttk.Frame(notebook, width = 1300, height = 510, borderwidth = 5, relief = tk.SUNKEN)
notebook.add(frame2, text = 'MODELAGEM')
frame3 = ttk.Frame(notebook, width = 1300, height = 510, borderwidth = 5, relief = tk.SUNKEN)
notebook.add(frame3, text = 'DOCUMENTAÇÃO')
def notebook_sem_inib():
    notebook_sem_inib = ttk.Notebook(frame2)
    notebook_sem_inib.grid(row=3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx=50, pady=85)
    global frame4
    frame4 = ttk.Frame(notebook_sem_inib, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_sem_inib.add(frame4, text = 'CONTOIS')
    global frame5
    frame5 = ttk.Frame(notebook_sem_inib, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_sem_inib.add(frame5, text = 'MONOD')
    global frame6
    frame6 = ttk.Frame(notebook_sem_inib, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_sem_inib.add(frame6, text = 'MOSER')
def notebook_sem_inib_simul():
    notebook_sem_inib_sim = ttk.Notebook(frame1)
    notebook_sem_inib_sim.grid(row=3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx=50, pady=85)
    global frame13
    frame13 = ttk.Frame(notebook_sem_inib_sim, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_sem_inib_sim.add(frame13, text = 'CONTOIS')
    global frame14
    frame14 = ttk.Frame(notebook_sem_inib_sim, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_sem_inib_sim.add(frame14, text = 'MONOD')
    global frame15
    frame15 = ttk.Frame(notebook_sem_inib_sim, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_sem_inib_sim.add(frame15, text = 'MOSER')
def notebook_inib_subs():
    notebook_inib_subs = ttk.Notebook(frame2)
    notebook_inib_subs.grid(row=3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx=50, pady=85)
    global frame7
    frame7 = ttk.Frame(notebook_inib_subs, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_subs.add(frame7, text = 'ANDREWS')
    global frame8
    frame8 = ttk.Frame(notebook_inib_subs, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_subs.add(frame8, text = 'WU ET AL')
def notebook_inib_subs_simul():
    notebook_inib_subs_simul = ttk.Notebook(frame1)
    notebook_inib_subs_simul.grid(row=3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx=50, pady=85)
    global frame16
    frame16 = ttk.Frame(notebook_inib_subs_simul, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_subs_simul.add(frame16, text = 'ANDREWS')
    global frame17
    frame17 = ttk.Frame(notebook_inib_subs_simul, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_subs_simul.add(frame17, text = 'WU ET AL')
def notebook_inib_prod():
    notebook_inib_prod = ttk.Notebook(frame2)
    notebook_inib_prod.grid(row=3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx=50, pady=85)
    global frame9
    frame9 = ttk.Frame(notebook_inib_prod, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_prod.add(frame9, text = 'AIBA ET AL')
    global frame10
    frame10 = ttk.Frame(notebook_inib_prod, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_prod.add(frame10, text = 'HOPE & HANSFORD')
    global frame11
    frame11 = ttk.Frame(notebook_inib_prod, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_prod.add(frame11, text = 'LEVENSPIEL')
def notebook_inib_prod_simul():
    notebook_inib_prod_simul = ttk.Notebook(frame1)
    notebook_inib_prod_simul.grid(row=3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx=50, pady=85)
    global frame18
    frame18 = ttk.Frame(notebook_inib_prod_simul, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_prod_simul.add(frame18, text = 'AIBA ET AL')
    global frame19
    frame19 = ttk.Frame(notebook_inib_prod_simul, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_prod_simul.add(frame19, text = 'HOPE & HANSFORD')
    global frame20
    frame20 = ttk.Frame(notebook_inib_prod_simul, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_prod_simul.add(frame20, text = 'LEVENSPIEL')
def notebook_inib_biomas():
    notebook_inib_biomas = ttk.Notebook(frame2)
    notebook_inib_biomas.grid(row=3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx=50, pady=85)
    global frame12
    frame12 = ttk.Frame(notebook_inib_biomas, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_biomas.add(frame12, text = 'LEE ET AL')
def notebook_inib_biomas_simul():
    notebook_inib_biomas_simul = ttk.Notebook(frame1)
    notebook_inib_biomas_simul.grid(row=3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx=50, pady=85)
    global frame21
    frame21 = ttk.Frame(notebook_inib_biomas_simul, width = 318, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_biomas_simul.add(frame21, text = 'LEE ET AL')

def notebook_graf_simul():
    notebook_graf_simul = ttk.Notebook(frame1)
    notebook_graf_simul.place(x = 401, y = 115)
    global frame22
    frame22 = ttk.Frame(notebook_graf_simul, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_simul.add(frame22, text = 'Concentração')
    global frame23
    frame23 = ttk.Frame(notebook_graf_simul, width = 69, height = 22, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_simul.add(frame23, text = 'Produtividade X e P')
    global frame24
    frame24 = ttk.Frame(notebook_graf_simul, width = 69, height = 22, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_simul.add(frame24, text = u'Produtividade P.X\u207b\u00b9')
    global frame25
    frame25 = ttk.Frame(notebook_graf_simul, width = 69, height = 22, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_simul.add(frame25, text = 'Velocidade de Crescimento')

def notebook_docum():
    notebook_docum = ttk.Notebook(frame3)
    notebook_docum.place(x = 30, y = 165)
    global frame26
    frame26 = ttk.Frame(notebook_docum, width = 600, height = 310, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame26, text = 'Contois')
    global frame27
    frame27 = ttk.Frame(notebook_docum, width = 100, height = 1, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame27, text = 'Monod')
    global frame28
    frame28 = ttk.Frame(notebook_docum, width = 100, height = 1, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame28, text = 'Moser')
    global frame29
    frame29 = ttk.Frame(notebook_docum, width = 100, height = 1, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame29, text = 'Andrews')
    global frame30
    frame30 = ttk.Frame(notebook_docum, width = 100, height = 1, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame30, text = 'Wu et al')
    global frame31
    frame31 = ttk.Frame(notebook_docum, width = 100, height = 1, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame31, text = 'Aiba et al')
    global frame32
    frame32 = ttk.Frame(notebook_docum, width = 100, height = 1, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame32, text = 'Hope & Hansford')
    global frame33
    frame33 = ttk.Frame(notebook_docum, width = 100, height = 1, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame33, text = 'Levenspiel')
    global frame34
    frame34 = ttk.Frame(notebook_docum, width = 100, height = 1, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame34, text = 'Lee et al')
    
def notebook_algorit():
    notebook_algorit = ttk.Notebook(frame3)
    notebook_algorit.place(x = 660, y = 165)
    global frame35
    frame35 = ttk.Frame(notebook_algorit, width = 600, height = 310, borderwidth = 5, relief = tk.GROOVE)
    notebook_algorit.add(frame35, text = 'Integração Numérica')
    global frame36
    frame36 = ttk.Frame(notebook_algorit, width = 600, height = 310, borderwidth = 5, relief = tk.GROOVE)
    notebook_algorit.add(frame36, text = 'Algoritmo Genético')
    global frame37
    frame37 = ttk.Frame(notebook_algorit, width = 600, height = 310, borderwidth = 5, relief = tk.GROOVE)
    notebook_algorit.add(frame37, text = 'Algoritimo de Levenberg-Marquardt')
    
def notebook_graf_model():
    notebook_graf_model = ttk.Notebook(frame2)
    notebook_graf_model.place(x = 401, y = 115)
    global frame38
    frame38 = ttk.Frame(notebook_graf_model, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_model.add(frame38, text = 'Concentração')
    global frame39
    frame39 = ttk.Frame(notebook_graf_model, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_model.add(frame39, text = 'Produtividade X e P')
    global frame40
    frame40 = ttk.Frame(notebook_graf_model, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_model.add(frame40, text = u'Produtividade P.X\u207b\u00b9')
    global frame41
    frame41 = ttk.Frame(notebook_graf_model, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_model.add(frame41, text = 'Velocidade de Crescimento')
 
# Documentação modelos cinéticos:
Label(frame3, text = "Modelos Cinéticos", font = "Times 10 bold", fg = "black", bg = "grey75", borderwidth = 2, relief = "groove").place(x = 5, y = 140)
notebook_docum()
# Documentação algoritmos utilizados:
Label(frame3, text = "Implementação comptacional", font = "Times 10 bold", fg = "black", bg = "grey75", borderwidth = 2, relief = "groove").place(x = 632, y = 140)
notebook_algorit()   

# Documentação batelada:
Label(frame3, text = "Batelada", font = "Times 10 bold", fg = "black", bg = "grey75", borderwidth = 2, relief = "groove").place(x = 5, y = 0)
Label(frame3, bg = "grey85", width = 50, height = 6, borderwidth = 2, relief = "groove").place(x = 30, y = 25)
# Documentação balanço de massa:
Label(frame3, text = "Balanço de massa", font = "Times 10 bold", fg = "black", bg = "grey75", borderwidth = 2, relief = "groove").place(x = 415, y = 0)
Label(frame3, bg = "grey85", width = 118, height = 6, borderwidth = 2, relief = "groove").place(x = 442, y = 25)
Label(frame3, bg = "grey75", width = 28, height = 5, borderwidth = 2, relief = "sunken").place(x = 448, y = 32)
Label(frame3, bg = "grey77", width = 28, height = 5, borderwidth = 2, relief = "sunken").place(x = 654, y = 32)
Label(frame3, bg = "grey79", width = 28, height = 5, borderwidth = 2, relief = "sunken").place(x = 860, y = 32)
Label(frame3, bg = "grey81", width = 28, height = 5, borderwidth = 2, relief = "sunken").place(x = 1066, y = 32)
Label(frame3, text = "Equação Geral", font = "Times 8 bold", fg = "white", bg = "black", borderwidth = 2, relief = "groove").place(x = 451, y = 36)
Label(frame3, text = "Células", font = "Times 8 bold", fg = "white", bg = "black", borderwidth = 2, relief = "groove").place(x = 657, y = 36)
Label(frame3, text = "Substrato", font = "Times 8 bold", fg = "white", bg = "black", borderwidth = 2, relief = "groove").place(x = 863, y = 36)
Label(frame3, text = "Produto", font = "Times 8 bold", fg = "white", bg = "black", borderwidth = 2, relief = "groove").place(x = 1069, y = 36)
## Linhas para impressão das equações balanceadas:
# Equação geral:
Label(frame3, text = "Princípio da conservação de massa", font = "Times 8 bold", fg = "black", bg = "grey75", borderwidth = 2, relief = "flat").place(x = 450, y = 64)
Label(frame3, text = "Entrada - Saída + Geração - Consumo = Acúmulo", font = "Times 7 bold italic", fg = "black", bg = "grey75", borderwidth = 2, relief = "flat").place(x = 451, y = 85)
# Células:
Label(frame3, text = "0 - 0 + Gerado - 0 = Acúmulo", font = "Times 8 bold italic", fg = "black", bg = "grey77", borderwidth = 2, relief = "flat").place(x = 684, y = 56)
Label(frame3, text = "Cx = conc. de células", font = "Times 8", fg = "black", bg = "grey77", borderwidth = 2, relief = "flat").place(x = 727, y = 77)
Label(frame3, text = u"\u03bc = taxa de crescimento", font = "Times 8", fg = "black", bg = "grey77").place(x = 727, y = 92)
image_dif(imagem = "Diferencial_cx.png", num_frame = frame3, x = 658, y = 77)
# Substrato:
Label(frame3, text = "0 - 0 + 0 - Consumo = Acúmulo", font = "Times 8 bold italic", fg = "black", bg = "grey79", borderwidth = 2, relief = "flat").place(x = 885, y = 56)
Label(frame3, text = "Cs = conc. de subst", font = "Times 8", fg = "black", bg = "grey79", borderwidth = 2, relief = "flat").place(x = 964, y = 77)
Label(frame3, text = "Yxs = coef. rendim", font = "Times 8", fg = "black", bg = "grey79", borderwidth = 2, relief = "flat").place(x = 964, y = 92)
image_dif(imagem = "Diferencial_cs.png", num_frame = frame3, x = 863, y = 77)
# Produto:
Label(frame3, text = "0 - 0 + Gerado - 0 = Acúmulo", font = "Times 8 bold italic", fg = "black", bg = "grey81", borderwidth = 2, relief = "flat").place(x = 1092, y = 56)
Label(frame3, text = u"\u03B1 e \u03B2 = coef. prod" , font = "Times 8", fg = "black", bg = "grey81", borderwidth = 2, relief = "flat").place(x = 1172, y = 92)
Label(frame3, text = "Cp = conc. de prod", font = "Times 8", fg = "black", bg = "grey81", borderwidth = 2, relief = "flat").place(x = 1172, y = 77)
image_dif(imagem = "Diferencial_cp.png", num_frame = frame3, x = 1069, y = 77)
## Textos para documentação
# Batelada:
Modulo_documentacao.caixa_texto_batelada(frame = frame3, altura = 5, largura = 56, x = 35, y = 30)
# Modelos Cinéticos:
Modulo_documentacao.caixa_texto_modelo_contois(frame = frame26, altura = 19, largura = 95, x = 4, y = 0)
Modulo_documentacao.caixa_texto_modelo_monod(frame = frame27, altura = 19, largura = 95, x = 4, y = 0)
Modulo_documentacao.caixa_texto_modelo_moser(frame = frame28, altura = 19, largura = 95, x = 4, y = 0)
Modulo_documentacao.caixa_texto_modelo_andrews(frame = frame29, altura = 19, largura = 95, x = 4, y = 0)
Modulo_documentacao.caixa_texto_modelo_wu(frame = frame30, altura = 19, largura = 95, x = 4, y = 0)
Modulo_documentacao.caixa_texto_modelo_aiba(frame = frame31, altura = 19, largura = 95, x = 4, y = 0)
Modulo_documentacao.caixa_texto_modelo_h_h(frame = frame32, altura = 19, largura = 95, x = 4, y = 0)
Modulo_documentacao.caixa_texto_modelo_levenspiel(frame = frame33, altura = 19, largura = 95, x = 4, y = 0)
Modulo_documentacao.caixa_texto_modelo_lee(frame = frame34, altura = 19, largura = 95, x = 4, y = 0)

 
# Função botôes gráficos - simulacao:
def botao_com_graf(frame, comando_salvar, comando_destroy):
      load = Image.open("Salvar_mod.png")
      render = ImageTk.PhotoImage(load)
      img = Button(frame, image = render, border = 0, command = comando_salvar)
      img.image = render
      img.place(x = 451, y = 80)
      load = Image.open("Lixeira_mod.png")
      render = ImageTk.PhotoImage(load)
      img = Button(frame, image = render, border = 0, command = comando_destroy)
      img.image = render
      img.place(x = 450, y = 176)

def botao_paleta_graf(frame,comando):
    load = Image.open("Paleta_mod.png")
    render = ImageTk.PhotoImage(load)
    img = Button(frame, image = render, border = 0, command = comando)
    img.image = render
    img.place(x = 450, y = 130)
    
    
                                    ## PARA A REALIZAÇÃO DA SIMULAÇÃO ##
# Importação módulos - simulação:
# Função com as equações modelo para integração numérica:
func_integ_Monod = Modulos_Monod.simul_bat_Monod()
func_integ_Contois = Modulos_Contois.simul_bat_Contois()
func_integ_Andrews = Modulos_Andrews.simul_bat_Andrews()
func_integ_Aiba_et_al = Modulos_Aiba_et_al.simul_bat_Aiba_et_al()
func_integ_Moser = Modulos_Moser.simul_bat_Moser()
func_integ_Hope_Hansford = Modulos_Hope_Hansford.simul_bat_Hope_Hansford()
func_integ_Wu_et_al = Modulos_Wu_et_al.simul_bat_Wu_et_al()
func_integ_Levenspiel = Modulos_Levenspiel.simul_bat_Levenspiel()
func_integ_Lee_et_al = Modulos_Lee_et_al.simul_bat_Lee_et_al()
list_funcs_integ = [func_integ_Monod, func_integ_Contois, func_integ_Andrews, func_integ_Aiba_et_al, func_integ_Moser, func_integ_Hope_Hansford, func_integ_Wu_et_al, func_integ_Levenspiel, func_integ_Lee_et_al]
    
                                ## PARA A REALIZAÇÃO DA MODELAGEM ##
# Importação módulos - modelagem:
# Função com as equações modelo com os parâmetros atribuídos a argumentos:
func_args_Monod = Modulos_Monod.modelag_bat_Monod_func_args()
func_args_Contois = Modulos_Contois.modelag_bat_Contois_func_args()
func_args_Andrews = Modulos_Andrews.modelag_bat_Andrews_func_args()
func_args_Aiba_et_al = Modulos_Aiba_et_al.modelag_bat_Aiba_et_al_func_args()
func_args_Moser = Modulos_Moser.modelag_bat_Moser_func_args()
func_args_Hope_Hansford = Modulos_Hope__Hansford.modelag_bat_Hope_Hansford_func_args()
func_args_Wu_et_al = Modulos_Wu_et_al.modelag_bat_Wu_et_al_func_args()
func_args_Levenspiel = Modulos_Levenspiel.modelag_bat_Levenspiel_func_args()
func_args_Lee_et_al = Modulos_Lee_et_al.modelag_bat_Lee_et_al_func_args()
func_args_mi_constante = Modulos_mi_constante.modelag_bat_mi_const_func_args()
list_funcs_args = [func_args_Monod, func_args_Contois, func_args_Andrews, func_args_Aiba_et_al, func_args_Moser, func_args_Hope_Hansford, func_args_Wu_et_al, func_args_Levenspiel, func_args_Lee_et_al, func_args_mi_constante]

# Módulo para atribuição do peso:
dpC = Modulo_peso_limite_AG.peso()

# Chutes iniciais para ajuste do parametro
limites_Monod = Modulo_peso_limite_AG.limites()[0]
limites_Contois = Modulo_peso_limite_AG.limites()[1]
limites_Andrews = Modulo_peso_limite_AG.limites()[3]
limites_Aiba_et_al = Modulo_peso_limite_AG.limites()[5]
limites_Moser = Modulo_peso_limite_AG.limites()[2]
limites_Hope_Hansford = Modulo_peso_limite_AG.limites()[4]
limites_Wu_et_al = Modulo_peso_limite_AG.limites()[6]
limites_Levenspiel = Modulo_peso_limite_AG.limites()[7]
limites_Lee_et_al = Modulo_peso_limite_AG.limites()[8]
limites_mi_constante = Modulo_peso_limite_AG.limites()[9]
list_limites = [limites_Monod, limites_Contois, limites_Andrews, limites_Aiba_et_al, limites_Moser, limites_Hope_Hansford, limites_Wu_et_al, limites_Levenspiel, limites_Lee_et_al, limites_mi_constante]


# Definição combobox - seleção da cinética:

## Simulação:
# Caixas de separação:
Label(frame1, text="", width = 52, height = 33, borderwidth = 3,  relief = "sunken", bg = "grey85").place(x = 914, y = 2)
Label(frame1, text="", width = 53, height = 33, borderwidth = 3,  relief = "sunken", bg = "grey85").place(x = 10, y = 2)
def caixa_equa_simul():
    Label(frame1, text="", width = 47, height = 19, borderwidth = 5,  relief = "sunken", bg = "grey65").place(x = 920, y = 130)
ttk.Label(frame1, text = "SELECIONE A CINÉTICA DE REAÇÃO:", font = "times 12 bold").place(x = 16, y = 10)
v_1 = ("AUSÊNCIA DE INIBIÇÃO", "INIBIÇÃO PELO SUBSTRATO", "INIBIÇÃO PELO PRODUTO", "INIBIÇÃO PELA BIOMASSA", "CINÉTICA CONSTANTE")
combo_1 = Combobox(frame1, values = v_1, width = 39, font = "arial 10")
combo_1.set("-----------------------ESCOLHA-----------------------")
combo_1.place(x = 15, y = 32)
caixa_equa_simul()
     

                                                 ## MODELAGEM ##
# Caixas de separação:
Label(frame2, text="", width = 53, height = 33, borderwidth = 3,  relief = "sunken", bg = "grey85").place(x = 10, y = 2)
ttk.Label(frame2, text = "SELECIONE A CINÉTICA DE REAÇÃO:", font = "times 12 bold").place(x = 16, y = 10)
# Combobox:
v_2 = ("AUSÊNCIA DE INIBIÇÃO", "INIBIÇÃO PELO SUBSTRATO", "INIBIÇÃO PELO PRODUTO", "INIBIÇÃO PELA BIOMASSA", "CINÉTICA CONSTANTE")
combo_2 = Combobox(frame2, values = v_2, width = 39, font = "arial 10")
combo_2.set("-----------------------ESCOLHA-----------------------")
combo_2.place(x = 15, y = 32)


# Saídas:
Label(frame2, text="", width = 52, height = 33, borderwidth = 3,  relief = "sunken", bg = "grey85").place(x = 914, y = 2)
Label(frame2, text="", width = 50, height = 16, borderwidth = 3,  relief = "sunken", bg = "grey75").place(x = 921, y = 201)
load = Image.open("Tabela.png")
render = ImageTk.PhotoImage(load)
img = Label(frame2, image = render, border = 0)
img.image = render
img.place(x = 930, y = 205)
load = Image.open("Tabela.png")
render = ImageTk.PhotoImage(load)
img = Label(frame2, image = render, border = 0)
img.image = render
img.place(x = 930, y = 366.2)
Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
Label(frame2, text = "b", font = "times 42", fg = "grey40", bg = "grey40", width = 3,borderwidth=4, relief ='sunken').place(x = 1160, y = 288.2)
Label(frame2, text = "F. Obj:", font = "broadway 11", fg = "white", bg = "black", justify = "center",  borderwidth=4, relief ='sunken').place(x = 1095, y = 297.2)
Label(frame2, text = u"R\u00b2:", font = "broadway 11", fg = "white", bg = "black", justify = "center",  borderwidth=4, relief ='sunken').place(x = 1124, y = 327.2)
load = Image.open("Cronometro_mod.png")
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

# Caixa acesso arquivos e equações:
def aces_arq(frame):
    Label(frame, text = "", borderwidth=3, relief="groove", width = 33, height = 7, bg = "gray45").place(x = 1030, y = 7)
    Label(frame, text = "Acessar Arquivos", font = "arial 8 bold", fg = "white", bg = "black", borderwidth=4, relief="sunken").place(x = 1036, y = 13)
aces_arq(frame1)
aces_arq(frame2)
Label(frame1, text = "", borderwidth=4, relief="sunken", width = 65, height = 6, bg = "grey90").place(x = 431, y = 0)
Label(frame1, text = "Visualizar Equações", font = "arial 8 bold", fg = "white", bg = "black", borderwidth=4, relief="sunken").place(x = 436, y = 5)

# Caixa para plotagem dos gráficos:
def plot_graf(frame):
    Label(frame, text = "",  borderwidth=2.3, relief="ridge", width = 69, height = 22, bg = "white").place(x = 406, y = 115)

notebook_graf_simul()
notebook_graf_model()

# Função para impressão das equações e suas variáveis:
def equac_sai_contois():
    caixa_equa_simul()
    image(imagem = "Equacao_Contois_mod.png", num_frame = frame1, x = 1000, y = 212)
    Label(frame1, text = "CONTOIS", font = 'Batang 10 bold', fg = "black", bg = "white").place(x = 930, y = 140)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 304)
    tex_ksx = Label(frame1, text = u"KSX = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black",  bg = "grey65").place(x = 930, y = 334)
def equac_sai_monod():
    caixa_equa_simul()
    image(imagem = "Equacao_Monod_mod.png", num_frame = frame1, x = 1000, y = 212)
    Label(frame1, text = "MONOD", font = 'Batang 10 bold', fg = "black", bg = "white").place(x = 930, y = 140)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 304)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 334)
def equac_sai_moser():
    caixa_equa_simul()
    image(imagem = "Equacao_Moser_mod.png", num_frame = frame1, x = 1000, y = 212)
    Label(frame1, text = "MOSER", font = 'Batang 10 bold', fg = "black", bg = "white").place(x = 930, y = 140)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 304)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 334)
    tex_n = Label(frame1, text = "n = parâmetro expoente (adim)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 364)
def equac_sai_andrews(): 
    caixa_equa_simul()
    image(imagem = "Equacao_Andrews_mod.png", num_frame = frame1, x = 985, y = 212)
    Label(frame1, text = "ANDREWS", font = 'Batang 10 bold', fg = "black", bg = "white").place(x = 930, y = 140)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 304)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 334)
    tex_kis = Label(frame1, text = u"KIS = constante inibição por substrato (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 364)
def equac_sai_wu(): 
    caixa_equa_simul()
    image(imagem = "Equacao_Wu_mod.png", num_frame = frame1, x = 970, y = 212)
    Label(frame1, text = "WU ET AL", font = 'Batang 10 bold', fg = "black", bg = "white").place(x = 930, y = 140)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 304)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 334)
    tex_ke = Label(frame1, text = u"Ke = constante inibição por substrato (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 364)
    tex_v = Label(frame1, text = "v = parâmetro expoente (adim)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 394)
def equac_sai_aiba():
    caixa_equa_simul()
    image(imagem = "Equacao_Aiba_mod.png", num_frame = frame1, x = 970, y = 212) 
    Label(frame1, text = "AIBA ET AL", font = 'Batang 10 bold', fg = "black", bg = "white").place(x = 930, y = 140)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 304)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 334)
    tex_kp = Label(frame1, text = u"Kp = parâmetro expoente de inibição (volume.massa\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 364)  
def equac_sai_hh():
    caixa_equa_simul()      
    image(imagem = "Equacao_Hope_Hansford_mod.png", num_frame = frame1, x = 970, y = 212) 
    Label(frame1, text = "HOPE & HANSFORD", font = 'Batang 10 bold', fg = "black", bg = "white").place(x = 930, y = 140)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 304)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 334)
    tex_kp = Label(frame1, text = u"Kp = constante inibição por produto (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 364)               
def equac_sai_levenspiel():
    caixa_equa_simul()
    image(imagem = "Equacao_Levenspiel_mod.png", num_frame = frame1, x = 970, y = 212) 
    Label(frame1, text = "LEVENSPIEL", font = 'Batang 10 bold', fg = "black", bg = "white").place(x = 930, y = 140)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 304)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 334)
    tex_cpestr = Label(frame1, text = u"Cp* = concentração produto crítica (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 364)
    tex_n_lev = Label(frame1, text = "n = constante de Levenspiel (adim)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 394)   
def equac_sai_lee():  
    caixa_equa_simul()
    image(imagem = "Equacao_Lee_mod.png", num_frame = frame1, x = 970, y = 212) 
    Label(frame1, text = "LEE ET AL", font = 'Batang 10 bold', fg = "black", bg = "white").place(x = 930, y = 140)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 304)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 334)
    tex_cxestr = Label(frame1, text = u"Cx* = concentração celular crítica (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 364)
    tex_m = Label(frame1, text = "m = constante de Lee et al (adim)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 394)   
    
 # Criação botões para acesso às equações:
Button(frame1, text = "Contois", font = "Times 10 bold italic", fg = "black", bg = "white", command = equac_sai_contois).place(x = 546, y = 35)
Button(frame1, text = "Monod", font = "Times 10 bold italic", fg = "black", bg = "white", command = equac_sai_monod).place(x = 602, y = 35)
Button(frame1, text = "Moser", font = "Times 10 bold italic", fg = "black", bg = "white", command = equac_sai_moser).place(x = 655, y = 35)
Button(frame1, text = "Andrews", font = "Times 10 bold italic", fg = "black", bg = "white", command = equac_sai_andrews).place(x = 703, y = 35)
Button(frame1, text = "Wu et al", font = "Times 10 bold italic", fg = "black", bg = "white", command = equac_sai_wu).place(x = 764, y = 35)
Button(frame1, text = "Aiba et al", font = "Times 10 bold italic", fg = "black", bg = "white", command = equac_sai_aiba).place(x = 823, y = 35)
Button(frame1, text = "Hope & Hansford", font = "Times 10 bold italic", fg = "black", bg = "white", command = equac_sai_hh).place(x = 546, y = 65)
Button(frame1, text = "Levenspiel", font = "Times 10 bold italic", fg = "black", bg = "white", command = equac_sai_levenspiel).place(x = 657, y = 65)
Button(frame1, text = "Lee et al", font = "Times 10 bold italic", fg = "black", bg = "white", command = equac_sai_lee).place(x = 729, y = 65)  
    
    
# Programação da parte funcional do código - SIMULAÇÃO:
def simulacao(cont):
    # Vetor condição inicial:
    inic_cond_simul = [Cx0, Cs0, Cp0]
    print(inic_cond_simul)
    # Vetor tempo:
    t_simul = np.arange(t0,tf,0.1)
    print(t_simul)
    
    if cont == 0:
        def edos_int_bat_Monod(C,t):
            Cx,Cs,Cp=C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
        
            mi=mimax_sim*(Cs/(Ks_sim+Cs))
            dCxdt=(mi-Kd_sim)*Cx
            dCsdt=(-1/Yxs_sim)*mi*Cx
            dCpdt=alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim = odeint(edos_int_bat_Monod,inic_cond_simul,t_simul)
        print(C_sim)
    
    if cont == 1:
        def edos_int_bat_Contois(C,t):
            Cx,Cs,Cp=C
            mimax_sim = mimax
            KSX_sim = KSX
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
        
            mi=mimax_sim*(Cs/((KSX_sim*Cx)+Cs))
            dCxdt=(mi-Kd_sim)*Cx
            dCsdt=(-1/Yxs_sim)*mi*Cx
            dCpdt=alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim = odeint(edos_int_bat_Contois,inic_cond_simul,t_simul)
        print(C_sim)
        
    if cont == 2:
        def edos_int_bat_Andrews(C,t):
            Cx,Cs,Cp=C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
            KIS_sim = KIS
    
            mi=mimax_sim*(Cs/(Ks_sim+Cs+((Cs**2)/KIS_sim)))
            dCxdt=(mi-Kd_sim)*Cx
            dCsdt=(-1/Yxs_sim)*mi*Cx
            dCpdt=alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim = odeint(edos_int_bat_Andrews,inic_cond_simul,t_simul)
        print(C_sim)
        
    if cont == 3:
        def edos_int_bat_Aiba_et_al(C,t):
            Cx,Cs,Cp=C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
            Kp_aiba_sim = Kp_aiba
    
            mult_exp = -Cp*Kp_aiba_sim
            mi=mimax_sim*((Cs/(Ks_sim+Cs))*math.exp(mult_exp))
            dCxdt=(mi-Kd_sim)*Cx
            dCsdt=(-1/Yxs_sim)*mi*Cx
            dCpdt=alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim = odeint(edos_int_bat_Aiba_et_al,inic_cond_simul,t_simul)
        print(C_sim)
        
    if cont == 4:
        def edos_int_bat_Moser(C,t):
            Cx,Cs,Cp=C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
            u_sim = u
        
            mi=mimax_sim*(((Cs)**u_sim)/(Ks_sim+((Cs)**u_sim)))
            dCxdt=(mi-Kd_sim)*Cx
            dCsdt=(-1/Yxs_sim)*mi*Cx
            dCpdt=alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim = odeint(edos_int_bat_Moser,inic_cond_simul,t_simul)
        print(C_sim)
        
    if cont == 5:
        def edos_int_bat_Hope_Hansford(C,t):
            Cx,Cs,Cp=C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
            Kp_hope_sim = Kp_hh

            mi=mimax_sim*(Cs/(Ks_sim+Cs))*(Kp_hope_sim/(Kp_hope_sim+Cp))
            dCxdt=(mi-Kd_sim)*Cx
            dCsdt=(-1/Yxs_sim)*mi*Cx
            dCpdt=alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim = odeint(edos_int_bat_Hope_Hansford,inic_cond_simul,t_simul)
        print(C_sim)
        
    if cont == 6:
        def edos_int_bat_Wu_et_al(C,t):
            Cx,Cs,Cp=C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
            Ke_sim = Ke
            v_sim = v

            mi = mimax_sim * (Cs/(Ks_sim + Cs + Cs*((Cs/Ke_sim)**v_sim)))
            dCxdt=(mi-Kd_sim)*Cx
            dCsdt=(-1/Yxs_sim)*mi*Cx
            dCpdt=alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim = odeint(edos_int_bat_Wu_et_al,inic_cond_simul,t_simul)
        print(C_sim)
    
    if cont == 7:
        def edos_int_bat_Levenspiel(C,t):
            Cx,Cs,Cp=C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
            Cp_estr_sim = Cp_estr
            n_sim = n
        
            mi=mimax_sim*((Cs/(Ks_sim+Cs))*((1-(Cp/Cp_estr_sim))**n_sim))
            dCxdt=(mi-Kd_sim)*Cx
            dCsdt=(-1/Yxs_sim)*mi*Cx
            dCpdt=alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim = odeint(edos_int_bat_Levenspiel,inic_cond_simul,t_simul)
        print(C_sim)

    if cont == 8:
        def edos_int_bat_Lee_et_al(C,t):
            Cx,Cs,Cp=C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
            Cx_estr_sim = Cx_estr
            m_sim = m
        
            mi=mimax_sim*((Cs/(Ks_sim+Cs))*((1-(Cx/Cx_estr_sim))**m_sim))
            dCxdt=(mi-Kd_sim)*Cx
            dCsdt=(-1/Yxs_sim)*mi*Cx
            dCpdt=alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim = odeint(edos_int_bat_Lee_et_al,inic_cond_simul,t_simul)
        print(C_sim)

    # Gráfico - perfil de concentração:       
    x = "red"
    p = "green"
    s = "blue"
    def imprimir_perfil_concentracao_model_otim_exp (t_m, Cx_m, Cs_m, Cp_m):
        f = plt.figure(figsize=(8,6), dpi = 54) 
        plot = f.add_subplot(111) 
        lns1 = plot.plot(t_m ,Cx_m, color = x, linewidth=3,label='Cx modelo')
        lns2 = plot.plot(t_m,Cp_m, linestyle="--", color=p,linewidth=3,label='Cp modelo')
        ax2 = plot.twinx()
        lns3 = ax2.plot(t_m,Cs_m,linestyle=":", color=s,linewidth=3,label='Cs modelo') 
        plot.set_xlabel('Tempo de cultivo (h)',weight='bold')               
        plot.set_ylabel('Cx e Cp (g/L)', weight='bold')
        ax2.set_ylabel('Cs (g/L)', weight='bold') 
        lns = lns1+lns2+lns3
        labs = [l.get_label() for l in lns]
        plot.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.12),ncol=3, fancybox=True, shadow=True)                                                
        plot.grid(True)
        f.patch.set_facecolor('white')                                   
        plt.style.use('default')
        canvas = FigureCanvasTkAgg(f, frame22)
        a = canvas.get_tk_widget().place(x = 0, y = 0)
        def salvar_concent():
            a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
            defaultextension='.png')
            plt.savefig(a)
        botao_com_graf(frame = frame22, comando_salvar = lambda : salvar_concent(), comando_destroy = canvas.get_tk_widget().destroy)
    imprimir_perfil_concentracao_model_otim_exp(t_simul, C_sim[:,0], C_sim[:,1], C_sim[:,2])
    
    def graf_cor (x,p,s): 
        f = plt.figure(figsize=(8,6), dpi = 54) 
        plot = f.add_subplot(111) 
        lns1 = plot.plot(t_simul ,C_sim[:,0], color = x, linewidth=3,label='Cx modelo')
        lns2 = plot.plot(t_simul,C_sim[:,2], linestyle="--", color=p,linewidth=3,label='Cp modelo')
        ax2 = plot.twinx()
        lns3 = ax2.plot(t_simul,C_sim[:,1],linestyle=":", color=s,linewidth=3,label='Cs modelo') 
        plot.set_xlabel('Tempo de cultivo (h)',weight='bold')               
        plot.set_ylabel('Cx e Cp (g/L)', weight='bold')
        ax2.set_ylabel('Cs (g/L)', weight='bold') 
        lns = lns1+lns2+lns3
        labs = [l.get_label() for l in lns]
        plot.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.12),ncol=3, fancybox=True, shadow=True)                                                
        plot.grid(True)
        f.patch.set_facecolor('white')                                   
        plt.style.use('default')
        canvas = FigureCanvasTkAgg(f, frame22)
        a = canvas.get_tk_widget().place(x = 0, y = 0)
        def salvar():
            a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
            defaultextension='.png')
            plt.savefig(a)
        botao_com_graf(frame = frame22, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
        
    ## Escolha das cores:
    def seletor_cores():
        cor = colorchooser.askcolor(title = "Editar cores")
        return(cor[1])
    def cores_cx():
        global cor_x
        cor_x = colorchooser.askcolor(title ="Editar cores")
        cor_x = cor_x[1]
        fig = graf_cor (x = cor_x, p = "green", s = "blue")
        Button(frame22, text = "Cs", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cs).place(x = 460, y = 255) 
    def cores_cs():
        global cor_s
        cor_s = colorchooser.askcolor(title ="Editar cores")
        cor_s = cor_s[1]
        fig = graf_cor (x = cor_x, p = "green", s = cor_s)
        Button(frame22, text = "Cs", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cs).place(x = 460, y = 255)
        Button(frame22, text = "Cp", bg = "gray40", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cp).place(x = 460, y = 280)  
    def cores_cp():
        global cor_p
        cor_p = colorchooser.askcolor(title ="Editar cores")
        cor_p = cor_p[1] 
        fig = graf_cor (x = cor_x, p = cor_p, s = cor_s)
        Button(frame22, text = "Cp", bg = "gray40", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cp).place(x = 460, y = 280)
    def cores_concent():
        Button(frame22, text = "Cx", bg = "gray60", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cx).place(x = 460, y = 230)
        botao_paleta(frame = frame22, comando = cores_concent)
    
    botao_paleta_graf(frame = frame22, comando = cores_concent)
   
    # Cálculo produtividade - células e produto:
    Px = C_sim[1:,0]/t_simul[1:]
    Px[Px<0] = 0 # Se o valor é menor que 0 é substituido por 0
    Pp = C_sim[1:,2]/t_simul[1:]
    Pp[Pp<0] = 0 # Se o valor é menor que 0 é substituido por 0
    # Gráfico - produtividade:
    def graf_produtiv(px, pp):
        def imprimir_produtividade_celular_produto(t_m,Px_m, Pp_m):
            f = plt.figure(figsize=(8,6), dpi = 54) 
            plot = f.add_subplot(111)  
            lns1 = plot.plot(t_m ,Px_m,color = px,linewidth=3,label='Produtividade Celular')
            ax2 = plot.twinx()
            lns2 = ax2.plot(t_m,Pp_m,linestyle=":", color = pp,linewidth=3,label='Produtividade do Produto') 
            plot.set_xlabel('Tempo de cultivo (h)',weight='bold')               
            plot.set_ylabel('Produtividade Celular (g/L.h)', weight='bold')
            ax2.set_ylabel('Produtividade Produto (g/L.h)', weight='bold') 
            lns = lns1+lns2
            labs = [l.get_label() for l in lns]
            plot.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.12),ncol=2, fancybox=True, shadow=True )                                                
            plot.grid(True)
            f.patch.set_facecolor('white')                                   
            plt.style.use('default')    
            canvas = FigureCanvasTkAgg(f, frame23)
            a = canvas.get_tk_widget().place(x = 0, y = 0)
            def salvar():
                a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                defaultextension='.png')
                plt.savefig(a)
            botao_com_graf(frame = frame23, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
        imprimir_produtividade_celular_produto(t_simul[1:],Px, Pp)
        
        
    ## Escolha das cores:
    def seletor_cores():
        cor = colorchooser.askcolor(title = "Editar cores")
        return(cor[1])
    def cores_px():
        global cor_px
        cor_px = colorchooser.askcolor(title ="Editar cores")
        cor_px = cor_px[1]
        fig = graf_produtiv(px = cor_px, pp = "green")
        Button(frame23, text = "Pp", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_pp).place(x = 460, y = 255)   
    def cores_pp():
        global cor_pp
        cor_pp = colorchooser.askcolor(title ="Editar cores")
        cor_pp = cor_pp[1]
        fig = graf_produtiv(px = cor_px, pp = cor_pp)
        Button(frame23, text = "Pp", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_pp).place(x = 460, y = 255)
    def cores_produtiv():
        Button(frame23, text = "Px", bg = "gray60", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_px).place(x = 460, y = 230)    
       
    # Geração do gráfico:
    graf_produtiv(px = "red", pp = "green")
    ## Botão para seleção das cores:
    botao_paleta_graf(frame23, comando = cores_produtiv)
    
    # Cálculo produtivida específica:
    Ppx=C_sim[:,2]*(1/C_sim[:,0])
    Ppx[Ppx<0] = 0
    # Gráfico produtividade específica:
    def graf_produtiv_espec(Ppx_cor):
        def imprimir_produtividade_especifica_model_otim_exp (t_m, Ppx_m):
            f = plt.figure(figsize=(8,6), dpi = 54) 
            plot = f.add_subplot(111)  
            plt.plot(t_m,Ppx_m,color = Ppx_cor,linewidth=3, label='Simulado')
            plt.xlabel('Tempo de cultivo (h)',weight='bold')               
            plt.ylabel('Produtividade Específica (gp/gx)', weight='bold')
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08),ncol=2, fancybox=True, shadow=True )
            plt.grid(True)  
            f.patch.set_facecolor('white')                                   
            plt.style.use('default')                       
            canvas = FigureCanvasTkAgg(f, frame24)
            a = canvas.get_tk_widget().place(x = 0, y = 0)
            def salvar():
                a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                defaultextension='.png')
                plt.savefig(a)
            botao_com_graf(frame = frame24, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
        imprimir_produtividade_especifica_model_otim_exp(t_simul, Ppx)
        
    ## Escolha das cores:
    def seletor_cores_Ppx():
        cor_Ppx = colorchooser.askcolor(title ="Editar cores")
        cor_Ppx = cor_Ppx[1]
        graf_produtiv_espec(Ppx_cor = cor_Ppx)
        
    graf_produtiv_espec(Ppx_cor = "red")
    ## Botão para seleção das cores:
    botao_paleta_graf(frame24, comando = seletor_cores_Ppx) 
  
    # Cálculo taxa mi:
    if cont == 0:
        mi = mimax*(C_sim[:,1]/(Ks+C_sim[:,1]))
    if cont == 1:
        mi = mimax*(C_sim[:,1]/(KSX*C_sim[:,0]+C_sim[:,1]))
    if cont == 2:
        mi = mimax*(C_sim[:,1]/(Ks+ C_sim[:,1] + ((C_sim[:,1]**2)/KIS)))
    if cont == 3:
        mult = -Kp_aiba*C_sim[:,2]
        mi = mimax*((C_sim[:,1]/(Ks+C_sim[:,1]))*np.exp(mult))
    if cont == 4:
        mi = mimax*((C_sim[:,1]**u)/(Ks+(C_sim[:,1]**u)))
    if cont == 5:
        mi = mimax*(C_sim[:,1]/(Ks+C_sim[:,1]))*(Kp_hh/(Kp_hh+C_sim[:,2]))
    if cont == 6:
        mi = mimax*(C_sim[:,1]/(Ks+C_sim[:,1]+(C_sim[:,1]*((C_sim[:,1]/Ke)**v))))
    if cont == 7:
        mi = mimax*((C_sim[:,1]/(Ks+C_sim[:,1]))*((1-(C_sim[:,2]/Cp_estr))**n))
    if cont == 8:
        mi = mimax*((C_sim[:,1]/(Ks+C_sim[:,1]))*((1-(C_sim[:,2]/Cx_estr))**m))
    mi[mi<0] = 0
    # Gráfico - velocidade de crescimento microbiano:
    def graf_mi(mi_cor):
        def imprimir_taxa_especifica_crescimento (t_m,  mi_m):
            f = plt.figure(figsize=(8,6), dpi = 54) 
            plot = f.add_subplot(111)                                             
            plt.plot(t_m,mi_m,color = mi_cor,linewidth=3, label='Simulado')
            plt.xlabel('Tempo de cultivo (h)',weight='bold')               
            plt.ylabel('Taxa específica de crescimento', weight='bold')
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08),ncol=2, fancybox=True, shadow=True )  
            plt.grid(True)  
            f.patch.set_facecolor('white')                                   
            plt.style.use('default')   
            canvas = FigureCanvasTkAgg(f, frame25)
            a = canvas.get_tk_widget().place(x = 0, y = 0)
            def salvar():
                a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                defaultextension='.png')
                plt.savefig(a)  
            botao_com_graf(frame = frame25, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
        imprimir_taxa_especifica_crescimento(t_simul, mi)
           
    ## Escolha das cores:
    def seletor_cores_mi():
        cor_mi = colorchooser.askcolor(title ="Editar cores")
        cor_mi = cor_mi[1]
        graf_mi(mi_cor = cor_mi)
        
    graf_mi(mi_cor = "red")
    ## Botão para seleção das cores:
    botao_paleta_graf(frame25, comando = seletor_cores_mi)

    # # Inserindo 0 para o primeiro valor de produtividade:
    Px_ad = np.insert(Px,0,Px[0])
    Pp_ad = np.insert(Pp,0,Pp[0])
        
    # Saída .xlsx - concentração, produtividade e taxa de crescimento:
    def excel_concent():
        df_sai_simul = pd.DataFrame({'Tempo(h)': t_simul, 'Cx(g/L)': C_sim[:,0], 'Cs(g/L)': C_sim[:,1], 'Cp(g/L)': C_sim[:,2], 'Px(g/L)': Px_ad, 'Pp(g/L)': Pp_ad, 'Ppx(g/L)': Ppx, 'mi(h-¹)': mi})
        with pd.ExcelWriter('Simulacao_Concent_Produt_mi.xlsx') as writer:
            df_sai_simul.to_excel(writer, sheet_name="Saida_simulada")
            writer.save()
        os.system("start EXCEL Simulacao_Concent_Produt_mi.xlsx")
    Label(frame1, text = "Simulacao_Concent_Produt_mi.xlsx", font = "arial 8 italic", fg = "black", bg = "gray45").place(x = 1072, y = 63)
    
    # Função botão acesso excel:
    def botao_excel(imagem, num_frame, x, y):
        load = Image.open(imagem)
        render = ImageTk.PhotoImage(load)
        img = Button(num_frame, image = render, border = 0, command = excel_concent)
        img.image = render
        img.place(x = x, y = y)
    
    # Botão de acesso - arquivo .xlsx - parâmetros cinéticos:
    botao_excel(imagem = "Excel.png", num_frame = frame1, x = 1036, y = 55)
    
    
# FIM DA SIMULAÇÃO #    
    

# Programação da parte funcional do código - MODELAGEM: 
def explorer():
    explorador = askopenfilename()
    nome_arquivo = os.path.basename(explorador)
    Label(frame2,text=nome_arquivo,font="arial 8 bold", fg="black", borderwidth=2, relief="ridge", justify = "center", width = 40).place(x = 500, y = 50)
    # Captura dos dados de entrada - formato dataframe:
    excel_entrada = pd.read_excel(nome_arquivo)
    excel_entrada_np = excel_entrada.values
    # Separação - t_exp e C_exp a partir do df:
    t_exp = excel_entrada_np[:,1]
    print(t_exp)
    C_exp = abs(excel_entrada_np[:,2:5])
    print(C_exp)
    # Vetor tempo modelo:
    t = np.arange(0, max(t_exp + 0.1), 0.1)
    print(t)
    # Captura dos valores de C_exp iniciais:
    cond_inic = [C_exp[0,0], C_exp[0,1], C_exp[0,2]]
    print(cond_inic)
    print(nome_arquivo)

    def modelagem(cont_model):
        start = time.time()
        def func_ob_ag(parametros, *dados):
            # mimax, ks, alfa, Yxs, beta, kd = parametros
            t_exp,C_exp = dados
            p = tuple(parametros)
            C_sim = odeint(list_funcs_args[cont_model], cond_inic, t_exp, args = p)
            res = C_sim - C_exp
            for i in range(0,3):
                res[:,i] = res[:,i]/dpC[i]
            res = res.flatten()
            res = sum(res**2)
            return (res)
        
        def func_ob_alm(p):
            p=tuple(p)
            C_sim=odeint(list_funcs_args[cont_model],cond_inic,t_exp,args=p)
            res=C_sim-C_exp
            for i in range(0,3):
                res[:,i]=res[:,i]/dpC[i]
            return res.flatten()
        
        args = (t_exp,C_exp)
        resultado_ag = differential_evolution(func_ob_ag, list_limites[cont_model], args=args, popsize=5,  tol=0.01, mutation=(0.5, 1), recombination=0.7, updating='immediate')
        resultado_ag = resultado_ag.x
        resultado_ag = tuple(resultado_ag)
        
        lance_inic = [resultado_ag]
        resultado_alm = leastsq(func_ob_alm,lance_inic, args=(), Dfun=None, full_output=1)
          
        # Parada contagem do tempo:
        end = time.time()
        elapsed = end - start
        elapsed = round(elapsed,3)
        
        param_otim_alm = resultado_alm[0].round(3)
        param_otim_alm = tuple(param_otim_alm)
        
        # Cálculo do intervalo de confiança:
        res_otimo =resultado_alm[2]['fvec']
        sensT_otimo =resultado_alm[2]['fjac']
        npar = len(sensT_otimo[:,1])
        ndata = len(sensT_otimo[1,:])
        invXtX=np.linalg.inv(np.matmul(sensT_otimo,sensT_otimo.transpose()))
        sig2y= sum(res_otimo**2) / (ndata-npar)
        covparamers = invXtX*sig2y
        EPpar = np.sqrt(covparamers.diagonal())
        ICpar = EPpar*sc.t.interval(.95, ndata-npar, loc=0, scale=1)[1]
        ICpar = ICpar.round(3)
        print(ICpar)
        
         # Definição saída dos valores modelados na interface:
        Label(frame2, bg = "grey75", height = 1, width = 41).place(x = 960, y = 258)
        Label(frame2, bg = "grey75", height = 1, width = 41).place(x = 960, y = 417)
        if cont_model == 0 or cont_model == 1:
            Label(frame2, text = param_otim_alm[0], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 943, y = 258)
            Label(frame2, text = param_otim_alm[1], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1021, y = 258)
        else:
            if cont_model >=2 and cont_model <=5:
                Label(frame2, text = param_otim_alm[0], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 943, y = 258)
                Label(frame2, text = param_otim_alm[1], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1021, y = 258)
                Label(frame2, text = param_otim_alm[6], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1099, y = 258)
            else:
                Label(frame2, text = param_otim_alm[0], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 943, y = 258)
                Label(frame2, text = param_otim_alm[1], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1021, y = 258)
                Label(frame2, text = param_otim_alm[6], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1099, y = 258)
                Label(frame2, text = param_otim_alm[7], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1163, y = 258)       
        Label(frame2, text = param_otim_alm[2] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 934, y = 417)
        Label(frame2, text = param_otim_alm[3] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1000, y = 417)
        Label(frame2, text = param_otim_alm[4] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1090, y = 417)
        Label(frame2, text = param_otim_alm[5] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1170, y = 417)
       
        # Condições para marcação dos valores inadequados modelados:
        cond_mimax =  param_otim_alm[0] > 0.9 
        cond_Ks = param_otim_alm[1] >= C_exp[0,1] or param_otim_alm[1] == 0 
        cond_yxs = param_otim_alm[3] >= C_exp[0,1]
        cond_mi_kd = param_otim_alm[2] > param_otim_alm[0]
        # Checagem parâmetros negativos:
        cond_param_neg = False
        for i in range (len(param_otim_alm)):
            if param_otim_alm[i] < 0:
                cond_param_neg = True   
                
        if (cond_mimax or cond_Ks or cond_mi_kd or cond_param_neg == True):
            # Som de alerta:
            duration = 1000  # milliseconds
            freq = 440  # Hz
            winsound.Beep(freq, duration)
            # Botão pisca - pisca
            flash_delay = 500  
            flash_colours = ('red4', 'black') 
            def flashColour(object, colour_index):
                global button_flashing
                button_flashing = True
                if button_flashing:
                    object.config(background = flash_colours[colour_index])
                    janela.after(flash_delay, flashColour, object, 1 - colour_index)
                else:
                    object.config(background = flash_colours[0])
            def buttonCallback(self):
                global button_flashing
                button_flashing = True
                #button_flashing = not button_flashing
                if button_flashing:
                    self.config(text = 'Inadequação de parâmetros', font="Times 11 bold italic", width = 20, fg = "white")
                    flashColour(self, 0)
                    if cond_mimax:
                        Label(frame2, text = param_otim_alm[0], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey75").place(x = 943, y = 258)
                    if cond_Ks:
                        Label(frame2, text = param_otim_alm[1], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey75").place(x = 1021, y = 258)
                    if cond_yxs:
                        Label(frame2, text = param_otim_alm[3] , font = "batang 10 bold", fg = "red4", bg = "grey75", justify = "center").place(x = 1000, y = 417)
                    if cond_mi_kd:
                        Label(frame2, text = param_otim_alm[2] , font = "batang 10 bold", fg = "red4", bg = "grey75", justify = "center").place(x = 934, y = 417)
                    if cond_param_neg == True:
                        if param_otim_alm[0] <= 0: #mimaximo
                            Label(frame2, text = param_otim_alm[0], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey75").place(x = 943, y = 258)
                        if param_otim_alm[1] <= 0: #Ks
                            Label(frame2, text = param_otim_alm[1], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey75").place(x = 1021, y = 258)
                        if param_otim_alm[2] < 0 or cond_mi_kd: #Kd
                            Label(frame2, text = param_otim_alm[2] , font = "batang 10 bold", fg = "red4", bg = "grey75", justify = "center").place(x = 934, y = 417)
                        if (param_otim_alm[3] <= 0 or cond_yxs): #Yxs
                            Label(frame2, text = param_otim_alm[3] , font = "batang 10 bold", fg = "red4", bg = "grey75", justify = "center").place(x = 1000, y = 417)
                        if param_otim_alm[4] <= 0: #alfa
                            Label(frame2, text = param_otim_alm[4] , font = "batang 10 bold bold", fg = "red4", bg = "grey75", justify = "center").place(x = 1090, y = 417)
                        if param_otim_alm[5] < 0: #beta
                            Label(frame2, text = param_otim_alm[5] , font = "batang 10 bold", fg = "red4", bg = "grey75", justify = "center").place(x = 1170, y = 417)
                        if cont_model == 2:
                            if param_otim_alm[6] > 55:
                                Label(frame2, text = param_otim_alm[6], font = "batang 10 bold", justify = "center", fg = "red4", bg = "gre75y").place(x = 1099, y = 258)
                        if cont_model >= 3 and cont_model <=5 :
                            if (param_otim_alm[6] <= 0 or param_otim_alm[6] > 10):
                                Label(frame2, text = param_otim_alm[6], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey75").place(x = 1099, y = 258)
                        if cont_model >= 6 and cont_model <=8:
                            if param_otim_alm[6] <= 0:
                                Label(frame2, text = param_otim_alm[6], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey75").place(x = 1142, y = 258)
                            if param_otim_alm[7] <= 0:
                                Label(frame2, text = param_otim_alm[7], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey75").place(x = 1163, y = 258)
                else:
                    self.config(text = 'Press to start flashing', font="Times 12 bold italic",
                    background = flash_colours[0])

            my_button = Button(frame2, text = 'Exibir análise cinética',font = "Times 12 bold italic", fg = "white", borderwidth=4, relief="groove", width = 20,background = flash_colours[0],command = lambda:buttonCallback(my_button))
            my_button.place(x = 921, y = 161)
         
        else:
            my_button = Label(frame2, bg = "grey85", borderwidth=7.5, relief="flat", height = 2, width = 28).place(x = 921, y = 150)
           
            
        # Janela para acesso aos valores de Intervalo de Confiança:
        def int_conf():
            janela_interna = Tk()
            janela_interna.title("Intervalo de Confiança")
            janela_interna.geometry("400x200")
            janela_interna.configure(bg = "gray50")
            Label(janela_interna, text = "", font = "Times 32", bd = 4, relief = "sunken", width = 15, height = 2).place(x = 14, y = 32)
            def balan_massa():
                Label(janela_interna, text = "", font = "Times 32", bd = 4, relief = "sunken", width = 15, height = 2).place(x = 14, y = 32)
                Botao_bm = Button(janela_interna, text = "Balanço de massa", font = "arial 8 bold", fg = "white", bg = "gray20", command = balan_massa).place(x = 25, y = 20)
                Botao_mi = Button(janela_interna, text = u"Equação \u03bc", font = "arial 8 bold", fg = "white", bg = "gray20", command = mi).place(x = 140, y = 20)
                Label(janela_interna, text = u"Kd(±h\u207b\u00b9)    Yxs(±gx.gs\u207b\u00b9)    \u03B1(±gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "white", width = 42, height = 1).place(x = 29, y = 67)
                Label(janela_interna,bg = "white", width = 48, height = 1).place(x = 29, y = 90)
                Label(janela_interna, text = ICpar[2], font = "batang 11", fg = "black", bg = "white").place(x = 32, y = 90)
                Label(janela_interna, text = ICpar[3], font = "batang 11", fg = "black", bg = "white").place(x = 113, y = 90)
                Label(janela_interna, text = ICpar[4], font = "batang 11", fg = "black", bg = "white").place(x = 207, y = 90)
                Label(janela_interna, text = ICpar[5], font = "batang 11", fg = "black", bg = "white").place(x = 300, y = 90)
            Botao_bm = Button(janela_interna, text = "Balanço de massa", font = "arial 8 bold", fg = "white", bg = "gray20", command = balan_massa).place(x = 25, y = 20)
            def mi():
                Label(janela_interna, text = "", font = "Times 32", bd = 4, relief = "sunken", width = 15, height = 2).place(x = 14, y = 32)
                Botao_bm = Button(janela_interna, text = "Balanço de massa", font = "arial 8 bold", fg = "white", bg = "gray20", command = balan_massa).place(x = 25, y = 20)
                Botao_mi = Button(janela_interna, text = u"Equação \u03bc", font = "arial 8 bold", fg = "white", bg = "gray20", command = mi).place(x = 140, y = 20)
                Label(janela_interna,bg = "white", width = 48, height = 1).place(x = 29, y = 90)
                if (cont_model == 0 or cont_model == 1): #Monod e Contois
                    if (cont_model == 0): #Monod
                         Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)     Ks(±g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "white", width = 42, justify = "left").place(x = 29, y = 67) 
                    if (cont_model == 1): #Contois
                         Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)     KSX(±g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "white", width = 42, justify = "left").place(x = 29, y = 67) 
                    Label(janela_interna, text = ICpar[0], font = "batang 11", fg = "black", bg = "white").place(x = 133, y = 90)
                    Label(janela_interna, text = ICpar[1], font = "batang 11", fg = "black", bg = "white").place(x = 220, y = 90)
                if (cont_model >=2 and cont_model <=5):
                    if (cont_model == 2): #Andrews
                        Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)      Ks(±g.L\u207b\u00b9)     KIS(±g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "white", width = 42).place(x = 29, y = 67)
                    if (cont_model == 4): #Moser
                        Label(janela_interna,  text = u"\u03bcmáx(±h\u207b\u00b9)     Ks(±g.L\u207b\u00b9)     u(±adim)", font = "arial 10 bold", fg = "black", bg = "white", width = 42).place(x = 29, y = 67)
                    if (cont_model == 3 or cont_model ==5): #Aiba e Hope
                        Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)     Ks(±g.L\u207b\u00b9)     Kp(±g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "white", width = 42).place(x = 29, y = 67)
                    Label(janela_interna, text = ICpar[0], font = "batang 11", fg = "black", bg = "white").place(x = 92, y = 90)
                    Label(janela_interna, text = ICpar[1], font = "batang 11", fg = "black", bg = "white").place(x = 182, y = 90)
                    Label(janela_interna, text = ICpar[6], font = "batang 11", fg = "black", bg = "white").place(x = 270, y = 90)
                if (cont_model >=5 and cont_model <=8):
                    if (cont_model == 6): #Wu
                        Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)     Ks(±g.L\u207b\u00b9)     KE(±g.L\u207b\u00b9)     v(±adim)", font = "arial 10 bold", fg = "black", bg = "white", width = 42).place(x = 29, y = 67)
                    if (cont_model == 7): #Levenspiel
                        Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)    Ks(±g.L\u207b\u00b9)     n(±adim)     Cp*(±g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "white",width = 42).place(x = 29, y = 67)
                    if (cont_model ==8): # Lee
                        Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)    Ks(±g.L\u207b\u00b9)     Cx*(±g.L\u207b\u00b9)     m(±adim)", font = "arial 10 bold", fg = "black", bg = "white",width = 42).place(x = 29, y = 67)
                    Label(janela_interna, text = ICpar[0], font = "batang 11",  fg = "black", bg = "white").place(x = 52, y = 90)
                    Label(janela_interna, text = ICpar[1], font = "batang 11",  fg = "black", bg = "white").place(x = 143, y = 90)
                    Label(janela_interna, text = ICpar[6], font = "batang 11", fg = "black", bg = "white").place(x = 226, y = 90)
                    Label(janela_interna, text = ICpar[7], font = "batang 11",  fg = "black", bg = "white").place(x = 304, y = 90)        
            Botao_mi = Button(janela_interna, text = u"Equação \u03bc", font = "arial 8 bold", fg = "white", bg = "gray20", command = mi).place(x = 140, y = 20)
            Button(janela_interna, text = "Voltar", font = "arial 9 bold", fg = "white", bg = "gray30", command = janela_interna.destroy).place(x = 174, y = 160)
            janela_interna.mainloop()
        Button(frame2, text = "Intervalo de Confiança", font = "times 8 bold", fg = "black", bg = "white", command = int_conf).place(x = 921, y = 451)
        
        # Impressão do tempo de ajuste na interface:
        Label(frame2, text = elapsed, font = "batang 11 italic", fg = "black", bg = "grey40").place(x = 1000, y = 318)
        
        # Impressão das saídas no console:
        print("\nTempo de ajuste AG-ALM para o modelo", cont_model,":",elapsed)
        print("Parametros equacionados pelo modelo",cont_model,":", param_otim_alm)
        
        # Integração numérica - pós modelagem:
        C_otim = odeint(list_funcs_args[cont_model], cond_inic, t, args = (param_otim_alm))
        
        # Cálculo do coeficiente de regressão: 
        df_concents= pd.DataFrame({'Tempo(h)': t, 'Cx(g/L)': C_otim[:,0], 'Cs(g/L)': C_otim[:,1], 'Cp(g/L)': C_otim[:,2]})
        df_concents_exp= pd.DataFrame({'Tempo_exp(h)': t_exp,'Cx_exp(g/L)': C_exp[:,0],'Cs_exp(g/L)': C_exp[:,1],'Cp_exp(g/L)': C_exp[:,2]})
        df_teste = pd.DataFrame({'Tempo(h)': t})
        df_teste_conc = pd.DataFrame({'Cx(g/L)': C_otim[:,0], 'Cs(g/L)': C_otim[:,1], 'Cp(g/L)': C_otim[:,2]})
        df_teste_exp = pd.DataFrame({'Tempo_exp(h)': t_exp})
        df_teste_exp_conc = pd.DataFrame({'Cx_exp(g/L)': C_exp[:,0],'Cs_exp(g/L)': C_exp[:,1],'Cp_exp(g/L)': C_exp[:,2]})

        # Teste: qual tempo tem o menor intervalo de divisão temporal
        control_compar = len(t)
   
        ## Laço para comparação de tempos iguais (experimental e modelo) 
        i_compar_exp = 0
        i_compar_model = 0
        temp_model=[]
        temp_exp=[]
        concent_model = []
        concent_exp = []
        while (i_compar_exp  < control_compar) and (i_compar_model < control_compar):
            exp_teste = df_teste_exp.at[i_compar_exp, 'Tempo_exp(h)']
            model_teste = df_teste.at[i_compar_model, 'Tempo(h)']
            dif = np.round(exp_teste - model_teste,decimals=1)
            if dif != 0:
                i_compar_model = 1 + i_compar_model
            else:
                temp_model.append(model_teste)
                temp_exp.append(exp_teste)
                df_temp_model = pd.DataFrame({"Tempo(h)": temp_model})
                df_temp_exp = pd.DataFrame({"Tempo_exp(h)": temp_exp})
                debitado_model = df_teste_conc.loc[i_compar_model]
                debitado_model = pd.Series(debitado_model).values
                debitado_exp = df_teste_exp_conc.loc[i_compar_exp]
                debitado_exp = pd.Series(debitado_exp).values
                df_conc_model = pd.DataFrame({'Cx(g/L)':[debitado_model[0]],'Cs(g/L)':[debitado_model[1]],'Cp(g/L)':[debitado_model[2]]})
                concent_model.append(df_conc_model)
                df_conc_exp = pd.DataFrame({'Cx_exp(g/L)':[debitado_exp[0]], 'Cs_exp(g/L)':[debitado_exp[1]], 'Cp_exp(g/L)':[debitado_exp[2]]})
                concent_exp.append(df_conc_exp)
                i_compar_model =  1 + i_compar_model
                i_compar_exp =  1 + i_compar_exp   

        df_concent_model = pd.concat(concent_model)
        df_concent_exp = pd.concat(concent_exp)
        df_concent_model.reset_index(drop=True, inplace=True)
        df_concent_exp.reset_index(drop=True, inplace=True)

        # Cálculo do coeficiente de regressão:
        med_conc = df_conc_exp.mean(axis=0)
        med_conc_val = pd.Series(med_conc).values
        df_med_conc = pd.DataFrame({'Cxexp_med(g/L)':[med_conc_val[0]], 'Csexp_med(g/L)':[med_conc_val[1]],'Cpexp_med(g/L)':[med_conc_val[2]]})

        df_saida_compar = pd.concat ([df_temp_exp,df_concent_exp, df_temp_model, df_concent_model,df_med_conc], axis=1)
        
        ## Determinação da soma do quadrado do resíduo:
        df_saida_compar['DQres_Cx'] = (df_concent_exp['Cx_exp(g/L)'] - df_concent_model['Cx(g/L)']) ** 2
        df_saida_compar['DQres_Cs'] = (df_concent_exp['Cs_exp(g/L)'] - df_concent_model['Cs(g/L)']) ** 2
        df_saida_compar['DQres_Cp'] = (df_concent_exp['Cp_exp(g/L)'] - df_concent_model['Cp(g/L)']) ** 2
    
        ## Determinação da soma do quadrado do resíduo:
        cx_med = np.repeat(med_conc_val[0],len(temp_exp))
        cs_med = np.repeat(med_conc_val[1],len(temp_exp))
        cp_med = np.repeat(med_conc_val[2],len(temp_exp))
        df_SQtotal_cx = pd.DataFrame ({'Cxexp_med(g/L)': cx_med, 'Csexp_med(g/L)': cs_med, 'Cpexp_med(g/L)': cp_med})
        df_saida_compar['DQtot_Cx'] = (df_concent_exp['Cx_exp(g/L)'] - df_SQtotal_cx['Cxexp_med(g/L)']) ** 2
        df_saida_compar['DQtot_Cs'] = (df_concent_exp['Cs_exp(g/L)'] - df_SQtotal_cx['Csexp_med(g/L)']) ** 2
        df_saida_compar['DQtot_Cp'] = (df_concent_exp['Cp_exp(g/L)'] - df_SQtotal_cx['Cpexp_med(g/L)']) ** 2
        ## Soma SQres e QStot: 
        soma_SQres_SQtot = df_saida_compar.sum(axis=0) #pegar 11,12,13,14,15 e 16
        soma_SQres_SQtot_val= pd.Series(soma_SQres_SQtot).values
        SQres = soma_SQres_SQtot_val[11] + soma_SQres_SQtot_val[12] + soma_SQres_SQtot_val[13]
        SQtotal = soma_SQres_SQtot_val[14] + soma_SQres_SQtot_val[15] + soma_SQres_SQtot_val[16]
        df_soma_SQres_SQtot = pd.DataFrame({'SQres':[SQres], 'SQtot':[SQtotal]})
        ## Cálculo do R²:
        r2 = 1 - (SQres/SQtotal)
        r2 = round(r2,4)
    
        # Impressão do valor do R² na interface:
        Label(frame2, text = r2, font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 329.2)
        
        # Gráfico - perfil de concentração:       
        x = "red"
        p = "green"
        s = "blue"
        def imprimir_perfil_concentracao_model_otim_exp (t_ajus, t_m, Cx_ajus, Cs_ajus, Cp_ajus, Cx_m, Cs_m, Cp_m):
            f = plt.figure(figsize=(8,6), dpi = 54) 
            plot = f.add_subplot(111) 
            lns1 = plot.plot(t_m ,Cx_m, color = x, linewidth=3,label='Cx modelo')
            lns2 = plot.plot(t_ajus ,Cx_ajus,'o',color=x,markersize=6, label='Cx experimental')
            lns3 = plot.plot(t_m,Cp_m, linestyle="--", color=p,linewidth=3,label='Cp modelo')  
            lns4 = plot.plot(t_ajus ,Cp_ajus,'^',color = p, markersize=6,label='Cp experimental')
            ax2 = plot.twinx()
            lns5 = ax2.plot(t_m,Cs_m,linestyle=":", color=s,linewidth=3,label='Cs modelo') 
            lns6 = ax2.plot(t_ajus,Cs_ajus,'s',color=s, markersize=6,label='Cs experimental')
            plot.set_xlabel('Tempo de cultivo (h)',weight='bold')               
            plot.set_ylabel('Cx e Cp (g/L)', weight='bold')
            ax2.set_ylabel('Cs (g/L)', weight='bold') 
            lns = lns1+lns2+lns3+lns4+lns5+lns6
            labs = [l.get_label() for l in lns]
            plot.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.12),ncol=3, fancybox=True, shadow=True)                                                
            plot.grid(True)
            f.patch.set_facecolor('white')                                   
            plt.style.use('default')
            canvas = FigureCanvasTkAgg(f, frame37)
            a = canvas.get_tk_widget().place(x = 0, y = 0)
            def salvar():
                a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                defaultextension='.png')
                plt.savefig(a)
            botao_com_graf(frame = frame37, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
        imprimir_perfil_concentracao_model_otim_exp(t_exp, t, C_exp[:,0], C_exp[:,1], C_exp[:,2], C_otim[:,0], C_otim[:,1], C_otim[:,2])
        
        ## Gráfico para mudança de cor - perfil de concentração:
        def graf_cor (x,p,s): 
            f = plt.figure(figsize=(8,6), dpi = 54) 
            plot = f.add_subplot(111) 
            lns1 = plot.plot(t ,C_otim[:,0], color = x, linewidth=3,label='Cx modelo')
            lns2 = plot.plot(t_exp ,C_exp[:,0],'o',color=x,markersize=6, label='Cx experimental')
            lns3 = plot.plot(t,C_otim[:,2], linestyle="--", color=p,linewidth=3,label='Cp modelo')  
            lns4 = plot.plot(t_exp ,C_exp[:,2],'^',color = p, markersize=6,label='Cp experimental')
            ax2 = plot.twinx()
            lns5 = ax2.plot(t,C_otim[:,1],linestyle=":", color=s,linewidth=3,label='Cs modelo') 
            lns6 = ax2.plot(t_exp,C_exp[:,1],'s',color=s, markersize=6,label='Cs experimental')
            plot.set_xlabel('Tempo de cultivo (h)',weight='bold')               
            plot.set_ylabel('Cx e Cp (g/L)', weight='bold')
            ax2.set_ylabel('Cs (g/L)', weight='bold') 
            lns = lns1+lns2+lns3+lns4+lns5+lns6
            labs = [l.get_label() for l in lns]
            plot.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.12),ncol=3, fancybox=True, shadow=True )                                                
            plot.grid(True)
            f.patch.set_facecolor('white')                                   
            plt.style.use('default')
            canvas = FigureCanvasTkAgg(f, frame37)
            a = canvas.get_tk_widget().place(x = 0, y = 0)
            def salvar():
                a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                defaultextension='.png')
                plt.savefig(a)
            botao_com_graf(frame = frame37, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
        
       ## Escolha das cores:
        def seletor_cores():
            cor = colorchooser.askcolor(title = "Editar cores")
            return(cor[1])
        def cores_cx():
            global cor_x
            cor_x = colorchooser.askcolor(title ="Editar cores")
            cor_x = cor_x[1]
            fig = graf_cor (x = cor_x, p = "green", s = "blue")
            Button(frame37, text = "Cs", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cs).place(x = 460, y = 255) 
        def cores_cs():
            global cor_s
            cor_s = colorchooser.askcolor(title ="Editar cores")
            cor_s = cor_s[1]
            fig = graf_cor (x = cor_x, p = "green", s = cor_s)
            Button(frame37, text = "Cs", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cs).place(x = 460, y = 255)
            Button(frame37, text = "Cp", bg = "gray40", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cp).place(x = 460, y = 280)  
        def cores_cp():
            global cor_p
            cor_p = colorchooser.askcolor(title ="Editar cores")
            cor_p = cor_p[1] 
            fig = graf_cor (x = cor_x, p = cor_p, s = cor_s)
            Button(frame37, text = "Cp", bg = "gray40", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cp).place(x = 460, y = 280)
        def cores_concent():
            Button(frame37, text = "Cx", bg = "gray60", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cx).place(x = 460, y = 230)
            botao_paleta_graf(frame = frame37, comando = cores_concent)
        
        # Botão para mudança de cor:
        botao_paleta_graf(frame = frame37, comando = cores_concent)
        
        # Cálculo produtividade - células e produto:
        # Experimental: 
        Px_exp = C_exp[1:,0]/t_exp[1:] 
        Px_exp[Px_exp<0] = 0 # Se o valor é menor que 0 é substituido por 0
        # Modelada:
        Px = C_otim[1:,0]/t[1:]
        Px[Px<0] = 0 # Se o valor é menor que 0 é substituido por 0
        # Experimental:
        Pp_exp = C_exp[1:,2]/t_exp[1:]
        Pp_exp[Pp_exp<0] = 0 # Se o valor é menor que 0 é substituido por 0
        # Modelada:
        Pp = C_otim[1:,2]/t[1:]
        Pp[Pp<0] = 0 # Se o valor é menor que 0 é substituido por 0
        # Gráfico - produtividade:
        def graf_produtiv(px, pp):
            def imprimir_produtividade_celular_produto_model_otim_exp (t_ajus, t_m, Px_ajus, Pp_ajus, Px_m, Pp_m):
                f = plt.figure(figsize=(8,6), dpi = 54) 
                plot = f.add_subplot(111)  
                lns1 = plot.plot(t_m ,Px_m,color = px,linewidth=3,label='Produtividade Celular modelo')
                lns2 = plot.plot(t_ajus ,Px_ajus,'o',markersize=6, color = px, label='Produtividade Celular experimental')
                ax2 = plot.twinx()
                lns3 = ax2.plot(t_m,Pp_m,linestyle=":", color = pp,linewidth=3,label='Produtividade do Produto modelo') 
                lns4 = ax2.plot(t_ajus,Pp_ajus,'sb', markersize=6, color = pp,label='Produtividade do Produto experimental')
                plot.set_xlabel('Tempo de cultivo (h)',weight='bold')               
                plot.set_ylabel('Produtividade Celular (g/L.h)', weight='bold')
                ax2.set_ylabel('Produtividade Produto (g/L.h)', weight='bold') 
                lns = lns1+lns2+lns3+lns4
                labs = [l.get_label() for l in lns]
                plot.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.12),ncol=2, fancybox=True, shadow=True )                                                
                plot.grid(True)
                f.patch.set_facecolor('white')                                   
                plt.style.use('default')    
                canvas = FigureCanvasTkAgg(f, frame38)
                a = canvas.get_tk_widget().place(x = 0, y = 0)
                def salvar():
                    a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                    defaultextension='.png')
                    plt.savefig(a)
                botao_com_graf(frame = frame38, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
            imprimir_produtividade_celular_produto_model_otim_exp(t_exp[1:], t[1:],Px_exp, Pp_exp, Px, Pp)
            # Cálculo R²:
            df_Px_Pp = pd.DataFrame({'Tempo(h)':t[1:], 'Px(gx/t)': Px, 'Pp(gp/t)': Pp})
            df_t_exp = pd.DataFrame({'Tempo(h)': t_exp[1:]})
            df_Px_Pp_merge = df_Px_Pp.merge(df_t_exp, how = 'inner' ,indicator=False)
            df_Px_Pp_exp = pd.DataFrame({'Tempo_exp(h)':t_exp[1:], 'Px_exp(gx/t)': Px_exp, 'Pp_exp(gp/t)': Pp_exp})
            del df_Px_Pp_merge['Tempo(h)']
            del df_Px_Pp_exp['Tempo_exp(h)']
            df_Px_Pp_merge = df_Px_Pp_merge.values
            df_Px_Pp_exp = df_Px_Pp_exp.values
            resid = (df_Px_Pp_merge - df_Px_Pp_exp)**2
            resid = resid.flatten()
            resid = sum(resid)
            Px_medio = np.mean(df_Px_Pp_exp[:,0])
            Pp_medio = np.mean(df_Px_Pp_exp[:,1])
            Px_total = sum((df_Px_Pp_exp[:,0] - Px_medio)**2)
            Pp_total = sum((df_Px_Pp_exp[:,1] - Pp_medio)**2)
            Px_Pp_total = Px_total + Pp_total
            r2_Px_Pp = 1 - (resid/Px_Pp_total)
            Label(frame2, text = "", font = "batang 10",  bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            Label(frame2, text = r2_Px_Pp.round(4), font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 329.2)
        
        ## Escolha das cores:
        def seletor_cores():
            cor = colorchooser.askcolor(title = "Editar cores")
            return(cor[1])
        def cores_px():
            global cor_px
            cor_px = colorchooser.askcolor(title ="Editar cores")
            cor_px = cor_px[1]
            fig = graf_produtiv(px = cor_px, pp = "green")
            Button(frame38, text = "Pp", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_pp).place(x = 460, y = 255)   
        def cores_pp():
            global cor_pp
            cor_pp = colorchooser.askcolor(title ="Editar cores")
            cor_pp = cor_pp[1]
            fig = graf_produtiv(px = cor_px, pp = cor_pp)
            Button(frame38, text = "Pp", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_pp).place(x = 460, y = 255)
        def cores_produtiv():
            Button(frame38, text = "Px", bg = "gray60", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_px).place(x = 460, y = 230)    
       
        # Geração do gráfico:
        graf_produtiv(px = "red", pp = "green")
        ## Botão para seleção das cores:
        botao_paleta_graf(frame38, comando = cores_produtiv)
    
        # Cálculo produtivida específica:
        ## Experimental:
        Ppx_exp=C_exp[:,2]*(1/C_exp[:,0])
        Ppx_exp[Ppx_exp<0] = 0
        ## Modelada:
        Ppx=C_otim[:,2]*(1/C_otim[:,0])
        Ppx[Ppx<0] = 0
        # Gráfico produtividade específica:
        def graf_produtiv_espec(Ppx_cor, Ppx_exp_cor):
            def imprimir_produtividade_especifica_model_otim_exp (t_ajus,t_m, Ppx_ajus, Ppx_m):
                f = plt.figure(figsize=(8,6), dpi = 54) 
                plot = f.add_subplot(111)  
                plt.plot(t_m,Ppx_m,color = Ppx_cor,linewidth=3, label='Modelo')
                plt.plot(t_ajus,Ppx_ajus,'o',markersize=6, color = Ppx_exp_cor, label='Experimental')
                plt.xlabel('Tempo de cultivo (h)',weight='bold')               
                plt.ylabel('Produtividade Específica (gp/gx)', weight='bold')
                plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08),ncol=2, fancybox=True, shadow=True )
                plt.grid(True)  
                f.patch.set_facecolor('white')                                   
                plt.style.use('default')                       
                canvas = FigureCanvasTkAgg(f, frame39)
                a = canvas.get_tk_widget().place(x = 0, y = 0)
                def salvar():
                    a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                    defaultextension='.png')
                    plt.savefig(a)
                botao_com_graf(frame = frame39, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
            imprimir_produtividade_especifica_model_otim_exp(t_exp,t,Ppx_exp,Ppx)
            # Cálculo R²:
            df_Ppx = pd.DataFrame({'Tempo(h)':t, 'ppx(g/L)': Ppx})
            df_t_exp = pd.DataFrame({'Tempo(h)': t_exp})
            df_Ppx_merge = df_Ppx.merge(df_t_exp, how = 'inner' ,indicator=False)
            df_Ppx_exp = pd.DataFrame({'Tempo_exp(h)':t_exp, 'Ppx_exp(g/L)': Ppx_exp})
            del df_Ppx_merge['Tempo(h)']
            del df_Ppx_exp['Tempo_exp(h)']
            df_Ppx_merge = df_Ppx_merge.values
            df_Ppx_exp = df_Ppx_exp.values
            resid = (df_Ppx_merge - df_Ppx_exp)**2
            resid = resid.flatten()
            resid = sum(resid)
            Ppx_medio = np.mean(df_Ppx_exp)
            Ppx_total = sum((df_Ppx_exp- Ppx_medio)**2)
            r2_Ppx = 1 - (resid/Ppx_total)
            Label(frame2, text = "", font = "batang 10",  bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            Label(frame2, text = r2_Ppx[0].round(4), font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            print(r2_Ppx[0].round(4))
        
        ## Escolha das cores:
        def seletor_cores_Ppx():
            cor_Ppx = colorchooser.askcolor(title ="Editar cores")
            cor_Ppx = cor_Ppx[1]
            graf_produtiv_espec(Ppx_cor = cor_Ppx, Ppx_exp_cor = cor_Ppx)
            
        ## Geração do gráfico:
        graf_produtiv_espec(Ppx_cor = "red", Ppx_exp_cor = "red")
        ## Botão para seleção das cores:
        botao_paleta_graf(frame39, comando = seletor_cores_Ppx)
        
        # Cálculo taxa mi:
        ## Experimental e modelado:
        if cont_model == 0:
            mi_exp = param_otim_alm[0]*(C_exp[:,1]/(param_otim_alm[1]+C_exp[:,1]))
            mi = param_otim_alm[0]*(C_otim[:,1]/(param_otim_alm[1]+C_otim[:,1]))
        if cont_model == 1:
            mi_exp = param_otim_alm[0]*(C_exp[:,1]/(param_otim_alm[1]*C_exp[:,0]+C_exp[:,1]))
            mi = param_otim_alm[0]*(C_otim[:,1]/(param_otim_alm[1]*C_otim[:,0]+C_otim[:,1]))
        if cont_model == 2:
            mi_exp = param_otim_alm[0]*(C_exp[:,1]/(param_otim_alm[1]+ C_exp[:,1] + ((C_exp[:,1]**2)/param_otim_alm[6])))
            mi = param_otim_alm[0]*(C_otim[:,1]/(param_otim_alm[1]+ C_otim[:,1] + ((C_otim[:,1]**2)/param_otim_alm[6])))
        if cont_model == 3:
            mult_exp = -param_otim_alm[6]*C_exp[:,2]
            mi_exp = param_otim_alm[0]*((C_exp[:,1]/(param_otim_alm[1]+C_exp[:,1]))*np.exp(mult_exp))
            mult = -param_otim_alm[6]*C_otim[:,2]
            mi = param_otim_alm[0]*((C_otim[:,1]/(param_otim_alm[1]+C_otim[:,1]))*np.exp(mult))
        if cont_model == 4:
            mi_exp = param_otim_alm[0]*((C_exp[:,1]**param_otim_alm[6])/(param_otim_alm[1]+(C_exp[:,1]**param_otim_alm[6])))
            mi = param_otim_alm[0]*((C_otim[:,1]**param_otim_alm[6])/(param_otim_alm[1]+(C_otim[:,1]**param_otim_alm[6])))
        if cont_model == 5:
            mi_exp = param_otim_alm[0]*(C_exp[:,1]/(param_otim_alm[1]+C_exp[:,1]))*(param_otim_alm[6]/(param_otim_alm[6]+C_exp[:,2]))
            mi = param_otim_alm[0]*(C_otim[:,1]/(param_otim_alm[1]+C_otim[:,1]))*(param_otim_alm[6]/(param_otim_alm[6]+C_otim[:,2]))
        if cont_model == 6:
            mi_exp = param_otim_alm[0]*(C_exp[:,1]/(param_otim_alm[1]+C_exp[:,1]+(C_exp[:,1]*((C_exp[:,1]/param_otim_alm[6])**param_otim_alm[7]))))
            mi = param_otim_alm[0]*(C_otim[:,1]/(param_otim_alm[1]+C_otim[:,1]+(C_otim[:,1]*((C_otim[:,1]/param_otim_alm[6])**param_otim_alm[7]))))
        if cont_model == 7:
            mi_exp = param_otim_alm[0]*((C_exp[:,1]/(param_otim_alm[1]+C_exp[:,1]))*((1-(C_exp[:,2]/param_otim_alm[7]))**param_otim_alm[6]))
            mi = param_otim_alm[0]*((C_otim[:,1]/(param_otim_alm[1]+C_otim[:,1]))*((1-(C_otim[:,2]/param_otim_alm[7]))**param_otim_alm[6]))
        if cont_model == 8:
            mi_exp = param_otim_alm[0]*((C_exp[:,1]/(param_otim_alm[1]+C_exp[:,1]))*((1-(C_exp[:,0]/param_otim_alm[7]))**param_otim_alm[6]))
            mi = param_otim_alm[0]*((C_otim[:,1]/(param_otim_alm[1]+C_otim[:,1]))*((1-(C_otim[:,0]/param_otim_alm[7]))**param_otim_alm[6]))
        mi_exp[mi_exp<0] = 0
        mi[mi<0] = 0
        # Gráfico - velocidade de crescimento microbiano:
        def graf_mi(mi_cor, mi_exp_cor):
            def imprimir_taxa_especifica_crescimento (t_ajus,t_m, mi_ajus, mi_m):
                f = plt.figure(figsize=(8,6), dpi = 54) 
                plot = f.add_subplot(111)                                             
                plt.plot(t_m,mi_m,color = mi_cor,linewidth=3, label='Modelo')
                plt.plot(t_ajus,mi_ajus,'o',markersize=6, color = mi_exp_cor, label='Experimental')
                plt.xlabel('Tempo de cultivo (h)',weight='bold')               
                plt.ylabel('Taxa específica de crescimento', weight='bold')
                plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.08),ncol=2, fancybox=True, shadow=True )  
                plt.grid(True)  
                f.patch.set_facecolor('white')                                   
                plt.style.use('default')   
                canvas = FigureCanvasTkAgg(f, frame40)
                a = canvas.get_tk_widget().place(x = 0, y = 0)
                def salvar():
                    a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                    defaultextension='.png')
                    plt.savefig(a)  
                botao_com_graf(frame = frame40, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
            imprimir_taxa_especifica_crescimento(t_exp,t,mi_exp,mi)
            # Cálculo R²:
            df_mi = pd.DataFrame({'Tempo(h)':t, 'mi(h-¹)': mi})
            df_t_exp = pd.DataFrame({'Tempo(h)': t_exp})
            df_mi_merge = df_mi.merge(df_t_exp, how = 'inner' ,indicator=False)
            df_mi_exp = pd.DataFrame({'Tempo_exp(h)':t_exp, 'mi(h-¹)': mi_exp})
            del df_mi_merge['Tempo(h)']
            del df_mi_exp['Tempo_exp(h)']
            df_mi_merge = df_mi_merge.values
            df_mi_exp = df_mi_exp.values
            resid = (df_mi_merge - df_mi_exp)**2
            resid = resid.flatten()
            resid = sum(resid)
            mi_medio = np.mean(df_mi_exp)
            mi_total = sum((df_mi_exp- mi_medio)**2)
            r2_mi = 1 - (resid/mi_total)
            Label(frame2, text = "", font = "batang 10",  bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            Label(frame2, text = r2_mi[0].round(4), font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            print(r2_mi[0].round(4))
                
        ## Escolha das cores:
        def seletor_cores_mi():
            cor_mi = colorchooser.askcolor(title ="Editar cores")
            cor_mi = cor_mi[1]
            graf_mi(mi_cor = cor_mi, mi_exp_cor = cor_mi)
            
        ## Geração do gráfico:
        graf_mi(mi_cor = "red", mi_exp_cor = "red")
        ## Botão para seleção das cores:
        botao_paleta_graf(frame40, comando = seletor_cores_mi)
            
        # Cálculo res final:
        res_final = odeint(list_funcs_args[cont_model], cond_inic, t_exp, args = (param_otim_alm)) - C_exp
        for i in range(0,3):
            res_final[:,i] = res_final[:,i]/dpC[i]
        res_final = res_final.flatten()
        res_final = sum(res_final**2)
        res_final = round(res_final,2)
        
        # Impressão do valor do resíduo na interface:
        Label(frame2, text = res_final, font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 299)
        
        # Condicional - peso cálculo do res final:
        if cont_model ==0:
            res_final = res_final/6
        else:
            if cont_model ==1:
                res_final = res_final/6
            else:
                if cont_model ==2:
                    res_final = res_final/7
                else:
                    if cont_model ==3:
                        res_final = res_final/7
                    else:
                        if cont_model ==4:
                            res_final = res_final/7
                        else:
                            if cont_model ==5:
                                res_final = res_final/7    
                            else:
                                if cont_model ==9:
                                    res_final = res_final/5
                                else:
                                    res_final = res_final/8
        
        
        # # Inserindo 0 para o primeiro valor de produtividade:
        Px_exp_ad = np.insert(Px_exp,2,Px_exp[0])
        Px_ad = np.insert(Px,0,Px[0])
        Pp_exp_ad = np.insert(Pp_exp,0,Pp_exp[0])
        Pp_ad = np.insert(Pp,0,Pp[0])
        
        # Saída .xlsx - concentração, produtividade e taxa de crescimento:
        def excel_concent():
            df_sai_exp = pd.DataFrame({'Tempo_exp(h)': t_exp, 'Cx_exp(g/L)': C_exp[:,0], 'Cs_exp(g/L)': C_exp[:,1], 'Cp_exp(g/L)': C_exp[:,2], 'Px_exp(g/L)': Px_exp_ad, 'Pp_exp(g/L)': Pp_exp_ad, 'Ppx_exp(g/L)': Ppx_exp, 'mi_exp(h-¹)': mi_exp})
            df_sai_model = pd.DataFrame({'Tempo(h)': t, 'Cx(g/L)': C_otim[:,0], 'Cs(g/L)': C_otim[:,1], 'Cp(g/L)': C_otim[:,2], 'Px(g/L)': Px_ad, 'Pp(g/L)': Pp_ad, 'Ppx(g/L)': Ppx, 'mi(h-¹)': mi})
            df_r2 = pd.DataFrame({'R²':[r2]})
            df_tempo = pd.DataFrame({"Tempo(s)":[elapsed]})
            df_concents = pd.concat([df_sai_exp, df_sai_model, df_r2, df_tempo], axis = 1)
            with pd.ExcelWriter('Modelagem_Concent_Produt_mi.xlsx') as writer:
                df_concents.to_excel(writer, sheet_name="Saida_exp_modelada")
                writer.save()
            os.system("start EXCEL Modelagem_Concent_Produt_mi.xlsx")
        Label(frame2, text = "Modelagem_Concent_Produt_mi.xlsx", font = "arial 8 italic", fg = "black", bg = "gray45").place(x = 1072, y = 50)
        
        # Saída .xlsx - parâmetros cinéticos:
        def excel_param():
            if cont_model == 0: #Monod
                df_params_model =pd.DataFrame({'mimax(h-¹)':[param_otim_alm[0]],'Ks(g/L)':[param_otim_alm[1]],'Kd(h-¹)':[param_otim_alm[2]],'Yxs(gcél/gsub)':[param_otim_alm[3]], 'alfa(gprod/gcél)': [param_otim_alm[4]], 'beta(gprod/gcél.h)':[param_otim_alm[5]]})
                df_params_IC = pd.DataFrame({'IC mimax(h-¹)':[ICpar[0]],'IC Ks(g/L)':[ICpar[1]],'IC Kd(h-¹)':[ICpar[2]],'IC Yxs(gcél/gsub)':[ICpar[3]], 'IC alfa(gprod/gcél)': [ICpar[4]], 'IC beta(gprod/gcél.h)':[ICpar[5]]})
                df_params = pd.concat([df_params_model, df_params_IC], axis = 1)
            if cont_model == 1: #Contois
                df_params_model =pd.DataFrame({'mimax(h-¹)':[param_otim_alm[0]],'KSX(g/L)':[param_otim_alm[1]],'Kd(h-¹)':[param_otim_alm[2]],'Yxs(gcél/gsub)':[param_otim_alm[3]], 'alfa(gprod/gcél)': [param_otim_alm[4]], 'beta(gprod/gcél.h)':[param_otim_alm[5]]})
                df_params_IC = pd.DataFrame({'IC mimax(h-¹)':[ICpar[0]],'IC KSX(g/L)':[ICpar[1]],'IC Kd(h-¹)':[ICpar[2]],'IC Yxs(gcél/gsub)':[ICpar[3]], 'IC alfa(gprod/gcél)': [ICpar[4]], 'IC beta(gprod/gcél.h)':[ICpar[5]]})
                df_params = pd.concat([df_params_model, df_params_IC], axis = 1)
            if cont_model == 4: #Moser
                df_params_model =pd.DataFrame({'mimax(h-¹)':[param_otim_alm[0]],'Ks(g/L)':[param_otim_alm[1]],'Kd(h-¹)':[param_otim_alm[2]],'Yxs(gcél/gsub)':[param_otim_alm[3]], 'alfa(gprod/gcél)': [param_otim_alm[4]], 'beta(gprod/gcél.h)':[param_otim_alm[5]],'mi_exp(adim)':[param_otim_alm[6]]})
                df_params_IC = pd.DataFrame({'IC mimax(h-¹)':[ICpar[0]],'IC Ks(g/L)':[ICpar[1]],'IC Kd(h-¹)':[ICpar[2]],'IC Yxs(gcél/gsub)':[ICpar[3]], 'IC alfa(gprod/gcél)': [ICpar[4]], 'IC beta(gprod/gcél.h)':[ICpar[5]], 'IC mi_exp(adim)':[ICpar[6]]})
                df_params = pd.concat([df_params_model, df_params_IC], axis = 1)
            if cont_model == 2: #Andrews
                df_params_model =pd.DataFrame({'mimax(h-¹)':[param_otim_alm[0]],'Ks(g/L)':[param_otim_alm[1]],'Kd(h-¹)':[param_otim_alm[2]],'Yxs(gcél/gsub)':[param_otim_alm[3]], 'alfa(gprod/gcél)': [param_otim_alm[4]], 'beta(gprod/gcél.h)':[param_otim_alm[5]], 'KSI(g/L)':[param_otim_alm[6]]})
                df_params_IC = pd.DataFrame({'IC mimax(h-¹)':[ICpar[0]],'IC Ks(g/L)':[ICpar[1]],'IC Kd(h-¹)':[ICpar[2]],'IC Yxs(gcél/gsub)':[ICpar[3]], 'IC alfa(gprod/gcél)': [ICpar[4]], 'IC beta(gprod/gcél.h)':[ICpar[5]], 'IC KSI(g/L)':[ICpar[6]]})
                df_params = pd.concat([df_params_model, df_params_IC], axis = 1)
            if cont_model == 5: #Hope_Hansford
                df_params_model =pd.DataFrame({'mimax(h-¹)':[param_otim_alm[0]],'Ks(g/L)':[param_otim_alm[1]],'Kd(h-¹)':[param_otim_alm[2]],'Yxs(gcél/gsub)':[param_otim_alm[3]], 'alfa(gprod/gcél)': [param_otim_alm[4]], 'beta(gprod/gcél.h)':[param_otim_alm[5]], 'Kp(g/L)':[param_otim_alm[6]]})
                df_params_IC = pd.DataFrame({'IC mimax(h-¹)':[ICpar[0]],'IC Ks(g/L)':[ICpar[1]],'IC Kd(h-¹)':[ICpar[2]],'IC Yxs(gcél/gsub)':[ICpar[3]], 'IC alfa(gprod/gcél)': [ICpar[4]], 'IC beta(gprod/gcél.h)':[ICpar[5]], 'IC Kp(g/L)':[ICpar[6]]})
                df_params = pd.concat([df_params_model, df_params_IC], axis = 1)
            if cont_model == 3: #Aiba
                df_params_model =pd.DataFrame({'mimax(h-¹)':[param_otim_alm[0]],'Ks(g/L)':[param_otim_alm[1]],'Kd(h-¹)':[param_otim_alm[2]],'Yxs(gcél/gsub)':[param_otim_alm[3]], 'alfa(gprod/gcél)': [param_otim_alm[4]], 'beta(gprod/gcél.h)':[param_otim_alm[5]], 'Kp(L/g)':[param_otim_alm[6]]})
                df_params_IC = pd.DataFrame({'IC mimax(h-¹)':[ICpar[0]],'IC Ks(g/L)':[ICpar[1]],'IC Kd(h-¹)':[ICpar[2]],'IC Yxs(gcél/gsub)':[ICpar[3]], 'IC alfa(gprod/gcél)': [ICpar[4]], 'IC beta(gprod/gcél.h)':[ICpar[5]], 'IC Kp(g/L)':[ICpar[6]]})
                df_params = pd.concat([df_params_model, df_params_IC], axis = 1)
            if cont_model == 6: #Wu
                df_params_model =pd.DataFrame({'mimax(h-¹)':[param_otim_alm[0]],'Ks(g/L)':[param_otim_alm[1]],'Kd(h-¹)':[param_otim_alm[2]],'Yxs(gcél/gsub)':[param_otim_alm[3]], 'alfa(gprod/gcél)': [param_otim_alm[4]], 'beta(gprod/gcél.h)':[param_otim_alm[5]],'KE(g/L)':[param_otim_alm[6]], 'v(adim)':[param_otim_alm[7]]})
                df_params_IC = pd.DataFrame({'IC mimax(h-¹)':[ICpar[0]],'IC Ks(g/L)':[ICpar[1]],'IC Kd(h-¹)':[ICpar[2]],'IC Yxs(gcél/gsub)':[ICpar[3]], 'IC alfa(gprod/gcél)': [ICpar[4]], 'IC beta(gprod/gcél.h)':[ICpar[5]], 'IC KE(g/L)':[ICpar[6]], 'IC v(adim)':[ICpar[7]]})
                df_params = pd.concat([df_params_model, df_params_IC], axis = 1)
            if cont_model == 7: #Levenspiel
                df_params_model =pd.DataFrame({'mimax(h-¹)':[param_otim_alm[0]],'Ks(g/L)':[param_otim_alm[1]],'Kd(h-¹)':[param_otim_alm[2]],'Yxs(gcél/gsub)':[param_otim_alm[3]], 'alfa(gprod/gcél)': [param_otim_alm[4]], 'beta(gprod/gcél.h)':[param_otim_alm[5]], 'n(adim)':[param_otim_alm[6]], 'Cp_estr(g/L)':[param_otim_alm[7]]})
                df_params_IC = pd.DataFrame({'IC mimax(h-¹)':[ICpar[0]],'IC Ks(g/L)':[ICpar[1]],'IC Kd(h-¹)':[ICpar[2]],'IC Yxs(gcél/gsub)':[ICpar[3]], 'IC alfa(gprod/gcél)': [ICpar[4]], 'IC beta(gprod/gcél.h)':[ICpar[5]], 'IC n(adim)':[ICpar[6]], 'IC Cp_estr(g/L)':[ICpar[7]]})
                df_params = pd.concat([df_params_model, df_params_IC], axis = 1)
            if cont_model == 8: #Lee
                df_params_model =pd.DataFrame({'mimax(h-¹)':[param_otim_alm[0]],'Ks(g/L)':[param_otim_alm[1]],'Kd(h-¹)':[param_otim_alm[2]],'Yxs(gcél/gsub)':[param_otim_alm[3]], 'alfa(gprod/gcél)': [param_otim_alm[4]], 'beta(gprod/gcél.h)':[param_otim_alm[5]], 'm(adim)':[param_otim_alm[6]], 'Cx_estr(g/L)':[param_otim_alm[7]]})
                df_params_IC = pd.DataFrame({'IC mimax(h-¹)':[ICpar[0]],'IC Ks(g/L)':[ICpar[1]],'IC Kd(h-¹)':[ICpar[2]],'IC Yxs(gcél/gsub)':[ICpar[3]], 'IC alfa(gprod/gcél)': [ICpar[4]], 'IC beta(gprod/gcél.h)':[ICpar[5]], 'IC m(adim)':[ICpar[6]], 'IC Cx_estr(g/L)':[ICpar[7]]})
                df_params = pd.concat([df_params_model, df_params_IC], axis = 1)
            with pd.ExcelWriter('Modelagem_Parametros_Cineticos.xlsx') as writer:
                df_params.to_excel(writer, sheet_name="Param_model")
                writer.save()
            os.system("start EXCEL Modelagem_Parametros_Cineticos.xlsx")
        Label(frame2, text = "Modelagem_Params_Cineticos.xlsx", font = "arial 8 italic", fg = "black", bg = "gray45").place(x = 1072, y = 87)
        
        # Botão de acesso - arquivo .xlsx - concentração:
        load = Image.open("Excel.png")
        render = ImageTk.PhotoImage(load)
        img = Button(frame2, image = render, border = 0, command = excel_concent)
        img.image = render
        img.place(x = 1036, y = 42)
        
        
        # Botão de acesso - arquivo .xlsx - parâmetros cinéticos:
        load = Image.open("Excel.png")
        render = ImageTk.PhotoImage(load)
        img = Button(frame2, image = render, border = 0, command = excel_param)
        img.image = render
        img.place(x = 1036, y = 80)
        
    
        # Fim da modelagem:
        return()

    # Criação botões - MODELAGEM:
    def click_contois(): 
        tab_fun_cin()
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        #func_sai()
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     KSX(g.L\u207b\u00b9)", font = "arial 10 bold", justify = "center", fg = "black", bg = "grey75", width = 21).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
        modelagem(cont_model = 1)

    def click_monod(): 
        tab_fun_cin()
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        #func_sai()
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 20).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
        modelagem(cont_model = 0)
        
    def click_moser(): 
        tab_fun_cin()
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        #func_sai()    
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)     u(adim)", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 28).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
        modelagem(cont_model = 4)
        
    def click_aiba(): 
        tab_fun_cin()
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)     Kp(g.L\u207b\u00b9)", font = "arial 10 bold", justify = "center", fg = "black", bg = "grey75", width = 28).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
        modelagem(cont_model = 3)

    def click_hope_hansford(): 
        tab_fun_cin() 
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)     Kp(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 28).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
        modelagem(cont_model = 5)
        
    def click_levenspiel(): 
        tab_fun_cin() 
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)    Ks(g.L\u207b\u00b9)     n(adim)     Cp*(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 37).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)   \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
        modelagem(cont_model = 7)
        
    def click_andrews(): 
        tab_fun_cin() 
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)      Ks(g.L\u207b\u00b9)     KIS(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 30).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
        modelagem(cont_model = 2)
        
    def click_wu(): 
        tab_fun_cin()
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)     KE(g.L\u207b\u00b9)     v(adim)", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 37).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
        modelagem(cont_model = 6)
        
    def click_lee(): 
        tab_fun_cin()
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)    Ks(g.L\u207b\u00b9)     m(adim )     Cx*(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 37).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
        modelagem(cont_model = 8)

    def print_me_2():
        value_2 = combo_2.get()
        print(value_2)
        if value_2 == "AUSÊNCIA DE INIBIÇÃO":
            notebook_sem_inib()
            image(imagem = "Equacao_Contois_mod.png", num_frame = frame4, x = 60, y = 92)
            tex_mimax = Label(frame4, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ksx = Label(frame4, text = u"KSX = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            image(imagem = "Equacao_Monod_mod.png", num_frame = frame5, x = 60, y = 92)
            tex_mimax = Label(frame5, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame5, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            image(imagem = "Equacao_Moser_mod.png", num_frame = frame6, x = 60, y = 92)
            tex_mimax = Label(frame6, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame6, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            tex_n = Label(frame6, text = "n = parâmetro expoente (adim)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 244)
            Button(frame4, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = click_contois).place(x = 112, y = 28)
            Button(frame5, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = click_monod).place(x = 112, y = 28)
            Button(frame6, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = click_moser).place(x = 112, y = 28)
        if value_2 == "INIBIÇÃO PELO SUBSTRATO": 
            notebook_inib_subs()
            image(imagem = "Equacao_Andrews_mod.png", num_frame = frame7, x = 45, y = 90)
            tex_mimax = Label(frame7, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame7, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            tex_kis = Label(frame7, text = u"KIS = constante inibição por substrato (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 244)
            image(imagem = "Equacao_Wu_mod.png", num_frame = frame8, x = 26, y = 90)
            tex_mimax = Label(frame8, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame8, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            tex_ke = Label(frame8, text = u"Ke = constante inibição por substrato (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 244)
            tex_v = Label(frame8, text = "v = parâmetro expoente (adim)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 274)
            Button(frame7, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = click_andrews).place(x = 112, y = 28)
            Button(frame8, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = click_wu).place(x = 112, y = 28)
        if value_2 == "INIBIÇÃO PELO PRODUTO": 
            notebook_inib_prod()
            image(imagem = "Equacao_Aiba_mod.png", num_frame = frame9, x = 35, y = 92) 
            tex_mimax = Label(frame9, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame9, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            tex_kp = Label(frame9, text = u"Kp = parâmetro expoente de inibição (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 244)
            Button(frame9, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = click_aiba).place(x = 112, y = 28)
            Button(frame10, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = click_hope_hansford).place(x = 112, y = 28)
            Button(frame11, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = click_levenspiel).place(x = 112, y = 28)
            image(imagem = "Equacao_Hope_Hansford_mod.png", num_frame = frame10, x = 37, y = 92) 
            tex_mimax = Label(frame10, text =u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame10, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            tex_kp = Label(frame10, text = u"Kp = constante inibição por produto (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 244)
            image(imagem = "Equacao_Levenspiel_mod.png", num_frame = frame11, x = 26, y = 92) 
            tex_mimax = Label(frame11, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame11, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            tex_cpestr = Label(frame11, text = u"Cp* = concentração produto crítica (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 244)
            tex_n_lev = Label(frame11, text = "n = constante de Levenspiel (adim)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 274)
        if value_2 == "INIBIÇÃO PELA BIOMASSA": 
            notebook_inib_biomas()
            image(imagem = "Equacao_Lee_mod.png", num_frame = frame12, x = 26, y = 92) 
            tex_mimax = Label(frame12, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame12, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            tex_cxestr = Label(frame12, text = u"Cx* = concentração celular crítica (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 244)
            tex_m = Label(frame12, text = "m = constante de Lee et al (adim)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 274)
            Button(frame12, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = click_lee).place(x = 112, y = 28)
        
    Button(frame2, text="Pronto", bg = "black", fg="white", font="batang 12", command = print_me_2).place(x = 315, y = 29)
Button(frame2, text = "Carregar arquivo",  font="Batang 12", fg="white", bg="gray17", borderwidth=2, relief="raised", command = explorer).place(x = 568, y = 15) 
Label(frame2, borderwidth=2, relief="ridge", justify = "center", width = 40).place(x = 500, y = 50)

# Função para capturar os valores de entrada - SIMULAÇÃO
def capt_val_esc_contois():
    global Cx0, Cs0, Cp0, t0, tf, mimax, KSX, Kd, Yxs, alfa, beta
    Cx0 = float(entr_Cx0_contois.get())
    Cs0 = float(entr_Cs0_contois.get())
    Cp0 = float(entr_Cp0_contois.get())
    t0 = float(entr_t0_contois.get())
    tf = float(entr_tf_contois.get())
    mimax = float(slider_mimax_contois.get())
    KSX = float(slider_ks_contois.get())
    Kd = float(slider_kd_contois.get())
    Yxs = float(slider_yxs_contois.get())
    alfa = float(slider_alfa_contois.get())
    beta = float(slider_beta_contois.get())
    print(Cx0, Cs0, Cp0, t0, tf, mimax, KSX, Kd, Yxs, alfa, beta)
    simulacao(cont = 1)

def capt_val_esc_monod():
    global Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta
    Cx0 = float(entr_Cx0_monod.get())
    Cs0 = float(entr_Cs0_monod.get())
    Cp0 = float(entr_Cp0_monod.get())
    t0 = float(entr_t0_monod.get())
    tf = float(entr_tf_monod.get())
    mimax = float(slider_mimax_monod.get())
    Ks = float(slider_ks_monod.get())
    Kd = float(slider_kd_monod.get())
    Yxs = float(slider_yxs_monod.get())
    alfa = float(slider_alfa_monod.get())
    beta = float(slider_beta_monod.get())
    print(Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta)
    simulacao(cont = 0)
    
def capt_val_esc_moser():
    global Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta, u
    Cx0 = float(entr_Cx0_moser.get())
    Cs0 = float(entr_Cs0_moser.get())
    Cp0 = float(entr_Cp0_moser.get())
    t0 = float(entr_t0_moser.get())
    tf = float(entr_tf_moser.get())
    mimax = float(slider_mimax_moser.get())
    Ks = float(slider_ks_moser.get())
    Kd = float(slider_kd_moser.get())
    Yxs = float(slider_yxs_moser.get())
    alfa = float(slider_alfa_moser.get())
    beta = float(slider_beta_moser.get())
    u = float(slider_u.get())
    print(Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta, u)
    simulacao(cont = 4)

def capt_val_esc_andrews():
    global Cx0, Cs0, Cp0, t0, tf, Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta, KIS
    Cx0 = float(entr_Cx0_andrews.get())
    Cs0 = float(entr_Cs0_andrews.get())
    Cp0 = float(entr_Cp0_andrews.get())
    t0 = float(entr_t0_andrews.get())
    tf = float(entr_tf_andrews.get())
    mimax = float(slider_mimax_andrews.get())
    Ks = float(slider_ks_andrews.get())
    Kd = float(slider_kd_andrews.get())
    Yxs = float(slider_yxs_andrews.get())
    alfa = float(slider_alfa_andrews.get())
    beta = float(slider_beta_andrews.get())
    KIS = float(slider_kis.get())
    print(Cx0, Cs0, Cp0, t0, tf, Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta, KIS)
    simulacao(cont = 2)

def capt_val_esc_wu():
    global Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta, Ke, v
    Cx0 = float(entr_Cx0_wu.get())
    Cs0 = float(entr_Cs0_wu.get())
    Cp0 = float(entr_Cp0_wu.get())
    t0 = float(entr_t0_wu.get())
    tf = float(entr_tf_wu.get())
    mimax = float(slider_mimax_wu.get())
    Ks = float(slider_ks_wu.get())
    Kd = float(slider_kd_wu.get())
    Yxs = float(slider_yxs_wu.get())
    alfa = float(slider_alfa_wu.get())
    beta = float(slider_beta_wu.get())
    Ke = float(slider_ke.get())
    v = float(slider_v.get())
    print(Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta, Ke, v)
    simulacao(cont = 6)
    
def capt_val_esc_aiba():
    global Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta, Kp_aiba
    Cx0 = float(entr_Cx0_aiba.get())
    Cs0 = float(entr_Cs0_aiba.get())
    Cp0 = float(entr_Cp0_aiba.get())
    t0 = float(entr_t0_aiba.get())
    tf = float(entr_tf_aiba.get())
    mimax = float(slider_mimax_aiba.get())
    Ks = float(slider_ks_aiba.get())
    Kd = float(slider_kd_aiba.get())
    Yxs = float(slider_yxs_aiba.get())
    alfa = float(slider_alfa_aiba.get())
    beta = float(slider_beta_aiba.get())
    Kp_aiba = float(slider_kp_aiba.get())
    print(Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta, Kp_aiba)
    simulacao(cont = 3)
    
def capt_val_esc_h_h():
    global Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta, Kp_hh
    Cx0 = float(entr_Cx0_h_h.get())
    Cs0 = float(entr_Cs0_h_h.get())
    Cp0 = float(entr_Cp0_h_h.get())
    t0 = float(entr_t0_h_h.get())
    tf = float(entr_tf_h_h.get())
    mimax = float(slider_mimax_h_h.get())
    Ks = float(slider_ks_h_h.get())
    Kd = float(slider_kd_h_h.get())
    Yxs = float(slider_yxs_h_h.get())
    alfa = float(slider_alfa_h_h.get())
    beta = float(slider_beta_h_h.get())
    Kp_hh = float(slider_kp_h_h.get())
    print(Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta, Kp_hh)
    simulacao(cont = 5)
    
def capt_val_esc_levenspiel():
    global Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta, Cp_estr, n
    Cx0 = float(entr_Cx0_levenspiel.get())
    Cs0 = float(entr_Cs0_levenspiel.get())
    Cp0 = float(entr_Cp0_levenspiel.get())
    t0 = float(entr_t0_levenspiel.get())
    tf = float(entr_tf_levenspiel.get())
    mimax = float(slider_mimax_levenspiel.get())
    Ks = float(slider_ks_levenspiel.get())
    Kd = float(slider_kd_levenspiel.get())
    Yxs = float(slider_yxs_levenspiel.get())
    alfa = float(slider_alfa_levenspiel.get())
    beta = float(slider_beta_levenspiel.get())
    Cp_estr = float(slider_cp_estr.get())
    n = float(slider_n.get())
    print(Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta, Cp_estr, n)
    simulacao(cont = 7)
    
def capt_val_esc_lee():
    global Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta, Cx_estr, m
    Cx0 = float(entr_Cx0_lee.get())
    Cs0 = float(entr_Cs0_lee.get())
    Cp0 = float(entr_Cp0_lee.get())
    t0 = float(entr_t0_lee.get())
    tf = float(entr_tf_lee.get())
    mimax = float(slider_mimax_lee.get())
    Ks = float(slider_ks_lee.get())
    Kd = float(slider_kd_lee.get())
    Yxs = float(slider_yxs_lee.get())
    alfa = float(slider_alfa_lee.get())
    beta = float(slider_beta_lee.get())
    Cx_estr = float(slider_cx_estr.get())
    m = float(slider_m.get())
    print(Cx0, Cs0, Cp0, t0, tf, mimax, Ks, Kd, Yxs, alfa, beta, Cx_estr, m)
    simulacao(cont = 8)
    
# Função entradas numéricas:
def entr_simul_mimax_contois(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_mimax_contois, slider_mimax_contois
    spin_mimax_contois = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_mimax_contois.place(x = 15, y = 37)
    slider_mimax_contois = ttk.Scale(frame, variable=input, from_= 0.01, to = 1.5, orient='horizontal',length = 60)
    slider_mimax_contois.place(x = 59, y = 32) 
def entr_simul_mimax_monod(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_mimax_monod, slider_mimax_monod
    spin_mimax_monod = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_mimax_monod.place(x = 15, y = 37)
    slider_mimax_monod = ttk.Scale(frame, variable=input, from_= 0.01, to = 1.5, orient='horizontal',length = 60)
    slider_mimax_monod.place(x = 59, y = 32) 
def entr_simul_mimax_moser(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_mimax_moser, slider_mimax_moser
    spin_mimax_moser = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_mimax_moser.place(x = 15, y = 37)
    slider_mimax_moser = ttk.Scale(frame, variable=input, from_= 0.01, to = 1.5, orient='horizontal',length = 60)
    slider_mimax_moser.place(x = 59, y = 32) 
def entr_simul_mimax_andrews(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_mimax_andrews, slider_mimax_andrews
    spin_mimax_andrews = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_mimax_andrews.place(x = 15, y = 37)
    slider_mimax_andrews = ttk.Scale(frame, variable=input, from_= 0.01, to = 1.5, orient='horizontal',length = 60)
    slider_mimax_andrews.place(x = 59, y = 32) 
def entr_simul_mimax_wu(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_mimax_wu, slider_mimax_wu
    spin_mimax_wu = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_mimax_wu.place(x = 15, y = 37)
    slider_mimax_wu = ttk.Scale(frame, variable=input, from_= 0.01, to = 1.5, orient='horizontal',length = 60)
    slider_mimax_wu.place(x = 59, y = 32) 
def entr_simul_mimax_aiba(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_mimax_aiba, slider_mimax_aiba
    spin_mimax_aiba = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_mimax_aiba.place(x = 15, y = 37)
    slider_mimax_aiba = ttk.Scale(frame, variable=input, from_= 0.01, to = 1.5, orient='horizontal',length = 60)
    slider_mimax_aiba.place(x = 59, y = 32) 
def entr_simul_mimax_h_h(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_mimax_h_h, slider_mimax_h_h
    spin_mimax_h_h = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_mimax_h_h.place(x = 15, y = 37)
    slider_mimax_h_h = ttk.Scale(frame, variable=input, from_= 0.01, to = 1.5, orient='horizontal',length = 60)
    slider_mimax_h_h.place(x = 59, y = 32) 
def entr_simul_mimax_levenspiel(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_mimax_levenspiel, slider_mimax_levenspiel
    spin_mimax_levenspiel = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_mimax_levenspiel.place(x = 15, y = 37)
    slider_mimax_levenspiel = ttk.Scale(frame, variable=input, from_= 0.01, to = 1.5, orient='horizontal',length = 60)
    slider_mimax_levenspiel.place(x = 59, y = 32) 
def entr_simul_mimax_lee(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_mimax_lee, slider_mimax_lee
    spin_mimax_lee = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_mimax_lee.place(x = 15, y = 37)
    slider_mimax_lee = ttk.Scale(frame, variable=input, from_= 0.01, to = 1.5, orient='horizontal',length = 60)
    slider_mimax_lee.place(x = 59, y = 32) 

def entr_simul_ks_contois(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_ks_contois, slider_ks_contois
    spin_ks_contois = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_ks_contois.place(x = 15, y = 94)
    slider_ks_contois = ttk.Scale(frame, variable=input, from_= 0.01, to = 30, orient='horizontal',length = 100)
    slider_ks_contois.place(x = 58, y = 91)
def entr_simul_ks_monod(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_ks_monod, slider_ks_monod
    spin_ks_monod = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_ks_monod.place(x = 15, y = 94)
    slider_ks_monod = ttk.Scale(frame, variable=input, from_= 0.01, to = 30, orient='horizontal',length = 100)
    slider_ks_monod.place(x = 58, y = 91)
def entr_simul_ks_moser(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_ks_moser, slider_ks_moser
    spin_ks_moser = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_ks_moser.place(x = 15, y = 94)
    slider_ks_moser = ttk.Scale(frame, variable=input, from_= 0.01, to = 30, orient='horizontal',length = 100)
    slider_ks_moser.place(x = 58, y = 91)
def entr_simul_ks_andrews(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_ks_andrews, slider_ks_andrews
    spin_ks_andrews = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_ks_andrews.place(x = 15, y = 94)
    slider_ks_andrews = ttk.Scale(frame, variable=input, from_= 0.01, to = 30, orient='horizontal',length = 100)
    slider_ks_andrews.place(x = 58, y = 91)
def entr_simul_ks_wu(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_ks_wu, slider_ks_wu
    spin_ks_wu = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_ks_wu.place(x = 15, y = 94)
    slider_ks_wu = ttk.Scale(frame, variable=input, from_= 0.01, to = 30, orient='horizontal',length = 100)
    slider_ks_wu.place(x = 58, y = 91)
def entr_simul_ks_aiba(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_ks_aiba, slider_ks_aiba
    spin_ks_aiba = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_ks_aiba.place(x = 15, y = 94)
    slider_ks_aiba = ttk.Scale(frame, variable=input, from_= 0.01, to = 30, orient='horizontal',length = 100)
    slider_ks_aiba.place(x = 58, y = 91)
def entr_simul_ks_h_h(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_ks_h_h, slider_ks_h_h
    spin_ks_h_h = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_ks_h_h.place(x = 15, y = 94)
    slider_ks_h_h = ttk.Scale(frame, variable=input, from_= 0.01, to = 30, orient='horizontal',length = 100)
    slider_ks_h_h.place(x = 58, y = 91)
def entr_simul_ks_levenspiel(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_ks_levenspiel, slider_ks_levenspiel
    spin_ks_levenspiel = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_ks_levenspiel.place(x = 15, y = 94)
    slider_ks_levenspiel = ttk.Scale(frame, variable=input, from_= 0.01, to = 30, orient='horizontal',length = 100)
    slider_ks_levenspiel.place(x = 58, y = 91)
def entr_simul_ks_lee(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_ks_lee, slider_ks_lee
    spin_ks_lee = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_ks_lee.place(x = 15, y = 94)
    slider_ks_lee = ttk.Scale(frame, variable=input, from_= 0.01, to = 30, orient='horizontal',length = 100)
    slider_ks_lee.place(x = 58, y = 91)
    
def entr_simul_kd_contois(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_kd_contois, slider_kd_contois
    spin_kd_contois = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_kd_contois.place(x = 15, y = 157)
    slider_kd_contois = ttk.Scale(frame, variable=input, from_= 0.0, to = 1, orient='horizontal',length = 55)
    slider_kd_contois.place(x = 58, y = 154) 
def entr_simul_kd_monod(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_kd_monod, slider_kd_monod
    spin_kd_monod = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_kd_monod.place(x = 15, y = 157)
    slider_kd_monod = ttk.Scale(frame, variable=input, from_= 0.0, to = 1, orient='horizontal',length = 55)
    slider_kd_monod.place(x = 58, y = 154) 
def entr_simul_kd_moser(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_kd_moser, slider_kd_moser
    spin_kd_moser = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_kd_moser.place(x = 15, y = 157)
    slider_kd_moser = ttk.Scale(frame, variable=input, from_= 0.0, to = 1, orient='horizontal',length = 55)
    slider_kd_moser.place(x = 58, y = 154) 
def entr_simul_kd_andrews(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_kd_andrews, slider_kd_andrews
    spin_kd_andrews = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_kd_andrews.place(x = 15, y = 157)
    slider_kd_andrews = ttk.Scale(frame, variable=input, from_= 0.0, to = 1, orient='horizontal',length = 55)
    slider_kd_andrews.place(x = 58, y = 154) 
def entr_simul_kd_wu(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_kd_wu, slider_kd_wu
    spin_kd_wu = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_kd_wu.place(x = 15, y = 157)
    slider_kd_wu = ttk.Scale(frame, variable=input, from_= 0.0, to = 1, orient='horizontal',length = 55)
    slider_kd_wu.place(x = 58, y = 154)
def entr_simul_kd_aiba(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_kd_aiba, slider_kd_aiba
    spin_kd_aiba = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_kd_aiba.place(x = 15, y = 157)
    slider_kd_aiba = ttk.Scale(frame, variable=input, from_= 0.0, to = 1, orient='horizontal',length = 55)
    slider_kd_aiba.place(x = 58, y = 154)
def entr_simul_kd_h_h(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_kd_h_h, slider_kd_h_h
    spin_kd_h_h = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_kd_h_h.place(x = 15, y = 157)
    slider_kd_h_h = ttk.Scale(frame, variable=input, from_= 0.0, to = 1, orient='horizontal',length = 55)
    slider_kd_h_h.place(x = 58, y = 154)
def entr_simul_kd_levenspiel(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_kd_levenspiel, slider_kd_levenspiel
    spin_kd_levenspiel = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_kd_levenspiel.place(x = 15, y = 157)
    slider_kd_levenspiel = ttk.Scale(frame, variable=input, from_= 0.0, to = 1, orient='horizontal',length = 55)
    slider_kd_levenspiel.place(x = 58, y = 154)
def entr_simul_kd_lee(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_kd_lee, slider_kd_lee
    spin_kd_lee = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_kd_lee.place(x = 15, y = 157)
    slider_kd_lee = ttk.Scale(frame, variable=input, from_= 0.0, to = 1, orient='horizontal',length = 55)
    slider_kd_lee.place(x = 58, y = 154)
    
def entr_simul_yxs_contois(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_yxs_contois, slider_yxs_contois
    spin_yxs_contois = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_yxs_contois.place(x = 145, y = 157)
    slider_yxs_contois = ttk.Scale(frame, variable=input, from_= 0.0, to = 3, orient='horizontal',length = 80)
    slider_yxs_contois.place(x = 188, y = 154) 
def entr_simul_yxs_monod(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_yxs_monod, slider_yxs_monod
    spin_yxs_monod = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_yxs_monod.place(x = 145, y = 157)
    slider_yxs_monod = ttk.Scale(frame, variable=input, from_= 0.0, to = 3, orient='horizontal',length = 80)
    slider_yxs_monod.place(x = 188, y = 154) 
def entr_simul_yxs_moser(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_yxs_moser, slider_yxs_moser
    spin_yxs_moser = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_yxs_moser.place(x = 145, y = 157)
    slider_yxs_moser = ttk.Scale(frame, variable=input, from_= 0.0, to = 3, orient='horizontal',length = 80)
    slider_yxs_moser.place(x = 188, y = 154) 
def entr_simul_yxs_andrews(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_yxs_andrews, slider_yxs_andrews
    spin_yxs_andrews = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_yxs_andrews.place(x = 145, y = 157)
    slider_yxs_andrews = ttk.Scale(frame, variable=input, from_= 0.0, to = 3, orient='horizontal',length = 80)
    slider_yxs_andrews.place(x = 188, y = 154) 
def entr_simul_yxs_wu(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_yxs_wu, slider_yxs_wu
    spin_yxs_wu = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_yxs_wu.place(x = 145, y = 157)
    slider_yxs_wu = ttk.Scale(frame, variable=input, from_= 0.0, to = 3, orient='horizontal',length = 80)
    slider_yxs_wu.place(x = 188, y = 154)
def entr_simul_yxs_aiba(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_yxs_aiba, slider_yxs_aiba
    spin_yxs_aiba = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_yxs_aiba.place(x = 145, y = 157)
    slider_yxs_aiba = ttk.Scale(frame, variable=input, from_= 0.0, to = 3, orient='horizontal',length = 80)
    slider_yxs_aiba.place(x = 188, y = 154) 
def entr_simul_yxs_h_h(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_yxs_h_h, slider_yxs_h_h
    spin_yxs_h_h = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_yxs_h_h.place(x = 145, y = 157)
    slider_yxs_h_h = ttk.Scale(frame, variable=input, from_= 0.0, to = 3, orient='horizontal',length = 80)
    slider_yxs_h_h.place(x = 188, y = 154) 
def entr_simul_yxs_levenspiel(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_yxs_levenspiel, slider_yxs_levenspiel
    spin_yxs_levenspiel = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_yxs_levenspiel.place(x = 145, y = 157)
    slider_yxs_levenspiel = ttk.Scale(frame, variable=input, from_= 0.0, to = 3, orient='horizontal',length = 80)
    slider_yxs_levenspiel.place(x = 188, y = 154) 
def entr_simul_yxs_lee(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_yxs_lee, slider_yxs_lee
    spin_yxs_lee = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_yxs_lee.place(x = 145, y = 157)
    slider_yxs_lee = ttk.Scale(frame, variable=input, from_= 0.0, to = 3, orient='horizontal',length = 80)
    slider_yxs_lee.place(x = 188, y = 154)
    
def entr_simul_alfa_contois(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_alfa_contois, slider_alfa_contois
    spin_alfa_contois = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_alfa_contois.place(x = 15, y = 213)
    slider_alfa_contois = ttk.Scale(frame, variable=input, from_= 0.01, to = 10, orient='horizontal',length = 90)
    slider_alfa_contois.place(x = 58, y = 209)
def entr_simul_alfa_monod(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_alfa_monod, slider_alfa_monod
    spin_alfa_monod = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_alfa_monod.place(x = 15, y = 213)
    slider_alfa_monod = ttk.Scale(frame, variable=input, from_= 0.01, to = 10, orient='horizontal',length = 90)
    slider_alfa_monod.place(x = 58, y = 209)
def entr_simul_alfa_moser(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_alfa_moser, slider_alfa_moser
    spin_alfa_moser = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_alfa_moser.place(x = 15, y = 213)
    slider_alfa_moser = ttk.Scale(frame, variable=input, from_= 0.01, to = 10, orient='horizontal',length = 90)
    slider_alfa_moser.place(x = 58, y = 209)
def entr_simul_alfa_andrews(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_alfa_andrews, slider_alfa_andrews
    spin_alfa_andrews = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_alfa_andrews.place(x = 15, y = 213)
    slider_alfa_andrews = ttk.Scale(frame, variable=input, from_= 0.01, to = 10, orient='horizontal',length = 90)
    slider_alfa_andrews.place(x = 58, y = 209)
def entr_simul_alfa_wu(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_alfa_wu, slider_alfa_wu
    spin_alfa_wu= tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_alfa_wu.place(x = 15, y = 213)
    slider_alfa_wu = ttk.Scale(frame, variable=input, from_= 0.01, to = 10, orient='horizontal',length = 90)
    slider_alfa_wu.place(x = 58, y = 209)
def entr_simul_alfa_aiba(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_alfa_aiba, slider_alfa_aiba
    spin_alfa_aiba= tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_alfa_aiba.place(x = 15, y = 213)
    slider_alfa_aiba = ttk.Scale(frame, variable=input, from_= 0.01, to = 10, orient='horizontal',length = 90)
    slider_alfa_aiba.place(x = 58, y = 209)
def entr_simul_alfa_h_h(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_alfa_h_h, slider_alfa_h_h
    spin_alfa_h_h= tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_alfa_h_h.place(x = 15, y = 213)
    slider_alfa_h_h = ttk.Scale(frame, variable=input, from_= 0.01, to = 10, orient='horizontal',length = 90)
    slider_alfa_h_h.place(x = 58, y = 209)
def entr_simul_alfa_levenspiel(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_alfa_levenspiel, slider_alfa_levenspiel
    spin_alfa_levenspiel= tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_alfa_levenspiel.place(x = 15, y = 213)
    slider_alfa_levenspiel = ttk.Scale(frame, variable=input, from_= 0.01, to = 10, orient='horizontal',length = 90)
    slider_alfa_levenspiel.place(x = 58, y = 209)
def entr_simul_alfa_lee(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_alfa_lee, slider_alfa_lee
    spin_alfa_lee= tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_alfa_lee.place(x = 15, y = 213)
    slider_alfa_lee = ttk.Scale(frame, variable=input, from_= 0.01, to = 10, orient='horizontal',length = 90)
    slider_alfa_lee.place(x = 58, y = 209)
    
def entr_simul_beta_contois(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_beta_contois, slider_beta_contois
    spin_beta_contois = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_beta_contois.place(x = 160, y = 213)
    slider_beta_contois = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 90)
    slider_beta_contois.place(x = 203, y = 209)
def entr_simul_beta_monod(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_beta_monod, slider_beta_monod
    spin_beta_monod = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_beta_monod.place(x = 160, y = 213)
    slider_beta_monod = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 90)
    slider_beta_monod.place(x = 203, y = 209)
def entr_simul_beta_moser(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_beta_moser, slider_beta_moser
    spin_beta_moser = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_beta_moser.place(x = 160, y = 213)
    slider_beta_moser = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 90)
    slider_beta_moser.place(x = 203, y = 209)
def entr_simul_beta_andrews(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_beta_andrews, slider_beta_andrews
    spin_beta_andrews = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_beta_andrews.place(x = 160, y = 213)
    slider_beta_andrews = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 90)
    slider_beta_andrews.place(x = 203, y = 209)
def entr_simul_beta_wu(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_beta_wu, slider_beta_wu
    spin_beta_wu = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_beta_wu.place(x = 160, y = 213)
    slider_beta_wu = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 90)
    slider_beta_wu.place(x = 203, y = 209)
def entr_simul_beta_aiba(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_beta_aiba, slider_beta_aiba
    spin_beta_aiba = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_beta_aiba.place(x = 160, y = 213)
    slider_beta_aiba = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 90)
    slider_beta_aiba.place(x = 203, y = 209)
def entr_simul_beta_h_h(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_beta_h_h, slider_beta_h_h
    spin_beta_h_h = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_beta_h_h.place(x = 160, y = 213)
    slider_beta_h_h = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 90)
    slider_beta_h_h.place(x = 203, y = 209) 
def entr_simul_beta_levenspiel(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_beta_levenspiel, slider_beta_levenspiel
    spin_beta_levenspiel = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_beta_levenspiel.place(x = 160, y = 213)
    slider_beta_levenspiel = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 90)
    slider_beta_levenspiel.place(x = 203, y = 209)
def entr_simul_beta_lee(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_beta_lee, slider_beta_lee
    spin_beta_lee = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_beta_lee.place(x = 160, y = 213)
    slider_beta_lee = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 90)
    slider_beta_lee.place(x = 203, y = 209)   
        
def entr_simul_u(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.5)
    global spin_u, slider_u
    spin_u = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_u.place(x = 160, y = 37)
    slider_u = ttk.Scale(frame, variable=input, from_= 0.5, to = 3, orient='horizontal',length = 80)
    slider_u.place(x = 203, y = 32)
    
def entr_simul_kis(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_kis, slider_kis
    spin_kis = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_kis.place(x = 140, y = 37)
    slider_kis = ttk.Scale(frame, variable=input, from_= 0.01, to = 100, orient='horizontal',length = 110)
    slider_kis.place(x = 183, y = 32)
    
def entr_simul_ke(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_ke, slider_ke
    spin_ke = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_ke.place(x = 140, y = 37)
    slider_ke = ttk.Scale(frame, variable=input, from_= 0.01, to = 100, orient='horizontal',length = 110)
    slider_ke.place(x = 183, y = 32)
    
def entr_simul_v(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_v, slider_v
    spin_v = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_v.place(x = 165, y = 94)
    slider_v = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 85)
    slider_v.place(x = 208, y = 91)
    
def entr_simul_kp_aiba(frame):
    input = tk.DoubleVar(value=0.0)
    global spin_kp_aiba, slider_kp_aiba
    spin_kp_aiba = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_kp_aiba.place(x = 160, y = 37)
    slider_kp_aiba = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 85)
    slider_kp_aiba.place(x = 203, y = 32)
    
def entr_simul_kp_h_h(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_kp_h_h, slider_kp_h_h
    spin_kp_h_h = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_kp_h_h.place(x = 140, y = 37)
    slider_kp_h_h = ttk.Scale(frame, variable=input, from_= 0.0, to = 100, orient='horizontal',length = 110)
    slider_kp_h_h.place(x = 183, y = 32)
    
def entr_simul_cp_estr(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_cp_estr, slider_cp_estr
    spin_cp_estr = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_cp_estr.place(x = 140, y = 37)
    slider_cp_estr = ttk.Scale(frame, variable=input, from_= 0.01, to = 100, orient='horizontal',length = 110)
    slider_cp_estr.place(x = 183, y = 32)
    
def entr_simul_cx_estr(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_cx_estr, slider_cx_estr
    spin_cx_estr = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_cx_estr.place(x = 140, y = 37)
    slider_cx_estr = ttk.Scale(frame, variable=input, from_= 0.01, to = 100, orient='horizontal',length = 110)
    slider_cx_estr.place(x = 183, y = 32)
    
def entr_simul_n(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_n, slider_n
    spin_n = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_n.place(x = 165, y = 94)
    slider_n = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 85)
    slider_n.place(x = 208, y = 91)
    
def entr_simul_m(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_m, slider_m
    spin_m = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_m.place(x = 165, y = 94)
    slider_m = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 85)
    slider_m.place(x = 208, y = 91)


# Caixas separadoras - SIMULAÇÃO:
def caix_simul(frame, larg, alt, x, y):
    Label(frame, width = larg, height = alt, borderwidth = 5,relief = "sunken").place(x = x, y = y)
# Escritos:
def labels(frame, texto, fonte, borda, x, y):
    Label(frame, text = texto, font = fonte, relief = borda).place(x = x, y = y)

# Defindo as entradas para o console:
def entr_contois(frame):
    global entr_Cx0_contois, entr_Cs0_contois, entr_Cp0_contois, entr_t0_contois, entr_tf_contois
    entr_Cx0_contois = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_Cx0_contois.place(x = 50, y = 257)
    entr_Cs0_contois = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_Cs0_contois.place(x = 140, y = 257)
    entr_Cp0_contois = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey50", fg = "white")
    entr_Cp0_contois.place(x = 230, y = 257)
    entr_t0_contois = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_t0_contois.place(x = 50, y = 287)
    entr_tf_contois = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_tf_contois.place(x = 140, y = 287)    

def entr_monod(frame):
    global entr_Cx0_monod, entr_Cs0_monod, entr_Cp0_monod, entr_t0_monod, entr_tf_monod
    entr_Cx0_monod = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_Cx0_monod.place(x = 50, y = 257)
    entr_Cs0_monod = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_Cs0_monod.place(x = 140, y = 257)
    entr_Cp0_monod = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey50", fg = "white")
    entr_Cp0_monod.place(x = 230, y = 257)
    entr_t0_monod = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_t0_monod.place(x = 50, y = 287)
    entr_tf_monod = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_tf_monod.place(x = 140, y = 287) 
    
def entr_moser(frame):
    global entr_Cx0_moser, entr_Cs0_moser, entr_Cp0_moser, entr_t0_moser, entr_tf_moser
    entr_Cx0_moser = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_Cx0_moser.place(x = 50, y = 257)
    entr_Cs0_moser = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_Cs0_moser.place(x = 140, y = 257)
    entr_Cp0_moser = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey50", fg = "white")
    entr_Cp0_moser.place(x = 230, y = 257)
    entr_t0_moser = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_t0_moser.place(x = 50, y = 287)
    entr_tf_moser = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_tf_moser.place(x = 140, y = 287) 

def entr_andrews(frame):
    global entr_Cx0_andrews, entr_Cs0_andrews, entr_Cp0_andrews, entr_t0_andrews, entr_tf_andrews
    entr_Cx0_andrews = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_Cx0_andrews.place(x = 50, y = 257)
    entr_Cs0_andrews = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_Cs0_andrews.place(x = 140, y = 257)
    entr_Cp0_andrews = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey50", fg = "white")
    entr_Cp0_andrews.place(x = 230, y = 257)
    entr_t0_andrews = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_t0_andrews.place(x = 50, y = 287)
    entr_tf_andrews = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_tf_andrews.place(x = 140, y = 287)

def entr_wu(frame):
    global entr_Cx0_wu, entr_Cs0_wu, entr_Cp0_wu, entr_t0_wu, entr_tf_wu
    entr_Cx0_wu = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_Cx0_wu.place(x = 50, y = 257)
    entr_Cs0_wu = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_Cs0_wu.place(x = 140, y = 257)
    entr_Cp0_wu = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey50", fg = "white")
    entr_Cp0_wu.place(x = 230, y = 257)
    entr_t0_wu = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_t0_wu.place(x = 50, y = 287)
    entr_tf_wu = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_tf_wu.place(x = 140, y = 287)
    
def entr_aiba(frame):
    global entr_Cx0_aiba, entr_Cs0_aiba, entr_Cp0_aiba, entr_t0_aiba, entr_tf_aiba
    entr_Cx0_aiba = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_Cx0_aiba.place(x = 50, y = 257)
    entr_Cs0_aiba = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_Cs0_aiba.place(x = 140, y = 257)
    entr_Cp0_aiba = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey50", fg = "white")
    entr_Cp0_aiba.place(x = 230, y = 257)
    entr_t0_aiba = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_t0_aiba.place(x = 50, y = 287)
    entr_tf_aiba = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_tf_aiba.place(x = 140, y = 287)

def entr_h_h(frame):
    global entr_Cx0_h_h, entr_Cs0_h_h, entr_Cp0_h_h, entr_t0_h_h, entr_tf_h_h
    entr_Cx0_h_h = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_Cx0_h_h.place(x = 50, y = 257)
    entr_Cs0_h_h = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_Cs0_h_h.place(x = 140, y = 257)
    entr_Cp0_h_h = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey50", fg = "white")
    entr_Cp0_h_h.place(x = 230, y = 257)
    entr_t0_h_h = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_t0_h_h.place(x = 50, y = 287)
    entr_tf_h_h = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_tf_h_h.place(x = 140, y = 287)

def entr_levenspiel(frame):
    global entr_Cx0_levenspiel, entr_Cs0_levenspiel, entr_Cp0_levenspiel, entr_t0_levenspiel, entr_tf_levenspiel
    entr_Cx0_levenspiel = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_Cx0_levenspiel.place(x = 50, y = 257)
    entr_Cs0_levenspiel = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_Cs0_levenspiel.place(x = 140, y = 257)
    entr_Cp0_levenspiel = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey50", fg = "white")
    entr_Cp0_levenspiel.place(x = 230, y = 257)
    entr_t0_levenspiel = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_t0_levenspiel.place(x = 50, y = 287)
    entr_tf_levenspiel = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_tf_levenspiel.place(x = 140, y = 287)

def entr_lee(frame):
    global entr_Cx0_lee, entr_Cs0_lee, entr_Cp0_lee, entr_t0_lee, entr_tf_lee
    entr_Cx0_lee = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_Cx0_lee.place(x = 50, y = 257)
    entr_Cs0_lee = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_Cs0_lee.place(x = 140, y = 257)
    entr_Cp0_lee = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey50", fg = "white")
    entr_Cp0_lee.place(x = 230, y = 257)
    entr_t0_lee = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey30", fg = "white")
    entr_t0_lee.place(x = 50, y = 287)
    entr_tf_lee = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "grey40", fg = "white")
    entr_tf_lee.place(x = 140, y = 287)

# Função para definição dos labels - títulos de definição:
def labels_saida(frame):
    labels(frame, texto = "Parâmetros Crescimento", fonte = "batang 8 bold", borda = "flat", x = 115, y = 0)
    labels(frame, texto = u"\u03bcmáx (h\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 14)
    labels(frame, texto = "Parâmetros Balanço Massa", fonte = "batang 8 bold", borda = "flat", x = 100, y = 117)
    labels(frame, texto = u"Kd (h\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 132)
    labels(frame, texto = u"Yxs (gx.gs\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 228, y = 132)
    labels(frame, texto = u"\u03B1(gx.gp\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 189)
    labels(frame, texto = u"\u03B2[gx.(gp.h)\u207b\u00b9]", fonte = "times 9 bold", borda = "sunken", x = 226, y = 189)
    labels(frame, texto = "Variáveis Operacionais", fonte = "batang 8 bold", borda = "flat", x = 123, y = 234)
    labels(frame, texto = "Cx0:", fonte = "times 10 bold", borda = "flat", x = 18, y = 255)
    labels(frame, texto = "Cs0:", fonte = "times 10 bold", borda = "flat", x = 108, y = 255)
    labels(frame, texto = "Cp0:", fonte = "times 10 bold", borda = "flat", x = 198, y = 255)
    labels(frame, texto = "t0(h):", fonte = "times 10 bold", borda = "flat", x = 13, y = 285)
    labels(frame, texto = "tf(h):", fonte = "times 10 bold", borda = "flat", x = 107, y = 285)

# Função separação física simulação:
def separ_simul(frame):
    caix_simul(frame, larg = 40, alt = 7, x = 5, y = 5)
    caix_simul(frame, larg = 40, alt = 7, x = 5, y = 123)
    caix_simul(frame, larg = 40, alt = 4, x = 5, y = 240)
    
## Contois:
def contois():
    separ_simul(frame13)
    labels_saida(frame13)
    labels(frame = frame13, texto = "KSX (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 70)
    entr_simul_mimax_contois(frame13)
    entr_simul_ks_contois(frame13)
    entr_simul_kd_contois(frame13)
    entr_simul_yxs_contois(frame13)
    entr_simul_alfa_contois(frame13)
    entr_simul_beta_contois(frame13)
    entr_contois(frame13)
    Button(frame13, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 5, relief = "sunken", command = capt_val_esc_contois).place(x = 245, y = 290)  

## Monod:
def monod():
    separ_simul(frame14)
    labels_saida(frame14)
    labels(frame = frame14, texto = "Ks (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 70)
    entr_simul_mimax_monod(frame14)
    entr_simul_ks_monod(frame14)
    entr_simul_kd_monod(frame14)
    entr_simul_yxs_monod(frame14)
    entr_simul_alfa_monod(frame14)
    entr_simul_beta_monod(frame14)
    entr_monod(frame14)
    Button(frame14, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 5, relief = "sunken", command = capt_val_esc_monod).place(x = 245, y = 290) 
   
## Moser:
def moser():
    separ_simul(frame15)
    labels_saida(frame15)
    labels(frame = frame15, texto = "Ks (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 70)
    labels(frame = frame15, texto = "u (adim)", fonte = "times 9 bold", borda = "sunken", x = 251, y = 14)
    entr_simul_mimax_moser(frame15)
    entr_simul_ks_moser(frame15)
    entr_simul_kd_moser(frame15)
    entr_simul_yxs_moser(frame15)
    entr_simul_alfa_moser(frame15)
    entr_simul_beta_moser(frame15)
    entr_simul_u(frame15)
    entr_moser(frame15)
    Button(frame15, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 5, relief = "sunken", command = capt_val_esc_moser).place(x = 245, y = 290)

## Andrews:
def andrews():
    separ_simul(frame16)
    labels_saida(frame16)
    labels(frame = frame16, texto = "Ks (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 70)
    labels(frame = frame16, texto = "KSI (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 236, y = 14)
    entr_simul_mimax_andrews(frame16)
    entr_simul_ks_andrews(frame16)
    entr_simul_kd_andrews(frame16)
    entr_simul_yxs_andrews(frame16)
    entr_simul_alfa_andrews(frame16)
    entr_simul_beta_andrews(frame16)
    entr_simul_kis(frame16)
    entr_andrews(frame16)
    Button(frame16, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 5, relief = "sunken", command = capt_val_esc_andrews).place(x = 245, y = 290)
    
## Wu et al:
def wu():
    separ_simul(frame17)
    labels_saida(frame17)
    labels(frame = frame17, texto = "Ks (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 70)
    labels(frame = frame17, texto = "Ke (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 242, y = 14)
    labels(frame = frame17, texto = "v (adim)", fonte = "times 9 bold", borda = "sunken", x = 252, y = 70)
    entr_simul_mimax_wu(frame17)
    entr_simul_ks_wu(frame17)
    entr_simul_kd_wu(frame17)
    entr_simul_yxs_wu(frame17)
    entr_simul_alfa_wu(frame17)
    entr_simul_beta_wu(frame17)
    entr_simul_ke(frame17)
    entr_simul_v(frame17)
    entr_wu(frame17)
    Button(frame17, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 5, relief = "sunken", command = capt_val_esc_wu).place(x = 245, y = 290)

## Aiba et al:
def aiba():
    separ_simul(frame18)
    labels_saida(frame18)
    labels(frame = frame18, texto = "Ks (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 70)
    labels(frame = frame18, texto = "Kp (L.g\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 242, y = 14)
    entr_simul_mimax_aiba(frame18)
    entr_simul_ks_aiba(frame18)
    entr_simul_kd_aiba(frame18)
    entr_simul_yxs_aiba(frame18)
    entr_simul_alfa_aiba(frame18)
    entr_simul_beta_aiba(frame18)
    entr_simul_kp_aiba(frame18)
    entr_aiba(frame18)
    Button(frame18, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 5, relief = "sunken", command = capt_val_esc_aiba).place(x = 245, y = 290)

## Hope & Hansford:
def hope_hansford():
    separ_simul(frame19)
    labels_saida(frame19)
    labels(frame = frame19, texto = "Ks (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 70)
    labels(frame = frame19, texto = "Kp (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 242, y = 14)
    entr_simul_mimax_h_h(frame19)
    entr_simul_ks_h_h(frame19)
    entr_simul_kd_h_h(frame19)
    entr_simul_yxs_h_h(frame19)
    entr_simul_alfa_h_h(frame19)
    entr_simul_beta_h_h(frame19)
    entr_simul_kp_h_h(frame19)
    entr_h_h(frame19)
    Button(frame19, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 5, relief = "sunken", command = capt_val_esc_h_h).place(x = 245, y = 290)
    
## Levenspiel:
def levenspiel():
    separ_simul(frame20)
    labels_saida(frame20)
    labels(frame = frame20, texto = "Ks (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 70)
    labels(frame = frame20, texto = "Cp* (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 236, y = 14)
    labels(frame = frame20, texto = "n (adim)", fonte = "times 9 bold", borda = "sunken", x = 252, y = 70)
    entr_simul_mimax_levenspiel(frame20)
    entr_simul_ks_levenspiel(frame20)
    entr_simul_kd_levenspiel(frame20)
    entr_simul_yxs_levenspiel(frame20)
    entr_simul_alfa_levenspiel(frame20)
    entr_simul_beta_levenspiel(frame20)
    entr_simul_cp_estr(frame20)
    entr_simul_n(frame20)
    entr_levenspiel(frame20)
    Button(frame20, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 5, relief = "sunken", command = capt_val_esc_levenspiel).place(x = 245, y = 290)

## Lee et al:
def lee():
    separ_simul(frame21)
    labels_saida(frame21)
    labels(frame = frame21, texto = "Ks (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 70)
    labels(frame = frame21, texto = "Cx* (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 236, y = 14)
    labels(frame = frame21, texto = "m (adim)", fonte = "times 9 bold", borda = "sunken", x = 249, y = 70)
    entr_simul_mimax_lee(frame21)
    entr_simul_ks_lee(frame21)
    entr_simul_kd_lee(frame21)
    entr_simul_yxs_lee(frame21)
    entr_simul_alfa_lee(frame21)
    entr_simul_beta_lee(frame21)
    entr_simul_cx_estr(frame21)
    entr_simul_m(frame21)
    entr_lee(frame21)
    Button(frame21, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 5, relief = "sunken", command = capt_val_esc_lee).place(x = 245, y = 290)


def print_me_1():
        value_1 = combo_1.get()
        print(value_1)
        if value_1 == "AUSÊNCIA DE INIBIÇÃO":
            notebook_sem_inib_simul()
            contois()
            monod()
            moser()
        if value_1 == "INIBIÇÃO PELO SUBSTRATO":
            notebook_inib_subs_simul()
            andrews()
            wu()
        if value_1 == "INIBIÇÃO PELO PRODUTO":
            notebook_inib_prod_simul()
            aiba()
            hope_hansford()
            levenspiel()
        if value_1 == "INIBIÇÃO PELA BIOMASSA":
            notebook_inib_biomas_simul()
            lee()
            
Button(frame1, text="Pronto", bg = "black", fg="white", font="batang 12", command = print_me_1).place(x = 315, y = 29)


## Botão para puxar os valores de entrada ao console - SIMULAÇÃO:
#Button(frame13, text = "Enviar valores", font = "batang 9 bold", fg = "white", bg = "black", borderwidth = 3, relief = "sunken", command = capt_val_esc).place(x = 295, y = 300) 

# AVIS0:
labels(frame = frame1, texto = "Por favor, entre com valores para Cx0, Cs0 e Cp0 em unidades g/L", fonte = "times 9 bold", borda = "flat", x = 15, y = 480)



# Encerramento da interface:
janela.mainloop()

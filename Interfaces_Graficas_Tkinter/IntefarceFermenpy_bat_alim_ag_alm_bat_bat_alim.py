# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 12:53:34 2020

@author: Bruna Aparecida
"""

            ### *** INTERFACE FERMENPY PARA SIMULAÇÃO E MODELAGEM DE PFM EM BATELADA ALIMENTADA *** ###
                                 ## ** vazão constante, linear e exponencial ** ##

# Importação das bibliotecas, pacotes e módulos:
## Módulos propriamente construídos
### * Cinética com ausência de inibição * ###
import Modulos_Monod_bat_alim
import Modulos_Contois_bat_alim
import Modulos_Moser_bat_alim
#import Modulos_mi_constante_bat_alim
### * Cinética com inibição por acúmulo de substrato * ###:
import Modulos_Andrews_bat_alim
import Modulos_Wu_et_al_bat_alim
### * Cinética com inibição por acúmulo de produto * ###:
import Modulos_Aiba_et_al_bat_alim
import Modulos_Hoppe_Hansford_bat_alim
import Modulos_Levenspiel_bat_alim
### * Cinética com inibição por acúmulo de células (biomassa) * ###:
import Modulos_Lee_et_al_bat_alim
### * Módulos auxiliares * ### - documentação e limites para convergência
import Modulo_peso_limite_AG_bat_alim
#import Modulo_documentacao
## Bibliotecas científicas
## ** BACK-END ** ##
### * Base para operações matemáticas * ### - cálculos vetoriais, com dataframes e estatísticos
import numpy as np 
import pandas as pd 
import scipy.stats as sc
import math
### * Integração numérica * ###
from scipy.integrate import odeint
### * Convergência * ### - otimização por AG e ALM
from scipy.optimize import differential_evolution
from scipy.optimize import leastsq
### * Plotagem gráfica * ###
import matplotlib.pyplot as plt
## ** FRONT-END ** ##
### * Interface gráfica de usuário GUI * ### - geração da GUI, contagem de tempo, explorador de arquivos, som, imagens e gráficos embutidas
import time
import tkinter as tk
from tkinter import *
from tkinter import Label, Button
from tkinter.filedialog import askopenfilename # caixa externa - explorar files no computador
import os # divisão de strings
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from tkinter.ttk import Combobox
from tkinter.filedialog import asksaveasfilename
from tkinter import colorchooser
import winsound
from tkinter import ttk
import webbrowser

                                    #### **** INÍCIO DO DESENVOLVIMENTO DO PROGRAMA **** ####

# Criação da interface:
janela = Tk()
janela.title("*Fermenpy BA-I*")
janela.geometry("600x300")
titulo = Label(janela, text="MODELOS CINÉTICOS NÃO ESTRUTURADOS", font="times 16 bold", fg="BLACK", borderwidth=2, relief="groove").place(x=430,y=0)

# Carregar a imagem do logo:
load = Image.open("Logo.png")
render = ImageTk.PhotoImage(load)
img = Label(janela, image = render, border = 0, borderwidth = 3, relief = "sunken")
img.image = render
img.place(x = 45, y = 10)
# Identificação da versão do programa:
Label(janela, text = "Simulação e Modelagem para Batelada Alimentada", font = "times 7").place(x = 102, y = 70)

# Criação do notebook - abas seleção simulação ou modelagem
notebook = ttk.Notebook(janela)
notebook.grid(row=3, column =3, sticky=tk.E + tk.W + tk.N + tk.S, padx=30, pady=110)
frame1 = ttk.Frame(notebook, width = 1300, height = 510, borderwidth = 5, relief = tk.SUNKEN)
notebook.add(frame1, text = 'SIMULAÇÃO')
frame2 = ttk.Frame(notebook, width = 1300, height = 510, borderwidth = 5, relief = tk.SUNKEN)
notebook.add(frame2, text = 'MODELAGEM')
frame3 = ttk.Frame(notebook, width = 1300, height = 510, borderwidth = 5, relief = tk.SUNKEN)
notebook.add(frame3, text = 'DOCUMENTAÇÃO')

## Criação dos notebooks para seleção dos modelos, da consulta às figuras geradas e de informações (documentação):
def notebook_sem_inib_model():
    notebook_sem_inib = ttk.Notebook(frame2)
    notebook_sem_inib.grid(row = 3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx = 50, pady = 150)
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
    notebook_sem_inib_sim.grid(row=3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx = 50, pady = 85)
    global frame13
    frame13 = ttk.Frame(notebook_sem_inib_sim, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_sem_inib_sim.add(frame13, text = 'CONTOIS')
    global frame14
    frame14 = ttk.Frame(notebook_sem_inib_sim, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_sem_inib_sim.add(frame14, text = 'MONOD')
    global frame15
    frame15 = ttk.Frame(notebook_sem_inib_sim, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_sem_inib_sim.add(frame15, text = 'MOSER')
    global frame42
    frame42 = ttk.Frame(notebook_sem_inib_sim, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_sem_inib_sim.add(frame42, text = u'\u03bc CONSTANTE')
def notebook_infl_mi_const():
    notebook_infl_mi_const = ttk.Notebook(frame1)
    notebook_infl_mi_const.grid(row=3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx = 50, pady = 85)
    global frame43
    frame43 = ttk.Frame(notebook_infl_mi_const, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_infl_mi_const.add(frame43, text = u'INFLUÊNCIA VALOR DA TAXA \u03bc')
def notebook_inib_subs_model():
    notebook_inib_subs = ttk.Notebook(frame2)
    notebook_inib_subs.grid(row=3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx = 50, pady = 150)
    global frame7
    frame7 = ttk.Frame(notebook_inib_subs, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_subs.add(frame7, text = 'ANDREWS')
    global frame8
    frame8 = ttk.Frame(notebook_inib_subs, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_subs.add(frame8, text = 'WU ET AL')
def notebook_inib_subs_simul():
    notebook_inib_subs_simul = ttk.Notebook(frame1)
    notebook_inib_subs_simul.grid(row=3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx = 50, pady = 85)
    global frame16
    frame16 = ttk.Frame(notebook_inib_subs_simul, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_subs_simul.add(frame16, text = 'ANDREWS')
    global frame17
    frame17 = ttk.Frame(notebook_inib_subs_simul, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_subs_simul.add(frame17, text = 'WU ET AL')
def notebook_inib_prod_model():
    notebook_inib_prod = ttk.Notebook(frame2)
    notebook_inib_prod.grid(row=3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx = 50, pady = 150)
    global frame9
    frame9 = ttk.Frame(notebook_inib_prod, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_prod.add(frame9, text = 'AIBA ET AL')
    global frame10
    frame10 = ttk.Frame(notebook_inib_prod, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_prod.add(frame10, text = 'HOPPE & HANSFORD')
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
    notebook_inib_prod_simul.add(frame19, text = 'HOPPE & HANSFORD')
    global frame20
    frame20 = ttk.Frame(notebook_inib_prod_simul, width = 313, height = 320, borderwidth = 5, relief = tk.GROOVE)
    notebook_inib_prod_simul.add(frame20, text = 'LEVENSPIEL')
def notebook_inib_biomas_model():
    notebook_inib_biomas = ttk.Notebook(frame2)
    notebook_inib_biomas.grid(row=3, column =4, sticky=tk.E + tk.W + tk.N + tk.S, padx = 50, pady = 150)
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
    frame26 = ttk.Frame(notebook_docum, width = 602, height = 310, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame26, text = 'Contois')
    global frame27
    frame27 = ttk.Frame(notebook_docum, width = 602, height = 31, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame27, text = 'Monod')
    global frame28
    frame28 = ttk.Frame(notebook_docum, width = 602, height = 310, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame28, text = 'Moser')
    global frame29
    frame29 = ttk.Frame(notebook_docum, width = 602, height = 310, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame29, text = 'Andrews')
    global frame30
    frame30 = ttk.Frame(notebook_docum, width = 602, height = 310, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame30, text = 'Wu et al')
    global frame31
    frame31 = ttk.Frame(notebook_docum, width = 602, height = 310, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame31, text = 'Aiba et al')
    global frame32
    frame32 = ttk.Frame(notebook_docum, width = 602, height = 310, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame32, text = 'Hoppe & Hansford')
    global frame33
    frame33 = ttk.Frame(notebook_docum, width = 602, height = 310, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame33, text = 'Levenspiel')
    global frame34
    frame34 = ttk.Frame(notebook_docum, width = 602, height = 310, borderwidth = 5, relief = tk.GROOVE)
    notebook_docum.add(frame34, text = 'Lee et al')   
def notebook_algorit():
    notebook_algorit = ttk.Notebook(frame3)
    notebook_algorit.place(x = 660, y = 165)
    global frame35
    frame35 = ttk.Frame(notebook_algorit, width = 600, height = 230, borderwidth = 5, relief = tk.GROOVE)
    notebook_algorit.add(frame35, text = 'Integração Numérica')
    global frame36
    frame36 = ttk.Frame(notebook_algorit, width = 600, height = 230, borderwidth = 5, relief = tk.GROOVE)
    notebook_algorit.add(frame36, text = 'Algoritmo Genético')
    global frame37
    frame37 = ttk.Frame(notebook_algorit, width = 600, height = 230, borderwidth = 5, relief = tk.GROOVE)
    notebook_algorit.add(frame37, text = 'Algoritimo de Levenberg-Marquardt')    
def notebook_graf_model():
    notebook_graf_model = ttk.Notebook(frame2)
    notebook_graf_model.place(x = 401, y = 115)
    global frame38
    frame38 = ttk.Frame(notebook_graf_model, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_model.add(frame38, text = u'Concent.t\u207b\u00b9')
    global frame39
    frame39 = ttk.Frame(notebook_graf_model, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_model.add(frame39, text = 'Produtiv. (Px e Pp)')
    global frame40
    frame40 = ttk.Frame(notebook_graf_model, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_model.add(frame40, text = u'Produtiv. (p.x\u207b\u00b9)')
    global frame41
    frame41 = ttk.Frame(notebook_graf_model, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_model.add(frame41, text = u'Taxa \u03bcmáx.t\u207b\u00b9')
    global frame44
    frame44 = ttk.Frame(notebook_graf_model, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_model.add(frame44, text = u'Volume.t\u207b\u00b9')
    global frame45
    frame45 = ttk.Frame(notebook_graf_model, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_model.add(frame45, text = u'Vazão.t\u207b\u00b9')


# Funções de repetição:
## * SAÍDA PARÂMETROS MODELADOS * ##:
def tab_fun_cin():
    load = Image.open("Tabela.png")
    render = ImageTk.PhotoImage(load)
    img = Label(frame2, image = render, border = 0)
    img.image = render
    img.place(x = 930, y = 205)
## * IMPRESSÃO DE IMAGENS * ##:
## Função geral:
def carregar_imagem(frame, imagem, x, y, borderwidth, relief):
    load = Image.open(imagem)
    render = ImageTk.PhotoImage(load)
    img = Label(frame, image = render, border = 0, borderwidth = borderwidth, relief = relief)
    img.image = render
    img.place(x = x, y = y)
## * BOTÃO PARA DOWNLOAD DOS ARQUIVOS EXCEL GERADOS * ##: - vincular com excel concent
def botao_excel(imagem, num_frame, x, y, comando):
        load = Image.open(imagem)
        render = ImageTk.PhotoImage(load)
        img = Button(num_frame, image = render, border = 0, command = comando)
        img.image = render
        img.place(x = x, y = y)
## * ACESSO AOS ARQUIVOS EXCEL DISPONÍVEIS PARA DOWNLOAD:
def aces_arq(frame):
    Label(frame, text = "", borderwidth=3, relief="groove", width = 33, height = 7, bg = "gray45").place(x = 1030, y = 7)
    Label(frame, text = "Acessar Arquivos", font = "arial 8 bold", fg = "white", bg = "black", borderwidth=4, relief="sunken").place(x = 1036, y = 13)
## * ENTRADA PARA PARÂMETROS BATELADA ALIMENTADA * ##
def entry_bat_alim_geral():
    global entr_Q, entr_Cs_alim, entr_V0, entr_tf_bat
    entr_Q = tk.Entry(frame2, width = 7, font = "batang 8 bold", fg = "black", borderwidth = 2, relief = "sunken", bg = "white")
    entr_Q.place(x = 70, y = 90)
    entr_Cs_alim = tk.Entry(frame2, width = 7, font = "batang 8 bold", borderwidth = 2, relief = "sunken", bg = "white", fg = "black")
    entr_Cs_alim.place(x = 210, y = 90)
    entr_V0 = tk.Entry(frame2, width = 7, font = "batang 8 bold", borderwidth = 2, relief = "sunken", bg = "white", fg = "black")
    entr_V0.place(x = 70, y = 120)
    entr_tf_bat = tk.Entry(frame2, width = 7, font = "batang 8 bold", borderwidth = 2, relief = "sunken", bg = "white", fg = "black")
    entr_tf_bat.place(x = 308, y = 90)
    entr_lin_exp = tk.Entry(frame2, width = 7, font = "batang 8 bold", borderwidth = 2, relief = "sunken", bg = "white", fg = "black")
    entr_lin_exp.place(x = 210, y = 120)
    entr_lin_exp.configure(state = "disabled")
def entry_bat_alim_lin_exp():
    global entr_lin_exp
    entr_lin_exp = tk.Entry(frame2, width = 7, font = "batang 8 bold", borderwidth = 2, relief = "sunken", bg = "white", fg = "black")
    entr_lin_exp.place(x = 210, y = 120)
## * BOTÃO PARA ACESSO E EDIÇÃO DOS GRÁFICOS PELA INTERFACE * ##:
# - Salvar e apagar a figura na máquina e na interface, respectivamente:
def botao_com_graf(frame, comando_salvar, comando_destroy, x, y):
      load = Image.open("Salvar.png")
      render = ImageTk.PhotoImage(load)
      img = Button(frame, image = render, border = 0, command = comando_salvar)
      img.image = render
      img.place(x = 451, y = 80)
      load = Image.open("Lixeira.png")
      render = ImageTk.PhotoImage(load)
      img = Button(frame, image = render, border = 0, command = comando_destroy)
      img.image = render
      img.place(x = x, y = y)
# - Alterar as cores das curvas:
def botao_paleta_graf(frame,comando):
    load = Image.open("Paleta.png")
    render = ImageTk.PhotoImage(load)
    img = Button(frame, image = render, border = 0, command = comando)
    img.image = render
    img.place(x = 450, y = 130)
    
    
## * SAÍDAS DA MODELAGEM * ##:
## Caixas de separação:
Label(frame2, text="", width = 52, height = 33, borderwidth = 3,  relief = "sunken", bg = "grey85").place(x = 914, y = 2)
Label(frame2, text="", width = 50, height = 16, borderwidth = 3,  relief = "sunken", bg = "grey75").place(x = 921, y = 201)
## Imagens - tabelas e cronômetro:  
carregar_imagem(frame = frame2, imagem = "Tabela.png", x = 930, y = 205, borderwidth = 0, relief = "flat")
carregar_imagem(frame = frame2, imagem = "Tabela.png", x = 930, y = 366.2, borderwidth = 0, relief = "flat")
carregar_imagem(frame = frame2, imagem = "Cronometro.png", x = 932, y = 296, borderwidth = 0, relief = "flat")
## Caixinhas de saída de valores:
Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
Label(frame2, text = "b", font = "times 42", fg = "grey40", bg = "grey40", width = 3,borderwidth=4, relief ='sunken').place(x = 1160, y = 288.2)
## Indicação escrita - valor função objetiva e R²:
Label(frame2, text = "F. Obj:", font = "broadway 11", fg = "white", bg = "black", justify = "center",  borderwidth=4, relief ='sunken').place(x = 1095, y = 297.2)
Label(frame2, text = u"R\u00b2:", font = "broadway 11", fg = "white", bg = "black", justify = "center",  borderwidth=4, relief ='sunken').place(x = 1124, y = 327.2)
## Indicação da região de acesso:
aces_arq(frame2)


# Seleção do modo de alimentação:
## Combobox:
v_0 = ("Taxa de Vazão Constante", "Taxa de Vazão Linear", "Taxa de Vazão Exponencial")
combo_0 = Combobox(janela, values = v_0, width = 30, font = "arial 10")
combo_0.set("--------ESCOLHA SEU MODELO------------------")
combo_0.place(x = 650, y = 40)
## Indicação do pedido de seleção:
Label(janela, text = "Analisar operação de alimentação à:", font = "Arial 10").place(x = 432, y = 40)
## Status da seleção:
status_01 = Label (janela, width = 33, height = 5, bg = "gray30", relief = "sunken", borderwidth = 3). place (x = 1050, y = 20)
status_02 = Label (janela, text = "Fermentação selecionada", font = "batang 11 bold", fg = "white", bg = "black"). place (x = 1074, y = 30)
status_03 = Label (janela, width = 24, height = 1, bg = "grey40")
status_03.place (x = 1058, y = 65)
status_03.configure(text = "Sistema aguardando", font = "batang 12", bg = "pink", relief = "raised")

def botao_envio_bat_alim(comando, x, y):
    enviar = Button(frame2, text = "Enviar", command = comando)
    enviar.place(x = x, y = y)
# Funções para capturar os valores dos entry:
def pegar_val_alim_const():
    global Q_const, Cs_alim_const, V0_const, tf_bat_const
    Q_const = float(entr_Q.get())
    Cs_alim_const = float(entr_Cs_alim.get())
    V0_const = float(entr_V0.get())
    tf_bat_const = float(entr_tf_bat.get())
    print(Q_const, Cs_alim_const, V0_const, tf_bat_const)
    return(Q_const, Cs_alim_const, V0_const, tf_bat_const)
def pegar_val_alim_lin():
    global Q_lin, Cs_alim_lin, V0_lin, tf_bat_lin, a
    Q_lin = float(entr_Q.get())
    Cs_alim_lin = float(entr_Cs_alim.get())
    V0_lin = float(entr_V0.get())
    tf_bat_lin = float(entr_tf_bat.get())
    a = float(entr_lin_exp.get())
    print(Q_lin, Cs_alim_lin, V0_lin, tf_bat_lin, a)
    return(Q_lin, Cs_alim_lin, V0_lin,tf_bat_lin, a)
def pegar_val_alim_exp():
    global Q_exp, Cs_alim_exp, V0_exp, tf_bat_exp, beta_exp
    Q_exp = float(entr_Q.get())
    Cs_alim_exp = float(entr_Cs_alim.get())
    V0_exp= float(entr_V0.get())
    tf_bat_exp = float(entr_tf_bat.get())
    beta_exp = float(entr_lin_exp.get())
    print(Q_exp, Cs_alim_exp, V0_exp, tf_bat_exp, beta_exp)
    return(Q_exp, Cs_alim_exp, V0_exp, tf_bat_exp, beta_exp)

### Valor do combobox:
def print_alim():
    global def_alim
    def_alim = combo_0.get()
    print(def_alim)
    status_03.configure(text = def_alim, font = "batang 12", bg = "lightgreen", relief = "raised")  
## * ENTRADA DOS VALORES REFERENTES APENAS À BATELADA ALIMENTADA * ##
    # Criação das indicações escritas:
    ## Eixos:
    eixo_Q = Label(frame2, text = u"Q(L.h\u207b\u00b9)", width = 7, font = "times 10 bold", bg = "gray85", fg = "grey45")
    eixo_Q.place(x = 16, y = 90)
    eixo_Cs_alim = Label(frame2, text = u"Cs alim(gs.L\u207b\u00b9)", font = "times 10 bold", bg = "gray85", fg = "grey45")
    eixo_Cs_alim.place(x = 121, y = 90)
    eixo_V0 = Label(frame2, text = "V0(L)", font = "times 10 bold", bg = "gray85", fg = "grey45")
    eixo_V0.place(x = 29, y = 120)
    eixo_tf_bat = Label(frame2, text = "tf bat(h)", font = "times 10 bold", bg = "gray85", fg = "grey45")
    eixo_tf_bat.place(x = 260, y = 90)
    eixo_lin_exp = Label(frame2, text = "a / beta", font = "times 10 bold", width = 5, bg = "gray85", fg = "gray45")
    eixo_lin_exp.place(x = 150, y = 120)
    # Indicação para a entrada dos parâmetros referentes apenas à batelada alimentada pelo tk entry:
    Label(frame2, text = "Insira as constantes relacionadas:", font = "batang 11", bg = "gray85", relief = "raised").place(x = 17, y = 60)
    ## Função para avaliar o tipo de alimentação:
    if (def_alim == "Taxa de Vazão Constante"):
        entry_bat_alim_geral()
        botao_envio_bat_alim(comando = pegar_val_alim_const, x = 313, y = 114)
        eixo_Q.configure(fg = "black")
        eixo_Cs_alim.configure(fg = "black")
        eixo_tf_bat.configure(fg = "black")
        eixo_V0.configure(fg = "black")
    if (def_alim == "Taxa de Vazão Linear"):
        entry_bat_alim_geral()
        entry_bat_alim_lin_exp()
        botao_envio_bat_alim(comando = pegar_val_alim_lin, x = 313, y = 114)
        eixo_Q.configure(text = u"Q0(L.h\u207b\u00b9)", fg = "black")
        eixo_Cs_alim.configure(fg = "black")
        eixo_tf_bat.configure(fg = "black")
        eixo_V0.configure(fg = "black")
        eixo_lin_exp.configure(text = "a", fg = "black")
    if (def_alim == "Taxa de Vazão Exponencial"):
        entry_bat_alim_geral()
        entry_bat_alim_lin_exp()
        botao_envio_bat_alim(comando = pegar_val_alim_exp, x = 313, y = 114)
        eixo_Q.configure(text = u"Q0(L.h\u207b\u00b9)", fg = "black")
        eixo_Cs_alim.configure(fg = "black")
        eixo_tf_bat.configure(fg = "black")
        eixo_V0.configure(fg = "black")
        eixo_lin_exp.configure(text = "beta", fg = "black")
        
    
Button(janela, text = "Confirmar", command = print_alim).place(x = 820, y = 67)


## Seleção da cinética de reação
    
                                            ## ** MODELAGEM ** ##
# Caixas de separação:
Label(frame2, text="", width = 53, height = 33, borderwidth = 3,  relief = "sunken", bg = "grey85").place(x = 10, y = 2)
ttk.Label(frame2, text = "SELECIONE A CINÉTICA DE REAÇÃO:", font = "times 12 bold").place(x = 16, y = 10)
# Combobox:
v_model = ("AUSÊNCIA DE INIBIÇÃO", "INIBIÇÃO PELO SUBSTRATO", "INIBIÇÃO PELO PRODUTO", "INIBIÇÃO PELA BIOMASSA")
combo_2 = Combobox(frame2, values = v_model, width = 39, font = "arial 10")
combo_2.set("-----------------------ESCOLHA-----------------------")
combo_2.place(x = 15, y = 32)

# Importação módulos - modelagem:
## Função com as equações modelo e os parâmetros atribuídos a argumentos 
### * BATELADA * ###:
func_args_Monod = Modulos_Monod_bat_alim.modelag_bat_Monod_func_args()
func_args_Contois = Modulos_Contois_bat_alim.modelag_bat_Contois_func_args()
func_args_Andrews = Modulos_Andrews_bat_alim.modelag_bat_Andrews_func_args()
func_args_Aiba_et_al = Modulos_Aiba_et_al_bat_alim.modelag_bat_Aiba_et_al_func_args()
func_args_Moser = Modulos_Moser_bat_alim.modelag_bat_Moser_func_args()
func_args_Hoppe_Hansford = Modulos_Hoppe_Hansford_bat_alim.modelag_bat_Hoppe_Hansford_func_args()
func_args_Wu_et_al = Modulos_Wu_et_al_bat_alim.modelag_bat_Wu_et_al_func_args()
func_args_Levenspiel = Modulos_Levenspiel_bat_alim.modelag_bat_Levenspiel_func_args()
func_args_Lee_et_al = Modulos_Lee_et_al_bat_alim.modelag_bat_Lee_et_al_func_args()
#func_args_mi_constante_bat = Modulos_mi_constante_bat_alim.modelag_bat_mi_const_func_args()
list_funcs_args = [func_args_Monod, func_args_Contois, func_args_Andrews, func_args_Aiba_et_al, func_args_Moser, func_args_Hoppe_Hansford, func_args_Wu_et_al, func_args_Levenspiel, func_args_Lee_et_al]

# Módulo para atribuição do peso:
dpC = Modulo_peso_limite_AG_bat_alim.peso()

# Chutes iniciais para ajuste dos parêmetros:
limites_Monod = Modulo_peso_limite_AG_bat_alim.limites()[0]
limites_Contois = Modulo_peso_limite_AG_bat_alim.limites()[1]
limites_Andrews = Modulo_peso_limite_AG_bat_alim.limites()[3]
limites_Aiba_et_al = Modulo_peso_limite_AG_bat_alim.limites()[5]
limites_Moser = Modulo_peso_limite_AG_bat_alim.limites()[2]
limites_Hoppe_Hansford = Modulo_peso_limite_AG_bat_alim.limites()[4]
limites_Wu_et_al = Modulo_peso_limite_AG_bat_alim.limites()[6]
limites_Levenspiel = Modulo_peso_limite_AG_bat_alim.limites()[7]
limites_Lee_et_al = Modulo_peso_limite_AG_bat_alim.limites()[8]
limites_mi_constante = Modulo_peso_limite_AG_bat_alim.limites()[9]
list_limites = [limites_Monod, limites_Contois, limites_Andrews, limites_Aiba_et_al, limites_Moser, limites_Hoppe_Hansford, limites_Wu_et_al, limites_Levenspiel, limites_Lee_et_al, limites_mi_constante]





                                    ##### ***** MODELAGEM AG-ALM ***** #####

## * DISPONIBILIZAÇÃO DO TEMPLATE * ##
# Imagem logo excel ilustrativa:
carregar_imagem(frame = frame2, imagem = "Excel_template.png", x = 960, y = 41, borderwidth = 2, relief = "solid")
# Escrita do template excel para entrada dos dados:
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
# Botão para baixar o arquivo modelo na máquina:
Button(frame2, text = "Baixe nosso template", font = "arial 7 bold", fg = "black", bg = "white", borderwidth = 2, relief = "raised", command = excel_template).place(x = 923, y = 100)


#### **** INÍCIO DO CÓDIGO-FONTE FUNCIONAL **** ####
    
# Habilitação do explorador de arquivos - entrada de dados simulados/experimentais:
def explorer():
    explorador = askopenfilename()
    nome_arquivo = os.path.basename(explorador)
    arq_sel.configure(text = nome_arquivo, font ="arial 8 bold", fg = "black", borderwidth = 2, relief = "ridge", justify = "center")
    
    # Captura dos dados de entrada - formato dataframe:
    excel_entrada = pd.read_excel(explorador)
    excel_entrada_np = excel_entrada.values
    ## Separação - t_exp e C_exp a partir do df - batelada + batelada alimentada:
    t_exp = excel_entrada_np[:,1]
    print("Tempo total", t_exp)
    C_exp = (excel_entrada_np[:,2:5])
    cond_inic = [C_exp[0,0], C_exp[0,1], C_exp[0,2]]
    print(C_exp)
    
    ## Atribuição de variáveis - padronização:
    if (def_alim == "Taxa de Vazão Constante"):
        tf_bat = tf_bat_const
        Q = Q_const
        V0 = V0_const
        Cs0_corrent_alim = Cs_alim_const
    if (def_alim == "Taxa de Vazão Linear"):
        tf_bat = tf_bat_lin
        Q0 = Q_lin
        V0 = V0_lin
        Cs0_corrent_alim = Cs_alim_lin
    if (def_alim == "Taxa de Vazão Exponencial"):
        tf_bat = tf_bat_exp
        Q0 = Q_exp
        V0 = V0_exp
        Cs0_corrent_alim = Cs_alim_exp
    
    ### ** Separação - batelada ** :
    ## Intervalo
    int_bat = excel_entrada_np[1,1] - excel_entrada_np[0,1]
    ## Correção no index - cópia manual do funcionamento do algoritmo python:
    tf_bat_cor = tf_bat - int_bat
    print(tf_bat)
    ## Vetores tempo e concentração:
    t_exp_bat = np.arange(excel_entrada_np[0,1], (tf_bat_cor + int_bat), int_bat)
    C_exp_bat = (excel_entrada_np[:(len(t_exp_bat)),2:5])
    print("bat intervalo", int_bat)
    print("bat t_Exp", t_exp_bat)
    print("bat C_exp", C_exp_bat)
    # Captura dos valores de C_exp iniciais:
    cond_inic_bat = [C_exp_bat[0,0], C_exp_bat[0,1], C_exp_bat[0,2]]
    print(cond_inic_bat)
    # Vetor tempo modelo:
    
    ## * INÍCIO DA MODELAGEM * ##:
    def modelagem(cont_model):
        ### *** INÍCIO DA CONTAGEM DO TEMPO *** ###:
        start_tempo = time.time()
        print(cont_model)
        func_args_bat = list_funcs_args[cont_model]
        def func_ob_ag_bat(parametros, *dados):
            t_exp_bat,C_exp_bat = dados
            p = tuple(parametros)
            C_sim = odeint(func_args_bat, cond_inic_bat, t_exp_bat, args = p)
            res = C_sim - C_exp_bat
            for i in range(0,3):
                res[:,i] = res[:,i]/dpC[i]
            res = res.flatten()
            res = sum(res**2)
            return res
        ## Importação dos bounds para aplicação do AG:
        limites = list_limites[cont_model]
        print(limites)
        print(func_args_bat)
        # Definição dos argumentos:
        args = (t_exp_bat,C_exp_bat)
        resultado_ag_bat = differential_evolution(func_ob_ag_bat, limites, args=args, popsize=5,  tol=0.01, mutation=(0.5, 1), recombination=0.7, updating='immediate')
        resultado_ag_bat = resultado_ag_bat.x
        resultado_ag_bat = tuple(resultado_ag_bat)
        
        def func_obj_alm_bat(p):
            p = tuple(p)
            C_sim_bat = odeint(func_args_bat,cond_inic_bat,t_exp_bat,args=p)
            res = C_sim_bat - C_exp_bat
            for i in range(0,3):
                res[:,i]=res[:,i]/dpC[i]
            return res.flatten()
        ## Minimização da função objetiva pela função leastsq:
        lance_inic_bat = [resultado_ag_bat]
        resultado_alm_bat = leastsq(func_obj_alm_bat,lance_inic_bat, args=(), Dfun=None, full_output=1)
        param_otim_alm_bat = resultado_alm_bat[0]
        ## Armazenamento dos parâmetros otimizados em tuplas:
        param_otim_alm_bat = tuple(param_otim_alm_bat)
        print(param_otim_alm_bat)
        ## Tempo modelo:
        t_bat = np.arange(0, (t_exp_bat[-1] + 0.1), 0.1)
           
        ### ** Separação - batelada alimentada ** :
        # Tempo e concentração:
        int_bat_alim = int_bat
        t_exp_bat_alim = np.arange(tf_bat, (excel_entrada_np[len(excel_entrada_np) - 1, 1]) + int_bat_alim, int_bat_alim)
        C_exp_bat_alim = (excel_entrada_np[(len(t_exp_bat)):,2:5])
        #print("bat alim", int_bat_alim)
        print("bat alim", t_exp_bat_alim)
        print("bat alim", C_exp_bat_alim)
        # Captura dos valores de C_exp iniciais:
        Cx0_exp_bat_alim = C_exp_bat[:,0][len(C_exp_bat[:,0])-1]   
        Cs0_exp_bat_alim = C_exp_bat[:,1][len(C_exp_bat[:,1])-1]
        Cp0_exp_bat_alim = C_exp_bat[:,2][len(C_exp_bat[:,2])-1]
        cond_inic_bat_alim = [Cx0_exp_bat_alim, Cs0_exp_bat_alim, Cp0_exp_bat_alim]
        # Tempo modelo:
        t_alim = np.arange(tf_bat, max(t_exp + 0.1), 0.1)
        print("t alim compr", len(t_alim))
        
            #*ETAPA 2*# - BATELADA ALIMENTADA
        ##*Algoritmo Genético (global)*##
        # Função com as equações modelo com os parâmetros atribuídos a argumentos:
        #### Condicional para a função argumento - modelo cinético e de alimentação:

        ## * AUSÊNCIA DE INIBIÇÃO * ##:
        # - Monod (vazão constante):
        if (cont_model == 0 and def_alim == "Taxa de Vazão Constante"):
            def fun_args_monod_um():
                def func_args_alim_Monod_const(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
              
                    mi = mimaximo*(C[1]/(Ks + C[1]))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_const - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Monod_const)
            func_args_alim_model = fun_args_monod_um()
        # - Monod (vazão linear):   
        if (cont_model == 0 and def_alim == "Taxa de Vazão Linear"):
            def fun_args_monod_dois():
                def func_args_alim_Monod_lin(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
        
                    mi = mimaximo*(C[1]/(Ks+C[1]))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_lin - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Monod_lin)
            func_args_alim_model = fun_args_monod_dois()
            
        # - Monod (vazão exponencial):   
        if (cont_model == 0 and def_alim == "Taxa de Vazão Exponencial"):
            def fun_args_monod_tres():
                def func_args_alim_Monod_exp(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
        
                    mi = mimaximo*(C[1]/(Ks+C[1]))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_exp - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Monod_exp)
            func_args_alim_model = fun_args_monod_tres()
            
        # - Contois (vazão constante):
        if (cont_model == 1 and def_alim == "Taxa de Vazão Constante"):
            def fun_args_contois_um():
                def func_args_alim_Contois_const(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    KSX = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
              
                    mi = mimaximo*(C[1]/((KSX*C[0]) + C[1]))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_const - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Contois_const)
            func_args_alim_model = fun_args_contois_um()
            
        # - Contois (vazão linear):
        if (cont_model == 1 and def_alim == "Taxa de Vazão Linear"):
            def fun_args_contois_dois():
                def func_args_alim_Contois_lin(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    KSX = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
              
                    mi = mimaximo*(C[1]/((KSX*C[0]) + C[1]))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_lin - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Contois_lin)
            func_args_alim_model = fun_args_contois_dois()
            
        # - Contois (vazão exponencial):
        if (cont_model == 1 and def_alim == "Taxa de Vazão Exponencial"):
            def fun_args_contois_tres():
                def func_args_alim_Contois_exp(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    KSX = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
        
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mi = mimaximo*(C[1]/((KSX*C[0]) + C[1]))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_exp - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Contois_exp)
            func_args_alim_model = fun_args_contois_tres()
            
        # - Moser (vazão constante):
        if (cont_model == 4 and def_alim == "Taxa de Vazão Constante"):
            def fun_args_moser_um():
                def func_args_alim_Moser_const(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    u = args[5]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
             
                    mi = mimaximo*(((C[1])**u)/(Ks+((C[1])**u)))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_const - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Moser_const)
            func_args_alim_model = fun_args_moser_um()
            
        # - Moser (vazão linear):
        if (cont_model == 4 and def_alim == "Taxa de Vazão Linear"):
            def fun_args_moser_dois():
                def func_args_alim_Moser_lin(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    u = args[5]
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
             
                    mi = mimaximo*(((C[1])**u)/(Ks+((C[1])**u)))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_lin - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Moser_lin)
            func_args_alim_model = fun_args_moser_dois()
        
        # - Moser (vazão exponencial):
        if (cont_model == 4 and def_alim == "Taxa de Vazão Exponencial"):
            def fun_args_moser_tres():
                def func_args_alim_Moser_exp(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    u = args[5]
    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mi = mimaximo*(((C[1])**u)/(Ks+((C[1])**u)))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_exp - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Moser_exp)
            func_args_alim_model = fun_args_moser_tres()
        
        ## ** INIBIÇÃO PELO PRODUTO ** ##:
        # - Aiba et al (vazão constante):
        if (cont_model == 3 and def_alim == "Taxa de Vazão Constante"):
            def fun_args_aiba_um():
                def func_args_alim_Aiba_const(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    Kp = args[5]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
             
                    mult_exp = -Kp*C[2]
                    mi = mimaximo*((C[1]/(Ks + C[1]))*np.exp(mult_exp))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_const - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Aiba_const)
            func_args_alim_model = fun_args_aiba_um()
        
        # - Aiba et al (vazão linear):
        if (cont_model == 3 and def_alim == "Taxa de Vazão Linear"):
            def fun_args_aiba_dois():
                def func_args_alim_Aiba_lin(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    Kp = args[5]
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
             
                    mult_exp = -Kp*C[2]
                    mi = mimaximo*((C[1]/(Ks + C[1]))*np.exp(mult_exp))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_lin - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Aiba_lin)
            func_args_alim_model = fun_args_aiba_dois()
            
        # - Aiba (vazão exponencial):
        if (cont_model == 3 and def_alim == "Taxa de Vazão Exponencial"):
            def fun_args_aiba_tres():
                def func_args_alim_Aiba_exp(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    Kp = args[5]
    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mult_exp = -Kp*C[2]
                    mi = mimaximo*((C[1]/(Ks + C[1]))*np.exp(mult_exp))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_exp - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Aiba_exp)
            func_args_alim_model = fun_args_aiba_tres()
        
        # - Hoppe & Hansford (vazão constante):
        if (cont_model == 5 and def_alim == "Taxa de Vazão Constante"):
            def fun_args_hoppe_hansford_um():
                def func_args_alim_Hoppe_Hansford_const(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    Kp = args[5]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
             
                    mi = mimaximo*(C[1]/(Ks + C[1]))*(Kp/(Kp + C[2]))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_const - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Hoppe_Hansford_const)
            func_args_alim_model = fun_args_hoppe_hansford_um()
            
        # - Hoppe & Hansford (vazão linear):
        if (cont_model == 5 and def_alim == "Taxa de Vazão Linear"):
            def fun_args_hoppe_hansford_dois():
                def func_args_alim_Hoppe_Hansford_lin(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    Kp = args[5]
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
             
                    mi = mimaximo*(C[1]/(Ks + C[1]))*(Kp/(Kp + C[2]))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_lin - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Hoppe_Hansford_lin)
            func_args_alim_model = fun_args_hoppe_hansford_dois()
            
        # - Hoppe & Hansford (vazão exponencial):
        if (cont_model == 5 and def_alim == "Taxa de Vazão Exponencial"):
            def fun_args_hoppe_hansford_tres():
                def func_args_alim_Hoppe_Hansford_exp(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    Kp = args[5]
    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mi = mimaximo*(C[1]/(Ks + C[1]))*(Kp/(Kp + C[2]))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_exp - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Hoppe_Hansford_exp)
            func_args_alim_model = fun_args_hoppe_hansford_tres()
        
        # - Levenspiel (vazão constante):
        if (cont_model == 7 and def_alim == "Taxa de Vazão Constante"):
            def fun_args_levenspiel_um():
                def func_args_alim_Levenspiel_const(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    n = args[5]
                    Cp_estr = args[6]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
             
                    mi = mimaximo*((C[1]/(Ks+C[1]))*((abs(1-(C[2]/Cp_estr)))**n))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_const - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Levenspiel_const)
            func_args_alim_model = fun_args_levenspiel_um()  
         
        # - Levenspiel (vazão linear)
        if (cont_model == 7 and def_alim == "Taxa de Vazão Linear"):
            def fun_args_levenspiel_dois():
                def func_args_alim_Levenspiel_lin(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    n = args[5]
                    Cp_estr = args[6]
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
             
                    mi = mimaximo*((C[1]/(Ks+C[1]))*((abs(1-(C[2]/Cp_estr)))**n))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_lin - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Levenspiel_lin)
            func_args_alim_model = fun_args_levenspiel_dois()
        
        # - Levenspiel (vazão exponencial):
        if (cont_model == 7 and def_alim == "Taxa de Vazão Exponencial"):
            def fun_args_levenspiel_tres():
                def func_args_alim_Levenspiel_exp(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    n = args[5]
                    Cp_estr = args[6]
        
    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mi = mimaximo*((C[1]/(Ks+C[1]))*((abs(1-(C[2]/Cp_estr)))**n))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_exp - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Levenspiel_exp)
            func_args_alim_model = fun_args_levenspiel_tres()
        
        ## * INIBIÇÃO PELO SUBSTRATO * ##:
            
        # - Andrews (vazão constante):
        if (cont_model == 2 and def_alim == "Taxa de Vazão Constante"):
            def fun_args_andrews_um():
                def func_args_alim_Andrews_const(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    KIS = args[5]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
             
                    mi = mimaximo*(C[1]/(Ks + C[1] + ((C[1]**2)/KIS)))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_const - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Andrews_const)
            func_args_alim_model = fun_args_andrews_um() 
        
        # - Andrews (vazão linear)
        if (cont_model == 2 and def_alim == "Taxa de Vazão Linear"):
            def fun_args_andrews_dois():
                def func_args_alim_Andrews_lin(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    KIS = args[5]
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
             
                    mi = mimaximo*(C[1]/(Ks + C[1] + ((C[1]**2)/KIS)))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_lin - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Andrews_lin)
            func_args_alim_model = fun_args_andrews_dois()
            
        # - Andrews (vazão exponencial):
        if (cont_model == 2 and def_alim == "Taxa de Vazão Exponencial"):
            def fun_args_andrews_tres():
                def func_args_alim_Andrews_exp(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    KIS = args[5]
    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mi = mimaximo*(C[1]/(Ks + C[1] + ((C[1]**2)/KIS)))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_exp - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Andrews_exp)
            func_args_alim_model = fun_args_andrews_tres()
            
        # - Wu et al (vazão constante):
        if (cont_model == 6 and def_alim == "Taxa de Vazão Constante"):
            def fun_args_wu_um():
                def func_args_alim_Wu_const(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    KE = args[5]
                    v = args[6]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
             
                    mi = mimaximo * (C[1]/(Ks + C[1] + C[1]*((C[1]/KE)**v)))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_const - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Wu_const)
            func_args_alim_model = fun_args_wu_um() 
        
        # - Wu et al (vazão linear)
        if (cont_model == 6 and def_alim == "Taxa de Vazão Linear"):
            def fun_args_wu_dois():
                def func_args_alim_Wu_lin(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    KE = args[5]
                    v = args[6]
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
             
                    mi = mimaximo * (C[1]/(Ks + C[1] + C[1]*((C[1]/KE)**v)))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_lin - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Wu_lin)
            func_args_alim_model = fun_args_wu_dois()
            
        # - Wu et al (vazão exponencial):
        if (cont_model == 6 and def_alim == "Taxa de Vazão Exponencial"):
            def fun_args_wu_tres():
                def func_args_alim_Wu_exp(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    KE = args[5]
                    v = args[6]
    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mi = mimaximo * (C[1]/(Ks + C[1] + C[1]*((C[1]/KE)**v)))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_exp - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Wu_exp)
            func_args_alim_model = fun_args_wu_tres()
        
        ## * INIBIÇÃO PELA BIOMASSA * ##:
        # - Lee et al (vazão constante):
        if (cont_model == 8  and def_alim == "Taxa de Vazão Constante"):
            def fun_args_lee_um():
                def func_args_alim_Lee_const(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    m = args[5]
                    Cx_estr = args[6]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
             
                    mi = mimaximo*((C[1]/(Ks+C[1]))*((abs(1-(C[0]/Cx_estr)))**m))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_const - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Lee_const)
            func_args_alim_model = fun_args_lee_um()    
        
        # - Lee et al (vazão linear)
        if (cont_model == 8 and def_alim == "Taxa de Vazão Linear"):
            def fun_args_lee_dois():
                def func_args_alim_Lee_lin(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    m = args[5]
                    Cx_estr = args[6]
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
             
                    mi = mimaximo*((C[1]/(Ks+C[1]))*((abs(1-(C[0]/Cx_estr)))**m))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_lin - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Lee_lin)
            func_args_alim_model = fun_args_lee_dois()
        
        # - Lee et al (vazão exponencial):
        if (cont_model == 8 and def_alim == "Taxa de Vazão Exponencial"):
            def fun_args_lee_tres():
                def func_args_alim_Lee_exp(C, t_exp_bat_alim, *args):
                    mimaximo = args[0]
                    Ks = args[1]
                    Yxs = args[2]
                    alfa = args[3]
                    beta = args[4]
                    m = args[5]
                    Cx_estr = args[6]
    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mi = mimaximo*((C[1]/(Ks+C[1]))*((abs(1-(C[0]/Cx_estr)))**m))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_exp - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Lee_exp)
            func_args_alim_model = fun_args_lee_tres()
        
            
        # Módulos
        ## Função objetiva, compara os pontos experimentais com o sistema cinético adotado:
        def func_obj_ag_alim(parametros, *dados):
            t_exp_bat_alim,C_exp_bat_alim = dados
            p = tuple(parametros)
            C_sim_alim = odeint(func_args_alim_model, cond_inic_bat_alim, t_exp_bat_alim, args = p)
            res = C_sim_alim - C_exp_bat_alim
            for i in range(0,3):
                res[:,i] = res[:,i]/dpC[i]
            res = res.flatten()
            res = sum(res**2)
            return res
        # Definição dos argumentos:
        args = (t_exp_bat_alim,C_exp_bat_alim)
        resultado_ag_alim = differential_evolution(func_obj_ag_alim, list_limites[cont_model], args = args, popsize=5,  tol=0.01, mutation=(0.5, 1), recombination=0.7, updating='immediate')
        resultado_ag_alim = resultado_ag_alim.x
        resultado_ag_alim = tuple(resultado_ag_alim)

        ##*Algoritmo de Levenberg-Marquardt (local)*##
        ## Função objetiva para o ALM:
        def func_obj_alm_alim(p):
            p = tuple(p)
            C_sim_alim = odeint(func_args_alim_model,cond_inic_bat_alim,t_exp_bat_alim,args=p)
            res = C_sim_alim - C_exp_bat_alim
            for i in range(0,3):
                res[:,i]=res[:,i]/dpC[i]
            return res.flatten()
        ## Minimização da função objetiva pela função leastsq:
        lance_inic_alim = [resultado_ag_alim]
        resultado_alm_alim = leastsq(func_obj_alm_alim,lance_inic_alim, args=(), Dfun=None, full_output=1)
        param_otim_alm_alim = resultado_alm_alim[0]
        ## Armazenamento dos parâmetros otimizados em tuplas:
        param_otim_alm_alim = resultado_alm_alim[0].round(4)
        param_otim_alm_alim = tuple(param_otim_alm_alim)
        
        ### *** PARADA NA CONTAGEM DO TEMPO DE MODELAGEM *** ###:
        stop_tempo = time.time()
        elapsed = stop_tempo - start_tempo
        elapsed = round(elapsed,3)
        
        ### *** INTEGRAÇÃO NUMÉRICA PÓS - MODELAGEM: CONCENTRAÇÃO OTIMIZADA ***:
        ## * BATELADA * ##:
        #- Integrando com os valores dos parâmetros ajustados:
        C_otim_bat = odeint(func_args_bat, cond_inic_bat, t_bat, args = (param_otim_alm_bat))
        ## * BATELADA ALIMENTADA * ##:
        ## Integrando com os valores dos parâmetros ajustados:
        Cx0_otim_alim = C_otim_bat[:,0][len(C_otim_bat[:,0])-1]   
        Cs0_otim_alim = C_otim_bat[:,1][len(C_otim_bat[:,1])-1]
        Cp0_otim_alim = C_otim_bat[:,2][len(C_otim_bat[:,2])-1]
        cond_inic_alim = [Cx0_otim_alim, Cs0_otim_alim, Cp0_otim_alim]
        C_otim_alim = odeint(func_args_alim_model, cond_inic_alim, t_alim, args = (param_otim_alm_alim))
        print("compri c alim", len(C_otim_alim[:,0]))
        
        #### **** CÁLCULO DO INTERVALO DE CONFIANÇA **** ####:
        # - Batelada - saída apenas em formato .xlsx:
        res_otimo = resultado_alm_bat[2]['fvec']
        sensT_otimo = resultado_alm_bat[2]['fjac']
        npar = len(sensT_otimo[:,1])
        ndata = len(sensT_otimo[1,:])
        invXtX=np.linalg.inv(np.matmul(sensT_otimo,sensT_otimo.transpose()))
        sig2y= sum(res_otimo**2) / (ndata-npar)
        covparamers = invXtX*sig2y
        EPpar = np.sqrt(covparamers.diagonal())
        ICpar_bat = EPpar*sc.t.interval(.95, ndata-npar, loc=0, scale=1)[1]
        ICpar_bat = ICpar_bat.round(3)
        print(ICpar_bat)
        
        # - Batelada alimentada - saída na interface e em formato .xlsx:
        res_otimo = resultado_alm_alim[2]['fvec']
        sensT_otimo = resultado_alm_alim[2]['fjac']
        npar = len(sensT_otimo[:,1])
        ndata = len(sensT_otimo[1,:])
        invXtX=np.linalg.inv(np.matmul(sensT_otimo,sensT_otimo.transpose()))
        sig2y= sum(res_otimo**2) / (ndata-npar)
        covparamers = invXtX*sig2y
        EPpar = np.sqrt(covparamers.diagonal())
        ICpar_alim = EPpar*sc.t.interval(.95, ndata-npar, loc=0, scale=1)[1]
        ICpar_alim = ICpar_alim.round(3)
        print(ICpar_alim)
        
        ### *** DEFINIÇÃO SAÍDA DOS VALORES MODELADOS NA INTERFACE:
        # - Batelada alimentada:
        ## Saída parâmetros equação mi - tabela superior:
        Label(frame2, bg = "grey75", height = 1, width = 41).place(x = 960, y = 258)
        Label(frame2, bg = "grey75", height = 1, width = 41).place(x = 960, y = 417)
        if (cont_model == 0 or cont_model == 1): # - Monod (5p), Contois(5p)
            Label(frame2, text = param_otim_alm_alim[0], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 943, y = 255)
            Label(frame2, text = param_otim_alm_alim[1], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1021, y = 255)
        if (cont_model == 9): # - mi constante (4p)
                Label(frame2, text = param_otim_alm_alim[0], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 943, y = 255)
        else:
            if (cont_model >= 2 and cont_model <=5): # - Andrews (6p), Aiba (6p), Moser (6p), Hoppe & Hansford (6p)
                Label(frame2, text = param_otim_alm_alim[0], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 943, y = 255)
                Label(frame2, text = param_otim_alm_alim[1], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1021, y = 255)
                Label(frame2, text = param_otim_alm_alim[5], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1099, y = 255)
            if (cont_model > 5):  # - Wu (7p), Levenspiel (7p), Lee (7p)
                Label(frame2, text = param_otim_alm_alim[0], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 943, y = 255)
                Label(frame2, text = param_otim_alm_alim[1], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1021, y = 255)
                Label(frame2, text = param_otim_alm_alim[5], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1099, y = 255)
                Label(frame2, text = param_otim_alm_alim[6], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1163, y = 255)       
        ## Saída parâmetros balanço de massa - tabela inferior:
        if (cont_model == 9): # - mi constante (4p)
            Label(frame2, text = "----" , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 934, y = 417)
            Label(frame2, text = param_otim_alm_alim[1] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1000, y = 417)
            Label(frame2, text = param_otim_alm_alim[2] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1090, y = 417)
            Label(frame2, text = param_otim_alm_alim[3] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1170, y = 417)
        else: # - outros modelos cinéticos não constantes
            Label(frame2, text = "----" , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 934, y = 417)
            Label(frame2, text = param_otim_alm_alim[2] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1000, y = 417)
            Label(frame2, text = param_otim_alm_alim[3] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1090, y = 417)
            Label(frame2, text = param_otim_alm_alim[4] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1170, y = 417)
        
        # Condições para marcação dos valores inadequados modelados:
        cond_mimax_mi =  param_otim_alm_alim[0] > 0.9 
        ## situação não observada para Kd (cont_model = 9), portanto, não resultará em problemas:
        cond_Ks = param_otim_alm_alim[1] >= C_exp[0,1] or param_otim_alm_alim[1] == 0 
        if (cont_model != 9):
            cond_yxs = param_otim_alm_alim[2] >= C_exp[0,1]
        else:
            cond_yxs = param_otim_alm_alim[1] >= C_exp[0,1]
        # Checagem parâmetros negativos:
        cond_param_neg = False
        for i in range (len(param_otim_alm_alim)):
            if param_otim_alm_alim[i] < 0:
                cond_param_neg = True   
                
        if (cond_mimax_mi or cond_Ks or cond_param_neg == True):
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
                    if cond_mimax_mi:
                        Label(frame2, text = param_otim_alm_alim[0], font = "batang 11", justify = "center", fg = "red4", bg = "grey75").place(x = 943, y = 255)
                    if (cont_model != 9):
                        if (cond_Ks):
                            Label(frame2, text = param_otim_alm_alim[1], font = "batang 11", justify = "center", fg = "red4", bg = "grey75").place(x = 1021, y = 255)
                    if (cont_model != 9):
                        if (cond_yxs):
                            Label(frame2, text = param_otim_alm_alim[3] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 1000, y = 417)
                    else:
                        if (cond_yxs):
                            Label(frame2, text = param_otim_alm_alim[2] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 1000, y = 417)
                    if cond_param_neg == True:
                        if (param_otim_alm_alim[0] <= 0): #mimaximo, mi
                            Label(frame2, text = param_otim_alm_alim[0], font = "batang 11", justify = "center", fg = "red4", bg = "grey75").place(x = 943, y = 255)
                        if (cont_model != 9):
                            if (param_otim_alm_alim[1] <= 0): #Ks
                                Label(frame2, text = param_otim_alm_alim[1], font = "batang 11", justify = "center", fg = "red4", bg = "grey75").place(x = 1021, y = 255)
                        if (cont_model != 9):
                            if (param_otim_alm_alim[1] <= 0 or cond_yxs): #Yxs
                                Label(frame2, text = param_otim_alm_alim[1] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 1000, y = 417)
                        else: 
                            if (param_otim_alm_alim[2] <= 0 or cond_yxs): #Yxs
                                Label(frame2, text = param_otim_alm_alim[2] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 1000, y = 417)
                        if (cont_model != 9):
                            if (param_otim_alm_alim[3] <= 0): #alfa
                                Label(frame2, text = param_otim_alm_alim[3] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 1090, y = 417)
                        else:
                            if (param_otim_alm_alim[1] <= 0): #alfa
                                Label(frame2, text = param_otim_alm_alim[1] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 1090, y = 417)
                        if (cont_model != 9):
                            if (param_otim_alm_alim[4] < 0): #beta
                                Label(frame2, text = param_otim_alm_alim[4] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 1170, y = 417)
                        else:
                            if (param_otim_alm_alim[3] < 0): #beta
                                Label(frame2, text = param_otim_alm_alim[3] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 1170, y = 417)
                        if (cont_model == 2):
                            if (param_otim_alm_alim[5] > 55):
                                Label(frame2, text = param_otim_alm_alim[5], font = "batang 11", justify = "center", fg = "red4", bg = "gre75y").place(x = 1099, y = 255)
                        if (cont_model >= 3 and cont_model <=5):
                            if (param_otim_alm_alim[5] <= 0 or param_otim_alm_alim[5] > 10):
                                Label(frame2, text = param_otim_alm_alim[5], font = "batang 11", justify = "center", fg = "red4", bg = "grey75").place(x = 1099, y = 255)
                        if (cont_model >= 6 and cont_model <=8):
                            if (param_otim_alm_alim[5] <= 0):
                                Label(frame2, text = param_otim_alm_alim[5], font = "batang 11", justify = "center", fg = "red4", bg = "grey75").place(x = 1142, y = 255)
                            if (param_otim_alm_alim[6] <= 0):
                                Label(frame2, text = param_otim_alm_alim[6], font = "batang 11", justify = "center", fg = "red4", bg = "grey75").place(x = 1163, y = 255)
                else:
                    self.config(text = 'Press to start flashing', font="Times 12 bold italic",
                    background = flash_colours[0])

            my_button = Button(frame2, text = 'Exibir análise cinética',font = "Times 12 bold italic", fg = "white", borderwidth=4, relief="groove", width = 20,background = flash_colours[0],command = lambda:buttonCallback(my_button))
            my_button.place(x = 921, y = 161)
         
        else:
            my_button = Label(frame2, bg = "grey85", borderwidth=7.5, relief="flat", height = 2, width = 28).place(x = 921, y = 150)
        
        ### JANELA PARA ACESSO AOS VALORES DE INTERVALO DE CONFIANÇA:
        # - Batelada Alimentada:
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
                # - Saída dos parâmetros equacionados através dos balanços de massa (tabela inferior):
                Label(janela_interna, text = u"Kd(±h\u207b\u00b9)    Yxs(±gx.gs\u207b\u00b9)    \u03B1(±gp.gx\u207b\u00b9)    \u03B2[±gp.(gx.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", width = 42, height = 1).place(x = 29, y = 67)
                Label(janela_interna, width = 48, height = 1).place(x = 29, y = 90)
                if (cont_model == 9): # - mi constante
                    Label(janela_interna, text = ICpar_alim[1], font = "batang 11", fg = "black").place(x = 32, y = 90)
                    Label(janela_interna, text = ICpar_alim[2], font = "batang 11", fg = "black").place(x = 113, y = 90)
                    Label(janela_interna, text = ICpar_alim[3], font = "batang 11", fg = "black").place(x = 207, y = 90)
                    Label(janela_interna, text = ICpar_alim[4], font = "batang 11", fg = "black").place(x = 300, y = 90)
                else: # - Outros modelos cinéticos
                    Label(janela_interna, text = "----", font = "batang 11", fg = "black").place(x = 32, y = 90)
                    Label(janela_interna, text = ICpar_alim[2], font = "batang 11", fg = "black").place(x = 113, y = 90)
                    Label(janela_interna, text = ICpar_alim[3], font = "batang 11", fg = "black").place(x = 207, y = 90)
                    Label(janela_interna, text = ICpar_alim[4], font = "batang 11", fg = "black").place(x = 300, y = 90)
            Botao_bm = Button(janela_interna, text = "Balanço de massa", font = "arial 8 bold", fg = "white", bg = "gray20", command = balan_massa).place(x = 25, y = 20)
            def mi():
                Label(janela_interna, text = "", font = "Times 32", bd = 4, relief = "sunken", width = 15, height = 2).place(x = 14, y = 32)
                Botao_bm = Button(janela_interna, text = "Balanço de massa", font = "arial 8 bold", fg = "white", bg = "gray20", command = balan_massa).place(x = 25, y = 20)
                Botao_mi = Button(janela_interna, text = u"Equação \u03bc", font = "arial 8 bold", fg = "white", bg = "gray20", command = mi).place(x = 140, y = 20)
                Label(janela_interna,text = "", width = 48, height = 1).place(x = 29, y = 90)
                # - Saída dos parâmetros referentes aos equacionamentos particulares para a taxa mi:
                if (cont_model == 0 or cont_model == 1): #Monod (5p) e Contois (5p)
                    if (cont_model == 0): # Monod
                         Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)     Ks(±g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", width = 42, justify = "left").place(x = 29, y = 67) 
                    if (cont_model == 1): # Contois
                         Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)     KSX(±gs.gx\u207b\u00b9)", font = "arial 10 bold", fg = "black", width = 42, justify = "left").place(x = 29, y = 67) 
                    Label(janela_interna, text = ICpar_alim[0], font = "batang 11", fg = "black").place(x = 133, y = 90)
                    Label(janela_interna, text = ICpar_alim[1], font = "batang 11", fg = "black").place(x = 220, y = 90)
                if (cont_model == 9): # mi constante
                    Label(janela_interna, text = u"\u03bc(±h\u207b\u00b9)", font = "arial 10 bold", fg = "black", width = 42, justify = "left").place(x = 29, y = 67) 
                    Label(janela_interna, text = ICpar_alim[0], font = "batang 11", fg = "black").place(x = 179, y = 90)
                if (cont_model >=2 and cont_model <=5): # - Andrews (6p), Aiba (6p), Moser (6p), Hoppe & Hansford (6p)
                    if (cont_model == 2): # Andrews
                        Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)      Ks(±g.L\u207b\u00b9)     KIS(±g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", width = 42).place(x = 29, y = 67)
                    if (cont_model == 4): # Moser
                        Label(janela_interna,  text = u"\u03bcmáx(±h\u207b\u00b9)     Ks(±g.L\u207b\u00b9)     u(±adim)", font = "arial 10 bold", fg = "black", width = 42).place(x = 29, y = 67)
                    if (cont_model == 3 or cont_model ==5): # Aiba e Hoppe & Hansford
                        Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)     Ks(±g.L\u207b\u00b9)     Kp(±g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", width = 42).place(x = 29, y = 67)
                    Label(janela_interna, text = ICpar_alim[0], font = "batang 11", fg = "black").place(x = 92, y = 90)
                    Label(janela_interna, text = ICpar_alim[1], font = "batang 11", fg = "black").place(x = 182, y = 90)
                    Label(janela_interna, text = ICpar_alim[5], font = "batang 11", fg = "black").place(x = 270, y = 90)
                if (cont_model >5 and cont_model <=8): # - Wu (7p), Levenspiel (7p), Lee (7p)
                    if (cont_model == 6): # Wu
                        Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)     Ks(±g.L\u207b\u00b9)     KE(±g.L\u207b\u00b9)     v(±adim)", font = "arial 10 bold", fg = "black", width = 42).place(x = 29, y = 67)
                    if (cont_model == 7): # Levenspiel
                        Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)    Ks(±g.L\u207b\u00b9)     n(±adim)     Cp*(±g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", width = 42).place(x = 29, y = 67)
                    if (cont_model ==8): # Lee
                        Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)    Ks(±g.L\u207b\u00b9)     Cx*(±g.L\u207b\u00b9)     m(±adim)", font = "arial 10 bold", fg = "black", width = 42).place(x = 29, y = 67)
                    Label(janela_interna, text = ICpar_alim[0], font = "batang 11",  fg = "black").place(x = 52, y = 90)
                    Label(janela_interna, text = ICpar_alim[1], font = "batang 11",  fg = "black").place(x = 143, y = 90)
                    Label(janela_interna, text = ICpar_alim[5], font = "batang 11", fg = "black").place(x = 226, y = 90)
                    Label(janela_interna, text = ICpar_alim[6], font = "batang 11",  fg = "black").place(x = 304, y = 90)        
            Botao_mi = Button(janela_interna, text = u"Equação \u03bc", font = "arial 8 bold", fg = "white", bg = "gray20", command = mi).place(x = 140, y = 20)
            Button(janela_interna, text = "Voltar", font = "arial 9 bold", fg = "white", bg = "gray30", command = janela_interna.destroy).place(x = 174, y = 160)
            janela_interna.mainloop()
        Button(frame2, text = "Intervalo de Confiança", font = "times 8 bold", fg = "black", bg = "white", command = int_conf).place(x = 921, y = 451)
        
        ### IMPRESSÃO DO TEMPO DE AJUSTE NA INTERFACE:
        Label(frame2, text = elapsed, font = "batang 11 italic", fg = "black", bg = "grey40").place(x = 1000, y = 318)
        
        ### CONTROLE DE EXECUÇÃO PELO TERMINAL:
        #- Impressão das saídas no console:
        print("\nTempo de ajuste AG-ALM para o modelo", cont_model,":",elapsed)
        print("Parametros equacionados pelo modelo",cont_model,":", param_otim_alm_alim)

        ## UNIÃO DAS MATRIZES C_exp_bat E C_exp_alim:
        #*ETAPA 1*# - BATELADA
        Cx_exp_bat = C_exp_bat[:,0]
        Cx_bat = C_otim_bat[:,0]
        Cs_exp_bat = C_exp_bat[:,1]
        Cs_bat = C_otim_bat[:,1]
        Cp_exp_bat = C_exp_bat[:,2]
        Cp_bat = C_otim_bat[:,2]
        #*ETAPA 2*# - BATELADA ALIMENTADA
        Cx_exp_alim = C_exp_bat_alim[:,0]
        Cx_alim = C_otim_alim[:,0]
        Cs_exp_alim = C_exp_bat_alim[:,1]
        Cs_alim = C_otim_alim[:,1]
        Cp_exp_alim = C_exp_bat_alim[:,2]
        Cp_alim = C_otim_alim[:,2]

        ### Contadores gerais:
        #*ETAPA 1*# - BATELADA
        limite_bat_exp = len(C_exp_bat)
        limite_alim_exp = len(C_exp_bat_alim)
        limite_bat = len(C_otim_bat)
        limite_alim = len(C_otim_alim)

        Cx_exp = []
        Cs_exp = []
        Cp_exp = []
        Cx = []
        Cs = []
        Cp = []
        Ttotal = []
        bat_exp = 0
        alim_exp = 0
        bat = 0
        alim = 0
        while (bat_exp < limite_bat_exp):
            Cx_exp.append(Cx_exp_bat[bat_exp])
            Cs_exp.append(Cs_exp_bat[bat_exp])
            Cp_exp.append(Cp_exp_bat[bat_exp])
            bat_exp = bat_exp + 1     
        while (bat < limite_bat):
            Cx.append(Cx_bat[bat])
            Cs.append(Cs_bat[bat])
            Cp.append(Cp_bat[bat]) 
            Ttotal.append(t_bat[bat])
            bat = bat + 1    
        while (alim_exp < limite_alim_exp):
            Cx_exp.append(Cx_exp_alim[alim_exp])
            Cs_exp.append(Cs_exp_alim[alim_exp])
            Cp_exp.append(Cp_exp_alim[alim_exp])
            alim_exp = alim_exp + 1
        while (alim < limite_alim):
            Cx.append(Cx_alim[alim])
            Cs.append(Cs_alim[alim])
            Cp.append(Cp_alim[alim])
            Ttotal.append(t_alim[alim])
            alim = alim + 1
    
        ## Conversão das listas para arrays - necessário para operações matemáticas:
        Cx_exp = np.asarray(Cx_exp)
        Cs_exp = np.asarray(Cs_exp)
        Cp_exp = np.asarray(Cp_exp)
        Cx = np.asarray(Cx)
        Cs = np.asarray(Cs)
        Cp = np.asarray(Cp)
        Ttotal = np.asarray(Ttotal)
        
        ## Vetor tempo total do processo:
        Ttotal_exp = np.arange(0,(excel_entrada_np[len(excel_entrada_np) - 1, 1]) + int_bat_alim, int_bat_alim)
        print("t total exp", Ttotal_exp)
        #Ttotal = np.linspace(0, (excel_entrada_np[len(excel_entrada_np) - 1, 1]), divisor)
        print("t total", Ttotal)
        Ttotal_text = np.arange(0,(excel_entrada_np[len(excel_entrada_np) - 1, 1]) + 0.1, 0.1)
        Ttotal = Ttotal
        
        ### CÁLCULO DO COEFICIENTE DE REGRESSÃO - R^2:
        # - Batelada e Batelada Alimentada:
        # Cálculo do coeficiente de regressão: 
        df_concents = pd.DataFrame({'Tempo(h)': Ttotal, 'Cx(g/L)': Cx, 'Cs(g/L)': Cs, 'Cp(g/L)': Cp})
        df_concents_exp = pd.DataFrame({'Tempo_exp(h)': Ttotal_exp,'Cx_exp(g/L)': Cx_exp,'Cs_exp(g/L)': Cs_exp,'Cp_exp(g/L)': Cp_exp})
        df_teste = pd.DataFrame({'Tempo(h)': Ttotal})
        df_teste_conc = pd.DataFrame({'Cx(g/L)': Cx, 'Cs(g/L)': Cs, 'Cp(g/L)': Cp})
        df_teste_exp = pd.DataFrame({'Tempo_exp(h)': Ttotal_exp})
        df_teste_exp_conc = pd.DataFrame({'Cx_exp(g/L)': Cx_exp,'Cs_exp(g/L)': Cs_exp,'Cp_exp(g/L)': Cp_exp})

        # Teste: qual tempo tem o menor intervalo de divisão temporal
        control_compar = len(Ttotal)
        
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
        ### DataFrames de saída, desconsiderando os indexes - resultam em erros:
        df_concent_model = pd.concat(concent_model)
        df_concent_exp = pd.concat(concent_exp)
        df_concent_model.reset_index(drop=True, inplace=True)
        df_concent_exp.reset_index(drop=True, inplace=True)
        
        ### Cálculo do coeficiente de regressão:
        med_conc = df_conc_exp.mean(axis=0)
        med_conc_val = pd.Series(med_conc).values
        df_med_conc = pd.DataFrame({'Cxexp_med(g/L)':[med_conc_val[0]], 'Csexp_med(g/L)':[med_conc_val[1]],'Cpexp_med(g/L)':[med_conc_val[2]]})
        df_saida_compar = pd.concat ([df_temp_exp,df_concent_exp, df_temp_model, df_concent_model,df_med_conc], axis=1)
        
        ### Determinação da soma do quadrado do resíduo:
        df_saida_compar['DQres_Cx'] = (df_concent_exp['Cx_exp(g/L)'] - df_concent_model['Cx(g/L)']) ** 2
        df_saida_compar['DQres_Cs'] = (df_concent_exp['Cs_exp(g/L)'] - df_concent_model['Cs(g/L)']) ** 2
        df_saida_compar['DQres_Cp'] = (df_concent_exp['Cp_exp(g/L)'] - df_concent_model['Cp(g/L)']) ** 2
    
        ### Determinação da soma do quadrado do resíduo:
        cx_med = np.repeat(med_conc_val[0],len(temp_exp))
        cs_med = np.repeat(med_conc_val[1],len(temp_exp))
        cp_med = np.repeat(med_conc_val[2],len(temp_exp))
        df_SQtotal_cx = pd.DataFrame ({'Cxexp_med(g/L)': cx_med, 'Csexp_med(g/L)': cs_med, 'Cpexp_med(g/L)': cp_med})
        df_saida_compar['DQtot_Cx'] = (df_concent_exp['Cx_exp(g/L)'] - df_SQtotal_cx['Cxexp_med(g/L)']) ** 2
        df_saida_compar['DQtot_Cs'] = (df_concent_exp['Cs_exp(g/L)'] - df_SQtotal_cx['Csexp_med(g/L)']) ** 2
        df_saida_compar['DQtot_Cp'] = (df_concent_exp['Cp_exp(g/L)'] - df_SQtotal_cx['Cpexp_med(g/L)']) ** 2
        
        ### Soma SQres e QStot: 
        soma_SQres_SQtot = df_saida_compar.sum(axis=0) #pegar 11,12,13,14,15 e 16
        soma_SQres_SQtot_val= pd.Series(soma_SQres_SQtot).values
        SQres = soma_SQres_SQtot_val[11] + soma_SQres_SQtot_val[12] + soma_SQres_SQtot_val[13]
        SQtotal = soma_SQres_SQtot_val[14] + soma_SQres_SQtot_val[15] + soma_SQres_SQtot_val[16]
        df_soma_SQres_SQtot = pd.DataFrame({'SQres':[SQres], 'SQtot':[SQtotal]})
        print(soma_SQres_SQtot_val)
        ### Cálculo do R²:
        r2 = 1 - (SQres/SQtotal)
        r2 = round(r2,4)
        print(r2)
        
        ### *** CÁLCULO RES FINAL: - VALOR DA FUNÇÃO OBJETIVA:
        # - Batelada alimentada:
        res_final = odeint(func_args_alim_model, cond_inic_bat_alim, t_exp_bat_alim,args = (param_otim_alm_alim)) - C_exp_bat_alim
        for i in range(0,3):
            res_final[:,i] = res_final[:,i]/dpC[i]
        res_final = res_final.flatten()
        res_final = sum(res_final**2)
        res_final = round(res_final,2)
        ## Impressão do valor do resíduo na interface:
        Label(frame2, text = res_final, font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 299)
        ## Condicional - peso cálculo do res final:
        if (cont_model == 0):
            res_final = res_final/5
        else:
            if (cont_model == 1):
                res_final = res_final/5
            else:
                if (cont_model == 2):
                    res_final = res_final/6
                else:
                    if (cont_model == 3):
                        res_final = res_final/6
                    else:
                        if (cont_model == 4):
                            res_final = res_final/6
                        else:
                            if (cont_model == 5):
                                res_final = res_final/6   
                            else:
                                if (cont_model == 9):
                                    res_final = res_final/4
                                else:
                                    res_final = res_final/7
                                    
            
                                ### *** PLOTAGEM GRÁFICA *** ###
        
        ## DETERMINAÇÃO DO TAMANHO DOS EIXOS GRÁFICOS:
        def tamanho_graf():
            SMALL_SIZE = 13                        
            MEDIUM_SIZE = 16                      
            BIGGER_SIZE = 16                      
            plt.rc('font', size=SMALL_SIZE)          
            plt.rc('axes', titlesize=SMALL_SIZE)     
            plt.rc('axes', labelsize=MEDIUM_SIZE)    
            plt.rc('xtick', labelsize=SMALL_SIZE)    
            plt.rc('ytick', labelsize=SMALL_SIZE)    
            plt.rc('legend', fontsize=SMALL_SIZE)    
            plt.rc('figure', titlesize=BIGGER_SIZE) 
            
## ** // _____________________________________________GRÁFICO - PERFIL DE CONCENTRAÇÃO___________________________________________ // ** ##
        
        # - Original:      
        x = "red"
        p = "green"
        s = "blue"
        def imprimir_perfil_concentracao_model_otim_exp (t_ajus, t_m, Cx_ajus, Cs_ajus, Cp_ajus, Cx_m, Cs_m, Cp_m):
            tamanho_graf()
            f = plt.figure(figsize=(8.3,6), dpi = 54) 
            plot = f.add_subplot(111) 
            _ = lns1 = plot.plot(t_m ,Cx_m, color = x, linewidth=3,label='Cx modelo')
            _ = lns2 = plot.plot(t_ajus ,Cx_ajus,'o',color=x,markersize=6, label='Cx experimental')
            _ = lns3 = plot.plot(t_m,Cs_m, linestyle=":", color=s,linewidth=3,label='Cs modelo')  
            _ = lns4 = plot.plot(t_ajus ,Cs_ajus,'s',color = s, markersize=6,label='Cs experimental')
            ax2 = plot.twinx()
            _ = lns5 = ax2.plot(t_m,Cp_m,linestyle="--", color=p,linewidth=3,label='Cp modelo') 
            _ = lns6 = ax2.plot(t_ajus,Cp_ajus,'^',color=p, markersize=6,label='Cp experimental')
            _ = plot.axvline(x = tf_bat, color = "grey", linestyle="dashed", linewidth=3)
            _ = plot.set_xlabel('Tempo de cultivo (h)',weight='bold')               
            _ = plot.set_ylabel('Cx e Cs (g/L)', weight='bold')
            _ = ax2.set_ylabel('Cp (g/L)', weight='bold') 
            lns = lns1+lns2+lns3+lns4+lns5+lns6
            labs = [l.get_label() for l in lns]
            _ = plot.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.17),ncol=3, fancybox=True, shadow=True)                                                
            _ = plot.grid(True)
            f.patch.set_facecolor('white')                                   
            plt.style.use('default')
            canvas = FigureCanvasTkAgg(f, frame38)
            a = canvas.get_tk_widget().place(x = 0, y = 0)
            def salvar():
                a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                defaultextension='.png')
                plt.savefig(a)
            botao_com_graf(frame = frame38, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy, x = 450, y = 176)
        imprimir_perfil_concentracao_model_otim_exp(Ttotal_exp, Ttotal, Cx_exp, Cs_exp, Cp_exp, Cx, Cs, Cp)
        
        # - Mudança de cor em decorrência da entrada do usuário
        # Gráfico para mudança de cor - perfil de concentração:
        def graf_cor (x,p,s): 
            tamanho_graf()
            f = plt.figure(figsize=(8.3,6), dpi = 54) 
            plot = f.add_subplot(111) 
            _ = lns1 = plot.plot(Ttotal ,Cx, color = x, linewidth=3,label='Cx modelo')
            _ = lns2 = plot.plot(Ttotal_exp, Cx_exp,'o',color=x,markersize=6, label='Cx experimental')
            _ = lns3 = plot.plot(Ttotal, Cs, linestyle=":", color=s,linewidth=3,label='Cs modelo')  
            _ = lns4 = plot.plot(Ttotal_exp ,Cs_exp,'s',color = s, markersize=6,label='Cs experimental')
            ax2 = plot.twinx()
            _ = lns5 = ax2.plot(Ttotal, Cp,linestyle="--", color=p,linewidth=3,label='Cp modelo') 
            _ = lns6 = ax2.plot(t_exp,Cp_exp,'^',color=p, markersize=6,label='Cp experimental')
            _ = plot.axvline(x = tf_bat, color = "grey", linestyle="dashed", linewidth=3)
            _ = plot.set_xlabel('Tempo de cultivo (h)',weight='bold')               
            _ = plot.set_ylabel('Cx e Cs (g/L)', weight='bold')
            _ = ax2.set_ylabel('Cp (g/L)', weight='bold') 
            lns = lns1+lns2+lns3+lns4+lns5+lns6
            labs = [l.get_label() for l in lns]
            _ = plot.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.17),ncol=3, fancybox=True, shadow=True )                                                
            _ = plot.grid(True)
            f.patch.set_facecolor('white')                                   
            plt.style.use('default')
            canvas = FigureCanvasTkAgg(f, frame38)
            a = canvas.get_tk_widget().place(x = 0, y = 0)
            def salvar():
                a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                defaultextension='.png')
                plt.savefig(a)
            botao_com_graf(frame = frame38, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy, x = 450, y = 176)
        
        # - Escolha das cores:
        def seletor_cores():
            cor = colorchooser.askcolor(title = "Editar cores")
            return(cor[1])
        def cores_cx():
            global cor_x
            cor_x = colorchooser.askcolor(title ="Editar cores")
            cor_x = cor_x[1]
            fig = graf_cor (x = cor_x, p = "green", s = "blue")
            Button(frame38, text = "Cs", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_cs).place(x = 460, y = 258) 
        def cores_cs():
            global cor_s
            cor_s = colorchooser.askcolor(title ="Editar cores")
            cor_s = cor_s[1]
            fig = graf_cor (x = cor_x, p = "green", s = cor_s)
            Button(frame38, text = "Cs", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_cs).place(x = 460, y = 256)
            Button(frame38, text = "Cp", bg = "gray40", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_cp).place(x = 460, y = 284)  
        def cores_cp():
            global cor_p
            cor_p = colorchooser.askcolor(title ="Editar cores")
            cor_p = cor_p[1] 
            fig = graf_cor (x = cor_x, p = cor_p, s = cor_s)
            Button(frame38, text = "Cp", bg = "gray40", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_cp).place(x = 460, y = 286)
        def cores_concent():
            Button(frame38, text = "Cx", bg = "gray60", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_cx).place(x = 460, y = 230)
            botao_paleta_graf(frame = frame38, comando = cores_concent)
        
        # -  Botão para mudança de cor:
        botao_paleta_graf(frame = frame38, comando = cores_concent)

        #### **** Impressão do valor do R² concentração na interface **** ####:
        def r2_concent():
            Label(frame2, text = r2.round(4), font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            print(r2)
        ## Botão para acesso:
        Button(frame38, text = "R²", font = "batang 12 bold", fg = "black", bg = "grey70", command = r2_concent).place(x = 452, y = 45)

## ** \\ _____________________________________________GRÁFICO - PERFIL DE CONCENTRAÇÃO___________________________________________ \\ ** ##
        
              
## ** // __________________________________________GRÁFICO - PRODUTIVIDADE CELULAR E DO PRODUTO__________________________________ // ** ##
        
        ### ** CÁLCULO DA PRODUTIVIDADE CELULAR (Px) E DO PRODUTO (Pp) - TEMPORAL:
        ## Experimental: 
        # -- Células:
        Px_exp = Cx_exp[1:]/Ttotal_exp[1:] 
        Px_exp[Px_exp<0] = 0 # Se o valor é menor que 0 é substituido por 0
        # -- Produto:
        Pp_exp = Cp_exp[1:]/Ttotal_exp[1:]
        Pp_exp[Pp_exp<0] = 0 # Se o valor é menor que 0 é substituido por 0
        ## Modelada:
        # -- Células:
        Px = Cx[1:]/Ttotal[1:]
        Px[Px<0] = 0 # Se o valor é menor que 0 é substituido por 0
        Pp = Cp[1:]/Ttotal[1:]
        Pp[Pp<0] = 0 # Se o valor é menor que 0 é substituido por 0
        
        ## ** GRÁFICO ** ##:
        # - Função das cores selecionadas pelo usuário:
        def graf_produtiv(px, pp):
            def imprimir_produtividade_celular_produto_model_otim_exp (t_ajus, t_m, Px_ajus, Pp_ajus, Px_m, Pp_m):
                tamanho_graf()
                f = plt.figure(figsize=(8.3,6), dpi = 54) 
                plot = f.add_subplot(111)  
                _ = lns1 = plot.plot(t_m ,Px_m,color = px,linewidth=3,label='Produtividade Celular modelo')
                _ = lns2 = plot.plot(t_ajus ,Px_ajus,'o',markersize=6, color = px, label='Produtividade Celular experimental')
                ax2 = plot.twinx()
                _ = lns3 = ax2.plot(t_m,Pp_m,linestyle=":", color = pp,linewidth=3,label='Produtividade Produto modelo') 
                _ = lns4 = ax2.plot(t_ajus,Pp_ajus,'sb', markersize=6, color = pp,label='Produtividade Produto experimental')
                _ = plot.axvline(x = tf_bat, color = "grey", linestyle="dashed", linewidth=3)
                _ = plot.set_xlabel('Tempo de cultivo (h)',weight='bold')               
                _ = plot.set_ylabel('Produtividade Celular (gx/L.h)', weight='bold')
                ax2.set_ylabel('Produtividade Produto (gp/L.h)', weight='bold') 
                lns = lns1+lns2+lns3+lns4
                labs = [l.get_label() for l in lns]
                _ = plot.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.17),ncol=2, fancybox=True, shadow=True )                                                
                _ = plot.grid(True)
                f.patch.set_facecolor('white')                                   
                plt.style.use('default')    
                canvas = FigureCanvasTkAgg(f, frame39)
                a = canvas.get_tk_widget().place(x = 0, y = 0)
                def salvar():
                    a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                    defaultextension='.png')
                    plt.savefig(a)
                botao_com_graf(frame = frame39, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy, x = 450, y = 176)
            imprimir_produtividade_celular_produto_model_otim_exp(Ttotal_exp[1:], Ttotal[1:],Px_exp, Pp_exp, Px, Pp)
        
        # -  Escolha das cores:
        def seletor_cores_PxPp():
            cor = colorchooser.askcolor(title = "Editar cores")
            return(cor[1])
        def cores_px():
            global cor_px
            cor_px = colorchooser.askcolor(title ="Editar cores")
            cor_px = cor_px[1]
            fig = graf_produtiv(px = cor_px, pp = "green")
            Button(frame39, text = "Pp", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_pp).place(x = 460, y = 258)   
        def cores_pp():
            global cor_pp
            cor_pp = colorchooser.askcolor(title ="Editar cores")
            cor_pp = cor_pp[1]
            fig = graf_produtiv(px = cor_px, pp = cor_pp)
            Button(frame39, text = "Pp", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_pp).place(x = 460, y = 258)
        def cores_produtiv():
            Button(frame39, text = "Px", bg = "gray60", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_px).place(x = 460, y = 230)    
       
        # - Geração do gráfico padrão Fermenpy:
        graf_produtiv(px = "red", pp = "green")
        # - Botão para seleção das cores:
        botao_paleta_graf(frame39, comando = cores_produtiv)
        
        ### ** CÁLCULO DO COEFICIENTE DE REGRESSÃO - PRODUTIVIDADES ** ###:
        def r2_Px_Pp():
            ### CÁLCULO DO COEFICIENTE DE REGRESSÃO - R^2:
            # - Batelada e Batelada Alimentada:
            # Cálculo do coeficiente de regressão: 
            df_produtiv = pd.DataFrame({'Tempo(h)': Ttotal[1:], 'Px(gx/t)': Px, 'Pp(gs/t)': Pp})
            df_produtiv_exp = pd.DataFrame({'Tempo_exp(h)': Ttotal_exp[1:],'Px_exp(gs/t)': Px_exp,'Pp_exp(gp/t)': Pp_exp})
            df_teste = pd.DataFrame({'Tempo(h)': Ttotal[1:]})
            df_teste_produtiv = pd.DataFrame({'Px(gx/t)': Px, 'Pp(gp/L)': Pp})
            df_teste_exp = pd.DataFrame({'Tempo_exp(h)': Ttotal_exp[1:]})
            df_teste_exp_produtiv = pd.DataFrame({'Px_exp(gx/t)': Px_exp,'Pp_exp(gp/t)': Pp_exp})

            # Teste: qual tempo tem o menor intervalo de divisão temporal
            control_compar = len(Ttotal[1:])
        
            ## Laço para comparação de tempos iguais (experimental e modelo) 
            i_compar_exp = 0
            i_compar_model = 0
            temp_model=[]
            temp_exp=[]
            produtiv_model = []
            produtiv_exp = []
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
                    debitado_model = df_teste_produtiv.loc[i_compar_model]
                    debitado_model = pd.Series(debitado_model).values
                    debitado_exp = df_teste_exp_produtiv.loc[i_compar_exp]
                    debitado_exp = pd.Series(debitado_exp).values
                    df_produtiv_model = pd.DataFrame({'Px(gx/t)':[debitado_model[0]],'Pp(gp/t)':[debitado_model[1]]})
                    produtiv_model.append(df_produtiv_model)
                    df_produtiv_exp = pd.DataFrame({'Px_exp(gx/t)':[debitado_exp[0]], 'Pp_exp(gp/t)':[debitado_exp[1]]})
                    produtiv_exp.append(df_produtiv_exp)
                    i_compar_model =  1 + i_compar_model
                    i_compar_exp =  1 + i_compar_exp  
            ### DataFrames de saída, desconsiderando os indexes - resultam em erros:
            df_produtiv_model = pd.concat(produtiv_model)
            df_produtiv_exp = pd.concat(produtiv_exp)
            df_produtiv_model.reset_index(drop=True, inplace=True)
            df_produtiv_exp.reset_index(drop=True, inplace=True)
        
            ### Cálculo do coeficiente de regressão:
            med_produtiv = df_produtiv_exp.mean(axis=0)
            med_produtiv_val = pd.Series(med_produtiv).values
            df_med_produtiv = pd.DataFrame({'Pxexp_med(gx/t)':[med_produtiv_val[0]], 'Ppexp_med(gp/t)':[med_produtiv_val[1]]})
            df_saida_compar = pd.concat ([df_temp_exp,df_produtiv_exp, df_temp_model, df_produtiv_model,df_med_produtiv], axis=1)
        
            ### Determinação da soma do quadrado do resíduo:
            df_saida_compar['DQres_Px'] = (df_produtiv_exp['Px_exp(gx/t)'] - df_produtiv_model['Px(gx/t)']) ** 2
            df_saida_compar['DQres_Pp'] = (df_produtiv_exp['Pp_exp(gp/t)'] - df_produtiv_model['Pp(gp/t)']) ** 2
    
            ### Determinação da soma do quadrado do resíduo:
            Px_med = np.repeat(med_produtiv_val[0],len(temp_exp))
            Pp_med = np.repeat(med_produtiv_val[1],len(temp_exp))
            df_SQtotal_Px = pd.DataFrame ({'Pxexp_med(gx/t)': Px_med, 'Ppexp_med(gp/t)': Pp_med})
            df_saida_compar['DQtot_Px'] = (df_produtiv_exp['Px_exp(gx/t)'] - df_SQtotal_Px['Pxexp_med(gx/t)']) ** 2
            df_saida_compar['DQtot_Pp'] = (df_produtiv_exp['Pp_exp(gp/t)'] - df_SQtotal_Px['Ppexp_med(gp/t)']) ** 2
        
            ### Soma SQres e QStot: 
            soma_SQres_SQtot = df_saida_compar.sum(axis=0) #pegar 11,12,13,14
            soma_SQres_SQtot_val = pd.Series(soma_SQres_SQtot).values
            print(soma_SQres_SQtot_val)
            
            SQres = soma_SQres_SQtot_val[8] + soma_SQres_SQtot_val[9] 
            SQtotal = soma_SQres_SQtot_val[10] + soma_SQres_SQtot_val[11] 
            df_soma_SQres_SQtot = pd.DataFrame({'SQres':[SQres], 'SQtot':[SQtotal]})
            
            ### Cálculo do R²:
            r2_Px_Pp = 1 - (SQres/SQtotal)
            r2_Px_Pp = round(r2_Px_Pp, 4)
            Label(frame2, text = "", font = "batang 10",  bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            Label(frame2, text = r2_Px_Pp, font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            print(r2_Px_Pp)
           
        #### **** Impressão do valor do R² concentração na interface **** ####:
        # - Botão para acesso:
        Button(frame39, text = "R²", font = "batang 12 bold", fg = "black", bg = "grey70", command = r2_Px_Pp).place(x = 452, y = 45)    

## ** \\ __________________________________________GRÁFICO - PRODUTIVIDADE CELULAR E DO PRODUTO__________________________________ \\ ** ##
        

## ** // ______________________________________________GRÁFICO - PRODUTIVIDADE ESPECÍFICA_______________________________________ // ** ##          
        
        ### ** CÁLCULO DA PRODUTIVIDADE ESPECÍFICA (Ppx) - RELAÇÃO ENTRE PRODUTO E BIOMASSA:
        # -- Experimental:
        Ppx_exp = Cp_exp*(1/Cx_exp)
        Ppx_exp[Ppx_exp<0] = 0
        # -- Modelada:
        Ppx = Cp*(1/Cx)
        Ppx[Ppx<0] = 0
        
        ## ** GRÁFICO ** ##:
        # - Função das cores selecionadas pelo usuário:
        def graf_produtiv_espec(Ppx_cor, Ppx_exp_cor):
            def imprimir_produtividade_especifica_model_otim_exp (t_ajus,t_m, Ppx_ajus, Ppx_m):
                tamanho_graf()
                f = plt.figure(figsize=(8.3,6), dpi = 54) 
                plot = f.add_subplot(111)  
                _ = plt.plot(t_m,Ppx_m,color = Ppx_cor,linewidth=3, label='Modelo')
                _ = plt.plot(t_ajus,Ppx_ajus,'o',markersize=6, color = Ppx_exp_cor, label='Experimental')
                _ = plot.axvline(x = tf_bat, color = "grey", linestyle="dashed", linewidth=3)
                _ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
                _ = plt.ylabel('Produtividade Específica (gp/gx)', weight='bold')
                _ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.14),ncol=2, fancybox=True, shadow=True )
                _ = plt.grid(True)  
                f.patch.set_facecolor('white')                                   
                plt.style.use('default')                       
                canvas = FigureCanvasTkAgg(f, frame40)
                a = canvas.get_tk_widget().place(x = 0, y = 0)
                def salvar():
                    a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                    defaultextension='.png')
                    plt.savefig(a)
                botao_com_graf(frame = frame40, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy, x = 450, y = 176)
            imprimir_produtividade_especifica_model_otim_exp(Ttotal_exp, Ttotal, Ppx_exp, Ppx)
        
        # - Escolha das cores:
        def seletor_cores_Ppx():
            cor_Ppx = colorchooser.askcolor(title ="Editar cores")
            cor_Ppx = cor_Ppx[1]
            graf_produtiv_espec(Ppx_cor = cor_Ppx, Ppx_exp_cor = cor_Ppx)
            
        # - Geração do gráfico padrão do Fermenpy:
        graf_produtiv_espec(Ppx_cor = "red", Ppx_exp_cor = "red")
        # - Botão para seleção das cores:
        botao_paleta_graf(frame40, comando = seletor_cores_Ppx)
        
        ### ** CÁLCULO DO COEFICIENTE DE REGRESSÃO - PRODUTIVIDADES ** ###:
        def r2_Ppx():
            # Cálculo R²:
            df_Ppx = pd.DataFrame({'Tempo(h)':Ttotal, 'ppx(gp/gx)': Ppx})
            df_t_exp = pd.DataFrame({'Tempo(h)': Ttotal_exp})
            df_Ppx_merge = df_Ppx.merge(df_t_exp, how = 'inner' ,indicator=False)
            df_Ppx_exp = pd.DataFrame({'Tempo_exp(h)':Ttotal_exp, 'Ppx_exp(gp/gx)': Ppx_exp})
            del df_Ppx_merge['Tempo(h)']
            del df_Ppx_exp['Tempo_exp(h)']
            df_Ppx_merge = df_Ppx_merge.values
            df_Ppx_exp = df_Ppx_exp.values
            resid = (df_Ppx_merge - df_Ppx_exp)**2
            resid = resid.flatten()
            resid = sum(resid)
            Ppx_medio = np.mean(df_Ppx_exp)
            Ppx_total = sum((df_Ppx_exp- Ppx_medio)**2)
            global r2_Ppx
            r2_Ppx = 1 - (resid/Ppx_total) 
            Label(frame2, text = "", font = "batang 10",  bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            Label(frame2, text = r2_Ppx[0].round(4), font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            print(r2_Ppx[0])
            
        #### **** Impressão do valor do R² concentração na interface **** ####:
        ## Botão para acesso:
        Button(frame40, text = "R²", font = "batang 12 bold", fg = "black", bg = "grey70", command = r2_Ppx).place(x = 452, y = 45)
        
## ** \\ ______________________________________________GRÁFICO - PRODUTIVIDADE ESPECÍFICA_______________________________________ \\ ** ## 
       

## ** // ___________________________________________GRÁFICO - TAXA ESPECÍFICA DE CRESCIMENTO____________________________________ // ** ##                   

        ### ** CÁLCULO DA PRODUTIVIDADE ESPECÍFICA (Ppx) - RELAÇÃO ENTRE PRODUTO E BIOMASSA:
        # -- Experimental e modelada:
        if (cont_model == 0): # - Monod
            mi_exp = param_otim_alm_alim[0]*(Cs_exp/(param_otim_alm_alim[1] + Cs_exp))
            mi = param_otim_alm_alim[0]*(Cs/(param_otim_alm_alim[1] + Cs))
        if (cont_model == 1): # - Contois 
            mi_exp = param_otim_alm_alim[0]*(Cs_exp/(param_otim_alm_alim[1] * Cx_exp + Cs_exp))
            mi = param_otim_alm_alim[0]*(Cs/(param_otim_alm_alim[1] * Cx + Cs))
        if (cont_model == 2): # - Andrews
            mi_exp = param_otim_alm_alim[0]*(Cs_exp/(param_otim_alm_alim[1] + Cs_exp + ((Cs_exp**2)/param_otim_alm_alim[5])))
            mi = param_otim_alm_alim[0]*(Cs/(param_otim_alm_alim[1] + Cs + ((Cs**2)/param_otim_alm_alim[5])))
        if (cont_model == 3): # Aiba
            mult_exp = -param_otim_alm_alim[5]*Cp_exp
            mi_exp = param_otim_alm_alim[0]*((Cs_exp/(param_otim_alm_alim[1] + Cs_exp))*np.exp(mult_exp))
            mult = -param_otim_alm_alim[5]*Cp
            mi = param_otim_alm_alim[0]*((Cs/(param_otim_alm_alim[1] + Cs))*np.exp(mult))
        if (cont_model == 4): # - Moser
            mi_exp = param_otim_alm_alim[0]*((Cs_exp**param_otim_alm_alim[5])/(param_otim_alm_alim[1] + (Cs_exp**param_otim_alm_alim[5])))
            mi = param_otim_alm_alim[0]*((Cs**param_otim_alm_alim[5])/(param_otim_alm_alim[1] + (Cs**param_otim_alm_alim[5])))
        if (cont_model == 5): # - Hoppe & Hansford
            mi_exp = param_otim_alm_alim[0]*(Cs_exp/(param_otim_alm_alim[1] + Cs_exp))*(param_otim_alm_alim[5]/(param_otim_alm_alim[5] + Cp_exp))
            mi = param_otim_alm_alim[0]*(Cs/(param_otim_alm_alim[1] + Cs))*(param_otim_alm_alim[5]/(param_otim_alm_alim[5] + Cp))
        if (cont_model == 6): # - Wu
            mi_exp = param_otim_alm_alim[0]*(Cs_exp/(param_otim_alm_alim[1] + Cs_exp + (Cs_exp*((Cs_exp/param_otim_alm_alim[5])**param_otim_alm_alim[6]))))
            mi = param_otim_alm_alim[0]*(Cs/(param_otim_alm_alim[1] + Cs + (Cs*((Cs/param_otim_alm_alim[5])**param_otim_alm_alim[6]))))
        if (cont_model == 7): # - Levenspiel
            mi_exp = param_otim_alm_alim[0]*((Cs_exp/(param_otim_alm_alim[1] + Cs_exp))*((1-(Cp_exp/param_otim_alm_alim[6]))**param_otim_alm_alim[5]))
            mi = param_otim_alm_alim[0]*((Cs/(param_otim_alm_alim[1] + Cs))*((1-(Cp/param_otim_alm_alim[6]))**param_otim_alm_alim[5]))
        if (cont_model == 8): # - Lee
            mi_exp = param_otim_alm_alim[0]*((Cs_exp/(param_otim_alm_alim[1] + Cs_exp))*((1-(Cx_exp/param_otim_alm_alim[6]))**param_otim_alm_alim[5]))
            mi = param_otim_alm_alim[0]*((Cs/(param_otim_alm_alim[1] + Cs))*((1-(Cx/param_otim_alm_alim[6]))**param_otim_alm_alim[5]))
        if (cont_model == 9): # - mi constante
            mi_exp = np.repeat(param_otim_alm_alim[0],len(Ttotal_exp))
            mi = np.repeat(param_otim_alm_alim[0],len(Ttotal))
        mi_exp[mi_exp<0] = 0
        mi[mi<0] = 0
        
        ## * GRÁFICO * ##:
        # - Figura como função das entradas fornecidas pelo usuário:
        def graf_mi(mi_cor, mi_exp_cor):
            def imprimir_taxa_especifica_crescimento (t_ajus,t_m, mi_ajus, mi_m):
                tamanho_graf()
                f = plt.figure(figsize=(8.3,6), dpi = 54) 
                plot = f.add_subplot(111)                                             
                _ = plt.plot(t_m,mi_m,color = mi_cor,linewidth=3, label='Modelo')
                _ = plt.plot(t_ajus,mi_ajus,'o',markersize=6, color = mi_exp_cor, label='Experimental')
                _ = plot.axvline(x = tf_bat, color = "grey", linestyle="dashed", linewidth=3)
                _ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
                _ = plt.ylabel('Taxa $\mu (h^{-1}$)', weight='bold')
                _ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.14),ncol=2, fancybox=True, shadow=True )  
                _ = plt.grid(True)  
                f.patch.set_facecolor('white')                                   
                plt.style.use('default')   
                canvas = FigureCanvasTkAgg(f, frame41)
                a = canvas.get_tk_widget().place(x = 0, y = 0)
                def salvar():
                    a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                    defaultextension='.png')
                    plt.savefig(a)  
                botao_com_graf(frame = frame41, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy, x = 450, y = 176)
            imprimir_taxa_especifica_crescimento(Ttotal_exp, Ttotal, mi_exp, mi)
        
        # - Escolha das cores:
        def seletor_cores_mi():
            cor_mi = colorchooser.askcolor(title ="Editar cores")
            cor_mi = cor_mi[1]
            graf_mi(mi_cor = cor_mi, mi_exp_cor = cor_mi)
            
        # - Geração do gráfico padrão fermenpy:
        graf_mi(mi_cor = "red", mi_exp_cor = "red")
        # - Botão para seleção das cores:
        botao_paleta_graf(frame41, comando = seletor_cores_mi)
        
        ### ** CÁLCULO DO COEFICIENTE DE REGRESSÃO - TAXA ESPECÍFICA DE CRESCIMENTO MICROBIANO ** ###:
        def r2_mi():
            # Cálculo R²:
            if (cont_model == 9):
                Label(frame2, text = "", font = "batang 10",  bg = "grey40", width = 10).place(x = 1168, y = 329.2)
                Label(frame2, text = "Não atribuído", font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            else:
                df_mi = pd.DataFrame({'Tempo(h)': Ttotal, 'mi(h-¹)': mi})
                df_t_exp = pd.DataFrame({'Tempo(h)': Ttotal_exp})
                df_mi_merge = df_mi.merge(df_t_exp, how = 'inner' ,indicator=False)
                df_mi_exp = pd.DataFrame({'Tempo_exp(h)':Ttotal_exp, 'mi(h-¹)': mi_exp})
                print(df_mi_merge)
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
                print(r2_mi[0])
                
        #### **** Impressão do valor do R² concentração na interface **** ####:
        ## Botão para acesso:
        Button(frame41, text = "R²", font = "batang 12 bold", fg = "black", bg = "grey70", command = r2_mi).place(x = 452, y = 45)  

## ** \\ ___________________________________________GRÁFICO - TAXA ESPECÍFICA DE CRESCIMENTO____________________________________ \\ ** ## 
           
        
## ** // _____________________________________________GRÁFICO - VARIAÇÃO DE VOLUME___________________________________________ // ** ##
        
        ### *** CÁLCULO DO PERFIL DE VARIAÇÃO DE VOLUME - RELAÇÃO TEMPORAL DEPENDENTE DA ALIMENTAÇÃO:
        ## ** Controle do processo - análise do perfil matemático ** ##:
        # - ALIMENTAÇÃO CONSTANTE:
        if (def_alim == "Taxa de Vazão Constante"):
            ## Cálculo volume(t) - integração dV/dt = Q para Q constante:
            # - Experimental:
            V_calc_exp = Q * t_exp_bat_alim  + V0
            # - Modelada:
            V_calc = Q * t_alim  + V0
        # - ALIMENTAÇÃO LINEAR:
        if (def_alim == "Taxa de Vazão Linear"):
            ## Cálculo volume(t) - integração dV/dt = Q para descrito pela equação linear:
            # - Experimental:
            V_calc_exp = (Q0*(t_exp_bat_alim + (a*t_exp_bat_alim**2))) + V0
            # - Modelada:
            V_calc = (Q0*(t_alim + (a*t_alim**2))) + V0
        # - ALIMENTAÇÃO EXPONENCIAL:
        if (def_alim == "Taxa de Vazão Exponencial"):
            ## Cálculo volume(t) - integração dV/dt = Q para Q descrito pela equação exponencial::
            # - Experimental:
            V_calc_exp = ((Q0/beta_exp)*((np.exp(beta_exp*t_exp_bat_alim)) - 1)) + V0
            # - Modelada:
            V_calc = ((Q0/beta_exp)*((np.exp(beta_exp*t_alim)) - 1)) + V0
        
        ## * GRÁFICO * ##:
        # - Figura como função das entradas fornecidas pelo usuário:
        def graf_vol(vol_cor, vol_exp_cor):
            def imprimir_vol (t_ajus,t_m, vol_ajus, vol_m):
                tamanho_graf()
                f = plt.figure(figsize=(8.3,6), dpi = 54) 
                plot = f.add_subplot(111)                                             
                _ = plt.plot(t_m,vol_m,color = vol_cor,linewidth=3, label='Modelo')
                _ = plt.plot(t_ajus,vol_ajus,'o',markersize=6, color = vol_exp_cor, label='Experimental')
                _ = plot.axvline(x = tf_bat, color = "grey", linestyle="dashed", linewidth=3)
                _ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
                _ = plt.ylabel('Volume (L)', weight='bold')
                _ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.14),ncol=2, fancybox=True, shadow=True )  
                _ = plt.grid(True)  
                f.patch.set_facecolor('white')                                   
                plt.style.use('default')   
                canvas = FigureCanvasTkAgg(f, frame44)
                a = canvas.get_tk_widget().place(x = 0, y = 0)
                def salvar():
                    a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                    defaultextension='.png')
                    plt.savefig(a)  
                botao_com_graf(frame = frame44, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy, x = 450, y = 176)
            imprimir_vol (t_exp_bat_alim, t_alim, V_calc_exp, V_calc)
            
        # - Escolha das cores:
        def seletor_cores_vol():
            cor_vol = colorchooser.askcolor(title ="Editar cores")
            cor_vol = cor_vol[1]
            graf_vol(vol_cor = cor_vol, vol_exp_cor = cor_vol)
            
        # - Geração do gráfico padrão fermenpy:
        graf_vol(vol_cor = "orange", vol_exp_cor = "orange")
        # - Botão para seleção das cores:
        botao_paleta_graf(frame44, comando = seletor_cores_vol)
        
        ### ** CÁLCULO DO COEFICIENTE DE REGRESSÃO - VARIAÇÃO TEMPORAL DE VOLUME ** ###:
        def r2_vol():
            df_vol = pd.DataFrame({'Tempo(h)': t_alim})
            df_t_exp = pd.DataFrame({'Tempo(h)': t_exp_bat_alim})
            df_vol_merge = pd.merge(df_vol, df_t_exp, how = 'right', on = 'Tempo(h)')
            df_vol_exp = pd.DataFrame({'Tempo_exp(h)':t_exp_bat_alim, 'Vol(L)': V_calc_exp})
            print(df_vol_merge)
            print(df_vol)
            print(df_t_exp)
            del df_vol_merge['Tempo(h)']
            del df_vol_exp['Tempo_exp(h)']
            df_vol_merge = df_vol_merge.values
            df_vol_exp = df_vol_exp.values
            resid = (df_vol_merge - df_vol_exp)**2
            resid = resid.flatten()
            resid = sum(resid)
            vol_medio = np.mean(df_vol_exp)
            vol_total = sum((df_vol_exp- vol_medio)**2)
            r2_vol = 1 - (resid/vol_total)
            Label(frame2, text = "", font = "batang 10",  bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            Label(frame2, text = r2_vol[0].round(4), font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            print(r2_vol[0])
    
        #### **** Impressão do valor do R² concentração na interface **** ####:
        ## Botão para acesso:
        Button(frame44, text = "R²", font = "batang 12 bold", fg = "black", bg = "grey70", command = r2_vol).place(x = 452, y = 45) 

## ** \\ _____________________________________________GRÁFICO - VARIAÇÃO DE VOLUME___________________________________________ \\ ** ##              

        
## ** // _____________________________________________GRÁFICO - VARIAÇÃO DE VAZÃO___________________________________________ // ** ##
        
        ### *** CÁLCULO DO PERFIL DE VARIAÇÃO DE VAZÃO - RELAÇÃO TEMPORAL DEPENDENTE DA ALIMENTAÇÃO:
        ## ** Controle do processo - análise do perfil matemático ** ##:
        # - ALIMENTAÇÃO CONSTANTE:
        if (def_alim == "Taxa de Vazão Constante"):
            # - Experimental:
            Q_calc_exp = np.repeat(Q, len(t_exp_bat_alim))
            # - Modelada:
            Q_calc = np.repeat(Q, len(t_alim))
        # - ALIMENTAÇÃO LINEAR:
        if (def_alim == "Taxa de Vazão Linear"):
            ### Função Q(t) original:
            # - Experimental:
            Q_calc_exp = Q0*(1 + a*t_exp_bat_alim)
            # - Modelada:
            Q_calc = Q0*(1 + a*t_alim)
        # - ALIMENTAÇÃO EXPONENCIAL:
        if (def_alim == "Taxa de Vazão Exponencial"):
            ### Função Q(t) original:
            # - Experimental:
            Q_calc_exp = Q0 * np.exp(beta_exp * t_exp_bat_alim)
            # - Modelada:
            Q_calc = Q0 * np.exp(beta_exp * t_alim)
        
        ## * GRÁFICO * ##:
        # - Figura como função das entradas fornecidas pelo usuário:
        def graf_vaz(vaz_cor, vaz_exp_cor):
            def imprimir_vaz(t_ajus,t_m, vaz_ajus, vaz_m):
                tamanho_graf()
                f = plt.figure(figsize=(8.3,6), dpi = 54) 
                plot = f.add_subplot(111)                                             
                _ = plt.plot(t_m,vaz_m,color = vaz_cor,linewidth=3, label='Modelo')
                _ = plt.plot(t_ajus,vaz_ajus,'o',markersize=6, color = vaz_exp_cor, label='Experimental')
                _ = plot.axvline(x = tf_bat, color = "grey", linestyle="dashed", linewidth=3)
                _ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
                _ = plt.ylabel('Vazão (L/h)', weight='bold')
                _ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.14),ncol=2, fancybox=True, shadow=True )  
                _ = plt.grid(True)  
                f.patch.set_facecolor('white')                                   
                plt.style.use('default')   
                canvas = FigureCanvasTkAgg(f, frame45)
                a = canvas.get_tk_widget().place(x = 0, y = 0)
                def salvar():
                    a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                    defaultextension='.png')
                    plt.savefig(a)  
                botao_com_graf(frame = frame45, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy, x = 450, y = 176)
            imprimir_vaz(t_exp_bat_alim, t_alim, Q_calc_exp, Q_calc)
            
        # - Escolha das cores:
        def seletor_cores_vaz():
            cor_vaz = colorchooser.askcolor(title ="Editar cores")
            cor_vaz = cor_vaz[1]
            graf_vaz(vaz_cor = cor_vaz, vaz_exp_cor = cor_vaz)
            
        # - Geração do gráfico padrão fermenpy:
        graf_vaz(vaz_cor = "lime", vaz_exp_cor = "lime")
        # - Botão para seleção das cores:
        botao_paleta_graf(frame45, comando = seletor_cores_vaz)
        
        ### ** CÁLCULO DO COEFICIENTE DE REGRESSÃO - VARIAÇÃO DA VAZÃO ** ###:
        def r2_vaz():
            df_vaz = pd.DataFrame({'Tempo(h)': t_alim, 'Vazão (L/h)': Q_calc})
            df_t_exp = pd.DataFrame({'Tempo(h)': t_exp_bat_alim})
            df_vaz_merge = df_vaz.merge(df_t_exp, on = 'Tempo(h)')
            print(df_vaz_merge)
            df_vaz_exp = pd.DataFrame({'Tempo_exp(h)':t_exp_bat_alim, 'Vazão (L/h)': Q_calc_exp})
            del df_vaz_merge['Tempo(h)']
            del df_vaz_exp['Tempo_exp(h)']
            df_vaz_merge = df_vaz_merge.values
            df_vaz_exp = df_vaz_exp.values
            resid = (df_vaz_merge - df_vaz_exp)**2
            resid = resid.flatten()
            resid = sum(resid)
            vaz_medio = np.mean(df_vaz_exp)
            vaz_total = sum((df_vaz_exp - vaz_medio)**2)
            r2_vaz = 1 - (resid/vaz_total)
            Label(frame2, text = "", font = "batang 10",  bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            Label(frame2, text = r2_vaz[0].round(4), font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            print(r2_vaz[0])
        
        #### **** Impressão do valor do R² concentração na interface **** ####:
        ## Botão para acesso:
        Button(frame45, text = "R²", font = "batang 12 bold", fg = "black", bg = "grey70", command = r2_vaz).place(x = 452, y = 45) 

## ** \\ _____________________________________________GRÁFICO - VARIAÇÃO DE VOLUME___________________________________________ \\ ** ##            
        
        
### *** ____________________________SAÍDAS EM FORMATO PLANILHAS EXCEL____________________________ *** ###
        # - Inserindo 0 para o primeiro valor de produtividade:
        ## Experimental:
        # -- Células
        Px_exp_ad = np.insert(Px_exp,0,0)
        # -- Produto:
        Pp_exp_ad = np.insert(Pp_exp,0,0)
        ## Modelada:
        # -- Células:
        Px_ad = np.insert(Px,0,0)
        # -- Produto:
        Pp_ad = np.insert(Pp,0,0)
        
        # - Saída .xlsx - concentração, produtividades e taxa de crescimento:
        def excel_concent_produtiv():
            df_sai_exp = pd.DataFrame({'Tempo_exp(h)': t_exp, 'Cx_exp(g/L)': C_exp[:,0], 'Cs_exp(g/L)': C_exp[:,1], 'Cp_exp(g/L)': C_exp[:,2], 'Px_exp(gcél/L.h)': Px_exp_ad, 'Pp_exp(gprod/L.h)': Pp_exp_ad, 'Ppx_exp(gprod/gcél)': Ppx_exp, 'mi_exp(h-¹)': mi_exp})
            df_sai_model = pd.DataFrame({'Tempo(h)': Ttotal, 'Cx(g/L)': Cx, 'Cs(g/L)': Cs, 'Cp(g/L)': Cp, 'Px(gcél/L.h)': Px_ad, 'Pp(gprod/L.h)': Pp_ad, 'Ppx(gprod/gcél)': Ppx, 'mi(h-¹)': mi})
            df_tempo_exp_bat_alim = pd.DataFrame({'Tempo_exp_alim(h)': t_exp_bat_alim})
            df_Q_V_exp = pd.DataFrame({'Q_exp(L/h)': Q_calc_exp, 'V_exp(L)': V_calc_exp})
            df_tempo_bat_alim = pd.DataFrame({'Tempo_alim(h)': t_alim})
            df_Q_V = pd.DataFrame({'Q(L/h)': Q_calc, 'V(L)': V_calc})
            df_r2 = pd.DataFrame({'R²':[r2]})
            df_fun_err_val = pd.DataFrame({'Função erro': [res_final]})
            df_tempo = pd.DataFrame({"Tempo(s)":[elapsed]})
            df_concents = pd.concat([df_sai_exp, df_sai_model, df_tempo_exp_bat_alim, df_Q_V_exp, df_tempo_bat_alim, df_Q_V, df_r2, df_fun_err_val, df_tempo], axis = 1)
            with pd.ExcelWriter('Modelagem_Conc_Prod_mi_Q_V.xlsx') as writer:
                df_concents.to_excel(writer, sheet_name="Saida_exp_modelada")
                writer.save()
            os.system("start EXCEL Modelagem_Conc_Prod_mi_Q_V.xlsx")
        Label(frame2, text = "Modelagem_Conc_Prod_mi_Q_V.xlsx", font = "arial 8 italic", fg = "black", bg = "gray45").place(x = 1072, y = 50)
        
        ## Botões de acesso - arquivo .xlsx - parâmetros cinéticos:
        botao_excel(imagem = "Excel.png", num_frame = frame2, x = 1036, y = 42, comando = excel_concent_produtiv)

        
        # Saída .xlsx - parâmetros cinéticos:
        lista_processos = ["BATELADA", "BATELADA ALIMENTADA"]
        def excel_param():
            if (cont_model == 0): # Monod (5p)
                # - Batelada:
                df_params_model_bat =pd.DataFrame({'mimax(h-¹)':[param_otim_alm_bat[0]],'Ks(g/L)':[param_otim_alm_bat[1]],'Yxs(gcél/gsub)':[param_otim_alm_bat[2]], 'alfa(gprod/gcél)': [param_otim_alm_bat[3]], 'beta(gprod/gcél.h)':[param_otim_alm_bat[4]]})
                df_params_IC_bat = pd.DataFrame({'IC mimax(h-¹)':[ICpar_bat[0]],'IC Ks(g/L)':[ICpar_bat[1]],'IC Yxs(gcél/gsub)':[ICpar_bat[2]], 'IC alfa(gprod/gcél)': [ICpar_bat[3]], 'IC beta(gprod/gcél.h)':[ICpar_bat[4]]})
                # - Batelada alimentada:
                df_params_model_alim =pd.DataFrame({'mimax(h-¹)':[param_otim_alm_alim[0]],'Ks(g/L)':[param_otim_alm_alim[1]],'Yxs(gcél/gsub)':[param_otim_alm_alim[2]], 'alfa(gprod/gcél)': [param_otim_alm_alim[3]], 'beta(gprod/gcél.h)':[param_otim_alm_alim[4]]})
                df_params_IC_alim = pd.DataFrame({'IC mimax(h-¹)':[ICpar_alim[0]],'IC Ks(g/L)':[ICpar_alim[1]],'IC Yxs(gcél/gsub)':[ICpar_alim[2]], 'IC alfa(gprod/gcél)': [ICpar_alim[3]], 'IC beta(gprod/gcél.h)':[ICpar_alim[4]]})
            if (cont_model == 1): # Contois (5p)
                # - Batelada:
                df_params_model_bat =pd.DataFrame({'mimax(h-¹)':[param_otim_alm_bat[0]],'KSX(gsub/gcél)':[param_otim_alm_bat[1]], 'Yxs(gcél/gsub)':[param_otim_alm_bat[2]], 'alfa(gprod/gcél)': [param_otim_alm_bat[3]], 'beta(gprod/gcél.h)':[param_otim_alm_bat[4]]})
                df_params_IC_bat = pd.DataFrame({'IC mimax(h-¹)':[ICpar_bat[0]],'IC KSX(gsub/gcél)':[ICpar_bat[1]],'IC Yxs(gcél/gsub)':[ICpar_bat[2]], 'IC alfa(gprod/gcél)': [ICpar_bat[3]], 'IC beta(gprod/gcél.h)':[ICpar_bat[4]]})
                # - Batelada alimentada:
                df_params_model_alim =pd.DataFrame({'mimax(h-¹)':[param_otim_alm_alim[0]],'KSX(gsub/gcél)':[param_otim_alm_alim[1]], 'Yxs(gcél/gsub)':[param_otim_alm_alim[2]], 'alfa(gprod/gcél)': [param_otim_alm_alim[3]], 'beta(gprod/gcél.h)':[param_otim_alm_alim[4]]})
                df_params_IC_alim = pd.DataFrame({'IC mimax(h-¹)':[ICpar_alim[0]],'IC KSX(gsub/gcél)':[ICpar_alim[1]],'IC Yxs(gcél/gsub)':[ICpar_alim[2]], 'IC alfa(gprod/gcél)': [ICpar_alim[3]], 'IC beta(gprod/gcél.h)':[ICpar_alim[4]]})
            if (cont_model == 4): # Moser (5p)
                # - Batelada:
                df_params_model_bat = pd.DataFrame({'mimax(h-¹)':[param_otim_alm_bat[0]],'Ks(g/L)':[param_otim_alm_bat[1]],'Yxs(gcél/gsub)':[param_otim_alm_bat[2]], 'alfa(gprod/gcél)': [param_otim_alm_bat[3]], 'beta(gprod/gcél.h)':[param_otim_alm_bat[4]],'u(adim)':[param_otim_alm_bat[5]]})
                df_params_IC_bat = pd.DataFrame({'IC mimax(h-¹)':[ICpar_bat[0]],'IC Ks(g/L)':[ICpar_bat[1]], 'IC Yxs(gcél/gsub)':[ICpar_bat[2]], 'IC alfa(gprod/gcél)': [ICpar_bat[3]], 'IC beta(gprod/gcél.h)':[ICpar_bat[4]], 'IC mi_exp(adim)':[ICpar_bat[5]]})
                # - Batelada alimentada:
                df_params_model_alim = pd.DataFrame({'mimax(h-¹)':[param_otim_alm_alim[0]],'Ks(g/L)':[param_otim_alm_alim[1]],'Yxs(gcél/gsub)':[param_otim_alm_alim[2]], 'alfa(gprod/gcél)': [param_otim_alm_alim[3]], 'beta(gprod/gcél.h)':[param_otim_alm_alim[4]],'u(adim)':[param_otim_alm_alim[5]]})
                df_params_IC_alim = pd.DataFrame({'IC mimax(h-¹)':[ICpar_alim[0]],'IC Ks(g/L)':[ICpar_alim[1]], 'IC Yxs(gcél/gsub)':[ICpar_alim[2]], 'IC alfa(gprod/gcél)': [ICpar_alim[3]], 'IC beta(gprod/gcél.h)':[ICpar_alim[4]], 'IC mi_exp(adim)':[ICpar_alim[5]]})
            if (cont_model == 2): # Andrews (6p)
                # - Batelada:
                df_params_model_bat = pd.DataFrame({'mimax(h-¹)':[param_otim_alm_bat[0]],'Ks(g/L)':[param_otim_alm_bat[1]],'Yxs(gcél/gsub)':[param_otim_alm_bat[2]], 'alfa(gprod/gcél)': [param_otim_alm_bat[3]], 'beta(gprod/gcél.h)':[param_otim_alm_bat[4]], 'KSI(g/L)':[param_otim_alm_bat[5]]})
                df_params_IC_bat = pd.DataFrame({'IC mimax(h-¹)':[ICpar_bat[0]],'IC Ks(g/L)':[ICpar_bat[1]],'IC Yxs(gcél/gsub)':[ICpar_bat[2]], 'IC alfa(gprod/gcél)': [ICpar_bat[3]], 'IC beta(gprod/gcél.h)':[ICpar_bat[4]], 'IC KSI(g/L)':[ICpar_bat[5]]})
                # - Batelada alimentada:
                df_params_model_alim = pd.DataFrame({'mimax(h-¹)':[param_otim_alm_alim[0]],'Ks(g/L)':[param_otim_alm_alim[1]],'Yxs(gcél/gsub)':[param_otim_alm_alim[2]], 'alfa(gprod/gcél)': [param_otim_alm_alim[3]], 'beta(gprod/gcél.h)':[param_otim_alm_alim[4]], 'KSI(g/L)':[param_otim_alm_alim[5]]})
                df_params_IC_alim = pd.DataFrame({'IC mimax(h-¹)':[ICpar_alim[0]],'IC Ks(g/L)':[ICpar_alim[1]],'IC Yxs(gcél/gsub)':[ICpar_alim[2]], 'IC alfa(gprod/gcél)': [ICpar_alim[3]], 'IC beta(gprod/gcél.h)':[ICpar_alim[4]], 'IC KSI(g/L)':[ICpar_alim[5]]})
            if (cont_model == 5): # Hoppe_Hansford (6p)
                # - Batelada:
                df_params_model_bat =pd.DataFrame({'mimax(h-¹)':[param_otim_alm_bat[0]],'Ks(g/L)':[param_otim_alm_bat[1]],'Yxs(gcél/gsub)':[param_otim_alm_bat[2]], 'alfa(gprod/gcél)': [param_otim_alm_bat[3]], 'beta(gprod/gcél.h)':[param_otim_alm_bat[4]], 'Kp(g/L)':[param_otim_alm_bat[5]]})
                df_params_IC_bat = pd.DataFrame({'IC mimax(h-¹)':[ICpar_bat[0]],'IC Ks(g/L)':[ICpar_bat[1]], 'IC Yxs(gcél/gsub)':[ICpar_bat[2]], 'IC alfa(gprod/gcél)': [ICpar_bat[3]], 'IC beta(gprod/gcél.h)':[ICpar_bat[4]], 'IC Kp(g/L)':[ICpar_bat[5]]})
                # - Batelada alimentada:
                df_params_model_alim =pd.DataFrame({'mimax(h-¹)':[param_otim_alm_alim[0]],'Ks(g/L)':[param_otim_alm_alim[1]],'Yxs(gcél/gsub)':[param_otim_alm_alim[2]], 'alfa(gprod/gcél)': [param_otim_alm_alim[3]], 'beta(gprod/gcél.h)':[param_otim_alm_alim[4]], 'Kp(g/L)':[param_otim_alm_alim[5]]})
                df_params_IC_alim = pd.DataFrame({'IC mimax(h-¹)':[ICpar_alim[0]],'IC Ks(g/L)':[ICpar_alim[1]], 'IC Yxs(gcél/gsub)':[ICpar_alim[2]], 'IC alfa(gprod/gcél)': [ICpar_alim[3]], 'IC beta(gprod/gcél.h)':[ICpar_alim[4]], 'IC Kp(g/L)':[ICpar_alim[5]]})
            if (cont_model == 3): # Aiba (6p)
                # -  Batelada:
                df_params_model_bat = pd.DataFrame({'mimax(h-¹)':[param_otim_alm_bat[0]],'Ks(g/L)':[param_otim_alm_bat[1]],'Yxs(gcél/gsub)':[param_otim_alm_bat[2]], 'alfa(gprod/gcél)': [param_otim_alm_bat[3]], 'beta(gprod/gcél.h)':[param_otim_alm_bat[4]], 'Kp(L/g)':[param_otim_alm_bat[5]]})
                df_params_IC_bat= pd.DataFrame({'IC mimax(h-¹)':[ICpar_bat[0]],'IC Ks(g/L)':[ICpar_bat[1]],'IC Yxs(gcél/gsub)':[ICpar_bat[2]], 'IC alfa(gprod/gcél)': [ICpar_bat[3]], 'IC beta(gprod/gcél.h)':[ICpar_bat[4]], 'IC Kp(g/L)':[ICpar_bat[5]]})
                # -  Batelada alimentada:
                df_params_model_alim = pd.DataFrame({'mimax(h-¹)':[param_otim_alm_alim[0]],'Ks(g/L)':[param_otim_alm_alim[1]],'Yxs(gcél/gsub)':[param_otim_alm_alim[2]], 'alfa(gprod/gcél)': [param_otim_alm_alim[3]], 'beta(gprod/gcél.h)':[param_otim_alm_alim[4]], 'Kp(L/g)':[param_otim_alm_alim[5]]})
                df_params_IC_alim = pd.DataFrame({'IC mimax(h-¹)':[ICpar_alim[0]],'IC Ks(g/L)':[ICpar_alim[1]],'IC Yxs(gcél/gsub)':[ICpar_alim[2]], 'IC alfa(gprod/gcél)': [ICpar_alim[3]], 'IC beta(gprod/gcél.h)':[ICpar_alim[4]], 'IC Kp(g/L)':[ICpar_alim[5]]})
            if (cont_model == 6): # Wu (7p)
                # -  Batelada:
                df_params_model_bat = pd.DataFrame({'mimax(h-¹)':[param_otim_alm_bat[0]],'Ks(g/L)':[param_otim_alm_bat[1]],'Yxs(gcél/gsub)':[param_otim_alm_bat[2]], 'alfa(gprod/gcél)': [param_otim_alm_bat[3]], 'beta(gprod/gcél.h)':[param_otim_alm_bat[4]],'KE(g/L)':[param_otim_alm_bat[5]], 'v(adim)':[param_otim_alm_bat[6]]})
                df_params_IC_bat = pd.DataFrame({'IC mimax(h-¹)':[ICpar_bat[0]],'IC Ks(g/L)':[ICpar_bat[1]],'IC Yxs(gcél/gsub)':[ICpar_bat[2]], 'IC alfa(gprod/gcél)': [ICpar_bat[3]], 'IC beta(gprod/gcél.h)':[ICpar_bat[4]], 'IC KE(g/L)':[ICpar_bat[5]], 'IC v(adim)':[ICpar_bat[6]]})
                # -  Batelada alimentada:
                df_params_model_alim = pd.DataFrame({'mimax(h-¹)':[param_otim_alm_alim[0]],'Ks(g/L)':[param_otim_alm_alim[1]],'Yxs(gcél/gsub)':[param_otim_alm_alim[2]], 'alfa(gprod/gcél)': [param_otim_alm_alim[3]], 'beta(gprod/gcél.h)':[param_otim_alm_alim[4]],'KE(g/L)':[param_otim_alm_alim[5]], 'v(adim)':[param_otim_alm_alim[6]]})
                df_params_IC_alim = pd.DataFrame({'IC mimax(h-¹)':[ICpar_alim[0]],'IC Ks(g/L)':[ICpar_alim[1]],'IC Yxs(gcél/gsub)':[ICpar_alim[2]], 'IC alfa(gprod/gcél)': [ICpar_alim[3]], 'IC beta(gprod/gcél.h)':[ICpar_alim[4]], 'IC KE(g/L)':[ICpar_alim[5]], 'IC v(adim)':[ICpar_alim[6]]})
            if (cont_model == 7): # Levenspiel (7p)
                # - Batelada:
                df_params_model_bat = pd.DataFrame({'mimax(h-¹)':[param_otim_alm_bat[0]],'Ks(g/L)':[param_otim_alm_bat[1]],'Yxs(gcél/gsub)':[param_otim_alm_bat[2]], 'alfa(gprod/gcél)': [param_otim_alm_bat[3]], 'beta(gprod/gcél.h)':[param_otim_alm_bat[4]], 'n(adim)':[param_otim_alm_bat[5]], 'Cp_estr(g/L)':[param_otim_alm_bat[6]]})
                df_params_IC_bat = pd.DataFrame({'IC mimax(h-¹)':[ICpar_bat[0]],'IC Ks(g/L)':[ICpar_bat[1]], 'IC Yxs(gcél/gsub)':[ICpar_bat[2]], 'IC alfa(gprod/gcél)': [ICpar_bat[3]], 'IC beta(gprod/gcél.h)':[ICpar_bat[4]], 'IC n(adim)':[ICpar_bat[5]], 'IC Cp_estr(g/L)':[ICpar_bat[6]]})  
                # - Batelada alimentada:
                df_params_model_alim = pd.DataFrame({'mimax(h-¹)':[param_otim_alm_alim[0]],'Ks(g/L)':[param_otim_alm_alim[1]],'Yxs(gcél/gsub)':[param_otim_alm_alim[2]], 'alfa(gprod/gcél)': [param_otim_alm_alim[3]], 'beta(gprod/gcél.h)':[param_otim_alm_alim[4]], 'n(adim)':[param_otim_alm_alim[5]], 'Cp_estr(g/L)':[param_otim_alm_alim[6]]})
                df_params_IC_alim = pd.DataFrame({'IC mimax(h-¹)':[ICpar_alim[0]],'IC Ks(g/L)':[ICpar_alim[1]], 'IC Yxs(gcél/gsub)':[ICpar_alim[2]], 'IC alfa(gprod/gcél)': [ICpar_alim[3]], 'IC beta(gprod/gcél.h)':[ICpar_alim[4]], 'IC n(adim)':[ICpar_alim[5]], 'IC Cp_estr(g/L)':[ICpar_alim[6]]})  
            if (cont_model == 8): # Lee (7p)
                # - Batelada:
                df_params_model_bat =pd.DataFrame({'mimax(h-¹)':[param_otim_alm_bat[0]],'Ks(g/L)':[param_otim_alm_bat[1]],'Yxs(gcél/gsub)':[param_otim_alm_bat[2]], 'alfa(gprod/gcél)': [param_otim_alm_bat[3]], 'beta(gprod/gcél.h)':[param_otim_alm_bat[4]], 'm(adim)':[param_otim_alm_bat[5]], 'Cx_estr(g/L)':[param_otim_alm_bat[6]]})
                df_params_IC_bat = pd.DataFrame({'IC mimax(h-¹)':[ICpar_bat[0]],'IC Ks(g/L)':[ICpar_bat[1]],'IC Yxs(gcél/gsub)':[ICpar_bat[2]], 'IC alfa(gprod/gcél)': [ICpar_bat[3]], 'IC beta(gprod/gcél.h)':[ICpar_bat[4]], 'IC m(adim)':[ICpar_bat[5]], 'IC Cx_estr(g/L)':[ICpar_bat[6]]}) 
                # - Batelada alimentada:
                df_params_model_alim =pd.DataFrame({'mimax(h-¹)':[param_otim_alm_alim[0]],'Ks(g/L)':[param_otim_alm_alim[1]],'Yxs(gcél/gsub)':[param_otim_alm_alim[2]], 'alfa(gprod/gcél)': [param_otim_alm_alim[3]], 'beta(gprod/gcél.h)':[param_otim_alm_alim[4]], 'm(adim)':[param_otim_alm_alim[5]], 'Cx_estr(g/L)':[param_otim_alm_alim[6]]})
                df_params_IC_alim = pd.DataFrame({'IC mimax(h-¹)':[ICpar_alim[0]],'IC Ks(g/L)':[ICpar_alim[1]],'IC Yxs(gcél/gsub)':[ICpar_alim[2]], 'IC alfa(gprod/gcél)': [ICpar_alim[3]], 'IC beta(gprod/gcél.h)':[ICpar_alim[4]], 'IC m(adim)':[ICpar_alim[5]], 'IC Cx_estr(g/L)':[ICpar_alim[6]]}) 
            if (cont_model == 9): # mi constante (4p)
                df_params_model_alim =pd.DataFrame({'mi(h-¹)':[param_otim_alm_alim[0]],'Yxs(gcél/gsub)':[param_otim_alm_alim[1]], 'alfa(gprod/gcél)': [param_otim_alm_alim[2]], 'beta(gprod/gcél.h)':[param_otim_alm_alim[3]]})
                df_params_IC_alim = pd.DataFrame({'IC mi(h-¹)':[ICpar_alim[0]],'IC Kd(h-¹)':[ICpar_alim[1]],'IC Yxs(gcél/gsub)':[ICpar_alim[1]], 'IC alfa(gprod/gcél)': [ICpar_alim[2]], 'IC beta(gprod/gcél.h)':[ICpar_alim[3]]})
            # - DataFrame com o modo de operação:
            df_tex_proces = pd.DataFrame({"OPERAÇÃO": lista_processos})
            df_IC = pd.concat([df_params_IC_bat, df_params_IC_alim], axis = 0)
            #df_params = pd.concat([df_params_model_bat, df_params_model_alim], axis = 0)
            df_saida = pd.concat([df_tex_proces, df_IC], axis = 0)
            with pd.ExcelWriter('Modelagem_Parametros_Cineticos.xlsx') as writer:
                df_saida.to_excel(writer, sheet_name="Param_model")
                writer.save()
            os.system("start EXCEL Modelagem_Parametros_Cineticos.xlsx")
        Label(frame2, text = "Modelagem_Params_Cineticos.xlsx", font = "arial 8 italic", fg = "black", bg = "gray45").place(x = 1072, y = 87)
        
        ## Botões de acesso - arquivo .xlsx - parâmetros cinéticos:
        botao_excel(imagem = "Excel.png", num_frame = frame2, x = 1036, y = 80, comando = excel_param)
               
        ####### ****** FIM DA MODELAGEM ******* #########
        return()
      

    # Selecionar os modelos não estruturados para a modelagem:
    ## * SAÍDA DOS VALORES OTIMIZADOS DE CADA PARÂMETRO RELACIONADO * ##
    def click_contois(): 
        tab_fun_cin()
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     KSX(gs.gx\u207b\u00b9)", font = "arial 10 bold", justify = "center", fg = "black", bg = "grey75", width = 21).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gp.gx\u207b\u00b9)    \u03B2[gp.(gx.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
    def model_contois():   
        modelagem(cont_model = 1)
    
    def click_monod(): 
        tab_fun_cin()
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 20).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gp.gx\u207b\u00b9)    \u03B2[gp.(gx.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380) 
    def model_monod():
        modelagem(cont_model = 0)
        
    def click_moser(): 
        tab_fun_cin()
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)   
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)     u(adim)", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 28).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gp.gx\u207b\u00b9)    \u03B2[gp.(gx.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
    def model_moser():
        modelagem(cont_model = 4)
    
    def click_mi_const(): 
        tab_fun_cin()
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)   
        Label(frame2, text = u"\u03bc(h\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "grey75", width = 5).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gp.gx\u207b\u00b9)    \u03B2[gp.(gx.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
    '''def model_mi_const():  
        modelagem(cont_model = 9)'''
        
    def click_aiba(): 
        tab_fun_cin()
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)     Kp(L.g\u207b\u00b9)", font = "arial 10 bold", justify = "center", fg = "black", bg = "grey75", width = 28).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gp.gx\u207b\u00b9)    \u03B2[gp.(gx.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
    def model_aiba():   
        modelagem(cont_model = 3)

    def click_hoppe_hansford(): 
        tab_fun_cin() 
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)     Kp(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 28).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gp.gx\u207b\u00b9)    \u03B2[gp.(gx.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
    def model_hoppe_hansford(): 
        modelagem(cont_model = 5)
        
    def click_levenspiel(): 
        tab_fun_cin() 
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)    Ks(g.L\u207b\u00b9)     n(adim)     Cp*(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 37).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gp.gx\u207b\u00b9)   \u03B2[gp.(gx.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
    def model_levenspiel():   
        modelagem(cont_model = 7)
        
    def click_andrews(): 
        tab_fun_cin() 
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)      Ks(g.L\u207b\u00b9)     KIS(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 30).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gp.gx\u207b\u00b9)    \u03B2[gp.(gx.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
    def model_andrews():   
        modelagem(cont_model = 2)
        
    def click_wu(): 
        tab_fun_cin()
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)     KE(g.L\u207b\u00b9)     v(adim)", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 37).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gp.gx\u207b\u00b9)    \u03B2[gp.(gx.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
    def model_wu():    
        modelagem(cont_model = 6)
        
    def click_lee(): 
        tab_fun_cin()
        Label(frame2, text = "b", font = "times 18", fg = "grey40", bg = "grey40",  borderwidth=4, relief ='sunken', width = 6).place(x = 990, y = 310)
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)    Ks(g.L\u207b\u00b9)     m(adim )     Cx*(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 37).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gp.gx\u207b\u00b9)    \u03B2[gp.(gx.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey75", justify = "center", width = 41).place(x = 932, y = 380)
    def model_lee():   
        modelagem(cont_model = 8)
    
    ## * HABILITAÇÃO DOS MODELOS NÃO ESTRUTURADOS - OPÇÃO DO USUÁRIO ATRAVÉS DO COMBOBOX * ##:
    # Função para captura do valor selecionado:
    def combobox_model():
        val_model = combo_2.get()
        print(val_model)
        # Disponibilização dos modelos através dos notebooks:
        if val_model == "AUSÊNCIA DE INIBIÇÃO":
            notebook_sem_inib_model()
            carregar_imagem(frame = frame4, imagem = "Equacao_Contois.png", borderwidth = 2, relief = "sunken", x = 46, y = 92)
            tex_mimax = Label(frame4, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ksx = Label(frame4, text = u"KSX = constante de saturação (mass.mass\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            carregar_imagem(frame = frame5, imagem = "Equacao_Monod.png", borderwidth = 2, relief = "sunken", x = 60, y = 92)
            tex_mimax = Label(frame5, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame5, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            carregar_imagem(frame = frame6, imagem = "Equacao_Moser.png", borderwidth = 2, relief = "sunken", x = 60, y = 92)
            tex_mimax = Label(frame6, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame6, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            tex_u = Label(frame6, text = "u = parâmetro expoente (adim)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 244)
            carregar_imagem(frame = frame45, imagem = "Equacao_mi_const.png", borderwidth = 2, relief = "sunken", x = 120, y = 92)
            tex_mi = Label(frame45, text = u"\u03bc = taxa específica de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 154)
            tex_mi_explic = Label(frame45, text = "A velocidade de crescimento microbiano mantém-se\nconstante durante todo o tempo t de cultivo", font = 'arial 9 italic', fg = "black", relief = "sunken").place(x = 0, y = 200)
            Button(frame4, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = model_contois).place(x = 112, y = 28)
            Button(frame4, text = "Preparar ambiente", bg = "gray40", fg="white", borderwidth=4, relief="raised", font="batang 9", command = click_contois).place(x = 187, y = 282)
            Button(frame5, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = model_monod).place(x = 112, y = 28)
            Button(frame5, text = "Preparar ambiente", bg = "gray40", fg="white", borderwidth=4, relief="raised", font="batang 9", command = click_monod).place(x = 187, y = 282)
            Button(frame6, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = model_moser).place(x = 112, y = 28)
            Button(frame6, text = "Preparar ambiente", bg = "gray40", fg="white", borderwidth=4, relief="raised", font="batang 9", command = click_moser).place(x = 187, y = 282)
            Button(frame45, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8).place(x = 112, y = 28)
            Button(frame45, text = "Preparar ambiente", bg = "gray40", fg="white", borderwidth=4, relief="raised", font="batang 9", command = click_mi_const).place(x = 187, y = 282)
        if val_model == "INIBIÇÃO PELO SUBSTRATO": 
            notebook_inib_subs_model()
            carregar_imagem(frame = frame7, imagem = "Equacao_Andrews.png", borderwidth = 2, relief = "sunken", x = 45, y = 90)
            tex_mimax = Label(frame7, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame7, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            tex_kis = Label(frame7, text = u"KIS = constante inibição por substrato (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 244)
            carregar_imagem(frame = frame8, imagem = "Equacao_Wu.png", borderwidth = 2, relief = "sunken", x = 26, y = 90)
            tex_mimax = Label(frame8, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame8, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            tex_ke = Label(frame8, text = u"KE = constante inibição por substrato (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 244)
            tex_v = Label(frame8, text = "v = parâmetro expoente (adim)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 274)
            Button(frame7, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = model_andrews).place(x = 112, y = 28)
            Button(frame7, text = "Preparar ambiente", bg = "gray40", fg="white", borderwidth=4, relief="raised", font="batang 9", command = click_andrews).place(x = 187, y = 282)
            Button(frame8, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = model_wu).place(x = 112, y = 28)   
            Button(frame8, text = "Preparar ambiente", bg = "gray40", fg="white", borderwidth=4, relief="raised", font="batang 9", command = click_wu).place(x = 187, y = 282)
        if val_model == "INIBIÇÃO PELO PRODUTO": 
            notebook_inib_prod_model()
            carregar_imagem(frame = frame9, imagem = "Equacao_Aiba.png", borderwidth = 2, relief = "sunken", x = 35, y = 92) 
            tex_mimax = Label(frame9, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame9, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            tex_kp = Label(frame9, text = u"Kp = parâmetro expoente de inibição (vol.mass\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 244)
            carregar_imagem(frame = frame10, imagem = "Equacao_Hoppe_Hansford.png", borderwidth = 2, relief = "sunken", x = 37, y = 92) 
            tex_mimax = Label(frame10, text =u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame10, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            tex_kp = Label(frame10, text = u"Kp = constante inibição por produto (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 244)
            carregar_imagem(frame = frame11, imagem = "Equacao_Levenspiel.png", borderwidth = 2, relief = "sunken", x = 26, y = 92) 
            tex_mimax = Label(frame11, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame11, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            tex_cpestr = Label(frame11, text = u"Cp* = concentração produto crítica (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 244)
            tex_n_lev = Label(frame11, text = "n = constante de Levenspiel (adim)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 274)
            Button(frame9, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = model_aiba).place(x = 112, y = 28)
            Button(frame9, text = "Preparar ambiente", bg = "gray40", fg="white", borderwidth=4, relief="raised", font="batang 9", command = click_aiba).place(x = 187, y = 282)
            Button(frame10, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = model_hoppe_hansford).place(x = 112, y = 28)
            Button(frame10, text = "Preparar ambiente", bg = "gray40", fg="white", borderwidth=4, relief="raised", font="batang 9", command = click_hoppe_hansford).place(x = 187, y = 282)
            Button(frame11, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = model_levenspiel).place(x = 112, y = 28)
            Button(frame11, text = "Preparar ambiente", bg = "gray40", fg="white", borderwidth=4, relief="raised", font="batang 8", command = click_levenspiel).place(x = 202, y = 282)
        if val_model == "INIBIÇÃO PELA BIOMASSA": 
            notebook_inib_biomas_model()
            carregar_imagem(frame = frame12, imagem = "Equacao_Lee.png", borderwidth = 2, relief = "sunken", x = 26, y = 92) 
            tex_mimax = Label(frame12, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 184)
            tex_ks = Label(frame12, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 214)
            tex_cxestr = Label(frame12, text = u"Cx* = concentração celular crítica (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 244)
            tex_m = Label(frame12, text = "m = constante de Lee et al (adim)", font = 'arial 9 italic', fg = "black").place(x = 0, y = 274)
            Button(frame12, text = "MODELAR", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 11", width = 8, command = model_lee).place(x = 112, y = 28)
            Button(frame12, text = "Preparar ambiente", bg = "gray40", fg="white", borderwidth=4, relief="raised", font="batang 8", command = click_lee).place(x = 202, y = 282)
            
    # Botão para acesso aos modelos disponibilizados:
    Button(frame2, text="Pronto", bg = "black", fg="white", font="batang 12", command = combobox_model).place(x = 315, y = 29)
    
# Caixa para plotagem dos gráficos gerados:
notebook_graf_model()
    
# Nome do arquivo excel selecionado é lançado em um label - VÍNCULO COM A FUNÇÃO EXPLORER:
arq_sel = Label(frame2, width = 50)
arq_sel.place(x = 460, y = 50)
# Botão para acesso ao buscador de arquivos da máquina:
Button(frame2, text = "Carregar arquivo",  font="Batang 12", fg="white", bg="gray17", borderwidth=2, relief="raised", command = explorer).place(x = 568, y = 15) 

# Encerramento da janela:
janela.mainloop() 

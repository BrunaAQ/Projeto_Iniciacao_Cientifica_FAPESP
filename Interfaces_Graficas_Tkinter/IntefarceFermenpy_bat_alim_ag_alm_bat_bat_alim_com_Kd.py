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
frame1 = ttk.Frame(notebook, width = 1100, height = 510, borderwidth = 5, relief = tk.SUNKEN)
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
    notebook_graf_simul.add(frame22, text = u'Concent.t\u207b\u00b9')
    global frame23
    frame23 = ttk.Frame(notebook_graf_simul, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_simul.add(frame23, text = 'Produtiv. (Px e Pp)')
    global frame24
    frame24 = ttk.Frame(notebook_graf_simul, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_simul.add(frame24, text = u'Produtiv. (p.x\u207b\u00b9)')
    global frame25
    frame25 = ttk.Frame(notebook_graf_simul, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_simul.add(frame25, text = u'Taxa \u03bcmáx.t\u207b\u00b9')
    global frame46
    frame46 = ttk.Frame(notebook_graf_simul, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_simul.add(frame46, text = u'Volume.t\u207b\u00b9')
    global frame47
    frame47 = ttk.Frame(notebook_graf_simul, width = 500, height = 335, borderwidth = 5, relief = tk.GROOVE)
    notebook_graf_simul.add(frame47, text = u'Vazão.t\u207b\u00b9')
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
# Função para impressão de imagens com bordas padronizadas:
def image(imagem, num_frame, x, y):
    load = Image.open(imagem)
    render = ImageTk.PhotoImage(load)
    img = Label(num_frame, image = render, border = 0, borderwidth = 2, relief = "sunken")
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
def aces_arq(frame, x1, x2, y1, y2):
    Label(frame, text = "", borderwidth=3, relief="groove", width = 33, height = 7, bg = "gray45").place(x = x1, y = y1)
    Label(frame, text = "Acessar Arquivos", font = "arial 8 bold", fg = "white", bg = "black", borderwidth=4, relief="sunken").place(x = x2, y = y2)
## * ENTRADA PARA PARÂMETROS BATELADA ALIMENTADA * ##
def entry_bat_alim_geral(frame, x1, x2, x3, x4, x5, y1, y2, y3, y4, y5):
    global entr_Q, entr_Cs_alim, entr_V0, entr_tf_bat
    entr_Q = tk.Entry(frame, width = 7, font = "batang 8 bold", fg = "black", borderwidth = 2, relief = "sunken", bg = "white")
    entr_Q.place(x = x1, y = y2)
    entr_Cs_alim = tk.Entry(frame, width = 7, font = "batang 8 bold", borderwidth = 2, relief = "sunken", bg = "white", fg = "black")
    entr_Cs_alim.place(x = x2, y = y2)
    entr_V0 = tk.Entry(frame, width = 7, font = "batang 8 bold", borderwidth = 2, relief = "sunken", bg = "white", fg = "black")
    entr_V0.place(x = x3, y = y3)
    entr_tf_bat = tk.Entry(frame, width = 7, font = "batang 8 bold", borderwidth = 2, relief = "sunken", bg = "white", fg = "black")
    entr_tf_bat.place(x = x4, y = y4)
    entr_lin_exp = tk.Entry(frame, width = 7, font = "batang 8 bold", borderwidth = 2, relief = "sunken", bg = "white", fg = "black")
    entr_lin_exp.place(x = x5, y = y5)
    entr_lin_exp.configure(state = "disabled")
def entry_bat_alim_lin_exp(frame, x, y):
    global entr_lin_exp
    entr_lin_exp = tk.Entry(frame, width = 7, font = "batang 8 bold", borderwidth = 2, relief = "sunken", bg = "white", fg = "black")
    entr_lin_exp.place(x = x, y = y)
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
## * PADRÃO DE ESTILO VISUAL DOS GRÁFICOS * ##:
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
    
            #### **** CODIFICAÇÃO PARA A PARTE REFERENTE À BATELADA ALIMENTADA - simulação e modelagem **** ####
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

## * ENTRADAS E SAÍDAS DA SIMULAÇÃO * ##:
# Caixas de separação:
Label(frame1, text="", width = 52, height = 33, borderwidth = 3,  relief = "sunken", bg = "grey85").place(x = 914, y = 2)
Label(frame1, text="", width = 53, height = 33, borderwidth = 3,  relief = "sunken", bg = "grey85").place(x = 10, y = 2)
def caixa_equa_simul():
    Label(frame1, text="", width = 47, height = 19, borderwidth = 5,  relief = "sunken", bg = "grey65").place(x = 920, y = 200)
ttk.Label(frame1, text = "SELECIONE A CINÉTICA DE REAÇÃO:", font = "times 12 bold").place(x = 16, y = 10)

def botao_envio_bat_alim(frame, comando, x, y):
    global enviar
    enviar = Button(frame, text = "Enviar", command = comando)
    enviar.place(x = x, y = y)
# Botão para exibição dos modelos disponíveis:
frames_simul = Button(frame1, text="Pronto", bg = "gray70", fg = "grey40", font="batang 12")
frames_simul.place(x = 315, y = 29)
# Funções para capturar os valores dos entry:
def pegar_val_alim_const():
    global Q_const, Cs_alim_const, V0_const, tf_bat_const
    Q_const = float(entr_Q.get())
    Cs_alim_const = float(entr_Cs_alim.get())
    V0_const = float(entr_V0.get())
    tf_bat_const = float(entr_tf_bat.get())
    enviar.configure(bg = "green", fg = "white")
    frames_simul.configure(bg = "black", fg = "white", command = print_me_1)
    botao_carregar.configure(command = explorer)
    print(Q_const, Cs_alim_const, V0_const, tf_bat_const)
    return(Q_const, Cs_alim_const, V0_const, tf_bat_const)
def pegar_val_alim_lin():
    global Q_lin, Cs_alim_lin, V0_lin, tf_bat_lin, a
    Q_lin = float(entr_Q.get())
    Cs_alim_lin = float(entr_Cs_alim.get())
    V0_lin = float(entr_V0.get())
    tf_bat_lin = float(entr_tf_bat.get())
    a = float(entr_lin_exp.get())
    enviar.configure(bg = "green", fg = "white")
    frames_simul.configure(bg = "black", fg = "white", command = print_me_1)
    botao_carregar.configure(command = explorer)
    print(Q_lin, Cs_alim_lin, V0_lin, tf_bat_lin, a)
    return(Q_lin, Cs_alim_lin, V0_lin,tf_bat_lin, a)
def pegar_val_alim_exp():
    global Q_exp, Cs_alim_exp, V0_exp, tf_bat_exp, beta_exp
    Q_exp = float(entr_Q.get())
    Cs_alim_exp = float(entr_Cs_alim.get())
    V0_exp = float(entr_V0.get())
    tf_bat_exp = float(entr_tf_bat.get())
    beta_exp = float(entr_lin_exp.get())
    enviar.configure(bg = "green", fg = "white")
    frames_simul.configure(bg = "black", fg = "white", command = print_me_1)
    botao_carregar.configure(command = explorer)
    print(Q_exp, Cs_alim_exp, V0_exp, tf_bat_exp, beta_exp)
    return(Q_exp, Cs_alim_exp, V0_exp, tf_bat_exp, beta_exp)
    
## * ENTRADAS E SAÍDAS DA SIMULAÇÃO - CONTINUAÇÃO * ##:
    
# Combobox para seleção da cinética de reação:
v_1 = ("AUSÊNCIA DE INIBIÇÃO", "INIBIÇÃO PELO SUBSTRATO", "INIBIÇÃO PELO PRODUTO", "INIBIÇÃO PELA BIOMASSA")
combo_1 = Combobox(frame1, values = v_1, width = 39, font = "arial 10")
combo_1.set("-----------------------ESCOLHA-----------------------")
combo_1.place(x = 15, y = 32)
caixa_equa_simul()
aces_arq(frame = frame1, x1 = 920, x2 = 926, y1 = 86, y2 = 92)
## Caixa para plotagem dos gráficos gerados:
notebook_graf_simul()

# Caixa para acesso às equações:
Label(frame1, text = "", borderwidth=4, relief="sunken", width = 50, height = 4, bg = "grey90").place(x = 921, y = 8)
Label(frame1, text = "Visualizar Equações", font = "times 8 bold", fg = "white", bg = "black", borderwidth=4, relief="sunken").place(x = 1150, y = 13)
## Função para impressão das equações e suas variáveis:
def equac_sai_contois():
    caixa_equa_simul()
    image(imagem = "Equacao_Contois.png", num_frame = frame1, x = 988, y = 282)
    Label(frame1, text = "CONTOIS", font = 'Courier 12 bold italic', fg = "black", bg = "white", relief = "raised").place(x = 930, y = 210)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 374)
    tex_ksx = Label(frame1, text = u"KSX = constante de saturação (mass.mass\u207b\u00b9)", font = 'arial 9 italic', fg = "black",  bg = "grey65").place(x = 930, y = 404)
def equac_sai_monod():
    caixa_equa_simul()
    image(imagem = "Equacao_Monod.png", num_frame = frame1, x = 1000, y = 282)
    Label(frame1, text = "MONOD", font = 'Courier 12 bold italic', fg = "black", bg = "white", relief = "raised").place(x = 930, y = 210)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 374)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 404)
def equac_sai_moser():
    caixa_equa_simul()
    image(imagem = "Equacao_Moser.png", num_frame = frame1, x = 1000, y = 282)
    Label(frame1, text = "MOSER", font = 'Courier 12 bold italic', fg = "black", bg = "white", relief = "raised").place(x = 930, y = 210)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 374)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 404)
    tex_u = Label(frame1, text = "u = parâmetro expoente (adim)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 434)
def equac_sai_mi_const():
    caixa_equa_simul()
    image(imagem = "Equacao_mi_const.png", num_frame = frame1, x = 1040, y = 278)
    Label(frame1, text = u"\u03bc constante", font = 'Courier 12 bold italic', fg = "black", bg = "white", relief = "raised").place(x = 930, y = 210)
    tex_mi = Label(frame1, text = u"\u03bc = taxa específica de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 314)
    tex_mi_explic = Label(frame1, text = "A velocidade de crescimento microbiano mantém-se\nconstante durante todo o tempo t de cultivo", font = 'arial 9 italic', fg = "black", bg = "grey65", relief = "sunken").place(x = 936, y = 385)
def equac_sai_andrews(): 
    caixa_equa_simul()
    image(imagem = "Equacao_Andrews.png", num_frame = frame1, x = 985, y = 282)
    Label(frame1, text = "ANDREWS", font = 'Courier 12 bold italic', fg = "black", bg = "white", relief = "raised").place(x = 930, y = 210)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 374)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 404)
    tex_kis = Label(frame1, text = u"KIS = constante inibição por substrato (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 434)
def equac_sai_wu(): 
    caixa_equa_simul()
    image(imagem = "Equacao_Wu.png", num_frame = frame1, x = 970, y = 282)
    Label(frame1, text = "WU et al", font = 'Courier 12 bold italic', fg = "black", bg = "white", relief = "raised").place(x = 930, y = 210)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 374)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 404)
    tex_ke = Label(frame1, text = u"KE = constante inibição por substrato (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 434)
    tex_v = Label(frame1, text = "v = parâmetro expoente (adim)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 464)
def equac_sai_aiba():
    caixa_equa_simul()
    image(imagem = "Equacao_Aiba.png", num_frame = frame1, x = 970, y = 282) 
    Label(frame1, text = "AIBA et al", font = 'Courier 12 bold italic', fg = "black", bg = "white", relief = "raised").place(x = 930, y = 210)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 374)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 404)
    tex_kp = Label(frame1, text = u"Kp = parâmetro expoente de inibição (vol.mass\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 434)  
def equac_sai_hh():
    caixa_equa_simul()      
    image(imagem = "Equacao_Hoppe_Hansford.png", num_frame = frame1, x = 970, y = 282) 
    Label(frame1, text = "HOPPE & HANSFORD", font = 'Courier 12 bold italic', fg = "black", bg = "white", relief = "raised").place(x = 930, y = 210)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 374)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 404)
    tex_kp = Label(frame1, text = u"Kp = constante inibição por produto (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 434)               
def equac_sai_levenspiel():
    caixa_equa_simul()
    image(imagem = "Equacao_Levenspiel.png", num_frame = frame1, x = 970, y = 282) 
    Label(frame1, text = "LEVENSPIEL", font = 'Courier 12 bold italic', fg = "black", bg = "white", relief = "raised").place(x = 930, y = 210)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 374)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 404)
    tex_cpestr = Label(frame1, text = u"Cp* = concentração produto crítica (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 434)
    tex_n_lev = Label(frame1, text = "n = constante de Levenspiel (adim)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 464)   
def equac_sai_lee():  
    caixa_equa_simul()
    image(imagem = "Equacao_Lee.png", num_frame = frame1, x = 970, y = 282) 
    Label(frame1, text = "LEE et al", font = 'Courier 12 bold italic', fg = "black", bg = "white", relief = "raised").place(x = 930, y = 210)
    tex_mimax = Label(frame1, text = u"\u03bcmáx = taxa específica máxima de crescimento (t\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 374)
    tex_ks = Label(frame1, text = u"Ks = constante de saturação (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 404)
    tex_cxestr = Label(frame1, text = u"Cx* = concentração celular crítica (mass.vol\u207b\u00b9)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 434)
    tex_m = Label(frame1, text = "m = constante de Lee et al (adim)", font = 'arial 9 italic', fg = "black", bg = "grey65").place(x = 930, y = 464)   

### * Criação botões para acesso às equações ### *:
Button(frame1, text = "Contois", font = "Times 7 bold italic", fg = "black", bg = "white", command = equac_sai_contois).place(x = 930, y = 35)
Button(frame1, text = "Monod", font = "Times 7 bold italic", fg = "black", bg = "white", command = equac_sai_monod).place(x = 970, y = 35)
Button(frame1, text = "Moser", font = "Times 7 bold italic", fg = "black", bg = "white", command = equac_sai_moser).place(x = 1006, y = 35)
Button(frame1, text = "Andrews", font = "Times 7 bold italic", fg = "black", bg = "grey90", command = equac_sai_andrews).place(x = 1040, y = 35)
Button(frame1, text = "Wu et al", font = "Times 7 bold italic", fg = "black", bg = "grey90", command = equac_sai_wu).place(x = 1082, y = 35)
Button(frame1, text = "Aiba et al", font = "Times 7 bold italic", fg = "black", bg = "grey80", command = equac_sai_aiba).place(x = 950, y = 56)
Button(frame1, text = "Hoppe & Hansford", font = "Times 7 bold italic", fg = "black", bg = "grey80", command = equac_sai_hh).place(x = 997, y = 56)
Button(frame1, text = "Levenspiel", font = "Times 7 bold italic", fg = "black", bg = "grey80", command = equac_sai_levenspiel).place(x = 1081, y = 56)
Button(frame1, text = "Lee et al", font = "Times 7 bold italic", fg = "black", bg = "grey70", command = equac_sai_lee).place(x = 1131, y = 56)  
Button(frame1, text = u"\u03bc constante", font = "Times 7 bold italic", fg = "white", bg = "grey50", command = equac_sai_mi_const).place(x = 1172, y = 56)    

# Caixas separadoras:
def caix_simul(frame, larg, alt, x, y):
    Label(frame, width = larg, height = alt, borderwidth = 5,relief = "sunken").place(x = x, y = y)
# Escritos:
def labels(frame, texto, fonte, borda, x, y):
    Label(frame, text = texto, font = fonte, relief = borda).place(x = x, y = y)
# Saída arquivos simulação:
sai_resul_simul = Label(frame1, bg = "gray45")
sai_resul_simul .place(x = 962, y = 143)
    
# Função para entradas numéricas:
# - Parâmetro: mi_máximo - #:
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
def entr_simul_mi_const(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_mimax_mi_const, slider_mimax_mi_const
    spin_mimax_mi_const = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_mimax_mi_const.place(x = 15, y = 37)
    slider_mimax_mi_const = ttk.Scale(frame, variable=input, from_= 0.01, to = 1.5, orient='horizontal',length = 60)
    slider_mimax_mi_const.place(x = 59, y = 32)    
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

# - Parâmetro: Ks - #:
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

# - Parâmetro: Kd - #:   
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
def entr_simul_kd_mi_const(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_kd_mi_const, slider_kd_mi_const
    spin_kd_mi_const = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_kd_mi_const.place(x = 15, y = 157)
    slider_kd_mi_const = ttk.Scale(frame, variable=input, from_= 0.0, to = 1, orient='horizontal',length = 55)
    slider_kd_mi_const.place(x = 58, y = 154) 
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

# - Parâmetro: Yxs - #:    
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
def entr_simul_yxs_mi_const(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_yxs_mi_const, slider_yxs_mi_const
    spin_yxs_mi_const = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_yxs_mi_const.place(x = 145, y = 157)
    slider_yxs_mi_const = ttk.Scale(frame, variable=input, from_= 0.0, to = 3, orient='horizontal',length = 80)
    slider_yxs_mi_const.place(x = 188, y = 154) 
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

# - Parâmetro: alfa - #:    
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
def entr_simul_alfa_mi_const(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_alfa_mi_const, slider_alfa_mi_const
    spin_alfa_mi_const = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_alfa_mi_const.place(x = 15, y = 213)
    slider_alfa_mi_const = ttk.Scale(frame, variable=input, from_= 0.01, to = 10, orient='horizontal',length = 90)
    slider_alfa_mi_const.place(x = 58, y = 209)
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

# - Parâmetro: beta - #:    
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
def entr_simul_beta_mi_const(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_beta_mi_const, slider_beta_mi_const
    spin_beta_mi_const = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_beta_mi_const.place(x = 160, y = 213)
    slider_beta_mi_const = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 90)
    slider_beta_mi_const.place(x = 203, y = 209)
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

## - - Parâmetros únicos -- ##:
    
### * Adimensional de Moser (u) * ###:       
def entr_simul_u(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.5)
    global spin_u, slider_u
    spin_u = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_u.place(x = 160, y = 37)
    slider_u = ttk.Scale(frame, variable=input, from_= 0.5, to = 3, orient='horizontal',length = 80)
    slider_u.place(x = 203, y = 32)

### * Constante de inibição de Andrews (efeitos de substrato) * ###:    
def entr_simul_kis(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_kis, slider_kis
    spin_kis = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_kis.place(x = 140, y = 37)
    slider_kis = ttk.Scale(frame, variable=input, from_= 0.01, to = 100, orient='horizontal',length = 110)
    slider_kis.place(x = 183, y = 32)

### * Constante de inibição de Wu et al (efeitos de produtos) * ###:     
def entr_simul_ke(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_ke, slider_ke
    spin_ke = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_ke.place(x = 140, y = 37)
    slider_ke = ttk.Scale(frame, variable=input, from_= 0.01, to = 100, orient='horizontal',length = 110)
    slider_ke.place(x = 183, y = 32)

## * Adimensional de Wu et al (efeitos de produto) * ##:    
def entr_simul_v(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_v, slider_v
    spin_v = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_v.place(x = 165, y = 94)
    slider_v = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 85)
    slider_v.place(x = 208, y = 91)
  
## * Constantes de inibição de Aiba et al e Hoppe & Hansford (efeitos de produto) * ##:
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

## * Concentração de saturação de Levenspiel (efeitos de produto) * ##:   
def entr_simul_cp_estr(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_cp_estr, slider_cp_estr
    spin_cp_estr = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_cp_estr.place(x = 140, y = 37)
    slider_cp_estr = ttk.Scale(frame, variable=input, from_= 0.01, to = 100, orient='horizontal',length = 110)
    slider_cp_estr.place(x = 183, y = 32)

## * Concentração de saturação celular de Lee et al (efeitos de biomassa) * ##:       
def entr_simul_cx_estr(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.01)
    global spin_cx_estr, slider_cx_estr
    spin_cx_estr = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_cx_estr.place(x = 140, y = 37)
    slider_cx_estr = ttk.Scale(frame, variable=input, from_= 0.01, to = 100, orient='horizontal',length = 110)
    slider_cx_estr.place(x = 183, y = 32)

## * Adimensional de Levenspiel (efeitos de produto) * ##:    
def entr_simul_n(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_n, slider_n
    spin_n = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_n.place(x = 165, y = 94)
    slider_n = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 85)
    slider_n.place(x = 208, y = 91)

## * Adimensional de Lee et al (efeitos de biomassa * ##:      
def entr_simul_m(frame):
    ## Criação dos botões deslizáveis:
    input = tk.DoubleVar(value=0.0)
    global spin_m, slider_m
    spin_m = tk.Spinbox(frame, textvariable=input, wrap=True, width=5)
    spin_m.place(x = 165, y = 94)
    slider_m = ttk.Scale(frame, variable=input, from_= 0.0, to = 10, orient='horizontal',length = 85)
    slider_m.place(x = 208, y = 91)

# Função para definição dos labels - títulos de definição:
def labels_saida(frame):
    labels(frame, texto = "Parâmetros Crescimento", fonte = "batang 8 bold", borda = "flat", x = 115, y = 0)
    labels(frame, texto = u"\u03bcmáx (h\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 14)
    labels(frame, texto = "Parâmetros Balanço Massa", fonte = "batang 8 bold", borda = "flat", x = 100, y = 117)
    labels(frame, texto = u"Kd (h\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 132)
    labels(frame, texto = u"Yxs (gx.gs\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 228, y = 132)
    labels(frame, texto = u"\u03B1(gp.gx\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 189)
    labels(frame, texto = u"\u03B2[gp.(gx.h)\u207b\u00b9]", fonte = "times 9 bold", borda = "sunken", x = 226, y = 189)
    labels(frame, texto = "Variáveis Operacionais", fonte = "batang 8 bold", borda = "flat", x = 123, y = 234)
    labels(frame, texto = "Cx0:", fonte = "times 10 bold", borda = "flat", x = 18, y = 255)
    labels(frame, texto = "Cs0:", fonte = "times 10 bold", borda = "flat", x = 108, y = 255)
    labels(frame, texto = "Cp0:", fonte = "times 10 bold", borda = "flat", x = 198, y = 255)
    labels(frame, texto = "t0(h):", fonte = "times 10 bold", borda = "flat", x = 13, y = 285)
    labels(frame, texto = "tf(h):", fonte = "times 10 bold", borda = "flat", x = 107, y = 285)
def labels_saida_mi_const(frame):
    labels(frame, texto = "Parâmetros Crescimento", fonte = "batang 8 bold", borda = "flat", x = 115, y = 0)
    labels(frame, texto = "Variáveis Operacionais", fonte = "batang 8 bold", borda = "flat", x = 123, y = 234)
    labels(frame, texto = "Cx0:", fonte = "times 10 bold", borda = "flat", x = 18, y = 255)
    labels(frame, texto = "t0(h):", fonte = "times 10 bold", borda = "flat", x = 13, y = 285)
    labels(frame, texto = "tf(h):", fonte = "times 10 bold", borda = "flat", x = 107, y = 285)

# Função separação física simulação:
def separ_simul(frame):
    caix_simul(frame, larg = 40, alt = 7, x = 5, y = 5)
    caix_simul(frame, larg = 40, alt = 7, x = 5, y = 123)
    caix_simul(frame, larg = 40, alt = 4, x = 5, y = 240)
def separ_simul_infl_mi_const(frame):
    caix_simul(frame, larg = 40, alt = 14, x = 5, y = 5)
    caix_simul(frame, larg = 40, alt = 4, x = 5, y = 240)
    
# AVIS0:
labels(frame = frame1, texto = "Por favor, entre com valores para Cx0, Cs0 e Cp0 em unidades g/L", fonte = "times 9 bold", borda = "flat", x = 15, y = 480)

## Capturar o modo de alimentação selecionado e exibir o layout para entrada correspondente:
### Caixa separadora do layout:
Label(frame1, text = "", width = 60, height = 6, relief = "sunken", borderwidth = 3).place(x = 470, y = 4)
### Valor do combobox:
def print_alim_simul():
    global def_alim
    def_alim = combo_0.get()
    print(def_alim)
    status_03.configure(text = def_alim, font = "batang 12", bg = "lightgreen", relief = "raised")  
## * ENTRADA DOS VALORES REFERENTES APENAS À BATELADA ALIMENTADA * ##
    # Criação das indicações escritas:
    ## Eixos:
    eixo_Q = Label(frame1, text = u"Q(L.h\u207b\u00b9)", width = 7, font = "times 10 bold", fg = "grey45")
    eixo_Q.place(x = 536, y = 40) 
    eixo_Cs_alim = Label(frame1, text = u"Cs alim(gs.L\u207b\u00b9)", font = "times 10 bold", fg = "grey45")
    eixo_Cs_alim.place(x = 641, y = 40) 
    eixo_V0 = Label(frame1, text = "V0(L)", font = "times 10 bold", fg = "grey45")
    eixo_V0.place(x = 549, y = 70)  
    eixo_tf_bat = Label(frame1, text = "tf bat(h)", font = "times 10 bold", fg = "grey45")
    eixo_tf_bat.place(x = 780, y = 40) 
    eixo_lin_exp = Label(frame1, text = "a / beta", font = "times 10 bold", width = 5, fg = "gray45")
    eixo_lin_exp.place(x = 670, y = 70)  
    # Indicação para a entrada dos parâmetros referentes apenas à batelada alimentada pelo tk entry:
    Label(frame1, text = "Insira as constantes relacionadas:", font = "courier 9 bold", bg = "gray85", relief = "raised").place(x = 480, y = 10)
    ## Função para avaliar o tipo de alimentação:
    if (def_alim == "Taxa de Vazão Constante"):
        entry_bat_alim_geral(frame = frame1, x1 = 590, x2 = 730, x3 = 590, x4 = 828, x5 = 730, y1 = 40, y2 = 40, y3 = 70, y4 = 40, y5 = 70)
        botao_envio_bat_alim(frame = frame1, comando = pegar_val_alim_const, x = 850, y = 71)
        eixo_Q.configure(fg = "black")
        eixo_Cs_alim.configure(fg = "black")
        eixo_tf_bat.configure(fg = "black")
        eixo_V0.configure(fg = "black")
    if (def_alim == "Taxa de Vazão Linear"):
        entry_bat_alim_geral(frame = frame1, x1 = 590, x2 = 730, x3 = 590, x4 = 828, x5 = 730, y1 = 40, y2 = 40, y3 = 70, y4 = 40, y5 = 70)
        entry_bat_alim_lin_exp(frame = frame1, x = 730, y = 70)
        botao_envio_bat_alim(frame = frame1, comando = pegar_val_alim_lin, x = 850, y = 71)
        eixo_Q.configure(text = u"Q0(L.h\u207b\u00b9)", fg = "black")
        eixo_Cs_alim.configure(fg = "black")
        eixo_tf_bat.configure(fg = "black")
        eixo_V0.configure(fg = "black")
        eixo_lin_exp.configure(text = "a", fg = "black")
    if (def_alim == "Taxa de Vazão Exponencial"):
        entry_bat_alim_geral(frame = frame1, x1 = 590, x2 = 730, x3 = 590, x4 = 828, x5 = 730, y1 = 40, y2 = 40, y3 = 70, y4 = 40, y5 = 70)
        entry_bat_alim_lin_exp(frame = frame1, x = 730, y = 70)
        botao_envio_bat_alim(frame = frame1, comando = pegar_val_alim_exp, x = 850, y = 71)
        eixo_Q.configure(text = u"Q0(L.h\u207b\u00b9)", fg = "black")
        eixo_Cs_alim.configure(fg = "black")
        eixo_tf_bat.configure(fg = "black")
        eixo_V0.configure(fg = "black")
        eixo_lin_exp.configure(text = "beta", fg = "black")
    but_alim_model.configure(bg = "gray94", fg = "black")
    but_alim_simul.configure(bg = "black", fg = "white")
        
but_alim_simul = Button(janela, text = "Enviar para simular", font = "times 8 italic bold", relief = "raised", borderwidth = 3, command = print_alim_simul)
but_alim_simul.place(x = 668, y = 67) 

## * ENTRADAS E SAÍDAS DA MODELAGEM * ##:
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
aces_arq(frame2, x1 = 1030, x2 = 1036, y1 = 7, y2 = 13)
## Caixa para plotagem dos gráficos gerados:
notebook_graf_model()
# Botão para acesso ao buscador de arquivos da máquina:
botao_carregar = Button(frame2, text = "Carregar arquivo",  font="Batang 12", fg="grey40", bg="gray70", borderwidth=2, relief="raised")
botao_carregar.place(x = 568, y = 15) 
## Capturar o modo de alimentação selecionado e exibir o layout para entrada correspondente:
### Valor do combobox:
def print_alim_modelag():
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
    Label(frame2, text = "Insira as constantes relacionadas:", font = "courier 9 bold", bg = "gray85", relief = "raised").place(x = 17, y = 60)
    ## Função para avaliar o tipo de alimentação:
    if (def_alim == "Taxa de Vazão Constante"):
        entry_bat_alim_geral(frame = frame2, x1 = 70, x2 = 210, x3 = 70, x4 = 308, x5 = 210, y1 = 90, y2 = 90, y3 = 120, y4 = 90, y5 = 120)
        botao_envio_bat_alim(frame = frame2, comando = pegar_val_alim_const, x = 313, y = 114)
        eixo_Q.configure(fg = "black")
        eixo_Cs_alim.configure(fg = "black")
        eixo_tf_bat.configure(fg = "black")
        eixo_V0.configure(fg = "black")
        botao_carregar.configure(fg = "white", bg = "gray17", command = '')
        arq_sel.configure(text = '')
    if (def_alim == "Taxa de Vazão Linear"):
        entry_bat_alim_geral(frame = frame2, x1 = 70, x2 = 210, x3 = 70, x4 = 308, x5 = 210, y1 = 90, y2 = 90, y3 = 120, y4 = 90, y5 = 120)
        entry_bat_alim_lin_exp(frame = frame2, x = 210, y = 120)
        botao_envio_bat_alim(frame = frame2, comando = pegar_val_alim_lin, x = 313, y = 114)
        eixo_Q.configure(text = u"Q0(L.h\u207b\u00b9)", fg = "black")
        eixo_Cs_alim.configure(fg = "black")
        eixo_tf_bat.configure(fg = "black")
        eixo_V0.configure(fg = "black")
        eixo_lin_exp.configure(text = "a", fg = "black")
        botao_carregar.configure(fg = "white", bg = "gray17", command = '')
        arq_sel.configure(text = '')
    if (def_alim == "Taxa de Vazão Exponencial"):
        entry_bat_alim_geral(frame = frame2, x1 = 70, x2 = 210, x3 = 70, x4 = 308, x5 = 210, y1 = 90, y2 = 90, y3 = 120, y4 = 90, y5 = 120)
        entry_bat_alim_lin_exp(frame = frame2, x = 210, y = 120)
        botao_envio_bat_alim(frame = frame2, comando = pegar_val_alim_exp, x = 313, y = 114)
        eixo_Q.configure(text = u"Q0(L.h\u207b\u00b9)", fg = "black")
        eixo_Cs_alim.configure(fg = "black")
        eixo_tf_bat.configure(fg = "black")
        eixo_V0.configure(fg = "black")
        eixo_lin_exp.configure(text = "beta", fg = "black")
        botao_carregar.configure(fg = "white", bg = "gray17", command = '')
        arq_sel.configure(text = '')
    but_alim_simul.configure(bg = "gray94", fg = "black")
    but_alim_model.configure(bg = "black", fg = "white")
        
#but_alim_simul = Button(janela, text = "Enviar para simular", font = "times 8 italic bold", command = print_alim)
#but_alim_simul.place(x = 665, y = 67)  
but_alim_model = Button(janela, text = "Enviar para modelar", font = "times 8 italic bold", relief = "raise", borderwidth = 3, command = print_alim_modelag)
but_alim_model.place(x = 776, y = 67)


    
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

                                    ##### ***** SIMULAÇÃO ***** #####

#### **** INÍCIO DO CÓDIGO-FONTE FUNCIONAL **** ####
def simulacao(cont):
    
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
    
    # Vetor condição inicial:
    # - BATELADA:
    inic_cond_bat_simul = [Cx0, Cs0, Cp0]
    print(inic_cond_bat_simul)
    # Vetor tempo:
    t_bat_simul = np.arange(t0, tf_bat, 0.5)
    print(t_bat_simul)
    
    # - Batelada Monod:  
    if (cont == 0):
        def edos_int_bat_Monod(C,t):
            Cx,Cs,Cp = C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
        
            mi = mimax_sim*(Cs/(Ks_sim + Cs))
            dCxdt = (mi - Kd_sim) * Cx
            dCsdt = (-1/Yxs_sim)*mi*Cx
            dCpdt = alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim_bat = odeint(edos_int_bat_Monod,inic_cond_bat_simul,t_bat_simul)
        print(C_sim_bat)
        
    # - Batelada Contois:
    if (cont == 1):
        def edos_int_bat_Contois(C,t):
            Cx,Cs,Cp = C
            mimax_sim = mimax
            KSX_sim = KSX
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
        
            mi = mimax_sim*(Cs/((KSX_sim*Cx)+Cs))
            dCxdt = (mi - Kd_sim) * Cx
            dCsdt = (-1/Yxs_sim)*mi*Cx
            dCpdt = alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim_bat = odeint(edos_int_bat_Contois, inic_cond_bat_simul, t_bat_simul)
        print(C_sim_bat)
    
    # -  Batelada Andrews:
    if (cont == 2):
        def edos_int_bat_Andrews(C,t):
            Cx,Cs,Cp = C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
            KIS_sim = KIS
    
            mi = mimax_sim*(Cs/(Ks_sim+Cs+((Cs**2)/KIS_sim)))
            dCxdt = (mi - Kd_sim) * Cx
            dCsdt = (-1/Yxs_sim)*mi*Cx
            dCpdt = alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim_bat = odeint(edos_int_bat_Andrews, inic_cond_bat_simul, t_bat_simul)
        print(C_sim_bat)
    
    # - Batelada Aiba et al:    
    if (cont == 3):
        def edos_int_bat_Aiba_et_al(C,t):
            Cx,Cs,Cp = C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
            Kp_aiba_sim = Kp_aiba
    
            mult_exp = -Cp*Kp_aiba_sim
            mi = mimax_sim*((Cs/(Ks_sim+Cs))*math.exp(mult_exp))
            dCxdt = (mi - Kd_sim) * Cx
            dCsdt = (-1/Yxs_sim)*mi*Cx
            dCpdt = alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim_bat = odeint(edos_int_bat_Aiba_et_al, inic_cond_bat_simul, t_bat_simul)
        print(C_sim_bat)
    
    # - Batelada Moser:
    if (cont == 4):
        def edos_int_bat_Moser(C,t):
            Cx,Cs,Cp = C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
            u_sim = u
        
            mi = mimax_sim*(((Cs)**u_sim)/(Ks_sim+((Cs)**u_sim)))
            dCxdt = (mi-Kd_sim)*Cx
            dCsdt = (-1/Yxs_sim)*mi*Cx
            dCpdt = alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim_bat = odeint(edos_int_bat_Moser, inic_cond_bat_simul, t_bat_simul)
        print(C_sim_bat)
    
    # - Batelada Hoppe & Hansford:    
    if (cont == 5):
        def edos_int_bat_Hoppe_Hansford(C,t):
            Cx,Cs,Cp = C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
            Kp_hope_sim = Kp_hh

            mi = mimax_sim*(Cs/(Ks_sim+Cs))*(Kp_hope_sim/(Kp_hope_sim+Cp))
            dCxdt = (mi - Kd_sim) * Cx
            dCsdt = (-1/Yxs_sim)*mi*Cx
            dCpdt = alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim_bat = odeint(edos_int_bat_Hoppe_Hansford, inic_cond_bat_simul, t_bat_simul)
        print(C_sim_bat)
    
    # - Batelada Wu et al:
    if (cont == 6):
        def edos_int_bat_Wu_et_al(C,t):
            Cx,Cs,Cp = C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
            Ke_sim = Ke
            v_sim = v

            mi = mimax_sim * (Cs/(Ks_sim + Cs + Cs*((Cs/Ke_sim)**v_sim)))
            dCxdt = (mi - Kd_sim) * Cx
            dCsdt = (-1/Yxs_sim)*mi*Cx
            dCpdt = alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim_bat = odeint(edos_int_bat_Wu_et_al, inic_cond_bat_simul, t_bat_simul)
        print(C_sim_bat)
    
    # - Batelada Levenspiel:
    if (cont == 7):
        def edos_int_bat_Levenspiel(C,t):
            Cx,Cs,Cp = C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
            Cp_estr_sim = Cp_estr
            n_sim = n
        
            mi = mimax_sim*((Cs/(Ks_sim+Cs))*((1-(Cp/Cp_estr_sim))**n_sim))
            dCxdt = (mi - Kd_sim) * Cx
            dCsdt = (-1/Yxs_sim)*mi*Cx
            dCpdt = alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim_bat = odeint(edos_int_bat_Levenspiel, inic_cond_bat_simul, t_bat_simul)
        print(C_sim_bat)
    
    # - Batelada Lee et al:
    if (cont == 8):
        def edos_int_bat_Lee_et_al(C,t):
            Cx,Cs,Cp = C
            mimax_sim = mimax
            Ks_sim = Ks
            Kd_sim = Kd
            Yxs_sim = Yxs
            alfa_sim = alfa
            beta_sim = beta
            Cx_estr_sim = Cx_estr
            m_sim = m
        
            mi = mimax_sim*((Cs/(Ks_sim+Cs))*((1-(Cx/Cx_estr_sim))**m_sim))
            dCxdt = (mi - Kd_sim) * Cx
            dCsdt = (-1/Yxs_sim)*mi*Cx
            dCpdt = alfa_sim*mi*Cx+beta_sim*Cx
            return(dCxdt,dCsdt,dCpdt)
        # Integrando numericamente:
        C_sim_bat = odeint(edos_int_bat_Lee_et_al, inic_cond_bat_simul, t_bat_simul)
        print(C_sim_bat)
    
    Cx_bat = C_sim_bat[:,0]
    Cs_bat = C_sim_bat[:,1]
    Cp_bat = C_sim_bat[:,2]
        
    # Vetor condição inicial:
    # - BATELADA ALIMENTADA:
    Cx0_simul_bat_alim = Cx_bat[len(Cx_bat)-1]   
    Cs0_simul_bat_alim = Cs_bat[len(Cs_bat)-1]
    Cp0_simul_bat_alim = Cp_bat[len(Cp_bat)-1] 
    inic_cond_alim_simul = [Cx0_simul_bat_alim, Cs0_simul_bat_alim, Cp0_simul_bat_alim]
    print(inic_cond_alim_simul)
    # Vetor tempo:
    t_bat_alim_simul = np.arange(tf_bat, tf, 0.5)
    print(t_bat_alim_simul)
        
    # - Batelada alimentada Monod:
    ## - Monod (vazão constante): 
    if (cont == 0 and def_alim == "Taxa de Vazão Constante"):
        def func_simul_alim_Monod_um():
            def func_simul_alim_Monod_const(C, t_bat_alim_simul):
                mimax_const = mimax
                Ks_const = Ks
                Kd_const = Kd
                Yxs_const = Yxs
                alfa_const = alfa
                beta_const = beta
                    
                Q_simul_const = Q
                V0_simul_const = V0
                Cs0_corrent_alim_simul_const = Cs0_corrent_alim
              
                mi = mimax_const*(C[1]/(Ks_const + C[1]))
                D = Q_simul_const/(V0_simul_const + Q_simul_const*t_bat_alim_simul)
                dCxdt = (mi - Kd_const - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_const - C[1]) - ((mi*C[0])/Yxs_const)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_const + alfa_const*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Monod_const)
        func_simul_bat_alim = func_simul_alim_Monod_um()

    # - Monod (vazão linear):   
    if (cont == 0 and def_alim == "Taxa de Vazão Linear"):
        def func_simul_alim_Monod_dois():
            def func_simul_alim_Monod_lin(C, t_bat_alim_simul):
                mimax_lin = mimax
                Ks_lin = Ks
                Kd_lin = Kd
                Yxs_lin = Yxs
                alfa_lin = alfa
                beta_lin = beta
                    
                Q0_simul_lin = Q0
                V0_simul_lin = V0
                Cs0_corrent_alim_simul_lin = Cs0_corrent_alim
                a_simul = a
                
                print(Q0_simul_lin, V0_simul_lin, Cs0_corrent_alim_simul_lin, a_simul)
        
                mi = mimax_lin*(C[1]/(Ks_lin + C[1]))
                D = (Q0_simul_lin*(1+a_simul*t_bat_alim_simul))/((Q0_simul_lin*(t_bat_alim_simul+(a_simul*t_bat_alim_simul**2)))+V0_simul_lin)
                dCxdt = (mi - Kd_lin - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_lin - C[1]) - ((mi*C[0])/Yxs_lin)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_lin + alfa_lin*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Monod_lin)
        func_simul_bat_alim = func_simul_alim_Monod_dois()
        
    # - Monod (vazão exponencial):   
    if (cont == 0  and def_alim == "Taxa de Vazão Exponencial"):
        def func_simul_alim_Monod_tres():
            def func_simul_alim_Monod_exp(C, t_bat_alim_simul):
                mimax_exp = mimax
                Ks_exp = Ks
                Kd_exp = Kd
                Yxs_exp = Yxs
                alfa_exp = alfa
                beta_exp_modelo = beta
                    
                Q0_simul_exp = Q0
                V0_simul_exp = V0
                Cs0_corrent_alim_simul_exp = Cs0_corrent_alim
                beta_simul_exp = beta_exp
                
                print(Q0_simul_exp, V0_simul_exp, Cs0_corrent_alim_simul_exp, beta_simul_exp)
        
                mi = mimax_exp*(C[1]/(Ks_exp + C[1]))
                multiplicacao = beta_simul_exp*t_bat_alim_simul
                exponencial = np.exp(multiplicacao)
                D = (Q0_simul_exp*np.exp(beta_simul_exp*t_bat_alim_simul))/(((Q0_simul_exp/beta_simul_exp)*(exponencial - 1)) + V0_simul_exp)
                dCxdt = (mi - Kd_exp - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_exp - C[1]) - ((mi*C[0])/Yxs_exp)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_exp_modelo + alfa_exp*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Monod_exp)
        func_simul_bat_alim = func_simul_alim_Monod_tres()
            
        
    # - Batelada alimentada Contois:
    ## - Contois (vazão constante): 
    if (cont == 1 and def_alim == "Taxa de Vazão Constante"):
        def func_simul_alim_Contois_um():
            def func_simul_alim_Contois_const(C, t_bat_alim_simul):
                mimax_const = mimax
                KSX_const = KSX
                Kd_const = Kd
                Yxs_const = Yxs
                alfa_const = alfa
                beta_const = beta
                    
                Q_simul_const = Q
                V0_simul_const = V0
                Cs0_corrent_alim_simul_const = Cs0_corrent_alim
              
                mi = mimax_const*(C[1]/((KSX_const*C[0]) + C[1]))
                D = Q_simul_const/(V0_simul_const + Q_simul_const*t_bat_alim_simul)
                dCxdt = (mi - Kd_const - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_const - C[1]) - ((mi*C[0])/Yxs_const)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_const + alfa_const*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Contois_const)
        func_simul_bat_alim = func_simul_alim_Contois_um()

    # - Contois (vazão linear):   
    if (cont == 1 and def_alim == "Taxa de Vazão Linear"):
        def func_simul_alim_Contois_dois():
            def func_simul_alim_Contois_lin(C, t_bat_alim_simul):
                mimax_lin = mimax
                KSX_lin = KSX
                Kd_lin = Kd
                Yxs_lin = Yxs
                alfa_lin = alfa
                beta_lin = beta
                    
                Q0_simul_lin = Q0
                V0_simul_lin = V0
                Cs0_corrent_alim_simul_lin = Cs0_corrent_alim
                a_simul = a
        
                mi = mimax_lin*(C[1]/((KSX_lin*C[0]) + C[1]))
                D = (Q0_simul_lin*(1+a_simul*t_bat_alim_simul))/((Q0_simul_lin*(t_bat_alim_simul+(a_simul*t_bat_alim_simul**2)))+V0_simul_lin)
                dCxdt = (mi - Kd_lin - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_lin - C[1]) - ((mi*C[0])/Yxs_lin)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_lin + alfa_lin*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Contois_lin)
        func_simul_bat_alim = func_simul_alim_Contois_dois()
        
    # - Contois (vazão exponencial):   
    if (cont == 1  and def_alim == "Taxa de Vazão Exponencial"):
        def func_simul_alim_Contois_tres():
            def func_simul_alim_Contois_exp(C, t_bat_alim_simul):
                mimax_exp = mimax
                KSX_exp = KSX
                Kd_exp = Kd
                Yxs_exp = Yxs
                alfa_exp = alfa
                beta_exp_modelo = beta
                    
                Q0_simul_exp = Q0
                V0_simul_exp = V0
                Cs0_corrent_alim_simul_exp = Cs0_corrent_alim
                beta_simul_exp = beta_exp
        
                mi = mimax_exp*(C[1]/((KSX_exp*C[0]) + C[1]))
                multiplicacao = beta_simul_exp*t_bat_alim_simul
                exponencial = np.exp(multiplicacao)
                D = (Q0_simul_exp*np.exp(beta_simul_exp*t_bat_alim_simul))/(((Q0_simul_exp/beta_simul_exp)*(exponencial - 1)) + V0_simul_exp)
                dCxdt = (mi - Kd_exp - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_exp - C[1]) - ((mi*C[0])/Yxs_exp)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_exp_modelo + alfa_exp*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Contois_exp)
        func_simul_bat_alim = func_simul_alim_Contois_tres()
    
    # - Batelada alimentada Andrews:
    ## - Andrews (vazão constante): 
    if (cont == 2 and def_alim == "Taxa de Vazão Constante"):
        def func_simul_alim_Andrews_um():
            def func_simul_alim_Andrews_const(C, t_bat_alim_simul):
                mimax_const = mimax
                Ks_const = Ks
                Kd_const = Kd
                Yxs_const = Yxs
                alfa_const = alfa
                beta_const = beta
                KIS_const = KIS
                    
                Q_simul_const = Q
                V0_simul_const = V0
                Cs0_corrent_alim_simul_const = Cs0_corrent_alim
              
                mi = mimax_const * (C[1]/(Ks_const + C[1] + ((C[1]**2)/KIS_const)))
                D = Q_simul_const/(V0_simul_const + Q_simul_const*t_bat_alim_simul)
                dCxdt = (mi - Kd_const - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_const - C[1]) - ((mi*C[0])/Yxs_const)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_const + alfa_const*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Andrews_const)
        func_simul_bat_alim = func_simul_alim_Andrews_um()

    # - Andrews (vazão linear):   
    if (cont == 2 and def_alim == "Taxa de Vazão Linear"):
        def func_simul_alim_Andrews_dois():
            def func_simul_alim_Andrews_lin(C, t_bat_alim_simul):
                mimax_lin = mimax
                Ks_lin = Ks
                Kd_lin = Kd
                Yxs_lin = Yxs
                alfa_lin = alfa
                beta_lin = beta
                KIS_lin = KIS
                    
                Q0_simul_lin = Q0
                V0_simul_lin = V0
                Cs0_corrent_alim_simul_lin = Cs0_corrent_alim
                a_simul = a
        
                mi = mimax_lin * (C[1]/(Ks_lin + C[1] + ((C[1]**2)/KIS_lin)))
                D = (Q0_simul_lin*(1+a_simul*t_bat_alim_simul))/((Q0_simul_lin*(t_bat_alim_simul+(a_simul*t_bat_alim_simul**2)))+V0_simul_lin)
                dCxdt = (mi - Kd_lin - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_lin - C[1]) - ((mi*C[0])/Yxs_lin)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_lin + alfa_lin*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Andrews_lin)
        func_simul_bat_alim = func_simul_alim_Andrews_dois()
        
    # - Andrews (vazão exponencial):   
    if (cont == 2 and def_alim == "Taxa de Vazão Exponencial"):
        def func_simul_alim_Andrews_tres():
            def func_simul_alim_Andrews_exp(C, t_bat_alim_simul):
                mimax_exp = mimax
                Ks_exp = Ks
                Kd_exp = Kd
                Yxs_exp = Yxs
                alfa_exp = alfa
                beta_exp_modelo = beta
                KIS_exp = KIS
                    
                Q0_simul_exp = Q0
                V0_simul_exp = V0
                Cs0_corrent_alim_simul_exp = Cs0_corrent_alim
                beta_simul_exp = beta_exp
        
                mi = mimax_exp * (C[1]/(Ks_exp + C[1] + ((C[1]**2)/KIS_exp)))
                multiplicacao = beta_simul_exp*t_bat_alim_simul
                exponencial = np.exp(multiplicacao)
                D = (Q0_simul_exp*np.exp(beta_simul_exp*t_bat_alim_simul))/(((Q0_simul_exp/beta_simul_exp)*(exponencial - 1)) + V0_simul_exp)
                dCxdt = (mi - Kd_exp - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_exp - C[1]) - ((mi*C[0])/Yxs_exp)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_exp_modelo + alfa_exp*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Andrews_exp)
        func_simul_bat_alim = func_simul_alim_Andrews_tres()
            
    
    # - Batelada alimentada Aiba et al:
    ## - Aiba (vazão constante): 
    if (cont == 3 and def_alim == "Taxa de Vazão Constante"):
        def func_simul_alim_Aiba_um():
            def func_simul_alim_Aiba_const(C, t_bat_alim_simul):
                mimax_const = mimax
                Ks_const = Ks
                Kd_const = Kd
                Yxs_const = Yxs
                alfa_const = alfa
                beta_const = beta
                Kp_aiba_const = Kp_aiba
                    
                Q_simul_const = Q
                V0_simul_const = V0
                Cs0_corrent_alim_simul_const = Cs0_corrent_alim
              
                mult_exp = -C[2] * Kp_aiba_const
                mi = mimax_const*((C[1]/(Ks_const + C[1]))*math.exp(mult_exp))
                D = Q_simul_const/(V0_simul_const + Q_simul_const*t_bat_alim_simul)
                dCxdt = (mi - Kd_const - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_const - C[1]) - ((mi*C[0])/Yxs_const)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_const + alfa_const*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Aiba_const)
        func_simul_bat_alim = func_simul_alim_Aiba_um()

    # - Aiba (vazão linear):   
    if (cont == 3 and def_alim == "Taxa de Vazão Linear"):
        def func_simul_alim_Aiba_dois():
            def func_simul_alim_Aiba_lin(C, t_bat_alim_simul):
                mimax_lin = mimax
                Ks_lin = Ks
                Kd_lin = Kd
                Yxs_lin = Yxs
                alfa_lin = alfa
                beta_lin = beta
                Kp_aiba_lin = Kp_aiba
                    
                Q0_simul_lin = Q0
                V0_simul_lin = V0
                Cs0_corrent_alim_simul_lin = Cs0_corrent_alim
                a_simul = a
        
                mult_exp = -C[2] * Kp_aiba_lin
                mi = mimax_lin*((C[1]/(Ks_lin + C[1]))*math.exp(mult_exp))
                D = (Q0_simul_lin*(1+a_simul*t_bat_alim_simul))/((Q0_simul_lin*(t_bat_alim_simul+(a_simul*t_bat_alim_simul**2)))+V0_simul_lin)
                dCxdt = (mi - Kd_lin - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_lin - C[1]) - ((mi*C[0])/Yxs_lin)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_lin + alfa_lin*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Aiba_lin)
        func_simul_bat_alim = func_simul_alim_Aiba_dois()
        
    # - Aiba (vazão exponencial):   
    if (cont == 3 and def_alim == "Taxa de Vazão Exponencial"):
        def func_simul_alim_Aiba_tres():
            def func_simul_alim_Aiba_exp(C, t_bat_alim_simul):
                mimax_exp = mimax
                Ks_exp = Ks
                Kd_exp = Kd
                Yxs_exp = Yxs
                alfa_exp = alfa
                beta_exp_modelo = beta
                Kp_aiba_exp = Kp_aiba
                    
                Q0_simul_exp = Q0
                V0_simul_exp = V0
                Cs0_corrent_alim_simul_exp = Cs0_corrent_alim
                beta_simul_exp = beta_exp
        
                mult_exp = -C[2] * Kp_aiba_exp
                mi = mimax_exp*((C[1]/(Ks_exp + C[1]))*math.exp(mult_exp))
                multiplicacao = beta_simul_exp*t_bat_alim_simul
                exponencial = np.exp(multiplicacao)
                D = (Q0_simul_exp*np.exp(beta_simul_exp*t_bat_alim_simul))/(((Q0_simul_exp/beta_simul_exp)*(exponencial - 1)) + V0_simul_exp)
                dCxdt = (mi - Kd_exp - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_exp - C[1]) - ((mi*C[0])/Yxs_exp)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_exp_modelo + alfa_exp*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Aiba_exp)
        func_simul_bat_alim = func_simul_alim_Aiba_tres()
    
    # - Batelada alimentada Moser:
    ## - Moser (vazão constante): 
    if (cont == 4 and def_alim == "Taxa de Vazão Constante"):
        def func_simul_alim_Moser_um():
            def func_simul_alim_Moser_const(C, t_bat_alim_simul):
                mimax_const = mimax
                Ks_const = Ks
                Kd_const = Kd
                Yxs_const = Yxs
                alfa_const = alfa
                beta_const = beta
                u_const = u
                    
                Q_simul_const = Q
                V0_simul_const = V0
                Cs0_corrent_alim_simul_const = Cs0_corrent_alim
              
                mi = mimax_const*(((C[1])**u_const)/(Ks_const + ((C[1])**u_const)))
                D = Q_simul_const/(V0_simul_const + Q_simul_const*t_bat_alim_simul)
                dCxdt = (mi - Kd_const - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_const - C[1]) - ((mi*C[0])/Yxs_const)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_const + alfa_const*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Moser_const)
        func_simul_bat_alim = func_simul_alim_Moser_um()

    # - Moser (vazão linear):   
    if (cont == 4 and def_alim == "Taxa de Vazão Linear"):
        def func_simul_alim_Moser_dois():
            def func_simul_alim_Moser_lin(C, t_bat_alim_simul):
                mimax_lin = mimax
                Ks_lin = Ks
                Kd_lin = Kd
                Yxs_lin = Yxs
                alfa_lin = alfa
                beta_lin = beta
                u_lin = u
                    
                Q0_simul_lin = Q0
                V0_simul_lin = V0
                Cs0_corrent_alim_simul_lin = Cs0_corrent_alim
                a_simul = a
        
                mi = mimax_lin*(((C[1])**u_lin)/(Ks_lin + ((C[1])**u_lin)))
                D = (Q0_simul_lin*(1+a_simul*t_bat_alim_simul))/((Q0_simul_lin*(t_bat_alim_simul+(a_simul*t_bat_alim_simul**2)))+V0_simul_lin)
                dCxdt = (mi - Kd_lin - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_lin - C[1]) - ((mi*C[0])/Yxs_lin)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_lin + alfa_lin*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Moser_lin)
        func_simul_bat_alim = func_simul_alim_Moser_dois()
        
    # - Moser (vazão exponencial):   
    if (cont == 4 and def_alim == "Taxa de Vazão Exponencial"):
        def func_simul_alim_Moser_tres():
            def func_simul_alim_Moser_exp(C, t_bat_alim_simul):
                mimax_exp = mimax
                Ks_exp = Ks
                Kd_exp = Kd
                Yxs_exp = Yxs
                alfa_exp = alfa
                beta_exp_modelo = beta
                u_exp = u
                    
                Q0_simul_exp = Q0
                V0_simul_exp = V0
                Cs0_corrent_alim_simul_exp = Cs0_corrent_alim
                beta_simul_exp = beta_exp
        
                mi = mimax_exp*(((C[1])**u_exp)/(Ks_exp + ((C[1])**u_exp)))
                multiplicacao = beta_simul_exp*t_bat_alim_simul
                exponencial = np.exp(multiplicacao)
                D = (Q0_simul_exp*np.exp(beta_simul_exp*t_bat_alim_simul))/(((Q0_simul_exp/beta_simul_exp)*(exponencial - 1)) + V0_simul_exp)
                dCxdt = (mi - Kd_exp - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_exp - C[1]) - ((mi*C[0])/Yxs_exp)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_exp_modelo + alfa_exp*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Moser_exp)
        func_simul_bat_alim = func_simul_alim_Moser_tres()
    
    # - Batelada alimentada Hoppe & Hansford:
    ## - HH (vazão constante): 
    if (cont == 5 and def_alim == "Taxa de Vazão Constante"):
        def func_simul_alim_Hoppe_Hansford_um():
            def func_simul_alim_Hoppe_Hansford_const(C, t_bat_alim_simul):
                mimax_const = mimax
                Ks_const = Ks
                Kd_const = Kd
                Yxs_const = Yxs
                alfa_const = alfa
                beta_const = beta
                Kp_hoppe_const = Kp_hh
                    
                Q_simul_const = Q
                V0_simul_const = V0
                Cs0_corrent_alim_simul_const = Cs0_corrent_alim
              
                mi = mimax_const*(C[1]/(Ks_const + C[1]))*(Kp_hoppe_const/(Kp_hoppe_const + C[2]))
                D = Q_simul_const/(V0_simul_const + Q_simul_const*t_bat_alim_simul)
                dCxdt = (mi - Kd_const - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_const - C[1]) - ((mi*C[0])/Yxs_const)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_const + alfa_const*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Hoppe_Hansford_const)
        func_simul_bat_alim = func_simul_alim_Hoppe_Hansford_um()

    # - HH (vazão linear):   
    if (cont == 5 and def_alim == "Taxa de Vazão Linear"):
        def func_simul_alim_Hoppe_Hansford_dois():
            def func_simul_alim_Hoppe_Hansford_lin(C, t_bat_alim_simul):
                mimax_lin = mimax
                Ks_lin = Ks
                Kd_lin = Kd
                Yxs_lin = Yxs
                alfa_lin = alfa
                beta_lin = beta
                Kp_hoppe_lin = Kp_hh
                    
                Q0_simul_lin = Q0
                V0_simul_lin = V0
                Cs0_corrent_alim_simul_lin = Cs0_corrent_alim
                a_simul = a
        
                mi = mimax_lin*(C[1]/(Ks_lin + C[1]))*(Kp_hoppe_lin/(Kp_hoppe_lin + C[2]))
                D = (Q0_simul_lin*(1+a_simul*t_bat_alim_simul))/((Q0_simul_lin*(t_bat_alim_simul+(a_simul*t_bat_alim_simul**2)))+V0_simul_lin)
                dCxdt = (mi - Kd_lin - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_lin - C[1]) - ((mi*C[0])/Yxs_lin)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_lin + alfa_lin*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Hoppe_Hansford_lin)
        func_simul_bat_alim = func_simul_alim_Hoppe_Hansford_dois()
        
    # - HH (vazão exponencial):   
    if (cont == 5  and def_alim == "Taxa de Vazão Exponencial"):
        def func_simul_alim_Hoppe_Hansford_tres():
            def func_simul_alim_Hoppe_Hansford_exp(C, t_bat_alim_simul):
                mimax_exp = mimax
                Ks_exp = Ks
                Kd_exp = Kd
                Yxs_exp = Yxs
                alfa_exp = alfa
                beta_exp_modelo = beta
                Kp_hoppe_exp = Kp_hh
                    
                Q0_simul_exp = Q0
                V0_simul_exp = V0
                Cs0_corrent_alim_simul_exp = Cs0_corrent_alim
                beta_simul_exp = beta_exp
        
                mi = mimax_exp*(C[1]/(Ks_exp + C[1]))*(Kp_hoppe_exp/(Kp_hoppe_exp + C[2]))
                multiplicacao = beta_simul_exp*t_bat_alim_simul
                exponencial = np.exp(multiplicacao)
                D = (Q0_simul_exp*np.exp(beta_simul_exp*t_bat_alim_simul))/(((Q0_simul_exp/beta_simul_exp)*(exponencial - 1)) + V0_simul_exp)
                dCxdt = (mi - Kd_exp - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_exp - C[1]) - ((mi*C[0])/Yxs_exp)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_exp_modelo + alfa_exp*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Hoppe_Hansford_exp)
        func_simul_bat_alim = func_simul_alim_Hoppe_Hansford_tres()
    
    # - Batelada alimentada Wu et al:
    ## - Wu (vazão constante): 
    if (cont == 6 and def_alim == "Taxa de Vazão Constante"):
        def func_simul_alim_Wu_et_al_um():
            def func_simul_alim_Wu_et_al_const(C, t_bat_alim_simul):
                mimax_const = mimax
                Ks_const = Ks
                Kd_const = Kd
                Yxs_const = Yxs
                alfa_const = alfa
                beta_const = beta
                Ke_const = Ke
                v_const = v
                    
                Q_simul_const = Q
                V0_simul_const = V0
                Cs0_corrent_alim_simul_const = Cs0_corrent_alim
              
                mi = mimax_const * (C[1]/(Ks_const + C[1] + C[1]*((C[1]/Ke_const)**v_const)))
                D = Q_simul_const/(V0_simul_const + Q_simul_const*t_bat_alim_simul)
                dCxdt = (mi - Kd_const - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_const - C[1]) - ((mi*C[0])/Yxs_const)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_const + alfa_const*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Wu_et_al_const)
        func_simul_bat_alim = func_simul_alim_Wu_et_al_um()

    # - Wu (vazão linear):   
    if (cont == 6 and def_alim == "Taxa de Vazão Linear"):
        def func_simul_alim_Wu_et_al_dois():
            def func_simul_alim_Wu_et_al_lin(C, t_bat_alim_simul):
                mimax_lin = mimax
                Ks_lin = Ks
                Kd_lin = Kd
                Yxs_lin = Yxs
                alfa_lin = alfa
                beta_lin = beta
                Ke_lin = Ke
                v_lin = v
                    
                Q0_simul_lin = Q0
                V0_simul_lin = V0
                Cs0_corrent_alim_simul_lin = Cs0_corrent_alim
                a_simul = a
        
                mi = mimax_lin * (C[1]/(Ks_lin + C[1] + C[1]*((C[1]/Ke_lin)**v_lin)))
                D = (Q0_simul_lin*(1+a_simul*t_bat_alim_simul))/((Q0_simul_lin*(t_bat_alim_simul+(a_simul*t_bat_alim_simul**2)))+V0_simul_lin)
                dCxdt = (mi - Kd_lin - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_lin - C[1]) - ((mi*C[0])/Yxs_lin)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_lin + alfa_lin*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Wu_et_al_lin)
        func_simul_bat_alim = func_simul_alim_Wu_et_al_dois()
        
    # - Wu(vazão exponencial):   
    if (cont == 6  and def_alim == "Taxa de Vazão Exponencial"):
        def func_simul_alim_Wu_et_al_tres():
            def func_simul_alim_Wu_et_al_exp(C, t_bat_alim_simul):
                mimax_exp = mimax
                Ks_exp = Ks
                Kd_exp = Kd
                Yxs_exp = Yxs
                alfa_exp = alfa
                beta_exp_modelo = beta
                Ke_exp = Ke
                v_exp = v
                    
                Q0_simul_exp = Q0
                V0_simul_exp = V0
                Cs0_corrent_alim_simul_exp = Cs0_corrent_alim
                beta_simul_exp = beta_exp
        
                mi = mimax_exp * (C[1]/(Ks_exp + C[1] + C[1]*((C[1]/Ke_exp)**v_exp)))
                multiplicacao = beta_simul_exp*t_bat_alim_simul
                exponencial = np.exp(multiplicacao)
                D = (Q0_simul_exp*np.exp(beta_simul_exp*t_bat_alim_simul))/(((Q0_simul_exp/beta_simul_exp)*(exponencial - 1)) + V0_simul_exp)
                dCxdt = (mi - Kd_exp - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_exp - C[1]) - ((mi*C[0])/Yxs_exp)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_exp_modelo + alfa_exp*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Wu_et_al_exp)
        func_simul_bat_alim = func_simul_alim_Wu_et_al_tres()
    
    # - Batelada alimentada Levenspiel:
    ## - Levenspiel (vazão constante): 
    if (cont == 7 and def_alim == "Taxa de Vazão Constante"):
        def func_simul_alim_Levenspiel_um():
            def func_simul_alim_Levenspiel_const(C, t_bat_alim_simul):
                mimax_const = mimax
                Ks_const = Ks
                Kd_const = Kd
                Yxs_const = Yxs
                alfa_const = alfa
                beta_const = beta
                Cp_estr_const = Cp_estr
                n_const = n
                    
                Q_simul_const = Q
                V0_simul_const = V0
                Cs0_corrent_alim_simul_const = Cs0_corrent_alim
              
                mi = mimax_const*((C[1]/(Ks_const + C[1]))*((abs(1 - (C[2]/Cp_estr_const)))**n_const))
                D = Q_simul_const/(V0_simul_const + Q_simul_const*t_bat_alim_simul)
                dCxdt = (mi - Kd_const - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_const - C[1]) - ((mi*C[0])/Yxs_const)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_const + alfa_const*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Levenspiel_const)
        func_simul_bat_alim = func_simul_alim_Levenspiel_um()

    # - Levenspiel (vazão linear):   
    if (cont == 7 and def_alim == "Taxa de Vazão Linear"):
        def func_simul_alim_Levenspiel_dois():
            def func_simul_alim_Levenspiel_lin(C, t_bat_alim_simul):
                mimax_lin = mimax
                Ks_lin = Ks
                Kd_lin = Kd
                Yxs_lin = Yxs
                alfa_lin = alfa
                beta_lin = beta
                Cp_estr_lin = Cp_estr
                n_lin= n
                    
                Q0_simul_lin = Q0
                V0_simul_lin = V0
                Cs0_corrent_alim_simul_lin = Cs0_corrent_alim
                a_simul = a
        
                mi = mimax_lin*((C[1]/(Ks_lin + C[1]))*((abs(1 - (C[2]/Cp_estr_lin)))**n_lin))
                D = (Q0_simul_lin*(1+a_simul*t_bat_alim_simul))/((Q0_simul_lin*(t_bat_alim_simul+(a_simul*t_bat_alim_simul**2)))+V0_simul_lin)
                dCxdt = (mi - Kd_lin - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_lin - C[1]) - ((mi*C[0])/Yxs_lin)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_lin + alfa_lin*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Levenspiel_lin)
        func_simul_bat_alim = func_simul_alim_Levenspiel_dois()
        
    # - Levenspiel (vazão exponencial):   
    if (cont == 7  and def_alim == "Taxa de Vazão Exponencial"):
        def func_simul_alim_Levenspiel_tres():
            def func_simul_alim_Levenspiel_exp(C, t_bat_alim_simul):
                mimax_exp = mimax
                Ks_exp = Ks
                Kd_exp = Kd
                Yxs_exp = Yxs
                alfa_exp = alfa
                beta_exp_modelo = beta
                Cp_estr_exp = Cp_estr
                n_exp = n
                    
                Q0_simul_exp = Q0
                V0_simul_exp = V0
                Cs0_corrent_alim_simul_exp = Cs0_corrent_alim
                beta_simul_exp = beta_exp
        
                mi = mimax_exp*((C[1]/(Ks_exp + C[1]))*((abs(1 - (C[2]/Cp_estr_exp)))**n_exp))
                multiplicacao = beta_simul_exp*t_bat_alim_simul
                exponencial = np.exp(multiplicacao)
                D = (Q0_simul_exp*np.exp(beta_simul_exp*t_bat_alim_simul))/(((Q0_simul_exp/beta_simul_exp)*(exponencial - 1)) + V0_simul_exp)
                dCxdt = (mi - Kd_exp - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_exp - C[1]) - ((mi*C[0])/Yxs_exp)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_exp_modelo + alfa_exp*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Levenspiel_exp)
        func_simul_bat_alim = func_simul_alim_Levenspiel_tres()
    
    # - Batelada alimentada Lee et al:
    ## - Lee (vazão constante): 
    if (cont == 8 and def_alim == "Taxa de Vazão Constante"):
        def func_simul_alim_Lee_et_al_um():
            def func_simul_alim_Lee_et_al_const(C, t_bat_alim_simul):
                mimax_const = mimax
                Ks_const = Ks
                Kd_const = Kd
                Yxs_const = Yxs
                alfa_const = alfa
                beta_const = beta
                Cx_estr_const = Cx_estr
                m_const = m
                    
                Q_simul_const = Q
                V0_simul_const = V0
                Cs0_corrent_alim_simul_const = Cs0_corrent_alim
              
                mi = mimax_const*((C[1]/(Ks_const + C[1]))*((abs(1 - (C[0]/Cx_estr_const)))**m_const))
                D = Q_simul_const/(V0_simul_const + Q_simul_const*t_bat_alim_simul)
                dCxdt = (mi - Kd_const - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_const - C[1]) - ((mi*C[0])/Yxs_const)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_const + alfa_const*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Lee_et_al_const)
        func_simul_bat_alim = func_simul_alim_Lee_et_al_um()

    # - Lee (vazão linear):   
    if (cont == 8 and def_alim == "Taxa de Vazão Linear"):
        def func_simul_alim_Lee_et_al_dois():
            def func_simul_alim_Lee_et_al_lin(C, t_bat_alim_simul):
                mimax_lin = mimax
                Ks_lin = Ks
                Kd_lin = Kd
                Yxs_lin = Yxs
                alfa_lin = alfa
                beta_lin = beta
                Cx_estr_lin = Cx_estr
                m_lin = m
                    
                Q0_simul_lin = Q0
                V0_simul_lin = V0
                Cs0_corrent_alim_simul_lin = Cs0_corrent_alim
                a_simul = a
        
                mi = mimax_lin*((C[1]/(Ks_lin + C[1]))*((abs(1 - (C[0]/Cx_estr_lin)))**m_lin))
                D = (Q0_simul_lin*(1+a_simul*t_bat_alim_simul))/((Q0_simul_lin*(t_bat_alim_simul+(a_simul*t_bat_alim_simul**2)))+V0_simul_lin)
                dCxdt = (mi - Kd_lin - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_lin - C[1]) - ((mi*C[0])/Yxs_lin)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_lin + alfa_lin*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Lee_et_al_lin)
        func_simul_bat_alim = func_simul_alim_Lee_et_al_dois()
        
    # - Lee (vazão exponencial):   
    if (cont == 8  and def_alim == "Taxa de Vazão Exponencial"):
        def func_simul_alim_Lee_et_al_tres():
            def func_simul_alim_Lee_et_al_exp(C, t_bat_alim_simul):
                mimax_exp = mimax
                Ks_exp = Ks
                Kd_exp = Kd
                Yxs_exp = Yxs
                alfa_exp = alfa
                beta_exp_modelo = beta
                Cx_estr_exp = Cx_estr
                m_exp = m
                    
                Q0_simul_exp = Q0
                V0_simul_exp = V0
                Cs0_corrent_alim_simul_exp = Cs0_corrent_alim
                beta_simul_exp = beta_exp
        
                mi = mimax_exp*((C[1]/(Ks_exp + C[1]))*((abs(1 - (C[0]/Cx_estr_exp)))**m_exp))
                multiplicacao = beta_simul_exp*t_bat_alim_simul
                exponencial = np.exp(multiplicacao)
                D = (Q0_simul_exp*np.exp(beta_simul_exp*t_bat_alim_simul))/(((Q0_simul_exp/beta_simul_exp)*(exponencial - 1)) + V0_simul_exp)
                dCxdt = (mi - Kd_exp - D)*C[0]
                dCsdt = D*(Cs0_corrent_alim_simul_exp - C[1]) - ((mi*C[0])/Yxs_exp)
                dCpdt = D*(Cp0_simul_bat_alim - C[2]) + C[0]*(beta_exp_modelo + alfa_exp*mi)
                return(dCxdt,dCsdt,dCpdt)
            return(func_simul_alim_Lee_et_al_exp)
        func_simul_bat_alim = func_simul_alim_Lee_et_al_tres()
            
    # Integrando numericamente:
    C_sim_bat_alim = odeint(func_simul_bat_alim, inic_cond_alim_simul, t_bat_alim_simul)
    print(C_sim_bat_alim)
    Cx_bat_alim = C_sim_bat_alim[:,0]
    Cs_bat_alim = C_sim_bat_alim[:,1]
    Cp_bat_alim = C_sim_bat_alim[:,2]
    
    # * UNIÃO DAS SAÍDAS BATELADA E BATELADA ALIMENTADA * #
    ## Contadores gerais
    limitebatelada = len(C_sim_bat)
    print("Limite batelada",limitebatelada)
    limitealimentada = len(C_sim_bat_alim)
    print("Limite batelada alimentada", limitealimentada)

    Cx_simul = []
    Cs_simul = []
    Cp_simul = []
    bat = 0
    batal = 0
    
    while (bat < limitebatelada):
        Cx_simul.append(Cx_bat[bat])
        Cs_simul.append(Cs_bat[bat])
        Cp_simul.append(Cp_bat[bat])
        bat = bat +  1       
    while (batal < limitealimentada):
        Cx_simul.append(Cx_bat_alim[batal])
        Cs_simul.append(Cs_bat_alim[batal])
        Cp_simul.append(Cp_bat_alim[batal])
        batal = batal + 1

    ## Vetor tempo total do processo:
    Ttotal_simul = np.arange(t0, tf, 0.5)

    ## Conversão das listas para arrays - necessário para operações matemáticas:
    Cx_simul = np.asarray(Cx_simul)
    Cs_simul = np.asarray(Cs_simul)
    Cp_simul = np.asarray(Cp_simul)
  
    
####__________________________________________ **** PLOTAGEM GRÁFICA **** __________________________________________####
    
#//__________________________________________ * - PERFIL DE CONCENTRAÇÃO - * _________________________________________//#
    
    # Gráfico - perfil de concentração:       
    x = "red"
    p = "green"
    s = "blue"
    def imprimir_perfil_concentracao_simul(t_m, Cx_m, Cs_m, Cp_m):
        tamanho_graf()
        f = plt.figure(figsize=(8.3,6), dpi = 54) 
        plot = f.add_subplot(111) 
        _ = lns1 = plot.plot(Ttotal_simul, Cx_m, color = x, linewidth=3,label='Cx modelo')
        _ = lns2 = plot.plot(Ttotal_simul, Cs_m, linestyle=":", color=s,linewidth=3,label='Cs modelo')
        ax2 = plot.twinx()
        _ = lns3 = ax2.plot(Ttotal_simul, Cp_m, linestyle="--", color=p,linewidth=3,label='Cp modelo') 
        _ = plot.axvline(x = tf_bat, color = "grey", linestyle="dashed", linewidth=3)
        _ = plot.set_xlabel('Tempo de cultivo (h)',weight='bold')               
        _ = plot.set_ylabel('Cx e Cs (g/L)', weight='bold')
        ax2.set_ylabel('Cp (g/L)', weight='bold') 
        _ = lns = lns1+lns2+lns3
        labs = [l.get_label() for l in lns]
        _ = plot.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.14),ncol=3, fancybox=True, shadow=True)                                                
        plot.grid(True)
        f.patch.set_facecolor('white')                                   
        plt.style.use('default')
        canvas = FigureCanvasTkAgg(f, frame22)
        a_concent = canvas.get_tk_widget().place(x = 0, y = 0)
        def salvar_concent():
            a_concent = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
            defaultextension='.png')
            plt.savefig(a_concent)
        botao_com_graf(frame = frame22, comando_salvar = lambda : salvar_concent(), comando_destroy = canvas.get_tk_widget().destroy, x = 450, y = 176)
    imprimir_perfil_concentracao_simul(Ttotal_simul, Cx_simul, Cs_simul, Cp_simul)
    
    def graf_cor (x,s,p): 
        tamanho_graf()
        f = plt.figure(figsize=(8.3,6), dpi = 54) 
        plot = f.add_subplot(111) 
        _ = lns1 = plot.plot(Ttotal_simul, Cx_simul, color = x, linewidth=3,label='Cx modelo')
        _ = lns2 = plot.plot(Ttotal_simul, Cs_simul, linestyle=":", color = s,linewidth=3,label='Cs modelo')
        ax2 = plot.twinx()
        _ = lns3 = ax2.plot(Ttotal_simul, Cp_simul,linestyle="--", color = p,linewidth=3,label='Cp modelo') 
        _ = plot.axvline(x = tf_bat, color = "grey", linestyle="dashed", linewidth=3)
        _ = plot.set_xlabel('Tempo de cultivo (h)',weight='bold')               
        _ = plot.set_ylabel('Cx e Cs (g/L)', weight='bold')
        ax2.set_ylabel('Cp (g/L)', weight='bold') 
        lns = lns1+lns2+lns3
        labs = [l.get_label() for l in lns]
        _ = plot.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.14),ncol=3, fancybox=True, shadow=True)                                                
        _ = plot.grid(True)
        f.patch.set_facecolor('white')                                   
        plt.style.use('default')
        canvas = FigureCanvasTkAgg(f, frame22)
        a_concent = canvas.get_tk_widget().place(x = 0, y = 0)
        def salvar():
            a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
            defaultextension='.png')
            plt.savefig(a)
        botao_com_graf(frame = frame22, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy, x = 450, y = 176)
        
    ## Escolha das cores:
    def seletor_cores():
        cor = colorchooser.askcolor(title = "Editar cores")
        return(cor[1])
    def cores_cx():
        global cor_x
        cor_x = colorchooser.askcolor(title ="Editar cores")
        cor_x = cor_x[1]
        fig = graf_cor (x = cor_x, p = "green", s = "blue")
        Button(frame22, text = "Cs", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_cs).place(x = 460, y = 258) 
    def cores_cs():
        global cor_s
        cor_s = colorchooser.askcolor(title ="Editar cores")
        cor_s = cor_s[1]
        fig = graf_cor (x = cor_x, p = "green", s = cor_s)
        Button(frame22, text = "Cs", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_cs).place(x = 460, y = 258)
        Button(frame22, text = "Cp", bg = "gray40", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_cp).place(x = 460, y = 286)  
    def cores_cp():
        global cor_p
        cor_p = colorchooser.askcolor(title ="Editar cores")
        cor_p = cor_p[1] 
        fig = graf_cor (x = cor_x, p = cor_p, s = cor_s)
        Button(frame22, text = "Cp", bg = "gray40", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_cp).place(x = 460, y = 286)
    def cores_concent():
        Button(frame22, text = "Cx", bg = "gray60", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_cx).place(x = 460, y = 230)
        botao_paleta_graf(frame = frame22, comando = cores_concent)
    
    botao_paleta_graf(frame = frame22, comando = cores_concent)

#\\__________________________________________ * - PERFIL DE CONCENTRAÇÃO - * _________________________________________\\#
    

#//___________________________________ * - PRODUTIVIDADE CELULAR E DO PRODUTO - * ____________________________________//#    
    
    ## Cálculos:
    Px = Cx_simul[1:]/Ttotal_simul[1:]
    Pp = Cp_simul[1:]/Ttotal_simul[1:]
    
    ## Plotando a figura gráfica - produtividades:
    # Gráfico - produtividades:
    def graf_produtiv(px, pp):
        def imprimir_produtividade_celular_produto(t_m,Px_m, Pp_m):
            tamanho_graf()
            f = plt.figure(figsize=(8.3,6), dpi = 54) 
            _ = plot = f.add_subplot(111)  
            _ = lns1 = plot.plot(t_m ,Px_m,color = px,linewidth=3,label='Produtividade Celular')
            ax2 = plot.twinx()
            _ = lns2 = ax2.plot(t_m,Pp_m,linestyle=":", color = pp,linewidth=3,label='Produtividade do Produto')
            _ = plot.axvline(x = tf_bat, color = "grey", linestyle="dashed", linewidth=3)
            _ = plot.set_xlabel('Tempo de cultivo (h)',weight='bold')               
            _ = plot.set_ylabel('Produtividade Celular (gx/L.h)', weight='bold')
            ax2.set_ylabel('Produtividade Produto (gp/L.h)', weight='bold') 
            lns = lns1+lns2
            labs = [l.get_label() for l in lns]
            _ = plot.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.14),ncol=2, fancybox=True, shadow=True )                                                
            _ =plot.grid(True)
            f.patch.set_facecolor('white')                                   
            plt.style.use('default')    
            canvas = FigureCanvasTkAgg(f, frame23)
            a_produtiv = canvas.get_tk_widget().place(x = 0, y = 0)
            def salvar():
                a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                defaultextension='.png')
                plt.savefig(a)
            botao_com_graf(frame = frame23, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy, x = 450, y = 176)
        imprimir_produtividade_celular_produto(Ttotal_simul[1:], Px, Pp)
    
    ## Escolha das cores:
    def seletor_cores():
        cor = colorchooser.askcolor(title = "Editar cores")
        return(cor[1])
    def cores_px():
        global cor_px
        cor_px = colorchooser.askcolor(title ="Editar cores")
        cor_px = cor_px[1]
        fig = graf_produtiv(px = cor_px, pp = "green")
        Button(frame23, text = "Pp", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_pp).place(x = 460, y = 258)   
    def cores_pp():
        global cor_pp
        cor_pp = colorchooser.askcolor(title ="Editar cores")
        cor_pp = cor_pp[1]
        fig = graf_produtiv(px = cor_px, pp = cor_pp)
        Button(frame23, text = "Pp", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_pp).place(x = 460, y = 258)
    def cores_produtiv():
        Button(frame23, text = "Px", bg = "gray60", fg="white", borderwidth=2, relief="raised", font="batang 10 bold", width = 2, command = cores_px).place(x = 460, y = 230)    
       
    # Geração do gráfico:
    graf_produtiv(px = "red", pp = "green")
    ## Botão para seleção das cores:
    botao_paleta_graf(frame23, comando = cores_produtiv)

#\\___________________________________ * - PRODUTIVIDADE CELULAR E DO PRODUTO - * ____________________________________\\#


#//_____________________________ * - PRODUTIVIDADE ESPECÍFICA (PRODUTO/BIOMASSA) - * ________________________________//#
   
    # Cálculo produtividade específica:
    Ppx = Cp_simul * (1 / Cx_simul)
    Ppx[Ppx<0] = 0
    # Gráfico produtividade específica:
    def graf_produtiv_espec(Ppx_cor):
        def imprimir_produtividade_especifica_model_otim_exp (t_m, Ppx_m):
            tamanho_graf()
            f = plt.figure(figsize=(8.3,6), dpi = 54) 
            plot = f.add_subplot(111)  
            _ = plt.plot(t_m,Ppx_m,color = Ppx_cor,linewidth=3, label='Simulado')
            _ = plot.axvline(x = tf_bat, color = "grey", linestyle="dashed", linewidth=3)
            _ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
            _ = plt.ylabel('Produtividade Específica (gp/gx)', weight='bold')
            _ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.14),ncol=2, fancybox=True, shadow=True )
            _ = plt.grid(True)  
            f.patch.set_facecolor('white')                                   
            plt.style.use('default')                       
            canvas = FigureCanvasTkAgg(f, frame24)
            a_produtiv_espec = canvas.get_tk_widget().place(x = 0, y = 0)
            def salvar():
                a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                defaultextension='.png')
                plt.savefig(a)
            botao_com_graf(frame = frame24, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy, x = 450, y = 176)
        imprimir_produtividade_especifica_model_otim_exp(Ttotal_simul, Ppx)
    
    ## Escolha das cores:
    def seletor_cores_Ppx():
        cor_Ppx = colorchooser.askcolor(title ="Editar cores")
        cor_Ppx = cor_Ppx[1]
        graf_produtiv_espec(Ppx_cor = cor_Ppx)
        
    graf_produtiv_espec(Ppx_cor = "red")
    ## Botão para seleção das cores:
    botao_paleta_graf(frame24, comando = seletor_cores_Ppx) 
    
#\\_____________________________ * - PRODUTIVIDADE ESPECÍFICA (PRODUTO/BIOMASSA) - * ________________________________\\#


#//______________________________ * - TAXA ESPECÍFICA DE CRESCIMENTO MICROBIANO - * _________________________________//#    

    # Cálculo taxa mi:
    if (cont == 0):
        mi = mimax*(Cs_simul/(Ks + Cs_simul))
    if (cont == 1):
        mi = mimax*(Cs_simul/(KSX*Cx_simul + Cs_simul))
    if (cont == 2):
        mi = mimax*(Cs_simul/(Ks + Cs_simul + ((Cs_simul**2)/KIS)))
    if (cont == 3):
        mult = -Kp_aiba*Cp_simul
        mi = mimax*((Cs_simul/(Ks + Cs_simul))*np.exp(mult))
    if (cont == 4):
        mi = mimax*((Cs_simul**u)/(Ks + (Cs_simul**u)))
    if (cont == 5):
        mi = mimax*(Cs_simul/(Ks + Cs_simul))*(Kp_hh/(Kp_hh + Cp_simul))
    if (cont == 6):
        mi = mimax*(Cs_simul/(Ks + Cs_simul + (Cs_simul*((Cs_simul/Ke)**v))))
    if (cont == 7):
        mi = mimax*((Cs_simul/(Ks + Cs_simul))*((1-(Cp_simul/Cp_estr))**n))
    if (cont == 8):
        mi = mimax*((Cs_simul/(Ks + Cs_simul))*((1-(Cx_simul/Cx_estr))**m))
    mi[mi<0] = 0
    # Gráfico - velocidade de crescimento microbiano:
    def graf_mi(mi_cor):
        def imprimir_taxa_especifica_crescimento (t_m,  mi_m):
            tamanho_graf()
            f = plt.figure(figsize=(8.3,6), dpi = 54) 
            plot = f.add_subplot(111)                                             
            _ = plt.plot(t_m,mi_m,color = mi_cor,linewidth=3, label='Simulado')
            _ = plot.axvline(x = tf_bat, color = "grey", linestyle="dashed", linewidth=3)
            _ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
            _ = plt.ylabel('Taxa $\mu (h^{-1}$)', weight='bold')
            _ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.14),ncol=2, fancybox=True, shadow=True )  
            _ = plt.grid(True)  
            f.patch.set_facecolor('white')                                   
            plt.style.use('default')   
            canvas = FigureCanvasTkAgg(f, frame25)
            a_mi = canvas.get_tk_widget().place(x = 0, y = 0)
            def salvar():
                a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                defaultextension='.png')
                plt.savefig(a)
            botao_com_graf(frame = frame25, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy, x = 450, y = 176)
        imprimir_taxa_especifica_crescimento(Ttotal_simul, mi)
    
    ## Escolha das cores:
    def seletor_cores_mi():
        cor_mi = colorchooser.askcolor(title ="Editar cores")
        cor_mi = cor_mi[1]
        graf_mi(mi_cor = cor_mi)
        
    graf_mi(mi_cor = "red")
    ## Botão para seleção das cores:
    botao_paleta_graf(frame25, comando = seletor_cores_mi)


#//______________________________ * - TAXA ESPECÍFICA DE CRESCIMENTO MICROBIANO - * _________________________________//# 
    
#//______________________________________ * - VAZÃO: VARIAÇÃO TEMPORAL - * _________________________________________//# 
        
    ### *** CÁLCULO DO PERFIL DE VARIAÇÃO DE VAZÃO - RELAÇÃO TEMPORAL DEPENDENTE DA ALIMENTAÇÃO:
    ## ** Controle do processo - análise do perfil matemático ** ##:
    # - ALIMENTAÇÃO CONSTANTE:
    if (def_alim == "Taxa de Vazão Constante"):
        Q_calc = np.repeat(Q, len(t_bat_alim_simul))
    # - ALIMENTAÇÃO LINEAR:
    if (def_alim == "Taxa de Vazão Linear"):
        ### Função Q(t) original:
        Q_calc = Q0*(1 + a*t_bat_alim_simul)
    # - ALIMENTAÇÃO EXPONENCIAL:
    if (def_alim == "Taxa de Vazão Exponencial"):
        ### Função Q(t) original:
        Q_calc = Q0 * np.exp(beta_exp * t_bat_alim_simul)
    
    # Gráfico - variação temporal do vazão:
    def graf_vaz(vaz_cor):
        def imprimir_vazao(t_m, vaz_m):
            tamanho_graf()
            f = plt.figure(figsize=(8.3,6), dpi = 54) 
            plot = f.add_subplot(111)                                             
            _ = plt.plot(t_m, vaz_m,color = vaz_cor,linewidth=3, label='Simulado')
            _ = plot.axvline(x = tf_bat, color = "grey", linestyle="dashed", linewidth=3)
            _ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
            _ = plt.ylabel('Vazão (L/h)', weight='bold')
            _ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.14),ncol=2, fancybox=True, shadow=True )  
            _ = plt.grid(True)  
            f.patch.set_facecolor('white')                                   
            plt.style.use('default')   
            canvas = FigureCanvasTkAgg(f, frame47)
            a_vaz = canvas.get_tk_widget().place(x = 0, y = 0)
            def salvar():
                a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                defaultextension='.png')
                plt.savefig(a)
            botao_com_graf(frame = frame47, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy, x = 450, y = 176)
        imprimir_vazao(t_bat_alim_simul, Q_calc)
   
    ## Escolha das cores:
    def seletor_cores_vaz():
        cor_vaz = colorchooser.askcolor(title ="Editar cores")
        cor_vaz = cor_vaz[1]
        graf_vaz(vaz_cor = cor_vaz)
        
    graf_vaz(vaz_cor = "orange")
    ## Botão para seleção das cores:
    botao_paleta_graf(frame47, comando = seletor_cores_vaz)


#\\______________________________________ * - VAZÃO: VARIAÇÃO TEMPORAL - * _________________________________________\\# 
    

#//______________________________________ * - VOLUME: VARIAÇÃO TEMPORAL - * _________________________________________//# 
    
    ### *** CÁLCULO DO PERFIL DE VARIAÇÃO DE VOLUME - RELAÇÃO TEMPORAL DEPENDENTE DA ALIMENTAÇÃO:
    ## ** Controle do processo - análise do perfil matemático ** ##:
    # - ALIMENTAÇÃO CONSTANTE:
    if (def_alim == "Taxa de Vazão Constante"):
        ## Cálculo volume(t) - integração dV/dt = Q para Q constante:
        V_calc = Q * t_bat_alim_simul  + V0
    # - ALIMENTAÇÃO LINEAR:
    if (def_alim == "Taxa de Vazão Linear"):
        ## Cálculo volume(t) - integração dV/dt = Q para descrito pela equação linear:
        V_calc = (Q0*(t_bat_alim_simul + (a*t_bat_alim_simul**2))) + V0
    # - ALIMENTAÇÃO EXPONENCIAL:
    if (def_alim == "Taxa de Vazão Exponencial"):
        ## Cálculo volume(t) - integração dV/dt = Q para Q descrito pela equação exponencial:
        V_calc = ((Q0/beta_exp)*((np.exp(beta_exp*t_bat_alim_simul)) - 1)) + V0
        
    # Gráfico - variação temporal do volume:
    def graf_vol(vol_cor):
        def imprimir_volume(t_m, vol_m):
            tamanho_graf()
            f = plt.figure(figsize=(8.3,6), dpi = 54) 
            plot = f.add_subplot(111)                                             
            _ = plt.plot(t_m, vol_m,color = vol_cor,linewidth=3, label='Simulado')
            _ = plot.axvline(x = tf_bat, color = "grey", linestyle="dashed", linewidth=3)
            _ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
            _ = plt.ylabel('Volume (L)', weight='bold')
            _ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.14),ncol=2, fancybox=True, shadow=True )  
            _ = plt.grid(True)  
            f.patch.set_facecolor('white')                                   
            plt.style.use('default')   
            canvas = FigureCanvasTkAgg(f, frame46)
            a_vol = canvas.get_tk_widget().place(x = 0, y = 0)
            def salvar():
                a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                defaultextension='.png')
                plt.savefig(a)
            botao_com_graf(frame = frame46, comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy, x = 450, y = 176)
        imprimir_volume(t_bat_alim_simul, V_calc)
    
    ## Escolha das cores:
    def seletor_cores_vol():
        cor_vol = colorchooser.askcolor(title ="Editar cores")
        cor_vol = cor_vol[1]
        graf_vol(vol_cor = cor_vol)
        
    graf_vol(vol_cor = "lime")
    ## Botão para seleção das cores:
    botao_paleta_graf(frame46, comando = seletor_cores_vol)


#//______________________________________ * - VOLUME: VARIAÇÃO TEMPORAL - * _________________________________________//#
 
####_______________________________________ **** FIM DA PLOTAGEM GRÁFICA **** ______________________________________####

    #### **** EXPORTAÇÃO DOS RESULTADOS PARA PLANILHAS EXCEL **** ####:
    ## Inserindo 0 para o primeiro valor de produtividade:
    Px_ad = np.insert(Px,0,0)
    Pp_ad = np.insert(Pp,0,0)
        
    # Saída .xlsx - concentração, produtividade e taxa de crescimento:
    def excel_concent():
        df_sai_conc_produtiv_mi = pd.DataFrame({'Tempo(h)': Ttotal_simul, 'Cx(g/L)': Cx_simul, 'Cs(g/L)': Cs_simul, 'Cp(g/L)': Cp_simul, 'Px(gcél/L.h)': Px_ad, 'Pp(gprod/L.h)': Pp_ad, 'Ppx(gprod/gcél)': Ppx, 'mi(h-¹)': mi})
        df_Q_V = pd.DataFrame({'Tempo_alim(h)': t_bat_alim_simul, 'Q(L/h)': Q_calc, 'V(L)': V_calc})
        df_sai_simul = pd.concat([df_sai_conc_produtiv_mi, df_Q_V], axis = 1)
        with pd.ExcelWriter('Simul_Conc_Produt_mi_vaz.vol.xlsx') as writer:
            df_sai_simul.to_excel(writer, sheet_name="Saida_simulada")
            writer.save()
        os.system("start EXCEL Simul_Conc_Produt_mi_vaz.vol.xlsx")
    sai_resul_simul.configure(text = "Simul_Conc_Produt_mi_vaz.vol.xlsx", font = "arial 8 italic", fg = "black")
    # Função botão acesso excel:
    def botao_excel(imagem, num_frame, x, y):
        load = Image.open(imagem)
        render = ImageTk.PhotoImage(load)
        img = Button(num_frame, image = render, border = 0, command = excel_concent)
        img.image = render
        img.place(x = x, y = y)
    
    # Botão de acesso - arquivo .xlsx - parâmetros cinéticos:
    botao_excel(imagem = "Excel.png", num_frame = frame1, x = 926, y = 135)

# Função para capturar os valores de entrada:

# * Contois * #:
def entr_contois(frame):
    global entr_Cx0_contois, entr_Cs0_contois, entr_Cp0_contois, entr_t0_contois, entr_tf_contois
    entr_Cx0_contois = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cx0_contois.place(x = 50, y = 257)
    entr_Cs0_contois = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cs0_contois.place(x = 140, y = 257)
    entr_Cp0_contois = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cp0_contois.place(x = 230, y = 257)
    entr_t0_contois = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_t0_contois.place(x = 50, y = 287)
    entr_tf_contois = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_tf_contois.place(x = 140, y = 287)  
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

# * Monod * #:
def entr_monod(frame):
    global entr_Cx0_monod, entr_Cs0_monod, entr_Cp0_monod, entr_t0_monod, entr_tf_monod
    entr_Cx0_monod = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cx0_monod.place(x = 50, y = 257)
    entr_Cs0_monod = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cs0_monod.place(x = 140, y = 257)
    entr_Cp0_monod = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cp0_monod.place(x = 230, y = 257)
    entr_t0_monod = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_t0_monod.place(x = 50, y = 287)
    entr_tf_monod = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_tf_monod.place(x = 140, y = 287) 
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

# * Moser * #: 
def entr_moser(frame):
    global entr_Cx0_moser, entr_Cs0_moser, entr_Cp0_moser, entr_t0_moser, entr_tf_moser
    entr_Cx0_moser = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cx0_moser.place(x = 50, y = 257)
    entr_Cs0_moser = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cs0_moser.place(x = 140, y = 257)
    entr_Cp0_moser = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cp0_moser.place(x = 230, y = 257)
    entr_t0_moser = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_t0_moser.place(x = 50, y = 287)
    entr_tf_moser = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_tf_moser.place(x = 140, y = 287) 
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

# * mi constante * #:
def entr_mi_const(frame):
    global entr_Cx0_mi_const, entr_Cs0_mi_const, entr_Cp0_mi_const, entr_t0_mi_const, entr_tf_mi_const
    entr_Cx0_mi_const = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cx0_mi_const.place(x = 50, y = 257)
    entr_Cs0_mi_const = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cs0_mi_const.place(x = 140, y = 257)
    entr_Cp0_mi_const = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cp0_mi_const.place(x = 230, y = 257)
    entr_t0_mi_const = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_t0_mi_const.place(x = 50, y = 287)
    entr_tf_mi_const = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_tf_mi_const.place(x = 140, y = 287)    
def capt_val_esc_mi_const():
    global Cx0, Cs0, Cp0, t0, tf, mimax, Kd, Yxs, alfa, beta
    Cx0 = float(entr_Cx0_mi_const.get())
    Cs0 = float(entr_Cs0_mi_const.get())
    Cp0 = float(entr_Cp0_mi_const.get())
    t0 = float(entr_t0_mi_const.get())
    tf = float(entr_tf_mi_const.get())
    mimax = float(slider_mimax_mi_const.get())
    Kd = float(slider_kd_mi_const.get())
    Yxs = float(slider_yxs_mi_const.get())
    alfa = float(slider_alfa_mi_const.get())
    beta = float(slider_beta_mi_const.get())
    print(Cx0, Cs0, Cp0, t0, tf, mimax, Kd, Yxs, alfa, beta)
    simulacao(cont = 9)

# * Andrews * #:  
def entr_andrews(frame):
    global entr_Cx0_andrews, entr_Cs0_andrews, entr_Cp0_andrews, entr_t0_andrews, entr_tf_andrews
    entr_Cx0_andrews = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cx0_andrews.place(x = 50, y = 257)
    entr_Cs0_andrews = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cs0_andrews.place(x = 140, y = 257)
    entr_Cp0_andrews = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cp0_andrews.place(x = 230, y = 257)
    entr_t0_andrews = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_t0_andrews.place(x = 50, y = 287)
    entr_tf_andrews = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_tf_andrews.place(x = 140, y = 287)
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

# * Wu et al * #:
def entr_wu(frame):
    global entr_Cx0_wu, entr_Cs0_wu, entr_Cp0_wu, entr_t0_wu, entr_tf_wu
    entr_Cx0_wu = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cx0_wu.place(x = 50, y = 257)
    entr_Cs0_wu = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cs0_wu.place(x = 140, y = 257)
    entr_Cp0_wu = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cp0_wu.place(x = 230, y = 257)
    entr_t0_wu = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_t0_wu.place(x = 50, y = 287)
    entr_tf_wu = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_tf_wu.place(x = 140, y = 287)
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

# * Aiba et al * #: 
def entr_aiba(frame):
    global entr_Cx0_aiba, entr_Cs0_aiba, entr_Cp0_aiba, entr_t0_aiba, entr_tf_aiba
    entr_Cx0_aiba = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cx0_aiba.place(x = 50, y = 257)
    entr_Cs0_aiba = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cs0_aiba.place(x = 140, y = 257)
    entr_Cp0_aiba = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cp0_aiba.place(x = 230, y = 257)
    entr_t0_aiba = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_t0_aiba.place(x = 50, y = 287)
    entr_tf_aiba = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_tf_aiba.place(x = 140, y = 287)
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

# * Hoppe & Hansford * #: 
def entr_h_h(frame):
    global entr_Cx0_h_h, entr_Cs0_h_h, entr_Cp0_h_h, entr_t0_h_h, entr_tf_h_h
    entr_Cx0_h_h = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cx0_h_h.place(x = 50, y = 257)
    entr_Cs0_h_h = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cs0_h_h.place(x = 140, y = 257)
    entr_Cp0_h_h = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cp0_h_h.place(x = 230, y = 257)
    entr_t0_h_h = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_t0_h_h.place(x = 50, y = 287)
    entr_tf_h_h = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_tf_h_h.place(x = 140, y = 287)
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

# * Levenspiel * #:
def entr_levenspiel(frame):
    global entr_Cx0_levenspiel, entr_Cs0_levenspiel, entr_Cp0_levenspiel, entr_t0_levenspiel, entr_tf_levenspiel
    entr_Cx0_levenspiel = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cx0_levenspiel.place(x = 50, y = 257)
    entr_Cs0_levenspiel = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cs0_levenspiel.place(x = 140, y = 257)
    entr_Cp0_levenspiel = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cp0_levenspiel.place(x = 230, y = 257)
    entr_t0_levenspiel = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_t0_levenspiel.place(x = 50, y = 287)
    entr_tf_levenspiel = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_tf_levenspiel.place(x = 140, y = 287)
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

# * Lee et al * #
def entr_lee(frame):
    global entr_Cx0_lee, entr_Cs0_lee, entr_Cp0_lee, entr_t0_lee, entr_tf_lee
    entr_Cx0_lee = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cx0_lee.place(x = 50, y = 257)
    entr_Cs0_lee = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cs0_lee.place(x = 140, y = 257)
    entr_Cp0_lee = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_Cp0_lee.place(x = 230, y = 257)
    entr_t0_lee = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_t0_lee.place(x = 50, y = 287)
    entr_tf_lee = tk.Entry(frame, width = 7, borderwidth = 2, relief = "sunken", font = "batang 8 bold", bg = "white", fg = "black")
    entr_tf_lee.place(x = 140, y = 287)
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

## Contois:
def contois():
    separ_simul(frame13)
    labels_saida(frame13)
    labels(frame = frame13, texto = "KSX (gs.gx\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 70)
    entr_simul_mimax_contois(frame13)
    entr_simul_ks_contois(frame13)
    entr_simul_kd_contois(frame13)
    entr_simul_yxs_contois(frame13)
    entr_simul_alfa_contois(frame13)
    entr_simul_beta_contois(frame13)
    entr_contois(frame13)
    Button(frame13, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 2, relief = "sunken", command = capt_val_esc_contois).place(x = 240, y = 282)  

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
    Button(frame14, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 2, relief = "sunken", command = capt_val_esc_monod).place(x = 240, y = 282)
   
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
    Button(frame15, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 2, relief = "sunken", command = capt_val_esc_moser).place(x = 240, y = 282)

## mi constante:
def mi_constante():
    separ_simul(frame42)
    labels_saida_mi_const(frame42)
    labels(frame = frame42, texto = u"\u03bc (h\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 14)
    labels(frame = frame42, texto = u"Kd (h\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 132)
    labels(frame = frame42, texto = u"Yxs (gx.gs\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 228, y = 132)
    labels(frame = frame42, texto = "Parâmetros Balanço Massa", fonte = "batang 8 bold", borda = "flat", x = 100, y = 117)
    labels(frame = frame42, texto = u"\u03B1(gp.gx\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 189)
    labels(frame = frame42, texto = u"\u03B2[gp.(gx.h)\u207b\u00b9]", fonte = "times 9 bold", borda = "sunken", x = 226, y = 189)
    labels(frame = frame42, texto = "Cs0:", fonte = "times 10 bold", borda = "flat", x = 108, y = 255)
    labels(frame = frame42, texto = "Cp0:", fonte = "times 10 bold", borda = "flat", x = 198, y = 255)
    entr_simul_mi_const(frame42)
    entr_simul_kd_mi_const(frame42)
    entr_simul_yxs_mi_const(frame42)
    entr_simul_alfa_mi_const(frame42)
    entr_simul_beta_mi_const(frame42)
    entr_mi_const(frame42)
    Button(frame42, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 2, relief = "sunken", command = capt_val_esc_mi_const).place(x = 240, y = 282)

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
    Button(frame16, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 2, relief = "sunken", command = capt_val_esc_andrews).place(x = 240, y = 282)
    
## Wu et al:
def wu():
    separ_simul(frame17)
    labels_saida(frame17)
    labels(frame = frame17, texto = "Ks (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 2, y = 70)
    labels(frame = frame17, texto = "KE (g.L\u207b\u00b9)", fonte = "times 9 bold", borda = "sunken", x = 242, y = 14)
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
    Button(frame17, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 2, relief = "sunken", command = capt_val_esc_wu).place(x = 240, y = 282)

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
    Button(frame18, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 2, relief = "sunken", command = capt_val_esc_aiba).place(x = 240, y = 282)

## Hoppe & Hansford:
def hoppe_hansford():
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
    Button(frame19, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 2, relief = "sunken", command = capt_val_esc_h_h).place(x = 240, y = 282)
    
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
    Button(frame20, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 2, relief = "sunken", command = capt_val_esc_levenspiel).place(x = 240, y = 282)

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
    Button(frame21, text = "Simular", font = "batang 8 bold", fg = "white", bg = "black", borderwidth = 2, relief = "sunken", command = capt_val_esc_lee).place(x = 240, y = 282)

def print_me_1():
        value_1 = combo_1.get()
        print(value_1)
        # Análise para criação de layout:   
        if value_1 == "AUSÊNCIA DE INIBIÇÃO":
            notebook_sem_inib_simul()
            contois()
            monod()
            moser()
            mi_constante()
            notebook_graf_simul()
        if value_1 == "INIBIÇÃO PELO SUBSTRATO":
            notebook_inib_subs_simul()
            andrews()
            wu()
        if value_1 == "INIBIÇÃO PELO PRODUTO":
            notebook_inib_prod_simul()
            aiba()
            hoppe_hansford()
            levenspiel()
        if value_1 == "INIBIÇÃO PELA BIOMASSA":
            notebook_inib_biomas_simul()
            lee()

#Button(frame1, text="Pronto", bg = "black", fg="white", font="batang 12", command = print_me_1).place(x = 315, y = 29)
    




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
    print(tf_bat)
    ## Vetores tempo e concentração:
    t_exp_bat = np.arange(excel_entrada_np[0,1], tf_bat, int_bat)
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                   
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
              
                    mi = mimaximo*(C[1]/(Ks + C[1]))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
        
                    mi = mimaximo*(C[1]/(Ks+C[1]))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
        
                    mi = mimaximo*(C[1]/(Ks+C[1]))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
              
                    mi = mimaximo*(C[1]/((KSX*C[0]) + C[1]))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
              
                    mi = mimaximo*(C[1]/((KSX*C[0]) + C[1]))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - Kd - D)*C[0]
                    dCsdt = D*(Cs0_corrent_alim_model_lin - C[1]) - ((mi*C[0])/Yxs)
                    dCpdt = D*(Cp0_exp_bat_alim - C[2]) + C[0]*(beta + alfa*mi)
                    return(dCxdt,dCsdt,dCpdt)
                return(func_args_alim_Contois_lin)
            func_args_alim_model = fun_args_contois_dois()
            
        # - Contois (vazão exponencial):
        if (cont_model == 1 and def_alim == "Taxa de Vazão Exponencial"):
            def fun_args_contois_tres():
                def func_args_alim_Contois_exp(C, t_exp_bat_alim, *args):
                    
        
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mi = mimaximo*(C[1]/((KSX*C[0]) + C[1]))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    u = args[6]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
             
                    mi = mimaximo*(((C[1])**u)/(Ks+((C[1])**u)))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    u = args[6]
        
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
             
                    mi = mimaximo*(((C[1])**u)/(Ks+((C[1])**u)))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    u = args[6]
        
    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mi = mimaximo*(((C[1])**u)/(Ks+((C[1])**u)))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    Kp = args[6]
        
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
             
                    mult_exp = -Kp*C[2]
                    mi = mimaximo*((C[1]/(Ks + C[1]))*np.exp(mult_exp))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    Kp = args[6]
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
             
                    mult_exp = -Kp*C[2]
                    mi = mimaximo*((C[1]/(Ks + C[1]))*np.exp(mult_exp))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    Kp = args[6]
    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mult_exp = -Kp*C[2]
                    mi = mimaximo*((C[1]/(Ks + C[1]))*np.exp(mult_exp))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    Kp = args[6]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
             
                    mi = mimaximo*(C[1]/(Ks + C[1]))*(Kp/(Kp + C[2]))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    Kp = args[6]
         
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
             
                    mi = mimaximo*(C[1]/(Ks + C[1]))*(Kp/(Kp + C[2]))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    Kp = args[6]
    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mi = mimaximo*(C[1]/(Ks + C[1]))*(Kp/(Kp + C[2]))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    n = args[6]
                    Cp_estr = args[7]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
             
                    mi = mimaximo*((C[1]/(Ks+C[1]))*((abs(1-(C[2]/Cp_estr)))**n))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    n = args[6]
                    Cp_estr = args[7]
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
             
                    mi = mimaximo*((C[1]/(Ks+C[1]))*((abs(1-(C[2]/Cp_estr)))**n))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    n = args[6]
                    Cp_estr = args[7]
        
    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mi = mimaximo*((C[1]/(Ks+C[1]))*((abs(1-(C[2]/Cp_estr)))**n))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    KIS = args[6]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
             
                    mi = mimaximo*(C[1]/(Ks + C[1] + ((C[1]**2)/KIS)))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    KIS = args[6]
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
             
                    mi = mimaximo*(C[1]/(Ks + C[1] + ((C[1]**2)/KIS)))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    KIS = args[6]
    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mi = mimaximo*(C[1]/(Ks + C[1] + ((C[1]**2)/KIS)))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    KE = args[6]
                    v = args[7]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
             
                    mi = mimaximo * (C[1]/(Ks + C[1] + C[1]*((C[1]/KE)**v)))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    KE = args[6]
                    v = args[7]
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
             
                    mi = mimaximo * (C[1]/(Ks + C[1] + C[1]*((C[1]/KE)**v)))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    KE = args[6]
                    v = args[7]
    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mi = mimaximo * (C[1]/(Ks + C[1] + C[1]*((C[1]/KE)**v)))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    m = args[6]
                    Cx_estr = args[7]
        
                    Q_model_const = Q
                    V0_model_const = V0
                    Cs0_corrent_alim_model_const = Cs0_corrent_alim
             
                    mi = mimaximo*((C[1]/(Ks+C[1]))*((abs(1-(C[0]/Cx_estr)))**m))
                    D = Q_model_const/(V0_model_const + Q_model_const*t_exp_bat_alim)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    m = args[6]
                    Cx_estr = args[7]
        
                    Q0_model_lin = Q0
                    V0_model_lin = V0
                    Cs0_corrent_alim_model_lin = Cs0_corrent_alim
                    a_model = a
             
                    mi = mimaximo*((C[1]/(Ks+C[1]))*((abs(1-(C[0]/Cx_estr)))**m))
                    D = (Q0_model_lin*(1+a_model*t_exp_bat_alim))/((Q0_model_lin*(t_exp_bat_alim+(a_model*t_exp_bat_alim**2)))+V0_model_lin)
                    dCxdt = (mi - Kd - D)*C[0]
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
                    Kd = args[2]
                    Yxs = args[3]
                    alfa = args[4]
                    beta = args[5]
                    m = args[6]
                    Cx_estr = args[7]
    
                    Q0_model_exp = Q0
                    V0_model_exp = V0
                    Cs0_corrent_alim_model_exp = Cs0_corrent_alim
                    beta_model_exp = beta_exp
              
                    mi = mimaximo*((C[1]/(Ks+C[1]))*((abs(1-(C[0]/Cx_estr)))**m))
                    multiplicacao = beta_model_exp*t_exp_bat_alim
                    exponencial = np.exp(multiplicacao)
                    D = (Q0_model_exp*np.exp(beta_model_exp*t_exp_bat_alim))/(((Q0_model_exp/beta_model_exp)*(exponencial - 1)) + V0_model_exp)
                    dCxdt = (mi - Kd - D)*C[0]
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
        # Definição saída dos valores modelados na interface:
        Label(frame2, bg = "grey75", height = 1, width = 41).place(x = 960, y = 258)
        Label(frame2, bg = "grey75", height = 1, width = 41).place(x = 960, y = 417)
        if (cont_model == 0 or cont_model == 1):
            Label(frame2, text = param_otim_alm_alim[0], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 943, y = 255)
            Label(frame2, text = param_otim_alm_alim[1], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1021, y = 255)
        if (cont_model == 9):
                Label(frame2, text = param_otim_alm_alim[0], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 943, y = 255)
        else:
            if (cont_model >=2 and cont_model <=5):
                Label(frame2, text = param_otim_alm_alim[0], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 943, y = 255)
                Label(frame2, text = param_otim_alm_alim[1], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1021, y = 255)
                Label(frame2, text = param_otim_alm_alim[6], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1099, y = 255)
            if (cont_model > 5):
                Label(frame2, text = param_otim_alm_alim[0], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 943, y = 255)
                Label(frame2, text = param_otim_alm_alim[1], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1021, y = 255)
                Label(frame2, text = param_otim_alm_alim[6], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1099, y = 255)
                Label(frame2, text = param_otim_alm_alim[7], font = "batang 11", justify = "center", fg = "black", bg = "grey75").place(x = 1163, y = 255)       
        if (cont_model == 9):
            Label(frame2, text = param_otim_alm_alim[1] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 934, y = 417)
            Label(frame2, text = param_otim_alm_alim[2] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1000, y = 417)
            Label(frame2, text = param_otim_alm_alim[3] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1090, y = 417)
            Label(frame2, text = param_otim_alm_alim[4] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1170, y = 417)
        else:
            Label(frame2, text = param_otim_alm_alim[2] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 934, y = 417)
            Label(frame2, text = param_otim_alm_alim[3] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1000, y = 417)
            Label(frame2, text = param_otim_alm_alim[4] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1090, y = 417)
            Label(frame2, text = param_otim_alm_alim[5] , font = "batang 11", fg = "black", bg = "grey75", justify = "center").place(x = 1170, y = 417)
        
        # Condições para marcação dos valores inadequados modelados:
        cond_mimax_mi =  param_otim_alm_alim[0] > 0.9 
        ## situação não observada para Kd (cont_model = 9), portanto, não resultará em problemas:
        cond_Ks = param_otim_alm_alim[1] >= C_exp[0,1] or param_otim_alm_alim[1] == 0 
        if (cont_model != 9):
            cond_yxs = param_otim_alm_alim[3] >= C_exp[0,1]
            cond_mi_kd = param_otim_alm_alim[2] > param_otim_alm_alim[0]
        else:
            cond_yxs = param_otim_alm_alim[2] >= C_exp[0,1]
            cond_mi_kd = param_otim_alm_alim[1] > param_otim_alm_alim[0]
        # Checagem parâmetros negativos:
        cond_param_neg = False
        for i in range (len(param_otim_alm_alim)):
            if param_otim_alm_alim[i] < 0:
                cond_param_neg = True   
                
        if (cond_mimax_mi or cond_Ks or cond_mi_kd or cond_param_neg == True):
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
                    if (cond_mimax_mi):
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
                    if (cont_model != 9):
                        if (cond_mi_kd):
                            Label(frame2, text = param_otim_alm_alim[2] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 934, y = 417)
                    else:
                        if (cond_mi_kd):
                            Label(frame2, text = param_otim_alm_alim[1] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 934, y = 417)
                    if (cond_param_neg == True):
                        if (param_otim_alm_alim[0] <= 0): #mimaximo, mi
                            Label(frame2, text = param_otim_alm_alim[0], font = "batang 11", justify = "center", fg = "red4", bg = "grey75").place(x = 943, y = 255)
                        if (cont_model != 9):
                            if (param_otim_alm_alim[1] <= 0): #Ks
                                Label(frame2, text = param_otim_alm_alim[1], font = "batang 11", justify = "center", fg = "red4", bg = "grey75").place(x = 1021, y = 255)
                        if (cont_model != 9):
                            if (param_otim_alm_alim[2] < 0 or cond_mi_kd or param_otim_alm_alim[2] == -0.0): #Kd
                                Label(frame2, text = param_otim_alm_alim[2] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 934, y = 417)
                        else:
                            if param_otim_alm_alim[1] < 0 or cond_mi_kd or param_otim_alm_alim[1] == -0.0: #Kd
                                Label(frame2, text = param_otim_alm_alim[1] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 934, y = 417)
                        if (cont_model != 9):
                            if (param_otim_alm_alim[3] <= 0 or cond_yxs): #Yxs
                                Label(frame2, text = param_otim_alm_alim[3] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 1000, y = 417)
                        else: 
                            if (param_otim_alm_alim[2] <= 0 or cond_yxs): #Yxs
                                Label(frame2, text = param_otim_alm_alim[2] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 1000, y = 417)
                        if (cont_model != 9):
                            if (param_otim_alm_alim[4] <= 0): #alfa
                                Label(frame2, text = param_otim_alm_alim[4] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 1090, y = 417)
                        else:
                            if (param_otim_alm_alim[2] <= 0): #alfa
                                Label(frame2, text = param_otim_alm_alim[2] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 1090, y = 417)
                        if (cont_model != 9):
                            if (param_otim_alm_alim[5] < 0): #beta
                                Label(frame2, text = param_otim_alm_alim[5] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 1170, y = 417)
                        else:
                            if (param_otim_alm_alim[4] < 0): #beta
                                Label(frame2, text = param_otim_alm_alim[4] , font = "batang 11", fg = "red4", bg = "grey75", justify = "center").place(x = 1170, y = 417)
                        if (cont_model == 2):
                            if (param_otim_alm_alim[6] > 55):
                                Label(frame2, text = param_otim_alm_alim[6], font = "batang 11", justify = "center", fg = "red4", bg = "gre75y").place(x = 1099, y = 255)
                        if (cont_model >= 3 and cont_model <=5) :
                            if (param_otim_alm_alim[6] <= 0 or param_otim_alm_alim[6] > 10):
                                Label(frame2, text = param_otim_alm_alim[6], font = "batang 11", justify = "center", fg = "red4", bg = "grey75").place(x = 1099, y = 255)
                        if (cont_model >= 6 and cont_model <=8):
                            if (param_otim_alm_alim[6] <= 0):
                                Label(frame2, text = param_otim_alm_alim[6], font = "batang 11", justify = "center", fg = "red4", bg = "grey75").place(x = 1142, y = 255)
                            if (param_otim_alm_alim[7] <= 0):
                                Label(frame2, text = param_otim_alm_alim[7], font = "batang 11", justify = "center", fg = "red4", bg = "grey75").place(x = 1163, y = 255)
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
                    Label(janela_interna, text = ICpar_alim[2], font = "batang 11", fg = "black").place(x = 32, y = 90)
                    Label(janela_interna, text = ICpar_alim[3], font = "batang 11", fg = "black").place(x = 113, y = 90)
                    Label(janela_interna, text = ICpar_alim[4], font = "batang 11", fg = "black").place(x = 207, y = 90)
                    Label(janela_interna, text = ICpar_alim[5], font = "batang 11", fg = "black").place(x = 300, y = 90)
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
                    Label(janela_interna, text = ICpar_alim[6], font = "batang 11", fg = "black").place(x = 270, y = 90)
                if (cont_model >5 and cont_model <=8): # - Wu (7p), Levenspiel (7p), Lee (7p)
                    if (cont_model == 6): # Wu
                        Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)     Ks(±g.L\u207b\u00b9)     KE(±g.L\u207b\u00b9)     v(±adim)", font = "arial 10 bold", fg = "black", width = 42).place(x = 29, y = 67)
                    if (cont_model == 7): # Levenspiel
                        Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)    Ks(±g.L\u207b\u00b9)     n(±adim)     Cp*(±g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", width = 42).place(x = 29, y = 67)
                    if (cont_model ==8): # Lee
                        Label(janela_interna, text = u"\u03bcmáx(±h\u207b\u00b9)    Ks(±g.L\u207b\u00b9)     Cx*(±g.L\u207b\u00b9)     m(±adim)", font = "arial 10 bold", fg = "black", width = 42).place(x = 29, y = 67)
                    Label(janela_interna, text = ICpar_alim[0], font = "batang 11",  fg = "black").place(x = 52, y = 90)
                    Label(janela_interna, text = ICpar_alim[1], font = "batang 11",  fg = "black").place(x = 143, y = 90)
                    Label(janela_interna, text = ICpar_alim[6], font = "batang 11", fg = "black").place(x = 226, y = 90)
                    Label(janela_interna, text = ICpar_alim[7], font = "batang 11",  fg = "black").place(x = 304, y = 90)        
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
        print(soma_SQres_SQtot_val)
        SQres = soma_SQres_SQtot_val[11] + soma_SQres_SQtot_val[12] + soma_SQres_SQtot_val[13]
        SQtotal = soma_SQres_SQtot_val[14] + soma_SQres_SQtot_val[15] + soma_SQres_SQtot_val[16]
        df_soma_SQres_SQtot = pd.DataFrame({'SQres':[SQres], 'SQtot':[SQtotal]})
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
            res_final = res_final/6
        else:
            if (cont_model == 1):
                res_final = res_final/6
            else:
                if (cont_model == 2):
                    res_final = res_final/7
                else:
                    if (cont_model == 3):
                        res_final = res_final/7
                    else:
                        if (cont_model == 4):
                            res_final = res_final/7
                        else:
                            if (cont_model == 5):
                                res_final = res_final/7   
                            else:
                                if (cont_model == 9):
                                    res_final = res_final/5
                                else:
                                    res_final = res_final/8
                                    
            
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
            df_SQtotal_Produtiv = pd.DataFrame ({'Pxexp_med(gx/t)': Px_med, 'Ppexp_med(gp/t)': Pp_med})
            df_saida_compar['DQtot_Px'] = (df_produtiv_exp['Px_exp(gx/t)'] - df_SQtotal_Produtiv['Pxexp_med(gx/t)']) ** 2
            df_saida_compar['DQtot_Pp'] = (df_produtiv_exp['Pp_exp(gp/t)'] - df_SQtotal_Produtiv['Ppexp_med(gp/t)']) ** 2
        
            ### Soma SQres e QStot: 
            soma_SQres_SQtot = df_saida_compar.sum(axis=0) #pegar 8,9,10 e 11
            soma_SQres_SQtot_val = pd.Series(soma_SQres_SQtot).values
            SQres = soma_SQres_SQtot_val[8] + soma_SQres_SQtot_val[9] 
            SQtotal = soma_SQres_SQtot_val[10] + soma_SQres_SQtot_val[11] 
            df_soma_SQres_SQtot = pd.DataFrame({'SQres':[SQres], 'SQtot':[SQtotal]})
            
            ### Cálculo do R²:
            r2_Px_Pp = 1 - (SQres/SQtotal)
            r2_Px_Pp = round(r2_Px_Pp, 4)
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
            # - Batelada e Batelada Alimentada:
            # Cálculo do coeficiente de regressão: 
            df_prod_espec = pd.DataFrame({'Tempo(h)': Ttotal, 'Ppx(gp/gx)': Ppx})
            df_prod_espec_exp = pd.DataFrame({'Tempo_exp(h)': Ttotal_exp,'Ppx_exp(gp/gx)': Ppx_exp})
            df_teste = pd.DataFrame({'Tempo(h)': Ttotal})
            df_teste_prod_espec = pd.DataFrame({'Ppx(gp/gx)': Ppx})
            df_teste_exp = pd.DataFrame({'Tempo_exp(h)': Ttotal_exp})
            df_teste_exp_prod_espec = pd.DataFrame({'Ppx_exp(gp/gx)': Ppx_exp})

            # Teste: qual tempo tem o menor intervalo de divisão temporal
            control_compar = len(Ttotal)
        
            ## Laço para comparação de tempos iguais (experimental e modelo) 
            i_compar_exp = 0
            i_compar_model = 0
            temp_model=[]
            temp_exp=[]
            prod_espec_model = []
            prod_espec_exp = []
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
                    debitado_model = df_teste_prod_espec.loc[i_compar_model]
                    debitado_model = pd.Series(debitado_model).values
                    debitado_exp = df_teste_exp_prod_espec.loc[i_compar_exp]
                    debitado_exp = pd.Series(debitado_exp).values
                    df_prod_espec_model = pd.DataFrame({'Ppx(gp/gx)':[debitado_model[0]]})
                    prod_espec_model.append(df_prod_espec_model)
                    df_prod_espec_exp = pd.DataFrame({'Ppx_exp(gp/gx)':[debitado_exp[0]]})
                    prod_espec_exp.append(df_prod_espec_exp)
                    i_compar_model =  1 + i_compar_model
                    i_compar_exp =  1 + i_compar_exp  
            ### DataFrames de saída, desconsiderando os indexes - resultam em erros:
            df_prod_espec_model = pd.concat(prod_espec_model)
            df_prod_espec_exp = pd.concat(prod_espec_exp)
            df_prod_espec_model.reset_index(drop=True, inplace=True)
            df_prod_espec_exp.reset_index(drop=True, inplace=True)
        
            ### Cálculo do coeficiente de regressão:
            med_prod_espec = df_prod_espec_exp.mean(axis=0)
            med_prod_espec_val = pd.Series(med_prod_espec).values
            df_med_prod_espec = pd.DataFrame({'Ppxexp_med(gp/gx)':[med_prod_espec_val[0]]})
            df_saida_compar = pd.concat ([df_temp_exp,df_prod_espec_exp, df_temp_model, df_prod_espec_model,df_med_prod_espec], axis=1)
        
            ### Determinação da soma do quadrado do resíduo:
            df_saida_compar['DQres_Ppx'] = (df_prod_espec_exp['Ppx_exp(gp/gx)'] - df_prod_espec_model['Ppx(gp/gx)']) ** 2
    
            ### Determinação da soma do quadrado do resíduo:
            Ppx_med = np.repeat(med_prod_espec_val[0],len(temp_exp))
            df_SQtotal_prod_espec = pd.DataFrame ({'Ppxexp_med(gp/gx)': Ppx_med})
            df_saida_compar['DQtot_Ppx'] = (df_prod_espec_exp['Ppx_exp(gp/gx)'] - df_SQtotal_prod_espec['Ppxexp_med(gp/gx)']) ** 2
        
            ### Soma SQres e QStot: 
            soma_SQres_SQtot = df_saida_compar.sum(axis=0) #pegar 5 e 6
            soma_SQres_SQtot_val = pd.Series(soma_SQres_SQtot).values
            print(soma_SQres_SQtot_val)
            SQres = soma_SQres_SQtot_val[5] 
            SQtotal = soma_SQres_SQtot_val[6] 
            df_soma_SQres_SQtot = pd.DataFrame({'SQres':[SQres], 'SQtot':[SQtotal]})
            
            ### Cálculo do R²:
            r2_Ppx = 1 - (SQres/SQtotal)
            r2_Ppx = round(r2_Ppx, 4)
            Label(frame2, text = r2_Ppx, font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            print(r2_Ppx)
            
        #### **** Impressão do valor do R² concentração na interface **** ####:
        ## Botão para acesso:
        Button(frame40, text = "R²", font = "batang 12 bold", fg = "black", bg = "grey70", command = r2_Ppx).place(x = 452, y = 45)
        
## ** \\ ______________________________________________GRÁFICO - PRODUTIVIDADE ESPECÍFICA_______________________________________ \\ ** ## 
       

## ** // ___________________________________________GRÁFICO - TAXA ESPECÍFICA DE CRESCIMENTO____________________________________ // ** ##                   

        ### ** CÁLCULO DA VELOCIDADE DE CRESCIMENTO MICROBIANO:
        # -- Experimental e modelada:
        if (cont_model == 0): # - Monod
            global mi_exp, mi
            mi_exp = param_otim_alm_alim[0]*(Cs_exp/(param_otim_alm_alim[1] + Cs_exp))
            mi = param_otim_alm_alim[0]*(Cs/(param_otim_alm_alim[1] + Cs))
        if (cont_model == 1): # - Contois 
            mi_exp = param_otim_alm_alim[0]*(Cs_exp/(param_otim_alm_alim[1] * Cx_exp + Cs_exp))
            mi = param_otim_alm_alim[0]*(Cs/(param_otim_alm_alim[1] * Cx + Cs))
        if (cont_model == 2): # - Andrews
            mi_exp = param_otim_alm_alim[0]*(Cs_exp/(param_otim_alm_alim[1] + Cs_exp + ((Cs_exp**2)/param_otim_alm_alim[6])))
            mi = param_otim_alm_alim[0]*(Cs/(param_otim_alm_alim[1] + Cs + ((Cs**2)/param_otim_alm_alim[6])))
        if (cont_model == 3): # Aiba
            mult_exp = -param_otim_alm_alim[6]*Cp_exp
            mi_exp = param_otim_alm_alim[0]*((Cs_exp/(param_otim_alm_alim[1] + Cs_exp))*np.exp(mult_exp))
            mult = -param_otim_alm_alim[6]*Cp
            mi = param_otim_alm_alim[0]*((Cs/(param_otim_alm_alim[1] + Cs))*np.exp(mult))
        if (cont_model == 4): # - Moser
            mi_exp = param_otim_alm_alim[0]*((Cs_exp**param_otim_alm_alim[6])/(param_otim_alm_alim[1] + (Cs_exp**param_otim_alm_alim[6])))
            mi = param_otim_alm_alim[0]*((Cs**param_otim_alm_alim[6])/(param_otim_alm_alim[1] + (Cs**param_otim_alm_alim[6])))
        if (cont_model == 5): # - Hoppe & Hansford
            mi_exp = param_otim_alm_alim[0]*(Cs_exp/(param_otim_alm_alim[1] + Cs_exp))*(param_otim_alm_alim[6]/(param_otim_alm_alim[6] + Cp_exp))
            mi = param_otim_alm_alim[0]*(Cs/(param_otim_alm_alim[1] + Cs))*(param_otim_alm_alim[6]/(param_otim_alm_alim[6] + Cp))
        if (cont_model == 6): # - Wu
            mi_exp = param_otim_alm_alim[0]*(Cs_exp/(param_otim_alm_alim[1] + Cs_exp + (Cs_exp*((Cs_exp/param_otim_alm_alim[6])**param_otim_alm_alim[7]))))
            mi = param_otim_alm_alim[0]*(Cs/(param_otim_alm_alim[1] + Cs + (Cs*((Cs/param_otim_alm_alim[6])**param_otim_alm_alim[7]))))
        if (cont_model == 7): # - Levenspiel
            mi_exp = param_otim_alm_alim[0]*((Cs_exp/(param_otim_alm_alim[1] + Cs_exp))*((1-(Cp_exp/param_otim_alm_alim[7]))**param_otim_alm_alim[6]))
            mi = param_otim_alm_alim[0]*((Cs/(param_otim_alm_alim[1] + Cs))*((1-(Cp/param_otim_alm_alim[7]))**param_otim_alm_alim[6]))
        if (cont_model == 8): # - Lee
            mi_exp = param_otim_alm_alim[0]*((Cs_exp/(param_otim_alm_alim[1] + Cs_exp))*((1-(Cx_exp/param_otim_alm_alim[7]))**param_otim_alm_alim[6]))
            mi = param_otim_alm_alim[0]*((Cs/(param_otim_alm_alim[1] + Cs))*((1-(Cx/param_otim_alm_alim[7]))**param_otim_alm_alim[6]))
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
        
        print("problema", mi_exp)
        mi_exp_r2 = mi_exp
        mi_r2 = mi
        ### ** CÁLCULO DO COEFICIENTE DE REGRESSÃO - TAXA ESPECÍFICA DE CRESCIMENTO MICROBIANO ** ###:
        def r2_mi():
            # - Batelada e Batelada Alimentada:
            # Cálculo do coeficiente de regressão: 
            df_mi_exp = pd.DataFrame({'Tempo_exp(h)': Ttotal_exp,'mi_exp(1/t)': mi_exp_r2})
            df_teste = pd.DataFrame({'Tempo(h)': Ttotal})
            df_teste_mi = pd.DataFrame({'mi(1/t)': mi_r2})
            df_teste_exp = pd.DataFrame({'Tempo_exp(h)': Ttotal_exp})
            df_teste_exp_mi = pd.DataFrame({'mi_exp(1/t)': mi_exp_r2})

            # Teste: qual tempo tem o menor intervalo de divisão temporal
            control_compar = len(Ttotal)
        
            ## Laço para comparação de tempos iguais (experimental e modelo) 
            i_compar_exp = 0
            i_compar_model = 0
            temp_model=[]
            temp_exp=[]
            mi_model = []
            mi_exp = []
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
                    debitado_model = df_teste_mi.loc[i_compar_model]
                    debitado_model = pd.Series(debitado_model).values
                    debitado_exp = df_teste_exp_mi.loc[i_compar_exp]
                    debitado_exp = pd.Series(debitado_exp).values
                    df_mi_model = pd.DataFrame({'mi(1/t)':[debitado_model[0]]})
                    mi_model.append(df_mi_model)
                    df_mi_exp = pd.DataFrame({'mi_exp(1/t)':[debitado_exp[0]]})
                    mi_exp.append(df_mi_exp)
                    i_compar_model =  1 + i_compar_model
                    i_compar_exp =  1 + i_compar_exp  
            ### DataFrames de saída, desconsiderando os indexes - resultam em erros:
            df_mi_model = pd.concat(mi_model)
            df_mi_exp = pd.concat(mi_exp)
            df_mi_model.reset_index(drop=True, inplace=True)
            df_mi_exp.reset_index(drop=True, inplace=True)
        
            ### Cálculo do coeficiente de regressão:
            med_mi = df_mi_exp.mean(axis=0)
            med_mi_val = pd.Series(med_mi).values
            df_med_mi = pd.DataFrame({'miexp_med(1/t)':[med_mi_val[0]]})
            df_saida_compar = pd.concat ([df_temp_exp,df_mi_exp, df_temp_model, df_mi_model,df_med_mi], axis=1)
        
            ### Determinação da soma do quadrado do resíduo:
            df_saida_compar['DQres_mi'] = (df_mi_exp['mi_exp(1/t)'] - df_mi_model['mi(1/t)']) ** 2
    
            ### Determinação da soma do quadrado do resíduo:
            Ppx_med = np.repeat(med_mi_val[0],len(temp_exp))
            df_SQtotal_mi = pd.DataFrame ({'miexp_med(1/t)': Ppx_med})
            df_saida_compar['DQtot_mi'] = (df_mi_exp['mi_exp(1/t)'] - df_SQtotal_mi['miexp_med(1/t)']) ** 2
        
            ### Soma SQres e QStot: 
            soma_SQres_SQtot = df_saida_compar.sum(axis=0) #pegar 5 e 6
            soma_SQres_SQtot_val = pd.Series(soma_SQres_SQtot).values
            SQres = soma_SQres_SQtot_val[5] 
            SQtotal = soma_SQres_SQtot_val[6] 
            df_soma_SQres_SQtot = pd.DataFrame({'SQres':[SQres], 'SQtot':[SQtotal]})
            
            ### Cálculo do R²:
            r2_mi = 1 - (SQres/SQtotal)
            r2_mi = round(r2_mi, 4)
            Label(frame2, text = r2_mi, font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            print(r2_mi)
                
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
             # - Batelada e Batelada Alimentada:
            # Cálculo do coeficiente de regressão: 
            df_vol = pd.DataFrame({'Tempo(h)': t_alim, 'vol(L)': V_calc})
            df_vol_exp = pd.DataFrame({'Tempo_exp(h)': t_exp_bat_alim,'vol_exp(L)': V_calc_exp})
            df_teste = pd.DataFrame({'Tempo(h)': t_alim})
            df_teste_vol = pd.DataFrame({'vol(L)': V_calc})
            df_teste_exp = pd.DataFrame({'Tempo_exp(h)': t_exp_bat_alim})
            df_teste_exp_vol = pd.DataFrame({'vol_exp(L)': V_calc_exp})

            # Teste: qual tempo tem o menor intervalo de divisão temporal
            control_compar = len(t_alim)
        
            ## Laço para comparação de tempos iguais (experimental e modelo) 
            i_compar_exp = 0
            i_compar_model = 0
            temp_model=[]
            temp_exp=[]
            vol_model = []
            vol_exp = []
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
                    debitado_model = df_teste_vol.loc[i_compar_model]
                    debitado_model = pd.Series(debitado_model).values
                    debitado_exp = df_teste_exp_vol.loc[i_compar_exp]
                    debitado_exp = pd.Series(debitado_exp).values
                    df_vol_model = pd.DataFrame({'vol(L)':[debitado_model[0]]})
                    vol_model.append(df_vol_model)
                    df_vol_exp = pd.DataFrame({'vol_exp(L)':[debitado_exp[0]]})
                    vol_exp.append(df_vol_exp)
                    i_compar_model =  1 + i_compar_model
                    i_compar_exp =  1 + i_compar_exp  
            ### DataFrames de saída, desconsiderando os indexes - resultam em erros:
            df_vol_model = pd.concat(vol_model)
            df_vol_exp = pd.concat(vol_exp)
            df_vol_model.reset_index(drop=True, inplace=True)
            df_vol_exp.reset_index(drop=True, inplace=True)
        
            ### Cálculo do coeficiente de regressão:
            med_vol = df_vol_exp.mean(axis=0)
            med_vol_val = pd.Series(med_vol).values
            df_med_vol = pd.DataFrame({'volexp_med(L)':[med_vol_val[0]]})
            df_saida_compar = pd.concat ([df_temp_exp,df_vol_exp, df_temp_model, df_vol_model,df_med_vol], axis=1)
        
            ### Determinação da soma do quadrado do resíduo:
            df_saida_compar['DQres_vol'] = (df_vol_exp['vol_exp(L)'] - df_vol_model['vol(L)']) ** 2
    
            ### Determinação da soma do quadrado do resíduo:
            vol_med = np.repeat(med_vol_val[0],len(temp_exp))
            df_SQtotal_vol = pd.DataFrame ({'volexp_med(L)': vol_med})
            df_saida_compar['DQtot_vol'] = (df_vol_exp['vol_exp(L)'] - df_SQtotal_vol['volexp_med(L)']) ** 2
        
            ### Soma SQres e QStot: 
            soma_SQres_SQtot = df_saida_compar.sum(axis=0) #pegar 5 e 6
            soma_SQres_SQtot_val = pd.Series(soma_SQres_SQtot).values
            SQres = soma_SQres_SQtot_val[5] 
            SQtotal = soma_SQres_SQtot_val[6] 
            df_soma_SQres_SQtot = pd.DataFrame({'SQres':[SQres], 'SQtot':[SQtotal]})
            
            ### Cálculo do R²:
            r2_vol = 1 - (SQres/SQtotal)
            r2_vol = round(r2_vol, 4)
            Label(frame2, text = r2_vol, font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            print(r2_vol)
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
            # - Batelada e Batelada Alimentada:
            # Cálculo do coeficiente de regressão: 
            df_vaz = pd.DataFrame({'Tempo(h)': t_alim, 'vaz(L/h)': Q_calc})
            df_vaz_exp = pd.DataFrame({'Tempo_exp(h)': t_exp_bat_alim,'vaz_exp(L/h)': Q_calc_exp})
            df_teste = pd.DataFrame({'Tempo(h)': t_alim})
            df_teste_vaz = pd.DataFrame({'vaz(L/h)': Q_calc})
            df_teste_exp = pd.DataFrame({'Tempo_exp(h)': t_exp_bat_alim})
            df_teste_exp_vaz = pd.DataFrame({'vaz_exp(L/h)': Q_calc_exp})

            # Teste: qual tempo tem o menor intervalo de divisão temporal
            control_compar = len(t_alim)
        
            ## Laço para comparação de tempos iguais (experimental e modelo) 
            i_compar_exp = 0
            i_compar_model = 0
            temp_model=[]
            temp_exp=[]
            vaz_model = []
            vaz_exp = []
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
                    debitado_model = df_teste_vaz.loc[i_compar_model]
                    debitado_model = pd.Series(debitado_model).values
                    debitado_exp = df_teste_exp_vaz.loc[i_compar_exp]
                    debitado_exp = pd.Series(debitado_exp).values
                    df_vaz_model = pd.DataFrame({'vaz(L/h)':[debitado_model[0]]})
                    vaz_model.append(df_vaz_model)
                    df_vaz_exp = pd.DataFrame({'vaz_exp(L/h)':[debitado_exp[0]]})
                    vaz_exp.append(df_vaz_exp)
                    i_compar_model =  1 + i_compar_model
                    i_compar_exp =  1 + i_compar_exp  
            ### DataFrames de saída, desconsiderando os indexes - resultam em erros:
            df_vaz_model = pd.concat(vaz_model)
            df_vaz_exp = pd.concat(vaz_exp)
            df_vaz_model.reset_index(drop=True, inplace=True)
            df_vaz_exp.reset_index(drop=True, inplace=True)
        
            ### Cálculo do coeficiente de regressão:
            med_vaz = df_vaz_exp.mean(axis=0)
            med_vaz_val = pd.Series(med_vaz).values
            df_med_vaz = pd.DataFrame({'vazexp_med(L/h)':[med_vaz_val[0]]})
            df_saida_compar = pd.concat ([df_temp_exp,df_vaz_exp, df_temp_model, df_vaz_model,df_med_vaz], axis=1)
        
            ### Determinação da soma do quadrado do resíduo:
            df_saida_compar['DQres_vaz'] = (df_vaz_exp['vaz_exp(L/h)'] - df_vaz_model['vaz(L/h)']) ** 2
    
            ### Determinação da soma do quadrado do resíduo:
            vaz_med = np.repeat(med_vaz_val[0],len(temp_exp))
            df_SQtotal_vaz = pd.DataFrame ({'vazexp_med(L/h)': vaz_med})
            df_saida_compar['DQtot_vaz'] = (df_vaz_exp['vaz_exp(L/h)'] - df_SQtotal_vaz['vazexp_med(L/h)']) ** 2
        
            ### Soma SQres e QStot: 
            soma_SQres_SQtot = df_saida_compar.sum(axis=0) #pegar 5 e 6
            soma_SQres_SQtot_val = pd.Series(soma_SQres_SQtot).values
            SQres = soma_SQres_SQtot_val[5] 
            SQtotal = soma_SQres_SQtot_val[6] 
            df_soma_SQres_SQtot = pd.DataFrame({'SQres':[SQres], 'SQtot':[SQtotal]})
            
            ### Cálculo do R²:
            r2_vaz = 1 - (SQres/SQtotal)
            r2_vaz = round(r2_vaz, 4)
            Label(frame2, text = r2_vaz, font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1168, y = 329.2)
            print(r2_vaz)
        
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
        def excel_param():
            const_sat_list = ['Ks(g/L)', 'KSX(g/L)', 'IC Ks(g/L)', 'IC KSX(g/L)']
            def excel_param_defin(const_sat, const_sat_ic):
                global df_params_model_bat, df_params_IC_bat, df_params_model_alim, df_params_IC_alim
                # - Batelada:
                df_params_model_bat =pd.DataFrame({'mimax(h-¹)':[param_otim_alm_bat[0]],const_sat :[param_otim_alm_bat[1]],'Kd(1/h)':[param_otim_alm_bat[2]],'Yxs(gcél/gsub)':[param_otim_alm_bat[3]], 'alfa(gprod/gcél)': [param_otim_alm_bat[4]], 'beta(gprod/gcél.h)':[param_otim_alm_bat[5]]})
                df_params_IC_bat = pd.DataFrame({'IC mimax(h-¹)':[ICpar_bat[0]],const_sat_ic:[ICpar_bat[1]],'IC Kd(1/h)':[ICpar_bat[2]],'IC Yxs(gcél/gsub)':[ICpar_bat[3]], 'IC alfa(gprod/gcél)': [ICpar_bat[4]], 'IC beta(gprod/gcél.h)':[ICpar_bat[5]]})
                # - Batelada alimentada:
                df_params_model_alim =pd.DataFrame({'mimax(h-¹)':[param_otim_alm_alim[0]],const_sat:[param_otim_alm_alim[1]],'Kd(1/h)':[param_otim_alm_alim[2]],'Yxs(gcél/gsub)':[param_otim_alm_alim[3]], 'alfa(gprod/gcél)': [param_otim_alm_alim[4]], 'beta(gprod/gcél.h)':[param_otim_alm_alim[5]]})
                df_params_IC_alim = pd.DataFrame({'IC mimax(h-¹)':[ICpar_alim[0]],const_sat_ic:[ICpar_alim[1]],'IC Kd(1/h)':[ICpar_alim[2]],'IC Yxs(gcél/gsub)':[ICpar_alim[3]], 'IC alfa(gprod/gcél)': [ICpar_alim[4]], 'IC beta(gprod/gcél.h)':[ICpar_alim[5]]})
                return(df_params_model_bat, df_params_IC_bat, df_params_model_alim, df_params_IC_alim)
            if (cont_model == 0): # Monod (6p)
                # - Batelada e Batelada Alimentada:
                df_params_model_bat = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[0]
                df_params_IC_bat = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[1]
                df_params_model_alim = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[2]
                df_params_IC_alim = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[3]
            if (cont_model == 1): # Contois (6p)
                # - Batelada e Batelada Alimentada:
                df_params_model_bat = excel_param_defin(const_sat = const_sat_list[1], const_sat_ic = const_sat_list[3])[0]
                df_params_IC_bat = excel_param_defin(const_sat = const_sat_list[1], const_sat_ic = const_sat_list[3])[1]
                df_params_model_alim = excel_param_defin(const_sat = const_sat_list[1], const_sat_ic = const_sat_list[3])[2]
                df_params_IC_alim = excel_param_defin(const_sat = const_sat_list[1], const_sat_ic = const_sat_list[3])[3]
            if (cont_model == 4): # Moser (6p)
                # - Batelada:
                df_params_model_bat_u = pd.DataFrame({'u(adim)':[param_otim_alm_bat[6]]})
                df_params_IC_bat_u = pd.DataFrame({'IC u(adim)':[ICpar_bat[6]]})
                df_params_model_bat_moser = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[0]
                df_params_IC_bat_moser = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[1]
                df_params_model_bat = pd.concat([df_params_model_bat_moser, df_params_model_bat_u], axis = 1)
                df_params_IC_bat = pd.concat([df_params_IC_bat_moser, df_params_IC_bat_u], axis = 1)
                # - Batelada alimentada:
                df_params_model_alim_u = pd.DataFrame({'u(adim)':[param_otim_alm_alim[6]]})
                df_params_IC_alim_u = pd.DataFrame({'IC u(adim)':[ICpar_alim[6]]})
                df_params_model_alim_moser = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[2]
                df_params_IC_alim_moser = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[3]
                df_params_model_alim = pd.concat([df_params_model_alim_moser, df_params_model_alim_u], axis = 1)
                df_params_IC_alim = pd.concat([df_params_IC_alim_moser, df_params_IC_alim_u], axis = 1)
            if (cont_model == 2): # Andrews (7p)
                # - Batelada:
                df_params_model_bat_KIS = pd.DataFrame({'KSI(g/L)':[param_otim_alm_bat[6]]})
                df_params_IC_bat_KIS = pd.DataFrame({'IC KSI(g/L)':[ICpar_bat[6]]})
                df_params_model_bat_andrews = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[0]
                df_params_IC_bat_andrews = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[1]
                df_params_model_bat = pd.concat([df_params_model_bat_andrews, df_params_model_bat_KIS], axis = 1)
                df_params_IC_bat = pd.concat([df_params_IC_bat_andrews, df_params_IC_bat_KIS], axis = 1)
                # - Batelada alimentada:
                df_params_model_alim_KIS = pd.DataFrame({'KSI(g/L)':[param_otim_alm_alim[6]]})
                df_params_IC_alim_KIS = pd.DataFrame({'IC KSI(g/L)':[ICpar_alim[6]]})
                df_params_model_alim_andrews = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[2]
                df_params_IC_alim_andrews = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[3]
                df_params_model_alim = pd.concat([df_params_model_alim_andrews, df_params_model_alim_KIS], axis = 1)
                df_params_IC_alim = pd.concat([df_params_IC_alim_andrews, df_params_IC_alim_KIS], axis = 1)
            if (cont_model == 5): # Hoppe_Hansford (7p)
                # - Batelada:
                df_params_model_bat_Kp =pd.DataFrame({'Kp(g/L)':[param_otim_alm_bat[6]]})
                df_params_IC_bat_Kp = pd.DataFrame({'IC Kp(g/L)':[ICpar_bat[6]]})
                df_params_model_bat_hh = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[0]
                df_params_IC_bat_hh = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[1]
                df_params_model_bat = pd.concat([df_params_model_bat_hh, df_params_model_bat_Kp], axis = 1)
                df_params_IC_bat = pd.concat([df_params_IC_bat_hh, df_params_IC_bat_Kp], axis = 1)
                # - Batelada alimentada:
                df_params_model_alim_Kp =pd.DataFrame({'Kp(g/L)':[param_otim_alm_alim[6]]})
                df_params_IC_alim_Kp = pd.DataFrame({'IC Kp(g/L)':[ICpar_alim[6]]})
                df_params_model_alim_hh = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[2]
                df_params_IC_alim_hh = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[3]
                df_params_model_alim = pd.concat([df_params_model_alim_hh, df_params_model_alim_Kp], axis = 1)
                df_params_IC_alim = pd.concat([df_params_IC_alim_hh, df_params_IC_alim_Kp], axis = 1)
            if (cont_model == 3): # Aiba (7p)
                ## - Batelada:
                df_params_model_bat_Kp =pd.DataFrame({'Kp(L/g)':[param_otim_alm_bat[6]]})
                df_params_IC_bat_Kp = pd.DataFrame({'IC Kp(L/g)':[ICpar_bat[6]]})
                df_params_model_bat_aiba = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[0]
                df_params_IC_bat_aiba = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[1]
                df_params_model_bat = pd.concat([df_params_model_bat_aiba, df_params_model_bat_Kp], axis = 1)
                df_params_IC_bat = pd.concat([df_params_IC_bat_aiba, df_params_IC_bat_Kp], axis = 1)
                # - Batelada alimentada:
                df_params_model_alim_Kp =pd.DataFrame({'Kp(L/g)':[param_otim_alm_alim[6]]})
                df_params_IC_alim_Kp = pd.DataFrame({'IC Kp(L/g)':[ICpar_alim[6]]})
                df_params_model_alim_aiba = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[2]
                df_params_IC_alim_aiba = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[3]
                df_params_model_alim = pd.concat([df_params_model_alim_aiba, df_params_model_alim_Kp], axis = 1)
                df_params_IC_alim = pd.concat([df_params_IC_alim_aiba, df_params_IC_alim_Kp], axis = 1)
            if (cont_model == 6): # Wu (8p)
                # -  Batelada:
                df_params_model_bat_v_KE = pd.DataFrame({'KE(g/L)':[param_otim_alm_bat[6]], 'v(adim)':[param_otim_alm_bat[7]]})
                df_params_IC_bat_v_KE = pd.DataFrame({'IC KE(g/L)':[ICpar_bat[6]], 'IC v(adim)':[ICpar_bat[7]]})
                df_params_model_bat_wu = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[0]
                df_params_IC_bat_wu = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[1]
                df_params_model_bat = pd.concat([df_params_model_bat_wu, df_params_model_bat_v_KE], axis = 1)
                df_params_IC_bat = pd.concat([df_params_IC_bat_wu, df_params_IC_bat_v_KE], axis = 1)
                # -  Batelada alimentada:
                df_params_model_alim_v_KE = pd.DataFrame({'KE(g/L)':[param_otim_alm_alim[6]], 'v(adim)':[param_otim_alm_alim[7]]})
                df_params_IC_alim_v_KE = pd.DataFrame({'IC KE(g/L)':[ICpar_alim[6]], 'IC v(adim)':[ICpar_alim[7]]})
                df_params_model_alim_wu = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[2]
                df_params_IC_alim_wu = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[3]
                df_params_model_alim = pd.concat([df_params_model_alim_wu, df_params_model_alim_v_KE], axis = 1)
                df_params_IC_alim = pd.concat([df_params_IC_alim_wu, df_params_IC_alim_v_KE], axis = 1)
            if (cont_model == 7): # Levenspiel (8p)
                # - Batelada:
                df_params_model_bat_n_Cp = pd.DataFrame({'n(adim)':[param_otim_alm_bat[6]], 'Cp_estr(g/L)':[param_otim_alm_bat[7]]})
                df_params_IC_bat_n_Cp = pd.DataFrame({'IC n(adim)':[ICpar_bat[6]], 'IC Cp_estr(g/L)':[ICpar_bat[7]]})  
                df_params_model_bat_levenspiel = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[0]
                df_params_IC_bat_levenspiel = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[1]
                df_params_model_bat = pd.concat([df_params_model_bat_levenspiel, df_params_model_bat_n_Cp], axis = 1)
                df_params_IC_bat = pd.concat([df_params_IC_bat_levenspiel, df_params_IC_bat_n_Cp], axis = 1)
                # - Batelada alimentada:
                df_params_model_alim_n_Cp = pd.DataFrame({'n(adim)':[param_otim_alm_alim[6]], 'Cp_estr(g/L)':[param_otim_alm_alim[7]]})
                df_params_IC_alim_n_Cp = pd.DataFrame({'IC n(adim)':[ICpar_alim[6]], 'IC Cp_estr(g/L)':[ICpar_alim[7]]}) 
                df_params_model_alim_levenspiel = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[2]
                df_params_IC_alim_levenspiel = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[3]
                df_params_model_alim = pd.concat([df_params_model_alim_levenspiel, df_params_model_alim_n_Cp], axis = 1)
                df_params_IC_alim = pd.concat([df_params_IC_alim_levenspiel, df_params_IC_alim_n_Cp], axis = 1)
            if (cont_model == 8): # Lee (8p)
                # - Batelada:
                df_params_model_bat_m_Cx = pd.DataFrame({'m(adim)':[param_otim_alm_bat[6]], 'Cx_estr(g/L)':[param_otim_alm_bat[7]]})
                df_params_IC_bat_m_Cx = pd.DataFrame({'IC m(adim)':[ICpar_bat[6]], 'IC Cx_estr(g/L)':[ICpar_bat[7]]})  
                df_params_model_bat_lee = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[0]
                df_params_IC_bat_lee = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[1]
                df_params_model_bat = pd.concat([df_params_model_bat_lee, df_params_model_bat_m_Cx], axis = 1)
                df_params_IC_bat = pd.concat([df_params_IC_bat_lee, df_params_IC_bat_m_Cx], axis = 1)
                # - Batelada alimentada:
                df_params_model_alim_m_Cx = pd.DataFrame({'m(adim)':[param_otim_alm_alim[6]], 'Cx_estr(g/L)':[param_otim_alm_alim[7]]})
                df_params_IC_alim_m_Cx = pd.DataFrame({'IC m(adim)':[ICpar_alim[6]], 'IC Cx_estr(g/L)':[ICpar_alim[7]]}) 
                df_params_model_alim_lee = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[2]
                df_params_IC_alim_lee = excel_param_defin(const_sat = const_sat_list[0], const_sat_ic = const_sat_list[2])[3]
                df_params_model_alim = pd.concat([df_params_model_alim_lee, df_params_model_alim_m_Cx], axis = 1)
                df_params_IC_alim = pd.concat([df_params_IC_alim_lee, df_params_IC_alim_m_Cx], axis = 1)
            # - DataFrame com o modo de operação:
            df_saida = pd.concat([df_params_model_bat, df_params_IC_bat, df_params_model_alim, df_params_IC_alim], axis = 1)
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
        
        Label(frame1, text = "Visite nossa página completa", font = "courier 12 bold", fg = "black", bg = "grey92", borderwidth = 2, relief = "groove").place(x = 10, y = 510)
        Button(frame1, text="https://brunaaq.github.io/Documentacao_fermenpy/", font = "calibri 8", fg = "blue", bg = "gray80", relief = "raised", borderwidth = 4, command=lambda: webbrowser.open('https://brunaaq.github.io/Documentacao_fermenpy/')).place(x = 100, y = 538)
        Label(frame2, text = "Visite nossa página completa", font = "courier 12 bold", fg = "black", bg = "grey92", borderwidth = 2, relief = "groove").place(x = 10, y = 510)
        Button(frame2, text="https://brunaaq.github.io/Documentacao_fermenpy/", font = "calibri 8", fg = "blue", bg = "gray80", relief = "raised", borderwidth = 4, command=lambda: webbrowser.open('https://brunaaq.github.io/Documentacao_fermenpy/')).place(x = 100, y = 538)
        Button(frame1, text="Encerrar programa", font = "Times 10 italic bold", fg = "white", bg = "black", relief = "raised", borderwidth = 4, command = janela.destroy).place(x = 1150, y = 515)
        Button(frame2, text="Encerrar programa", font = "Times 10 italic bold", fg = "white", bg = "black", relief = "raised", borderwidth = 4, command = janela.destroy).place(x = 1150, y = 515)
        
    # Botão para acesso aos modelos disponibilizados:
    Button(frame2, text="Pronto", bg = "black", fg="white", font="batang 12", command = combobox_model).place(x = 315, y = 29)
    
    
# Nome do arquivo excel selecionado é lançado em um label - VÍNCULO COM A FUNÇÃO EXPLORER:
arq_sel = Label(frame2, width = 50)
arq_sel.place(x = 460, y = 50)

# Encerramento da janela:
janela.mainloop() 

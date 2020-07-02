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

# Função para tabela parâmetros cinéticos:
def tab_fun_cin():
    load = Image.open("Tabela_6_gl.png")
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

# Função botôes gráficos:
def botao(comando_salvar, comando_destroy):
      load = Image.open("Salvar.png")
      render = ImageTk.PhotoImage(load)
      img = Button(frame2, image = render, border = 0, command = comando_salvar)
      img.image = render
      img.place(x = 848, y = 225)
      load = Image.open("Lixeira.png")
      render = ImageTk.PhotoImage(load)
      img = Button(frame2, image = render, border = 0, command = comando_destroy)
      img.image = render
      img.place(x = 847, y = 321)
      

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

# Caixa acesso arquivos:
def aces_arq(frame):
    Label(frame, text = "", borderwidth=3, relief="groove", width = 33, height = 7, bg = "gray45").place(x = 1030, y = 7)
    Label(frame, text = "Acessar Arquivos", font = "arial 8 bold", fg = "white", bg = "black", borderwidth=4, relief="sunken").place(x = 1036, y = 13)
aces_arq(frame1)
aces_arq(frame2)

# Caixa para plotagem dos gráficos:
def plot_graf(frame):
    Label(frame, text = "",  borderwidth=2.3, relief="ridge", width = 69, height = 22, bg = "white").place(x = 406, y = 115)
plot_graf(frame1)
plot_graf(frame2)

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
        Label(frame2, text = "b", font = "batang 12", fg = "grey", bg = "grey", width = 30 ).place(x = 960, y = 258)
        Label(frame2, text = "b", font = "batang 12", fg = "grey", bg = "grey", width = 32).place(x = 960, y = 417)
        if cont_model == 0 or cont_model == 1:
            Label(frame2, text = param_otim_alm[0], font = "batang 11", justify = "center", fg = "black", bg = "grey").place(x = 978, y = 258)
            Label(frame2, text = param_otim_alm[1], font = "batang 11", justify = "center", fg = "black", bg = "grey").place(x = 1056, y = 258)
        else:
            if cont_model >=2 and cont_model <=5:
                Label(frame2, text = param_otim_alm[0], font = "batang 11", justify = "center", fg = "black", bg = "grey").place(x = 978, y = 258)
                Label(frame2, text = param_otim_alm[1], font = "batang 11", justify = "center", fg = "black", bg = "grey").place(x = 1056, y = 258)
                Label(frame2, text = param_otim_alm[6], font = "batang 11", justify = "center", fg = "black", bg = "grey").place(x = 1142, y = 258)
            else:
                Label(frame2, text = param_otim_alm[0], font = "batang 11", justify = "center", fg = "black", bg = "grey").place(x = 978, y = 258)
                Label(frame2, text = param_otim_alm[1], font = "batang 11", justify = "center", fg = "black", bg = "grey").place(x = 1056, y = 258)
                Label(frame2, text = param_otim_alm[6], font = "batang 11", justify = "center", fg = "black", bg = "grey").place(x = 1142, y = 258)
                Label(frame2, text = param_otim_alm[7], font = "batang 11", justify = "center", fg = "black", bg = "grey").place(x = 1220, y = 258)       
        Label(frame2, text = param_otim_alm[2] , font = "batang 11", fg = "black", bg = "grey", justify = "center").place(x = 969, y = 417)
        Label(frame2, text = param_otim_alm[3] , font = "batang 11", fg = "black", bg = "grey", justify = "center").place(x = 1035, y = 417)
        Label(frame2, text = param_otim_alm[4] , font = "batang 11", fg = "black", bg = "grey", justify = "center").place(x = 1125, y = 417)
        Label(frame2, text = param_otim_alm[5] , font = "batang 11", fg = "black", bg = "grey", justify = "center").place(x = 1205, y = 417)
        
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
                        Label(frame2, text = param_otim_alm[0], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey").place(x = 978, y = 258)
                    if cond_Ks:
                        Label(frame2, text = param_otim_alm[1], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey").place(x = 1056, y = 258)
                    if cond_yxs:
                        Label(frame2, text = param_otim_alm[3] , font = "batang 10 bold", fg = "red4", bg = "grey", justify = "center").place(x = 1035, y = 417)
                    if cond_mi_kd:
                        Label(frame2, text = param_otim_alm[2] , font = "batang 10 bold", fg = "red4", bg = "grey", justify = "center").place(x = 969, y = 417)
                    if cond_param_neg == True:
                        if param_otim_alm[0] <= 0: #mimaximo
                            Label(frame2, text = param_otim_alm[0], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey").place(x = 978, y = 258)
                        if param_otim_alm[1] <= 0: #Ks
                            Label(frame2, text = param_otim_alm[1], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey").place(x = 1056, y = 258)
                        if param_otim_alm[2] < 0 or cond_mi_kd: #Kd
                            Label(frame2, text = param_otim_alm[2] , font = "batang 10 bold", fg = "red4", bg = "grey", justify = "center").place(x = 969, y = 417)
                        if (param_otim_alm[3] <= 0 or cond_yxs): #Yxs
                            Label(frame2, text = param_otim_alm[3] , font = "batang 10 bold", fg = "red4", bg = "grey", justify = "center").place(x = 1035, y = 417)
                        if param_otim_alm[4] <= 0: #alfa
                            Label(frame2, text = param_otim_alm[4] , font = "batang 10 bold bold", fg = "red4", bg = "grey", justify = "center").place(x = 1125, y = 417)
                        if param_otim_alm[5] < 0: #beta
                            Label(frame2, text = param_otim_alm[5] , font = "batang 10 bold", fg = "red4", bg = "grey", justify = "center").place(x = 1205, y = 417)
                        if cont_model == 2:
                            if param_otim_alm[6] > 55:
                                Label(frame2, text = param_otim_alm[6], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey").place(x = 1142, y = 258)
                        if cont_model >= 3 and cont_model <=5 :
                            if (param_otim_alm[6] <= 0 or param_otim_alm[6] > 10):
                                Label(frame2, text = param_otim_alm[6], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey").place(x = 1142, y = 258)
                        if cont_model >= 6 and cont_model <=8:
                            if param_otim_alm[6] <= 0:
                                Label(frame2, text = param_otim_alm[6], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey").place(x = 1142, y = 258)
                            if param_otim_alm[7] <= 0:
                                Label(frame2, text = param_otim_alm[7], font = "batang 10 bold", justify = "center", fg = "red4", bg = "grey").place(x = 1220, y = 258)
                else:
                    self.config(text = 'Press to start flashing', font="Times 12 bold italic",
                    background = flash_colours[0])

            my_button = Button(frame2, text = 'Exibir análise cinética',font = "Times 12 bold italic", fg = "white", borderwidth=4, relief="groove", width = 20,background = flash_colours[0],command = lambda:buttonCallback(my_button))
            my_button.place(x = 950, y = 164)
         
        else:
            my_button = Label(frame2, text = "b", font = "times 12", fg = "grey", bg = "grey", borderwidth=7.5, relief="flat", width = 20).place(x = 950, y = 164)
            
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
        Button(frame2, text = "Intervalo de Confiança", font = "times 8", fg = "white", bg = "gray20").place(x = 921, y = 463)
        
        # Impressão do tempo de ajuste na interface:
        Label(frame2, text = elapsed, font = "batang 11 italic", fg = "black", bg = "grey40", width = 7).place(x = 1029, y = 318)
        
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
        Label(frame2, text = r2, font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1198, y = 329.2)
        
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
            canvas = FigureCanvasTkAgg(f, frame2)
            a = canvas.get_tk_widget().place(x = 420, y = 123)
            def salvar():
                a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                defaultextension='.png')
                plt.savefig(a)
            botao(comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
        imprimir_perfil_concentracao_model_otim_exp(t_exp, t, C_exp[:,0], C_exp[:,1], C_exp[:,2], C_otim[:,0], C_otim[:,1], C_otim[:,2])
        
        ## Gráfico para mudança de cor - perfil de concentração:
        def graf_cor (x,p,s): 
            Button(frame2, text = "Concentração", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_concent).place(x = 407, y = 455)
            Button(frame2, text = "Produtividade X e P", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_produtiv).place(x = 480, y = 455)
            Button(frame2, text = u"Produtividade P.X\u207b\u00b9", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_produtiv_espec).place(x = 580, y = 455)
            Button(frame2, text = "Velocidade de Crescimento", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_mi).place(x = 681, y = 455)
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
            canvas = FigureCanvasTkAgg(f, frame2)
            a = canvas.get_tk_widget().place(x = 420, y = 123)
            def salvar():
                a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                defaultextension='.png')
                plt.savefig(a)
            botao(comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
            Button(frame2, text = "Concentração", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "white", bg = "black").place(x = 407, y = 455)
            Label(frame2, text = "", font = "batang 10",  bg = "grey40", width = 10).place(x = 1198, y = 329.2)
            Label(frame2, text = r2, font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1198, y = 329.2)
        
        ## Escolha das cores:
        def seletor_cores():
            cor = colorchooser.askcolor(title = "Editar cores")
            return(cor[1])
        def cores_cx():
            global cor_x
            cor_x = colorchooser.askcolor(title ="Editar cores")
            cor_x = cor_x[1]
            fig = graf_cor (x = cor_x, p = "green", s = "blue")
            #Button(janela, text = "Cx", bg = "gray30", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cx).place(x = 883, y = 325)
            Button(frame2, text = "Cs", bg = "gray20", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cs).place(x = 883, y = 405) 
        def cores_cs():
            global cor_s
            cor_s = colorchooser.askcolor(title ="Editar cores")
            cor_s = cor_s[1]
            fig = graf_cor (x = cor_x, p = "green", s = cor_s)
            Button(frame2, text = "Cs", bg = "gray20", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cs).place(x = 883, y = 404)
            Button(frame2, text = "Cp", bg = "gray20", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cp).place(x = 883, y = 435)  
        def cores_cp():
            global cor_p
            cor_p = colorchooser.askcolor(title ="Editar cores")
            cor_p = cor_p[1] 
            fig = graf_cor (x = cor_x, p = cor_p, s = cor_s)
            Button(frame2, text = "Cp", bg = "gray20", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cp).place(x = 883, y = 435)
        def cores_concent():
            Button(frame2, text = "Cx", bg = "gray30", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_cx).place(x = 883, y = 375)
        load = Image.open("Paleta.png")
        render = ImageTk.PhotoImage(load)
        img = Button(frame2, image = render, border = 0, command = cores_concent)
        img.image = render
        img.place(x = 877, y = 275)
        def fig_concent():
            plot_graf(frame2)
            graf_cor(x = "red", p = "green", s = "blue") 
            l
            
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
                Button(frame2, text = "Concentração", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_concent).place(x = 407, y = 455)
                Button(frame2, text = "Produtividade X e P", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_produtiv).place(x = 480, y = 455)
                Button(frame2, text = u"Produtividade P.X\u207b\u00b9", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_produtiv_espec).place(x = 580, y = 455)
                Button(frame2, text = "Velocidade de Crescimento", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_mi).place(x = 681, y = 455)
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
                canvas = FigureCanvasTkAgg(f, frame2)
                a = canvas.get_tk_widget().place(x = 420, y = 123)
                def salvar():
                    a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                    defaultextension='.png')
                    plt.savefig(a)
                botao(comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
                Button(frame2, text = "Produtividade X e P", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "white", bg = "black").place(x = 480, y = 455)
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
            Label(frame2, text = "", font = "batang 10",  bg = "grey40", width = 10).place(x = 1198, y = 329.2)
            Label(frame2, text = r2_Px_Pp.round(4), font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1198, y = 329.2)
        
        ## Escolha das cores:
        def seletor_cores():
            cor = colorchooser.askcolor(title = "Editar cores")
            return(cor[1])
        def cores_px():
            global cor_px
            cor_px = colorchooser.askcolor(title ="Editar cores")
            cor_px = cor_px[1]
            fig = graf_produtiv(px = cor_px, pp = "green")
            Button(frame2, text = "Pp", bg = "gray20", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_pp).place(x = 883, y = 405)   
        def cores_pp():
            global cor_pp
            cor_pp = colorchooser.askcolor(title ="Editar cores")
            cor_pp = cor_pp[1]
            fig = graf_produtiv(px = cor_px, pp = cor_pp)
            Button(frame2, text = "Pp", bg = "gray20", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_pp).place(x = 883, y = 404)
        def cores_produtiv():
            Button(frame2, text = "Px", bg = "gray30", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = cores_px).place(x = 883, y = 375)    
        def fig_produtiv():
            plot_graf(frame2)
            graf_produtiv(px = "red", pp = "green")
             ## Botão para seleção das cores:
            load = Image.open("Paleta.png")
            render = ImageTk.PhotoImage(load)
            img = Button(frame2, image = render, border = 0, command = cores_produtiv)
            img.image = render
            img.place(x = 877, y = 275)
            
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
                Button(frame2, text = "Concentração", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_concent).place(x = 407, y = 455)
                Button(frame2, text = "Produtividade X e P", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_produtiv).place(x = 480, y = 455)
                Button(frame2, text = u"Produtividade P.X\u207b\u00b9", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_produtiv_espec).place(x = 580, y = 455)
                Button(frame2, text = "Velocidade de Crescimento", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_mi).place(x = 681, y = 455)
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
                canvas = FigureCanvasTkAgg(f, frame2)
                a = canvas.get_tk_widget().place(x = 420, y = 123)
                def salvar():
                    a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                    defaultextension='.png')
                    plt.savefig(a)
                botao(comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
                Button(frame2, text = u"Produtividade P.X\u207b\u00b9", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "white", bg = "black").place(x = 580, y = 455)
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
            Label(frame2, text = "", font = "batang 10",  bg = "grey40", width = 10).place(x = 1198, y = 329.2)
            Label(frame2, text = r2_Ppx[0].round(4), font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1198, y = 329.2)
            print(r2_Ppx[0].round(4))
        
        ## Escolha das cores:
        def seletor_cores_Ppx():
            cor_Ppx = colorchooser.askcolor(title ="Editar cores")
            cor_Ppx = cor_Ppx[1]
            graf_produtiv_espec(Ppx_cor = cor_Ppx, Ppx_exp_cor = cor_Ppx)
            
        ## Função para geração do gráfico:
        def fig_produtiv_espec():
            plot_graf(frame2)
            graf_produtiv_espec(Ppx_cor = "red", Ppx_exp_cor = "red")
            ## Botão para seleção das cores:
            load = Image.open("Paleta.png")
            render = ImageTk.PhotoImage(load)
            img = Button(frame2, image = render, border = 0, command = seletor_cores_Ppx)
            img.image = render
            img.place(x = 877, y = 275)
        
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
                Button(frame2, text = "Concentração", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_concent).place(x = 407, y = 455)
                Button(frame2, text = "Produtividade X e P", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_produtiv).place(x = 480, y = 455)
                Button(frame2, text = u"Produtividade P.X\u207b\u00b9", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_produtiv_espec).place(x = 580, y = 455)
                Button(frame2, text = "Velocidade de Crescimento", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_mi).place(x = 681, y = 455)
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
                canvas = FigureCanvasTkAgg(f, frame2)
                a = canvas.get_tk_widget().place(x = 420, y = 123)
                def salvar():
                    a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
                    defaultextension='.png')
                    plt.savefig(a)  
                botao(comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
                Botao_mi = Button(frame2, text = "Velocidade de Crescimento", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "white", bg = "black").place(x = 681, y = 455)
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
            Label(frame2, text = "", font = "batang 10",  bg = "grey40", width = 10).place(x = 1198, y = 329.2)
            Label(frame2, text = r2_mi[0].round(4), font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1198, y = 329.2)
            print(r2_mi[0].round(4))
                
        ## Escolha das cores:
        def seletor_cores_mi():
            cor_mi = colorchooser.askcolor(title ="Editar cores")
            cor_mi = cor_mi[1]
            graf_mi(mi_cor = cor_mi, mi_exp_cor = cor_mi)
            
        ## Função para geração do gráfico:
        def fig_mi():
            plot_graf(frame2)
            graf_mi(mi_cor = "red", mi_exp_cor = "red")
            ## Botão para seleção das cores:
            load = Image.open("Paleta.png")
            render = ImageTk.PhotoImage(load)
            img = Button(frame2, image = render, border = 0, command = seletor_cores_mi)
            img.image = render
            img.place(x = 877, y = 275)
            
        # Cálculo res final:
        res_final = odeint(list_funcs_args[cont_model], cond_inic, t_exp, args = (param_otim_alm)) - C_exp
        for i in range(0,3):
            res_final[:,i] = res_final[:,i]/dpC[i]
        res_final = res_final.flatten()
        res_final = sum(res_final**2)
        res_final = round(res_final,2)
        
        # Impressão do valor do resíduo na interface:
        Label(frame2, text = res_final, font = "batang 10 italic", fg = "black", bg = "grey40", width = 10).place(x = 1198, y = 299)
        
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
        
        # Planilhas para seleção do tipo de gráfico:
        Button(frame2, text = "Concentração", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_concent).place(x = 407, y = 455)
        Button(frame2, text = "Produtividade X e P", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_produtiv).place(x = 480, y = 455)
        Button(frame2, text = u"Produtividade P.X\u207b\u00b9", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_produtiv_espec).place(x = 580, y = 455)
        Button(frame2, text = "Velocidade de Crescimento", font = "arial 7 bold", borderwidth=1, relief="solid", fg = "black", bg = "white", command = fig_mi).place(x = 681, y = 455)
        
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
        Label(frame2, text = "Modelagem_Concent_Produt_mi.xlsx", font = "arial 10 italic", fg = "black", bg = "gray45").place(x = 1105, y = 58)
        
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
        Label(frame2, text = "Modelagem_Parametros_Cineticos.xlsx", font = "arial 10 italic", fg = "black", bg = "gray45").place(x = 1105, y = 100)
        
        # Botão de acesso - arquivo .xlsx - concentração:
        load = Image.open("Excel.png")
        render = ImageTk.PhotoImage(load)
        img = Button(frame2, image = render, border = 0)
        img.image = render
        img.place(x = 1036, y = 38)
        
        # Botão de acesso - arquivo .xlsx - parâmetros cinéticos:
        load = Image.open("Excel.png")
        render = ImageTk.PhotoImage(load)
        img = Button(frame2, image = render, border = 0)
        img.image = render
        img.place(x = 1036, y = 78)
    
        # Fim da modelagem:
        return()

    # Criação botões - MODELAGEM:
    def click_contois(): 
        tab_fun_cin()
        #func_sai()
        load = Image.open("Equacao_Contois.png")
        render = ImageTk.PhotoImage(load)
        img_contois = Label(frame2, image = render, border = 0)
        img_contois.image = render
        img_contois.place(x = 50, y = 360)  
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     KSX(g.L\u207b\u00b9)", font = "arial 10 bold", justify = "center", fg = "black", bg = "grey", width = 21).place(x = 930, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey", justify = "center", width = 41).place(x = 932, y = 380)
        modelagem(cont_model = 1)

    def click_monod(): 
        tab_fun_cin()
        #func_sai()
        load = Image.open("Equacao_Monod.png")
        render = ImageTk.PhotoImage(load)
        img_monod = Label(frame2, image = render, border = 0)
        img_monod.image = render
        img_monod.place(x = 50, y = 360)      
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "grey", justify = "center", width = 20).place(x = 930, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey", justify = "center", width = 41).place(x = 932, y = 380)
        modelagem(cont_model = 0)
        
    def click_moser(): 
        tab_fun_cin()
        #func_sai()
        load = Image.open("Equacao_Moser.png")
        render = ImageTk.PhotoImage(load)
        img_moser = Label(frame2, image = render, border = 0)
        img_moser.image = render
        img_moser.place(x = 50, y = 360)    
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)     u(adim)", font = "arial 10 bold", fg = "black", bg = "grey", justify = "center", width = 28).place(x = 930, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "grey", justify = "center", width = 41).place(x = 932, y = 380)
        modelagem(cont_model = 4)
        
    def click_aiba(): 
        load = Image.open("Tabela_6_gl.png")
        render = ImageTk.PhotoImage(load)
        img = Label(frame2, image = render, border = 0)
        img.image = render
        img.place(x = 960, y = 205)  
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)     Kp(g.L\u207b\u00b9)", font = "arial 10 bold", justify = "center", fg = "black", bg = "lightgrey", width = 28).place(x = 962, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "lightgrey", justify = "center", width = 41).place(x = 932, y = 380)
        #modelagem(cont_model = 3)

    def click_hope_hansford(): 
        load = Image.open("Tabela_6_gl.png")
        render = ImageTk.PhotoImage(load)
        img = Label(frame2, image = render, border = 0)
        img.image = render
        img.place(x = 960, y = 205)      
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)     Kp(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "lightgrey", justify = "center", width = 28).place(x = 962, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "lightgrey", justify = "center", width = 41).place(x = 932, y = 380)
        #modelagem(cont_model = 5)
        
    def click_levenspiel(): 
        load = Image.open("Tabela_6_gl.png")
        render = ImageTk.PhotoImage(load)
        img = Label(frame2, image = render, border = 0)
        img.image = render
        img.place(x = 960, y = 205)    
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)    Ks(g.L\u207b\u00b9)     n(adim)     Cp*(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "lightgrey", justify = "center", width = 37).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)   \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "lightgrey", justify = "center", width = 41).place(x = 962, y = 380)
        #modelagem(cont_model = 7)
        
    def click_andrews(): 
        load = Image.open("Tabela_6_gl.png")
        render = ImageTk.PhotoImage(load)
        img = Label(frame2, image = render, border = 0)
        img.image = render
        img.place(x = 960, y = 205)    
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)      Ks(g.L\u207b\u00b9)     KIS(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "lightgrey", justify = "center", width = 30).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "lightgrey", justify = "center", width = 41).place(x = 962, y = 380)
        #modelagem(cont_model = 2)
        
    def click_wu(): 
        load = Image.open("Tabela_6_gl.png")
        render = ImageTk.PhotoImage(load)
        img = Label(frame2, image = render, border = 0)
        img.image = render
        img.place(x = 960, y = 205)    
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)     Ks(g.L\u207b\u00b9)     KE(g.L\u207b\u00b9)     v(adim)", font = "arial 10 bold", fg = "black", bg = "lightgrey", justify = "center", width = 40).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[±gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "lightgrey", justify = "center", width = 41).place(x = 962, y = 380)
        #modelagem(cont_model = 6)
        
    def click_lee(): 
        load = Image.open("Tabela_6_gl.png")
        render = ImageTk.PhotoImage(load)
        img = Label(frame2, image = render, border = 0)
        img.image = render
        img.place(x = 960, y = 205)    
        Label(frame2, text = u"\u03bcmáx(h\u207b\u00b9)    Ks(g.L\u207b\u00b9)     m(adim )     Cx*(g.L\u207b\u00b9)", font = "arial 10 bold", fg = "black", bg = "lightgrey", justify = "center", width = 37).place(x = 932, y = 220)
        Label(frame2, text = u"Kd(h\u207b\u00b9)    Yxs(gx.gs\u207b\u00b9)    \u03B1(gx.gp\u207b\u00b9)    \u03B2[gx.(gp.h)\u207b\u00b9]", font = "arial 10 bold", fg = "black", bg = "white", justify = "center", width = 41).place(x = 962, y = 380)
        #modelagem(cont_model = 8)

    def print_me_2():
        value_2 = combo_2.get()
        print(value_2)
        if value_2 == "AUSÊNCIA DE INIBIÇÃO":
            Button(frame2, text = "CONTOIS", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 12", width = 8, command = click_contois).place(x = 172, y = 120)
            Button(frame2, text = "MONOD", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 12", width = 8, command = click_monod).place(x = 172, y = 200)
            Button(frame2, text = "MOSER", bg = "gray20", fg="white", borderwidth=2, relief="ridge", font="batang 12", width = 8, command = click_moser).place(x = 172, y = 280)

    Button(frame2, text="Pronto", bg = "black", fg="white", font="batang 12", command = print_me_2).place(x = 315, y = 29)
Button(frame2, text = "Carregar arquivo",  font="Batang 12", fg="white", bg="gray17", borderwidth=2, relief="raised", command = explorer).place(x = 568, y = 15) 
Label(frame2, borderwidth=2, relief="ridge", justify = "center", width = 40).place(x = 500, y = 50)

# Encerramento da interface:
janela.mainloop()

## ALGORITMO PARA CONSTRUÇÃO DA CURVA DE CALIBRAÇÃO PARA BIOMASSA:

## Bibliotecas científicas
import numpy as np 
import pandas as pd 
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution
from scipy.optimize import leastsq
import scipy.stats as sc
import tkinter as tk
from tkinter import *
from tkinter import Label, Button
from tkinter.filedialog import askopenfilename # caixa externa - explorar files no computador
import os # divisão de strings
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from tkinter.ttk import Combobox
from tkinter.filedialog import asksaveasfilename
from tkinter.commondialog import Dialog
from tkinter import colorchooser
from tkinter import filedialog
import webbrowser

# Criação da interface:
interface = Tk()
interface.title("CalibraPy")
interface.geometry("920x650")
interface.configure(bg = "gray75")
titulo = Label(interface, text="CURVA DE CALIBRAÇÃO PARA BIOMASSA", font="times 14 bold", fg="black", bg = "gray70", borderwidth=4, relief="sunken").grid(row = 0, column = 0, columnspan=1)
interface.resizable(0,0)

# Saída nome do arquivo excel:
Label(interface, width = 27, height = 4, borderwidth = 4, relief = "sunken", bg = "grey65").place(x = 400, y = 150)
Label(interface, text = "Acessar Arquivo", font = "Georgia 10", fg = "black", bg = "gray70", borderwidth = 3, relief = "sunken").place(x =390, y = 142)
saida_arquivo = Label(interface, font = "arial 8 italic", fg = "black", bg = "grey65")
saida_arquivo.place(x = 449, y = 189)

## Escrita do template excel para entrada dos dados:
def excel_template():
    template_Cx_DO_calibrar = pd.read_excel("Template_Cx_DO_calibrar.xlsx", "Template_modelo")
    template_DO_quanticificar_Cx = pd.read_excel("Template_DO_quantificar_Cx.xlsx","Template_modelo")
    os.system("start EXCEL Template_Cx_DO_calibrar.xlsx")  
    os.system("start EXCEL Template_DO_quantificar_Cx.xlsx")  
# Template Excel - botão de acesso:
load = Image.open("Excel_template.png")
render = ImageTk.PhotoImage(load)
img = Label(interface, image = render, border = 0, borderwidth = 2, relief = "solid")
img.image = render
img.grid(row = 2, column = 4, padx = 6)
Button(interface, text = "Baixe nosso template", font = "arial 7 bold", fg = "black", bg = "white", borderwidth = 2, relief = "raised", command = excel_template).grid(row = 3, column = 4, padx = 10)
 
# Ajuda - link com a página web do projeto:
botao_ajuda = Button(interface, text = "AJUDA", font="georgia 10 bold", fg = "white", bg = "grey20", command=lambda: webbrowser.open('https://brunaaq.github.io/Documentacao_fermenpy/tutorial.html'))
botao_ajuda.grid(row=0, column = 4, sticky = E+N)

# Função construção botões alocados para ferramentas gráficas:
def botao_com_graf(comando_salvar, comando_destroy):
      load = Image.open("Salvar_mod.png")
      render = ImageTk.PhotoImage(load)
      img = Button(interface, image = render, border = 0, command = comando_salvar)
      img.image = render
      img.place(x = 868, y = 330)
      load = Image.open("Lixeira_mod.png")
      render = ImageTk.PhotoImage(load)
      img = Button(interface, image = render, border = 0, command = comando_destroy)
      img.image = render
      img.place(x = 867, y = 426)  
     
    
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
Label(interface, width = 40, height = 5, borderwidth = 4, relief = "sunken",bg = "grey70").grid(row = 5, column = 0, pady = 120, sticky=S)


# Separação saída:
Label(interface, width = 33, height = 4, borderwidth = 4, relief = "sunken", bg = "grey65").place(x = 620, y = 150)
tit_equa_sai = Label(interface, text = "Regressão Linear", font = "Georgia 10", fg = "black", bg = "gray70",  borderwidth = 3, relief = "sunken").place(x = 610, y = 142)
sai_equa = Label(interface, text = "Cx =                   * D.O. +                    ", font = "times 9 bold", fg = "black", bg = "gray90", borderwidth = 3, relief = "sunken").place(x = 625, y = 170)
sai_r2 = Label(interface, text = "R² =                   ", font = "times 9 bold", fg = "black", bg = "gray90", borderwidth = 3, relief = "sunken").place(x = 625, y = 193)

# Saída para o gráfico:
Label(interface, width = 72, height = 26, borderwidth = 4, relief = "sunken", bg = "grey85").place(x = 395, y = 223)

# Programação da apresentação inicial da interface - tudo sem função, apenas demonstrativa:
## Construir curva de calibração
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
num_leit_entr = tk.Entry(interface, width = 3, borderwidth = 2, relief = "sunken", font = "batang 12 bold", bg = "white", fg = "black")
num_leit_entr.grid(row = 5, column = 0, padx = 89, pady = 230, sticky=N+E)
num_leit_entr.configure(state='disable')
botao_entr_num_leit = Button(interface, text = "Ir", font = "batang 8 bold", fg = "gray30", bg = "gray70", relief = "raised")
botao_entr_num_leit.grid(row = 5, column = 0, padx = 65, pady = 232, sticky=N+E)
tex_qual = Label(interface, text = "Qual?",font = "times 10", fg = "gray30", bg = "gray70")
tex_qual.grid(row = 5, column = 0, padx = 125, pady = 231, sticky=N+E)
## Calcular biomassa:
tit_inserir_curva = Label(interface, text = "Quantificar Biomassa",font = "times 11 italic",  borderwidth = 2, relief = "sunken", fg = "black", bg = "gray95")
tit_inserir_curva.grid(row = 5, column = 0, padx = 48, pady = 192, sticky=S+W)
tit_inserir_equ = Label(interface, text = "Insira a Equação (não se esqueça dos sinais)",font = "times 10",  borderwidth = 3, relief = "groove", fg = "gray30", bg = "gray70")
tit_inserir_equ.grid(row = 5, column = 0, padx = 64, pady = 160, sticky=S+W)
cx_equacao = Label(interface, text = "Cx = ",font = "times 10 italic", fg = "gray30", bg = "gray70")
cx_equacao.grid(row = 5, column = 0, padx = 64, pady = 130, sticky=S+W)
do_equacao = Label(interface, text = "*D.O. +",font = "times 10 italic", fg = "gray30", bg = "gray70")
do_equacao.grid(row = 5, column = 0, padx = 159, pady = 130, sticky=S+W)
entr_a = tk.Entry(interface, width = 6, borderwidth = 2, relief = "sunken", font = "batang 10 bold", bg = "white", fg = "black")
entr_a.grid(row = 5, column = 0, padx = 96, pady = 130, sticky=S+W)
entr_a.configure(state = "disabled")
entr_b = tk.Entry(interface, width = 6, borderwidth = 2, relief = "sunken", font = "batang 10 bold", bg = "white", fg = "black")
entr_b.grid(row = 5, column = 0, padx = 134, pady = 130, sticky=S+E)
entr_b.configure(state = "disabled")
botao_ok_calc = Button(interface, text = "Enviar", font = "batang 8 bold", fg = "gray30", bg = "gray70", borderwidth=2, relief="sunken")
botao_ok_calc.grid(row = 5, column = 0, padx = 62, pady = 124, sticky=S+E)

## Parte funcional do código:

arquivo_excel = Label(interface,font="arial 8 bold italic", fg="black", borderwidth=2, relief="ridge", justify = "center", bg = "gray85",  width = 40)
arquivo_excel.grid(row = 5, column = 0, pady = 68, sticky=N)
# Explorador para carregar o arquivo de entrada:
def explorador():
    explorador = askopenfilename()
    print(explorador)
    nome_arquivo = os.path.basename(explorador)
    arquivo_excel.configure(text=nome_arquivo)
    # Captura dos dados de entrada - formato dataframe:
    excel_entrada = pd.read_excel(explorador)
    global excel_entrada_np
    excel_entrada_np = excel_entrada.values
    print(excel_entrada_np)

# Captura da ação desejada pelo operador:   
def printar_val():
    val_selec = combo.get() 
    print(val_selec)
    if val_selec == "CONSTRUIR CURVA DE CALIBRAÇÃO":
        arquivo_excel.configure(text="")
        botao_explor.configure(fg = "white", bg = "black", relief = "groove", command = explorador)
        tit_criar_curva.configure(relief = "raised")
        tit_num_leit.config(font = "times 10 bold", fg = "black", bg = "gray70")
        botao_unic.config(fg = "white", bg = "grey40", relief = "raised", command = unica, activebackground="lightgreen")
        botao_dupl.config(fg = "white", bg = "grey40", relief = "raised", command = duplicata, activebackground="lightgreen")
        botao_tripl.config(fg = "white", bg = "grey40", relief = "raised",command = triplicata, activebackground="lightgreen")
        botao_outra.config(fg = "white", bg = "grey40", relief = "raised", command = entr_leit, activebackground="lightgreen")
        botao_ok_calib.config(fg = "white", bg = "black")
        
    if val_selec == "UTILIZAR CURVA PRÉ-EXISTENTE": 
        arquivo_excel.configure(text="")
        botao_explor.configure(fg = "white", bg = "black", relief = "groove", command = explorador)
        tit_inserir_curva.configure(relief = "raised")
        tit_inserir_equ.configure(font = "times 10 bold", fg = "black", bg = "gray70")
        cx_equacao.configure(fg = "black", bg = "gray70")
        do_equacao.configure(fg = "black", bg = "gray70")
        entr_a.configure(state = "normal")
        entr_b.configure(state = "normal")
        botao_ok_calc.configure(fg = "black", bg = "lightgreen", relief = "raised")
        
# Função para entradas de leituras acima de triplicata:    
def entr_leit():
    botao_ok_calib.config(fg = "white", bg = "black", relief = "sunken")
    tit_coef_ang.config(fg = "gray30", bg = "gray70")
    tit_coef_lin.config(fg = "gray30", bg = "gray70")
    sai_coef_ang.config(fg = "gray70", bg = "gray70")
    sai_coef_lin.config(fg = "gray70", bg = "gray70")
    global num_leit_entr, botao_entr_num_leit
    num_leit_entr.configure(state = "normal") 
    botao_entr_num_leit.configure(fg = "white", bg = "black", activebackground="lightgreen") 
    tex_qual.configure(fg = "black", bg = "grey70")
    botao_unic.config(bg = "gray40")
    botao_dupl.config(bg = "gray40")
    botao_tripl.config(bg = "gray40")
    botao_outra.config(bg = "black")
     
# Leitura única:
def unica():
    global do_exp, cx_exp, cont
    cont = 1
    botao_ok_calib.config(fg = "white", bg = "black", relief = "sunken")
    tit_coef_ang.config(fg = "gray30", bg = "gray70")
    tit_coef_lin.config(fg = "gray30", bg = "gray70")
    sai_coef_ang.config(fg = "gray70", bg = "gray70")
    sai_coef_lin.config(fg = "gray70", bg = "gray70")
    do_exp = excel_entrada_np[:,0] #eixo x
    cx_exp = excel_entrada_np[:,1] #eixo y
    print(do_exp)
    print(cx_exp)
    botao_unic.config(bg = "black")
    botao_dupl.config(bg = "grey40")
    botao_tripl.config(bg = "grey40")
    botao_outra.config(bg = "gray40")
    botao_ok_calib.config(fg = "black", bg = "green", relief = "raised")
# Leitura em duplicata:
def duplicata():
    botao_ok_calib.config(fg = "white", bg = "black", relief = "sunken")
    tit_coef_ang.config(fg = "gray30", bg = "gray70")
    tit_coef_lin.config(fg = "gray30", bg = "gray70")
    sai_coef_ang.config(fg = "gray70", bg = "gray70")
    sai_coef_lin.config(fg = "gray70", bg = "gray70")
    global do_exp, cx_exp, do_desv_pad, cx_desv_pad, cont
    cont = 2
    print(cont)
    do_1 = excel_entrada_np[:,0] #eixo x
    do_2 = excel_entrada_np[:,2] #eixo x
    cx_1 = excel_entrada_np[:,1] #eixo y
    cx_2 = excel_entrada_np[:,3] #eixo y
    # Cálculo da média:
    do_exp = (do_1 + do_2)/cont
    cx_exp = (cx_1 + cx_2)/cont
    # Cálculo do desvio padrão:
    matriz_do = np.array([do_1,do_2])
    matriz_cx = np.array([cx_1,cx_2])
    ## Calculando a matriz transposta ##
    matriz_do_t = np.transpose(matriz_do)
    matriz_cx_t = np.transpose(matriz_cx)
    ## Função std para o desvio padrão da dispersão ##
    do_desv_pad = np.std(matriz_do_t, axis=1)
    cx_desv_pad = np.std(matriz_cx_t, axis=1)
    # Botões para a interface:
    botao_unic.config(bg = "gray40")
    botao_dupl.config(bg = "black")
    botao_tripl.config(bg = "gray40")
    botao_outra.config(bg = "gray40")
    botao_ok_calib.config(fg = "black", bg = "green", relief = "raised")
    
# Leitura em triplicata:
def triplicata():
    botao_ok_calib.config(fg = "white", bg = "black", relief = "sunken")
    tit_coef_ang.config(fg = "gray30", bg = "gray70")
    tit_coef_lin.config(fg = "gray30", bg = "gray70")
    sai_coef_ang.config(fg = "gray70", bg = "gray70")
    sai_coef_lin.config(fg = "gray70", bg = "gray70")
    global do_exp, cx_exp, do_desv_pad, cx_desv_pad, int_conf_do, int_conf_cx, cont
    cont = 3
    print(cont)
    do_1 = excel_entrada_np[:,0] #eixo x
    do_2 = excel_entrada_np[:,2] #eixo x
    do_3 = excel_entrada_np[:,4] #eixo x
    cx_1 = excel_entrada_np[:,1] #eixo y
    cx_2 = excel_entrada_np[:,3] #eixo y
    cx_3 = excel_entrada_np[:,5] #eixo y
    # Cálculo da média:
    do_exp = (do_1 + do_2 +do_3)/cont
    cx_exp = (cx_1 + cx_2 + cx_3)/cont
    # Cálculo do desvio padrão:
    matriz_do = np.array([do_1,do_2,do_3])
    matriz_cx = np.array([cx_1,cx_2,cx_3])
    ## Calculando a matriz transposta ##
    matriz_do_t = np.transpose(matriz_do)
    matriz_cx_t = np.transpose(matriz_cx)
    ## Função std para o desvio padrão da dispersão ##
    do_desv_pad = np.std(matriz_do_t, axis=1)
    cx_desv_pad = np.std(matriz_cx_t, axis=1)
    # Cálculo do intervalo de confiança:
    ## D.O. - eixo x ##
    int_conf_do = sc.norm.interval(0.05, loc = do_exp, scale = do_desv_pad)
    #int_conf_do = int_conf_do[1] - int_conf_do[0]
    ## Cx - eixo y ##
    int_conf_cx = sc.norm.interval(0.05, loc = cx_exp, scale = cx_desv_pad)
    int_conf_cx = int_conf_cx[1] - int_conf_cx[0]
    #print(int_conf_do, int_conf_cx)
    #print(int_conf_do)
    
    # Botões para interface:
    botao_unic.config(bg = "gray40")
    botao_dupl.config(bg = "gray40")
    botao_tripl.config(bg = "black")
    botao_outra.config(bg = "gray40")
    botao_ok_calib.config(fg = "black", bg = "green", relief = "raised")
    
# Leitura acima da triplicata:
def outra():
    botao_ok_calib.config(fg = "white", bg = "black", relief = "sunken")
    tit_coef_ang.config(fg = "gray30", bg = "gray70")
    tit_coef_lin.config(fg = "gray30", bg = "gray70")
    sai_coef_ang.config(fg = "gray70", bg = "gray70")
    sai_coef_lin.config(fg = "gray70", bg = "gray70")
    cont_calib = int(num_leit_entr.get())
    # Passando para o número de colunas para análise pelo for:
    cont_calib_corr = cont_calib *2
    print(cont_calib_corr)
    global do_exp, cx_exp, cont, do_desv_pad, cx_desv_pad, cont
    cont = 4
    do = [excel_entrada_np[:,0]] #eixo x
    cx = [excel_entrada_np[:,1]] #eixo y
    cont = cont_calib_corr - 1
    i = 2
    while (i <= cont):
        do_lei = excel_entrada_np[:,(i)] 
        cx_lei = excel_entrada_np[:,(i+1)] 
        do.append(do_lei)
        cx.append(cx_lei)
        i = i + 2
    # Cálculo da média:
    do_exp = sum(do)/cont_calib
    cx_exp = sum(cx)/cont_calib
    # Cálculo do desvio padrão:
    matriz_do = np.array(do)
    matriz_cx = np.array(cx)
    ## Calculando a matriz transposta ##
    matriz_do_t = np.transpose(matriz_do)
    matriz_cx_t = np.transpose(matriz_cx)
    ## Função std para o desvio padrão da dispersão ##
    do_desv_pad = np.std(matriz_do_t, axis=1)
    cx_desv_pad = np.std(matriz_cx_t, axis=1)
    #print(do_desv_pad, cx_desv_pad)
    # Botão para a interface:
    botao_unic.config(bg = "gray40")
    botao_dupl.config(bg = "gray40")
    botao_tripl.config(bg = "gray40")
    botao_outra.config(bg = "black")
    botao_ok_calib.config(fg = "black", bg = "green", relief = "raised")
botao_entr_num_leit.configure(command = outra)

    
# Comando, considerando conceitos estatísticos, para a construção da curva de calibração:
def calibra():
    global pl
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
    ## Avaliação preliminar: ##
    if (cont == 1):
        xerr = 0
        yerr = 0
        color = "grey"
    else:
        xerr = do_desv_pad
        yerr = cx_desv_pad
        color = "black"
    ## Figura:
    f = plt.figure(figsize=(8.3,7), dpi = 56) 
    plot = f.add_subplot(111)  
    plt.plot(do_exp,np.polyval(pl,do_exp),'g',linewidth=2) 
    plt.plot(do_exp,cx_exp,'o',markersize=14,color='grey',markeredgecolor='black')                  
    plt.xlabel("Densidade Óptica", weight='bold', fontsize = 16)                               
    plt.ylabel("Concentração de células (g/L)", weight='bold', fontsize = 16)  
    plot.errorbar(do_exp, cx_exp, xerr = xerr, yerr = yerr, linestyle='None', color = color, xuplims=True, uplims=True, xlolims=True, lolims=True)       
    plt.annotate(u'Linha de tendência modelo', xy=(2.7, 1.3), xytext=(1.4, 1.8), arrowprops=dict(facecolor='m',shrink=0.05), size=15)    
    plt.grid(True)                                                                                                                                                                     
    f.patch.set_facecolor('white')                                                   
    plt.style.use('default')   
    canvas = FigureCanvasTkAgg(f, interface)
    a = canvas.get_tk_widget().place(x = 400, y = 228)
    def salvar():
        a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
        defaultextension='.png')
        plt.savefig(a)
    botao_com_graf(comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
    
    # Criação do gráfico com mudança de cor:
    def mudar_cor (cor_model, cor_exp, cor_seta):
        f = plt.figure(figsize=(8.3,7), dpi = 56) 
        plot = f.add_subplot(111)      
        plt.plot(do_exp,np.polyval(pl,do_exp),color = cor_model, linewidth=2)  
        plt.plot(do_exp,cx_exp,'o',markersize=14,color=cor_exp,markeredgecolor='black')                         
        plt.xlabel("Densidade Óptica", weight='bold', fontsize = 16)                               
        plt.ylabel("Concentração de células (g/L)", weight='bold', fontsize = 16)  
        plot.errorbar(do_exp, cx_exp, xerr = xerr, yerr = yerr, linestyle='None', color = cor_exp, xuplims=True, uplims=True, xlolims=True, lolims=True)
        plt.annotate(u'Linha de tendência modelo', xy=(2.7, 1.3), xytext=(1.4, 1.8), arrowprops=dict(facecolor=cor_seta,shrink=0.05), size=15)    
        plt.grid(True)                                                                                                                                                                     
        f.patch.set_facecolor('white')                                                   
        plt.style.use('default')   
        canvas = FigureCanvasTkAgg(f, interface)
        a = canvas.get_tk_widget().place(x = 400, y = 228)
        def salvar():
            a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
            defaultextension='.png')
            plt.savefig(a)
        botao_com_graf(comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
      
    
    ## Escolha das cores:
    def seletor_cores_model():
        global cor_model_selec
        cor_model_selec = colorchooser.askcolor(title ="Editar cores")
        cor_model_selec = cor_model_selec[1]
        mudar_cor (cor_model = cor_model_selec, cor_exp = "grey", cor_seta = "m")
        Button(interface, text = "O", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = seletor_cores_exp).place(x = 879, y = 503)
    def seletor_cores_exp():
        global cor_exp_selec
        cor_exp_selec = colorchooser.askcolor(title ="Editar cores")
        cor_exp_selec = cor_exp_selec[1]
        mudar_cor (cor_model = cor_model_selec, cor_exp = cor_exp_selec, cor_seta = "m")
        Button(interface, text = "->", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 8 bold",  command = seletor_cores_seta).place(x = 879, y = 525)
    def seletor_cores_seta():
        global cor_seta_selec
        cor_seta_selec = colorchooser.askcolor(title ="Editar cores")
        cor_seta_selec = cor_seta_selec[1]
        mudar_cor (cor_model = cor_model_selec, cor_exp = cor_exp_selec, cor_seta = cor_seta_selec)
        Button(interface, text = "->", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 8 bold",  command = seletor_cores_seta).place(x = 879, y = 525)
    def seletor_cores_calib():
        Button(interface, text = "/", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = seletor_cores_model).place(x = 879, y = 480)
    
    ## Botão para seleção das cores:
    load = Image.open("Paleta_mod.png")
    render = ImageTk.PhotoImage(load)
    img = Button(interface, image = render, border = 0, command = seletor_cores_calib)
    img.image = render
    img.place(x = 867, y = 380)  
           
    # Saída - valores coeficientes:
    sai_coef_ang.config(text = pl[0].round(4), font = "batang 10", fg = "black")
    sai_coef_lin.config(text = pl[1].round(4), font = "batang 10", fg = "black")
    sai_a.config(text = pl[0].round(4), fg = "black")
    sai_b.config(text = pl[1].round(4), fg = "black")
    sai_r2.config(text = R2.round(5), fg = "black")
    
    # Criação do dataframe para exportação dos dados:
    def desv_excel():
        df_desv = pd.DataFrame({"D.O.med": do_exp, "D.O.desv": do_desv_pad, "Cx_med(g/L)": cx_exp,  "Cx_desv(g/L)": cx_exp})
        with pd.ExcelWriter('Media_desvio_leituras.xlsx') as writer:
            df_desv.to_excel(writer, sheet_name="Media_desvio")
            writer.save()
        os.system("start EXCEL Media_desvio_leituras.xlsx")
    ## Botão para acesso:
    load = Image.open("Excel.png")
    render = ImageTk.PhotoImage(load)
    img = Button(interface, image = render, border = 0, borderwidth =2, relief = "raised", command = desv_excel)
    img.image = render
    img.place(x = 407, y = 172)
    saida_arquivo.configure(text = "Media_desvio_leituras.xlsx", bg = "gray80", borderwidth = 3, relief = "sunken")

# Passando o comando para o botão -  lançamento dos resultados:    
botao_ok_calib.config(command = calibra)

# Puxar os coeficientes já calculados pelo algoritmo:
def puxar():
    entr_a.configure(text = pl[0].round(4))
    entr_b.configure(text = pl[1].round(4))
    print("bruna")

# Função para calcular Cx:
def calc_cx():
    global do_cal, cx_cal
    do_cal = excel_entrada_np[:,0] #eixo x
    cx_cal = coefic_a * do_cal + coefic_b
    print(cx_cal)
    # Criando o dataframe com o cx calculado para exportação:
    def cx_excel():
        df_cx = pd.DataFrame({"D.O.exp": do_cal, "Cx_exp(g/L)": cx_cal})
        with pd.ExcelWriter('Concentracao_celular.xlsx') as writer:
            df_cx.to_excel(writer, sheet_name="DO_Cx_exp")
            writer.save()
        os.system("start EXCEL Concentracao_celular.xlsx")
    ## Botão para acesso:
    load = Image.open("Excel.png")
    render = ImageTk.PhotoImage(load)
    img = Button(interface, image = render, border = 0, borderwidth =2, relief = "raised", command = cx_excel)
    img.image = render
    img.place(x = 407, y = 172)
    ## Nome do arquivo gerado:
    saida_arquivo.configure(text = "Concentracao_celular.xlsx")
    
    ## Figura:
    f = plt.figure(figsize=(8.3,7), dpi = 56) 
    plot = f.add_subplot(111)  
    plt.plot(do_cal,cx_cal,'o',markersize=14,color='grey',markeredgecolor='black')                  
    plt.xlabel("Densidade Óptica", weight='bold', fontsize = 16)                               
    plt.ylabel("Concentração de células (g/L)", weight='bold', fontsize = 16)  
    plt.grid(True)                                                                                                                                                                     
    f.patch.set_facecolor('white')                                                   
    plt.style.use('default')   
    canvas = FigureCanvasTkAgg(f, interface)
    a = canvas.get_tk_widget().place(x = 400, y = 228)
    def salvar():
        a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
        defaultextension='.png')
        plt.savefig(a)
    botao_com_graf(comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
    
    # Criação do gráfico com mudança de cor:
    def mudar_cor (cor_exp):
        f = plt.figure(figsize=(8.3,7), dpi = 56) 
        plot = f.add_subplot(111)      
        plt.plot(do_cal,cx_cal,'o',markersize=14,color=cor_exp,markeredgecolor='black')                         
        plt.xlabel("Densidade Óptica", weight='bold', fontsize = 16)                               
        plt.ylabel("Concentração de células (g/L)", weight='bold', fontsize = 16)  
        plt.grid(True)                                                                                                                                                                     
        f.patch.set_facecolor('white')                                                   
        plt.style.use('default')   
        canvas = FigureCanvasTkAgg(f, interface)
        a = canvas.get_tk_widget().place(x = 400, y = 228)
        def salvar():
            a = asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*")), 
            defaultextension='.png')
            plt.savefig(a)
        botao_com_graf(comando_salvar = lambda : salvar(), comando_destroy = canvas.get_tk_widget().destroy)
      
    ## Escolha das cores:
    def seletor_cores_exp():
        global cor_model_selec
        cor_exp_selec = colorchooser.askcolor(title ="Editar cores")
        cor_exp_selec = cor_exp_selec[1]
        mudar_cor (cor_exp = cor_exp_selec)
    def seletor_cores_calib():
        Button(interface, text = "O", bg = "gray50", fg="white", borderwidth=2, relief="raised", font="batang 10 bold",  command = seletor_cores_exp).place(x = 879, y = 480)
    
    ## Botão para seleção das cores:
    load = Image.open("Paleta_mod.png")
    render = ImageTk.PhotoImage(load)
    img = Button(interface, image = render, border = 0, command = seletor_cores_calib)
    img.image = render
    img.place(x = 867, y = 380)  
    
    
# Função para capturar os dados dos coeficientes:
def capt_coef():
    global  coefic_a, coefic_b
    coefic_a = float(entr_a.get())
    coefic_b = float(entr_b.get())
    print(coefic_a, coefic_b)
    sai_a.configure(text = coefic_a, fg = "black")
    sai_b.configure(text = coefic_b, fg = "black")
    sai_r2.configure(text = "----", fg = "black")
    botao_ok_calc.configure(text = "Calcular", fg ="white", bg = "green", relief = "raised", command = calc_cx)
botao_ok_calc.configure(command = capt_coef)
  
Button(interface, text = "AVANÇAR", font = "batang 7 bold", fg = "white", bg = "black", borderwidth=4, relief="flat", command = printar_val).grid(row = 3, column = 3, padx = 2)

interface.mainloop()

'''
2 leituras - 4 colunas - python=3
3 leituras - 6 colunas - python=5
4 leituras - 8 colunas - python=7
5 leituras -10 colunas - python=9
'''

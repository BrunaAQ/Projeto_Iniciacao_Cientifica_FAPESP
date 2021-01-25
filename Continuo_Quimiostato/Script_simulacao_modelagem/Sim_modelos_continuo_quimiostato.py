# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 13:36:39 2020

@author: Bruna Aparecida
"""

#### **** SIMULAÇÃO E MODELAGEM MODELOS CINÉTICOS NÃO ESTRUTURADOS - CULTIVOS FERMENTATIVOS EM QUIMIOSTATO **** ####

## * Módulos e bibliotecas:
# - Importação de módulos de autoria própria:
import Modulo_Monod_quimiostato
import Modulo_Moser_quimiostato
import Modulo_Contois_quimiostato
import Modulo_peso_limites_quimiostato
import Modulo_Andrews_quimiostato
import Modulo_Wu_et_al_quimiostato
import Modulo_Aiba_et_al_quimiostato
import Modulo_Hoppe_Hansford_quimiostato
import Modulo_Levenspiel_quimiostato
import Modulo_Lee_et_al_quimiostato
# - Importação de pacotes científicos disponíveis:
import numpy as np
import matplotlib.pyplot as plt
import math 
import pandas as pd
import time
from scipy.integrate import odeint
from scipy.optimize import differential_evolution
from scipy.optimize import leastsq
from scipy.optimize import minimize
import scipy.stats as sc

                                                #### **** SIMULAÇÃO **** ####

                    ############################# PARTE FUNCIONAL DO CÓDIGO ######################################

##_______ - Entrada manual do modelo cinético não estruturado desejado para a taxa mi_________##:
modelo = input("Qual modelo deseja simular?\n")
#print(modelo)

# * Função teste condicional * #:
def teste_cont(tipograf_01, tipograf_02, tipograf_03, contador):
    if (modelo == tipograf_01 or modelo == tipograf_02 or modelo == tipograf_03):
        global cont
        cont = contador
        #print(cont)
    
# * - Monod - * #:
teste_cont(tipograf_01 = "Monod", tipograf_02 = "MONOD", tipograf_03 = "monod", contador = 0)
# * - Contois - * #:
teste_cont(tipograf_01 = "Contois", tipograf_02 = "CONTOIS", tipograf_03 = "contois", contador = 1)
# * - Andrews - * #:
teste_cont(tipograf_01 = "Andrews", tipograf_02 = "ANDREWS", tipograf_03 = "andrews", contador = 2)
# * - Aiba et al - * #:
teste_cont(tipograf_01 = "Aiba", tipograf_02 = "AIBA", tipograf_03 = "aiba", contador = 3)
# * - Moser - * #:
teste_cont(tipograf_01 = "Moser", tipograf_02 = "MOSER", tipograf_03 = "moser", contador = 2)
# * - Hoppe & Hansford - * #:
teste_cont(tipograf_01 = "Hoppe", tipograf_02 = "HOPPE", tipograf_03 = "hoppe", contador = 5)
# * - Wu et al - * #:
teste_cont(tipograf_01 = "Wu", tipograf_02 = "WU", tipograf_03 = "wu", contador = 6)
# * - Levenspiel - * #:
teste_cont(tipograf_01 = "Levenspiel", tipograf_02 = "LEVENSPIEL", tipograf_03 = "levenspiel", contador = 7)
# * - Lee et al - * #:
teste_cont(tipograf_01 = "Lee", tipograf_02 = "LEE", tipograf_03 = "lee", contador = 8)
##_______ - Entrada manual do modelo cinético não estruturado desejado para a taxa mi_________##:

##__________Simulação por importação de módulos e funções____________###

# - Funções com os sistemas de equações lineares para o quimiostato:
simul_monod = Modulo_Monod_quimiostato.func_quimiostato_Monod_simul()
simul_contois = Modulo_Contois_quimiostato.func_quimiostato_Contois_simul()
#simul_andrews = Modulo_Andrews_quimiostato.func_quimiostato_Andrews_simul()
#simul_aiba = Modulo_Aiba_et_al_quimiostato.func_quimiostato_Aiba_et_al_simul()
simul_moser = Modulo_Moser_quimiostato.func_quimiostato_Moser_simul()
#simul_hoppe = Modulo_Hoppe_Hansford_quimiostato.func_quimiostato_Hoppe_Hansford_simul()
#simul_wu = Modulo_Wu_et_al_quimiostato.func_quimiostato_Wu_et_al_simul()
#simul_levenspiel = Modulo_Levenspiel_quimiostato.func_quimiostato_Levenspiel_simul()
#simul_lee = Modulo_Lee_et_al_quimiostato.func_quimiostato_Lee_et_al_simul()
list_fun_simul = [simul_monod, simul_contois, simul_moser]

# - Parâmetros operacionais e cinéticos de entrada:
input_monod = Modulo_Monod_quimiostato.entr_Monod()
input_contois = Modulo_Contois_quimiostato.entr_Contois()
#input_andrews = Modulo_Andrews_quimiostato.entr_Andrews()
#input_aiba = Modulo_Aiba_et_al_quimiostato.entr_Aiba_et_al()
input_moser = Modulo_Moser_quimiostato.entr_Moser()
#input_hoppe = Modulo_Hoppe_Hansford_quimiostato.entr_Hoppe_Hansford()
#input_wu = Modulo_Wu_et_al_quimiostato.entr_Wu_et_al()
#input_levenspiel = Modulo_Levenspiel_quimiostato.entr_Levenspiel()
#input_lee = Modulo_Lee_et_al_quimiostato.entr_Lee_et_al()
list_params = [input_monod, input_contois, input_moser]

print("\n------------------------SAÍDAS-------------------------------")
# - Saídas calculadas para cada modelo em função do contador (cont) de controle:
saidas_calculadas = list_fun_simul[cont]
#D = saidas_calculadas[0]
Cx = round(saidas_calculadas[2],4)
Cs = round(saidas_calculadas[1],4)
Cp = round(saidas_calculadas[4],4)
mi = round(saidas_calculadas[3],4)
t = list_params[cont][1]

print('\nCx:', Cx, 'g/L', '\nCs:', Cs, 'g/L', '\nCp:', Cp, 'g/L', '\nTaxa mi:',  mi, '1/h')

# - Criação dos vetores para plotagem e operações matemáticas:
Cx = np.repeat(Cx, len(t))
Cs = np.repeat(Cs, len(t))
Cp = np.repeat(Cp, len(t))
mi = np.repeat(mi, len(t))

C_exp = np.zeros((len(t), 3))
C_exp[:,0] = Cx
C_exp[:,1] = Cs
C_exp[:,2] = Cp  

## * - Cálculo da diluição ótima para a cinética de Monod:
D_otim = list_params[cont][0][0]*(1 - math.sqrt((list_params[cont][0][1]) / (list_params[cont][0][1] + list_params[cont][0][3])))
D_otim = round(D_otim, 4)
print("\nA diluição ótima é dada por", D_otim, "1/h")

## * - Produtividade teórica:
Px_teor = round(saidas_calculadas[8],4)
print('\nA produtividade teórica calculdada é de:', Px_teor, 'gx/l.h')


##__________Simulação por importação de módulos e funções____________###

                            ## _________________ PLOTAGEM GRÁFICA _________________##

def tam_graf():
    # Gráfico batelada e batelada alimentada
    SMALL_SIZE = 20                       
    MEDIUM_SIZE = 24                                             

    ## Comando para determinar o tamanho segundo o qual os textos grafados no gráfico serão impressos na tela:
    plt.rc('font', size=SMALL_SIZE)          
    plt.rc('axes', titlesize=SMALL_SIZE)     
    plt.rc('axes', labelsize=MEDIUM_SIZE)    
    plt.rc('xtick', labelsize=SMALL_SIZE)    
    plt.rc('ytick', labelsize=SMALL_SIZE)    
    plt.rc('legend', fontsize=SMALL_SIZE) 
    

# * _____________________- PERFIL DE CONCENTRAÇÃO -______________________________ * #
     
# - Definição da figura:
tam_graf()
_ = f = plt.figure() 
# Definindo a criação de um gráfico 1x1 com um eixo secundário:    
_ = ax = f.add_subplot(111)                            
_ = lns1 = ax.plot(t, Cx,'red', linewidth=3, label = 'Cx')    
_ = lns2 = ax.plot(t, Cs, linestyle = ':', color = 'blue', linewidth = 3, label = 'Cs')  
_ = ax2 = ax.twinx()
_ = lns3 = ax2.plot(t, Cp, linestyle = '--', color = 'green', linewidth = 4, label = 'Cp')  
_ = ax.set_xlabel('Tempo de cultivo (h)', weight = 'bold')               
_ = ax.set_ylabel('Cx, Cs (g/L)', weight = 'bold')
_ = ax2.set_ylabel('Cp (g/L)', weight = 'bold') 
lns = lns1 + lns2 + lns3 
labs = [l.get_label() for l in lns]
_ = ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.11),ncol = 3, fancybox=True, shadow=True )
_ = ax.grid(True)                                                
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)                                                   
_ = f.patch.set_facecolor('white')                                
_ = plt.style.use('default') 

# * _____________________- PERFIL DE CONCENTRAÇÃO -______________________________ * #

# * _____________________- PERFIL DE VARIAÇÃO DA TAXA DE CRESCIMENTO -______________________________ * #

## Plotando a figura gráfica - velocidade de crescimento: 
tam_graf()   
_ = f = plt.figure() 
_ = ax = f.add_subplot(111)  
_ = plt.plot(t, mi, color = "orange", linewidth=3, label='Velocidade de crescimento')
_ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
_ = plt.ylabel('Taxa $\mu (h^{-1}$)', weight='bold')
_ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.11),ncol=2, fancybox=True, shadow=True)  
_ = plt.grid(True)
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)
_ = f.patch.set_facecolor('white')                                   
_ = plt.style.use('default')   

# * _____________________- PERFIL DE VARIAÇÃO DA TAXA DE CRESCIMENTO -______________________________ * #

# * _____________________- DETERMINAÇÃO DO "PONTO DE LAVAGEM" DO TANQUE -______________________________ * #

# - Importação do vetor D para teste de ponto de lavagem e de Cx e Cs para os valores de mi testados:
D_pont_lav = saidas_calculadas[5]
Cs_pont_lav = saidas_calculadas[6]
Cx_pont_lav = saidas_calculadas[7]


# - Definição da figura:
tam_graf()
_ = f = plt.figure() 
# Definindo a criação de um gráfico 1x1 com um eixo secundário:    
_ = ax = f.add_subplot(111)                            
_ = lns1 = ax.plot(D_pont_lav, Cx_pont_lav,'red', linewidth=3, label = 'Cx')     
_ = ax2 = ax.twinx()
_ = lns2 = ax2.plot(D_pont_lav, Cs_pont_lav, linestyle = ':', color = 'blue', linewidth = 3, label = 'Cs')  
_ = ax.set_xlabel('D (1/h)', weight = 'bold')               
_ = ax.set_ylabel('Cx (g/L)', weight = 'bold')
_ = ax2.set_ylabel('Cs (g/L)', weight = 'bold') 
lns = lns1 + lns2
labs = [l.get_label() for l in lns]
_ = ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.11),ncol = 3, fancybox=True, shadow=True )
_ = ax.grid(True)                                                
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)                                                   
_ = f.patch.set_facecolor('white')                                
_ = plt.style.use('default') 


# * _____________________- DETERMINAÇÃO DO "PONTO DE LAVAGEM" DO TANQUE -______________________________ * #


# * _____________________- DETERMINAÇÃO DA PRODUTIVIDADE EM RELAÇÃO À VAZÃO -______________________________ * #

PxQ = (list_params[cont][2][1] * Cx) / list_params[cont][2][0]

## Plotando a figura gráfica - velocidade de crescimento: 
tam_graf()   
_ = f = plt.figure() 
_ = ax = f.add_subplot(111)  
_ = plt.plot(t, PxQ, color = "purple", linewidth=3, label='Produtividade como função da vazão')
_ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
_ = plt.ylabel('Produtividade (gx/h)', weight='bold')
_ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.11),ncol=2, fancybox=True, shadow=True)  
_ = plt.grid(True)
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)
_ = f.patch.set_facecolor('white')                                   
_ = plt.style.use('default')   

# * _____________________- DETERMINAÇÃO DA PRODUTIVIDADE EM RELAÇÃO À VAZÃO -______________________________ * #

# * _____________________- DETERMINAÇÃO DA PRODUTIVIDADE BIOMASSA E PRODUTO -______________________________ * #

## Cálculo produtividade - celular e do produto:
Px = Cx[1:] / t[1:]
Pp = Cp[1:] / t[1:]

## Plotando a figura gráfica - produtividades:
tam_graf()    
_ = f = plt.figure() 
_ = ax = f.add_subplot(111)  
_ = lns1 = ax.plot(t[1:], Pp, color = "red", linewidth=3, label='Produtividade Celular')
_ = ax2 = ax.twinx()
_ = lns2 = ax2.plot(t[1:], Px, linestyle=":", color = "green", linewidth=3,label='Produtividade do Produto') 
_ = ax.set_xlabel('Tempo de cultivo contínuo (h)',weight='bold')               
_ = ax.set_ylabel('Produtividade Celular (gx/L.h)', weight='bold')
_ = ax2.set_ylabel('Produtividade Produto (gp/L.h)', weight='bold') 
lns = lns1 + lns2
labs = [l.get_label() for l in lns]
_ = ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.11),ncol=2, fancybox=True, shadow=True)  
_ = ax.grid(True)
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)
_ = f.patch.set_facecolor('white')                                   
_ = plt.style.use('default')    
plt.show()

# * _____________________- DETERMINAÇÃO DA PRODUTIVIDADE BIOMASSA E PRODUTO -______________________________ * #  
'''
# * _____________________- DETERMINAÇÃO DA PRODUTIVIDADE ESPECÍFICA -______________________________ * #

## Cálculo produtividade - celular e do produto:
Ppx = Cp / Cx

## Plotando a figura gráfica - produtividades:
tam_graf()   
_ = f = plt.figure() 
_ = ax = f.add_subplot(111)  
_ = plt.plot(t, Ppx, color = "lime", linewidth=3, label='Produtividade específica')
_ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
_ = plt.ylabel('Produtividade espec. (gp/gx)', weight='bold')
_ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.11),ncol=2, fancybox=True, shadow=True)  
_ = plt.grid(True)
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)
_ = f.patch.set_facecolor('white')                                   
_ = plt.style.use('default')  
# * _____________________- DETERMINAÇÃO DA PRODUTIVIDADE BIOMASSA E PRODUTO -______________________________ * #  
'''
                                 ## _________________ PLOTAGEM GRÁFICA _________________##


                                             #### ****  FIM DA SIMULAÇÃO **** ####
print("\n**Status do console pós-simulação**:\nA SIMULAÇÃO FOI CONCLUÍDA COM SUCESSO!!")
print("--------------------------------------------------------------------")

## - Resposta do usuário:
resposta = input("Deseja modelar os resultados simulados?\n")
#print(resposta, cont)


                               #### ****  MODELAGEM DOS DADOS SIMULADOS - CÓDIGO FUNCIONAL **** ####

# - Importação das funções argumento:
args_monod = Modulo_Monod_quimiostato.func_args_quimiostato_Monod()
args_contois = Modulo_Contois_quimiostato.func_args_quimiostato_Contois()
#simul_andrews = Modulo_Andrews_quimiostato.func_args_quimiostato_Andrews()
#simul_aiba = Modulo_Aiba_et_al_quimiostato.func_args_quimiostato_Aiba_et_al()
args_moser = Modulo_Moser_quimiostato.func_args_quimiostato_Moser()
#simul_hoppe = Modulo_Hoppe_Hansford_quimiostato.func_args_quimiostato_Hoppe_Hansford()
#simul_wu = Modulo_Wu_et_al_quimiostato.func_args_quimiostato_Wu_et_al()
#simul_levenspiel = Modulo_Levenspiel_quimiostato.func_args_quimiostato_Levenspiel()
#simul_lee = Modulo_Lee_et_al_quimiostato.func_args_quimiostato_Lee_et_al()
list_fun_args = [args_monod, args_contois]

# - Importação dos limites de convergência para o algoritmo genético AG:
limite_monod = Modulo_peso_limites_quimiostato.limites()[0]
limite_contois = Modulo_peso_limites_quimiostato.limites()[1]
#limite_andrews = Modulo_peso_limites_quimiostato.limites()[3]
#limite_aiba = Modulo_peso_limites_quimiostato.limites()[5]
limite_moser = Modulo_peso_limites_quimiostato.limites()[2]
#limite_hoppe = Modulo_peso_limites_quimiostato.limites()[4]
#limite_wu = Modulo_peso_limites_quimiostato.limites()[6]
#limite_levenspiel = Modulo_peso_limites_quimiostato.limites()[7]
#limite_lee = Modulo_peso_limites_quimiostato.limites()[8]
list_limites_ag = [limite_monod, limite_contois]

# - Importação do peso:
dpC =  Modulo_peso_limites_quimiostato.peso()


def func_quimiostato_Monod_modelag(D, Cs0_alim, mi, *args):
    #params = entr_Monod()[0]
    #oper = entr_Monod()[2]
    mimax = args[0]
    Ks = args[1]
    Yxs = args[2]
    alfa = args[3]
    beta = args[4]
    Q = 0.2
    V = 2
    Cs0_alim = 20
    
    # - Cálculo das variáveis para quantificação:
    D  = Q / V
    Cs_args = (D * Ks)/(mimax - D)
    Cx_args = (Cs0_alim - Cs_args) * Yxs
    mi = mimax*(Cs_args / (Ks + Cs_args))
    Cp_args = (Cx_args * (alfa * mi + beta)) / D

    Cs_args = np.repeat(Cs_args, len(t))
    Cx_args = np.repeat(Cx_args, len(t))
    Cp_args = np.repeat(Cp_args, len(t))
    C_args = np.zeros((len(t), 3))
    C_args[:,0] = Cx_args
    C_args[:,1] = Cs_args
    C_args[:,2] = Cp_args
    return(C_args)
#C_args = func_quimiostato_Monod_modelag()


if (resposta == "Sim" or resposta == "sim"):
    # Aplicar a modelagem por acoplamento AG-ALM:
    # Início da contagem do tempo de convergência computacional:
    start_tempo = time.time() 

    ##*Algoritmo Genético (global)*##
    ## Função com as equações modelo com os parâmetros atribuídos a argumentos:
    func_args = list_fun_args[cont]
    ## Atribuição de pesos a Cx, Cs e Cp para a modelagem (tendência de convergência - ideia de prioridade):
    peso =  dpC
    ## Função objetiva, compara os pontos experimentais com o sistema cinético adotado:
    def func_obj_ag(parametros, *dados):
        t, C_exp = dados
        p = tuple(parametros)
        C_sim = minimize(func_quimiostato_Monod_modelag, (0.2, 2, 10), args=p)
        res = C_sim - C_exp
        for i in range(0,3):
            res[:,i] = res[:,i]/dpC[i]
        res = res.flatten()
        res = sum(res**2)
        return res
    ## Importação dos bounds para aplicação do AG:
    limites = list_limites_ag[cont]
    print(limites)
    # Definição dos argumentos:
    args = (t, C_exp)
    resultado_ag = differential_evolution(func_obj_ag, limites, args = args, popsize=5,  tol=0.01, mutation=(0.5, 1), recombination=0.7, updating='immediate')
    resultado_ag = resultado_ag.x
    resultado_ag = tuple(resultado_ag) 
    
    ##*Algoritmo de Levenberg-Marquardt (local)*##
    ## Função objetiva para o ALM:
    def func_obj_alm(p):
        p = tuple(p)
        C_sim_bat = list_fun_args[cont](args = p)
        res = C_sim_bat - C_exp
        for i in range(0,3):
            res[:,i]=res[:,i]/dpC[i]
        return res.flatten()
    ## Minimização da função objetiva pela função leastsq:
    lance_inic = [resultado_ag]
    resultado_alm = leastsq(func_obj_alm,lance_inic, args=(), Dfun=None, full_output=1)
    param_otim_alm = resultado_alm[0]
    '''
    ## Cálculo do intervalo de confiança (I.C.) correspondente:
    res_otimo_bat = resultado_alm_bat[2]['fvec']
    sensT_otimo_bat =resultado_alm_bat[2]['fjac']
    npar_bat = len(sensT_otimo_bat[:,1])
    ndata_bat = len(sensT_otimo_bat[1,:])
    invXtX_bat = np.linalg.inv(np.matmul(sensT_otimo_bat,sensT_otimo_bat.transpose()))
    sig2y_bat = sum(res_otimo_bat**2) / (ndata_bat-npar_bat)
    covparamers_bat = invXtX_bat*sig2y_bat
    EPpar_bat = np.sqrt(covparamers_bat.diagonal())
    ICpar_bat = EPpar_bat*sc.t.interval(.95, ndata_bat-npar_bat, loc=0, scale=1)[1]
    '''
    ## Armazenamento dos parâmetros otimizados em tuplas:
    param_otim_alm = tuple(param_otim_alm)
    
    
    
else:
    print("\n**Status do console**: \nO ALGORITMO FOI ENCERRADO")
    print("--------------------------------------------------------------------")



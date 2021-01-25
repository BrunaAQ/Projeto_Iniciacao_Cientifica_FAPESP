# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 15:11:48 2020

@author: Bruna Aparecida
"""



                                # MODELO CINÉTICO DE CRESCIMENTO MICROBIANO SEM INIBIÇÃO - CONTOIS #

# Módulos com as funções de: 
# 1) Entrada dos valores iniciais dos parâmetros cinéticos, concentrações iniciais e tempo total de cultivo;
# 2) Simulação

# Importação dos pacotes:
import numpy as np

# Função 1)
def entr_Contois():
    def entr_val_Contois():
        mimaximo = 0.5 #0.45 #unidade 1/h - taxa específica de crescimento
        KSX = 0.2 #3.14 #unidade g/L - constante de semi-saturação
        Kd = 0.1 #0.021  #unidade de 1/h - constante de morte celular
        Cs0_alim = 20 #1.5 # unidade g/L - concentração inicial de microrganismo
        tf = 50 # unidade horas - tempo final da integração
        Yxs = 0.5 #0.6 #unidade g células/g substrato - coeficiente estequiométrico
        alfa = 0.01 #0.05 # unidade g produto/g células - coeficiente estequiométrico
        beta =  0.01 #0 # unidade g produto/g células . h - coeficiente estequiométrico
        V = 2
        Q = 0.2
        t0 = 20
        return(mimaximo, KSX, Kd, Cs0_alim, tf, Yxs, alfa, beta, V, Q, t0)
    mimaximo, KSX, Kd, Cs0_alim, tf, Yxs, alfa, beta, V, Q, t0 = entr_val_Contois()
    entr_val_params = [mimaximo, KSX, Kd, Cs0_alim, tf, Yxs, alfa, beta]
    t = np.arange(t0,tf,0.5)
    entr_val_oper = [V, Q, t0]
    return(entr_val_params, t, entr_val_oper)

# Função 2)
def func_quimiostato_Contois_simul():
    params = entr_Contois()[0]
    oper = entr_Contois()[2]
    mimax = params[0]
    KSX = params[1]
    Yxs = params[5]
    alfa = params[6]
    beta = params[7]
    Q = oper[1]
    V = oper[0]
    Cs0_alim = params[3]
    
    # - Cálculo das variáveis para quantificação:
    D = Q / V
    Cx = (Cs0_alim * (mimax - D)) / ((mimax - D) + (D * KSX * Yxs))
    Cs = (D * KSX * Cx) / (mimax - D)
    mi = mimax*(Cs / ((KSX * Cx) + Cs))
    Cp = (Cx * (alfa * mi + beta)) / D
    
    # - Cálculo do "ponto de lavagem":
    D_pont_lav = np.arange(0, mimax, 0.1)
    ## * Cálculo de Cx e Cs para os valores de mi testados:
    Cx_pont_lav = (Cs0_alim * (mimax - D_pont_lav)) / ((mimax - D_pont_lav) + (D_pont_lav * KSX * Yxs))
    Cs_pont_lav = (D_pont_lav * KSX * Cx_pont_lav) / (mimax - D_pont_lav)
    return(D, Cs, Cx, mi, Cp, D_pont_lav, Cs_pont_lav, Cx_pont_lav)

# Função 3)
def func_args_quimiostato_Contois():  
    def func_quimiostato_Contois_model(C, t, *args):
        params = entr_Contois()[0]
        oper = entr_Contois()[2]
        mimax = args[0]
        KSX = args[1]
        Yxs = args[5]
        alfa = args[6]
        beta = args[7]
        Q = oper[1]
        V = oper[0]
        Cs0_alim = params[3]
    
        # - Cálculo das variáveis para quantificação:
        D = Q / V
        Cx = (Cs0_alim * (mimax - D)) / ((mimax - D) + (D * KSX * Yxs))
        Cs = (D * KSX * Cx) / (mimax - D)
        mi = mimax*(Cs / ((KSX * Cx) + Cs))
        Cp = (Cx * (alfa * mi + beta)) / D
    
        # - Cálculo do "ponto de lavagem":
        D_pont_lav = np.arange(0, mimax, 0.1)
        ## * Cálculo de Cx e Cs para os valores de mi testados:
        Cx_pont_lav = (Cs0_alim * (mimax - D_pont_lav)) / ((mimax - D_pont_lav) + (D_pont_lav * KSX * Yxs))
        Cs_pont_lav = (D_pont_lav * KSX * Cx_pont_lav) / (mimax - D_pont_lav)
        return(D, Cs, Cx, mi, Cp, D_pont_lav, Cs_pont_lav, Cx_pont_lav)
    return(func_args_quimiostato_Contois)

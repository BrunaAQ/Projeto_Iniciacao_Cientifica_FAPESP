# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 15:04:07 2020

@author: Bruna Aparecida
"""


                      # MODELO CINÉTICO DE CRESCIMENTO MICROBIANO INIBIÇÃO PRODUTO - AIBA ET AL #

# Módulos com as funções de: 
# 1) Entrada dos valores iniciais dos parâmetros cinéticos, concentrações iniciais e tempo total de cultivo;
# 2) Simulação

# Importação dos pacotes:
import numpy as np

# Função 1)
def entr_Aiba_et_al():
    def entr_val_Aiba_et_al():
        mimaximo = 0.5 #0.45 #unidade 1/h - taxa específica de crescimento
        Ks = 0.2 #3.14 #unidade g/L - constante de semi-saturação
        Kd = 0.1 #0.021  #unidade de 1/h - constante de morte celular
        Cs0_alim = 20 #1.5 # unidade g/L - concentração inicial de microrganismo
        tf = 50 # unidade horas - tempo final da integração
        Yxs = 0.5 #0.6 #unidade g células/g substrato - coeficiente estequiométrico
        alfa = 0.01 #0.05 # unidade g produto/g células - coeficiente estequiométrico
        beta =  0.01 #0 # unidade g produto/g células . h - coeficiente estequiométrico
        Kp = 10
        V = 2
        Q = 0.2
        t0 = 20
        return(mimaximo, Ks, Kd, Cs0_alim, tf, Yxs, alfa, beta, Kp, V, Q, t0)
    mimaximo, Ks, Kd, Cs0_alim, tf, Yxs, alfa, beta, Kp, V, Q, t0 = entr_val_Aiba_et_al()
    entr_val_params = [mimaximo, Ks, Kd, Cs0_alim, tf, Yxs, alfa, beta, Kp]
    t = np.arange(t0,tf,0.5)
    entr_val_oper = [V, Q, t0]
    return(entr_val_params, t, entr_val_oper)

# Função 2)
def func_quimiostato_Aiba_et_al_simul():
    params = entr_Aiba_et_al()[0]
    oper = entr_Aiba_et_al()[2]
    mimax = params[0]
    Ks = params[1]
    Yxs = params[5]
    alfa = params[6]
    beta = params[7]
    Kp = params[8]
    Q = oper[1]
    V = oper[0]
    Cs0_alim = params[3]
    
    # - Cálculo das variáveis para quantificação:
    D = Q / V
    Cs = (D * Ks)/(mimax - D)
    Cx = (Cs0_alim - Cs) * Yxs
    mult_exp = - Kp * Cp
    mi = mimax * ((Cs / (Ks + Cs)) * np.exp(mult_exp))
    Cp = (Cx * (alfa * mi + beta)) / D
    
    # - Cálculo do "ponto de lavagem":
    D_pont_lav = np.arange(0, mimax, 0.1)
    ## * Cálculo de Cx e Cs para os valores de mi testados:
    Cs_pont_lav = (D_pont_lav * Ks)/(mimax - D_pont_lav)
    Cx_pont_lav = (Cs0_alim - Cs_pont_lav) * Yxs
    return(D, Cs, Cx, mi, Cp, D_pont_lav, Cs_pont_lav, Cx_pont_lav)

# Função 3)
def func_args_quimiostato_Aiba_et_al():
    def func_quimiostato_Aiba_et_al_modelag(C, t, *args):
        params = entr_Aiba_et_al()[0]
        oper = entr_Aiba_et_al()[2]
        mimax = args[0]
        Ks = args[1]
        Yxs = args[5]
        alfa = args[6]
        beta = args[7]
        Kp = args[8]
        Q = oper[1]
        V = oper[0]
        Cs0_alim = params[3]
    
        # - Cálculo das variáveis para quantificação:
        D = Q / V
        Cs = (D * Ks)/(mimax - D)
        Cx = (Cs0_alim - Cs) * Yxs
        mult_exp = - Kp * Cp
        mi = mimax * ((Cs / (Ks + Cs)) * np.exp(mult_exp))
        Cp = (Cx * (alfa * mi + beta)) / D
    
        # - Cálculo do "ponto de lavagem":
        D_pont_lav = np.arange(0, mimax, 0.1)
        ## * Cálculo de Cx e Cs para os valores de mi testados:
        Cs_pont_lav = (D_pont_lav * Ks)/(mimax - D_pont_lav)
        Cx_pont_lav = (Cs0_alim - Cs_pont_lav) * Yxs
        return(D, Cs, Cx, mi, Cp, D_pont_lav, Cs_pont_lav, Cx_pont_lav)
    return(func_args_quimiostato_Aiba_et_al)

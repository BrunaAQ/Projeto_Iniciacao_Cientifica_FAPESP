# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 14:03:25 2020

@author: Bruna Aparecida
"""


                                # MODELO CINÉTICO DE CRESCIMENTO MICROBIANO SEM INIBIÇÃO - MONOD #

# Módulos com as funções de: 
# 1) Entrada dos valores iniciais dos parâmetros cinéticos, concentrações iniciais e tempo total de cultivo;
# 2) Simulação

# Importação dos pacotes:
import numpy as np

# Função 1)
def entr_Monod():
    def entr_val_Monod():
        mimaximo = 0.1168 #0.45 #unidade 1/h - taxa específica de crescimento
        Ks = 3 #3.14 #unidade g/L - constante de semi-saturação
        Kd = 0 #0.021  #unidade de 1/h - constante de morte celular
        Cs0_alim = 30 #1.5 # unidade g/L - concentração inicial de microrganismo
        tf = 53 # unidade horas - tempo final da integração
        Yxs = 0.577 #0.6 #unidade g células/g substrato - coeficiente estequiométrico
        alfa = 0.1 #0.05 # unidade g produto/g células - coeficiente estequiométrico
        beta =  0.8 #0 # unidade g produto/g células . h - coeficiente estequiométrico
        V = 4
        Q = 0.2
        t0 = 45
        return(mimaximo, Ks, Kd, Cs0_alim, tf, Yxs, alfa, beta, V, Q, t0)
    mimaximo, Ks, Kd, Cs0_alim, tf, Yxs, alfa, beta, V, Q, t0 = entr_val_Monod()
    entr_val_params = [mimaximo, Ks, Kd, Cs0_alim, tf, Yxs, alfa, beta]
    t = np.arange(t0,tf,0.5)
    entr_val_oper = [V, Q, t0]
    return(entr_val_params, t, entr_val_oper)

# Função 2)
def func_quimiostato_Monod_simul():
    params = entr_Monod()[0]
    oper = entr_Monod()[2]
    mimax = params[0]
    Ks = params[1]
    Yxs = params[5]
    alfa = params[6]
    beta = params[7]
    Q = oper[1]
    V = oper[0]
    Cs0_alim = params[3]
    
    # - Cálculo das variáveis para quantificação:
    D = Q / V
    Cs = (D * Ks)/(mimax - D)
    Cx = (Cs0_alim - Cs) * Yxs
    mi = mimax*(Cs / (Ks + Cs))
    Cp = (Cx * (alfa * mi + beta)) / D
    
    # - Produtividade específica
    Px = (Q * Cx) / V
    
    # - Cálculo do "ponto de lavagem":
    D_pont_lav = np.arange(0, (0.1 + 0.01), 0.01)
    ## * Cálculo de Cx e Cs para os valores de mi testados:
    Cs_pont_lav = (D_pont_lav * Ks)/(mimax - D_pont_lav)
    Cx_pont_lav = (Cs0_alim - Cs_pont_lav) * Yxs
    return(D, Cs, Cx, mi, Cp, D_pont_lav, Cs_pont_lav, Cx_pont_lav, Px)

def func_args_quimiostato_Monod():
    def func_quimiostato_Monod_modelag(*args):
        params = entr_Monod()[0]
        oper = entr_Monod()[2]
        mimax = args[0]
        Ks = args[1]
        Yxs = args[2]
        alfa = args[3]
        beta = args[4]
        Q = oper[1]
        V = oper[0]
        Cs0_alim = params[3]
    
        # - Cálculo das variáveis para quantificação:
        D = Q / V
        Cs = (D * Ks)/(mimax - D)
        Cx = (Cs0_alim - Cs) * Yxs
        mi = mimax*(Cs / (Ks + Cs))
        Cp = (Cx * (alfa * mi + beta)) / D
    
        # - Cálculo do "ponto de lavagem":
        D_pont_lav = np.arange(0, 0.1, 0.01)
        ## * Cálculo de Cx e Cs para os valores de mi testados:
        Cs_pont_lav = (D_pont_lav * Ks)/(mimax - D_pont_lav)
        Cx_pont_lav = (Cs0_alim - Cs_pont_lav) * Yxs
        return(D, Cs, Cx, Cp, mi, D_pont_lav, Cs_pont_lav, Cx_pont_lav)
    return(func_args_quimiostato_Monod)
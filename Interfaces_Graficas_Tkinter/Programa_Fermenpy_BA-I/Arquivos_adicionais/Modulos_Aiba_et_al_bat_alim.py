# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 20:21:09 2020

@author: Bruna Aparecida
"""

                     # MODELO CINÉTICO DE CRESCIMENTO MICROBIANO COM INIBIÇÃO - AIBA ET AL #

# Módulos com as funções de: 
# 1) Entrada dos valores iniciais dos parâmetros cinéticos, concentrações iniciais e tempo total de cultivo;
# 2) Importação dos dados experimentais de Cx, Cs e Cp diretamente de arquivos .xlsx;
# 3) Modelagem (parâmetros cinéticos passam a ser argumentos na função de integração numérica)

# Importação dos pacotes:
import numpy as np
import pandas as pd

# Função 1)
def entr_Aiba_et_al():
    def entr_val_Aiba_et_al():
        mimaximo = 0.5 #0.45 #unidade 1/h - taxa específica de crescimento
        Ks = 10 #3.14 #unidade g/L - constante de semi-saturação
        Kd = 0.0089 #0.021  #unidade de 1/h - constante de morte celular
        Cx0_bat = 0.1 #1.5 # unidade g/L - concentração inicial de microrganismo
        Cs0_bat = 30 #100  # unidade g/L - concentração inicial de substrato
        Cp0_bat = 0  # unidade g/L - concentração inicial de produto
        tf_bat = 10 # unidade horas - tempo final da integração
        Yxs = 0.2 #0.6 #unidade g células/g substrato - coeficiente estequiométrico
        alfa = 0.3 #0.05 # unidade g produto/g células - coeficiente estequiométrico
        beta =  0.01 #0 # unidade g produto/g células . h - coeficiente estequiométrico
        Kp = 0.08
        Cs0_alim = 200 #500
        tf_alim = 60
        V0 = 2
        Vf = 6
        Q = 0.252
        Q0 = 0.15
        a = 2
        Q0_exp = 0.5
        beta_exp = 0.07
        return(mimaximo,Ks,Kd,Cx0_bat,Cs0_bat,Cp0_bat,tf_bat,Yxs,alfa,beta, Kp, Cs0_alim, tf_alim, V0, Vf, Q, Q0, a, Q0_exp, beta_exp)
    mimaximo, Ks, Kd, Cx0_bat, Cs0_bat, Cp0_bat, tf_bat, Yxs, alfa, beta, Kp, Cs0_alim, tf_alim, V0, Vf, Q, Q0, a, Q0_exp, beta_exp = entr_val_Aiba_et_al()
    entr_val_bat = [mimaximo, Ks, Kd, Cx0_bat, Cs0_bat, Cp0_bat, tf_bat, Yxs, alfa, beta, Kp]
    cond_inic_bat = [entr_val_bat[3],entr_val_bat[4],entr_val_bat[5]]
    t_bat = np.arange(0,tf_bat,0.5)
    entr_val_alim = Cs0_alim, tf_alim, V0, Vf, Q, Q0, a, Q0_exp, beta_exp
    t_alim = np.arange(tf_bat,tf_alim,0.5)
    return(entr_val_bat,cond_inic_bat,t_bat, entr_val_alim, t_alim)

# Função 2)
def modelag_Aiba_et_al_dados_conc_sim():
   importado = pd.read_excel("monod_relatorio_fapesp_maior_int.xlsx","C_t_exp") 
   importado_np = importado.values
   t_exp = importado_np[:,1]
   Cx_exp = importado_np [:,2]
   Cs_exp = importado_np [:,3]
   Cp_exp = importado_np [:,4]
   C_exp = np.zeros((len(t_exp),3))
   C_exp[:,0] = Cx_exp
   C_exp[:,1] = Cs_exp
   C_exp[:,2] = Cp_exp
   return(C_exp, t_exp)

# Função 3)
def modelag_bat_Aiba_et_al_func_args():
    def bat_Aiba_et_al(C, t, *args):
        mimaximo = args[0]
        Ks = args[1]
        Kd = args[2]
        Yxs = args[3]
        alfa = args[4]
        beta = args[5]
        Kp = args[6]
        
        mult_exp = -Kp*C[2]
        mi = mimaximo*((C[1]/(Ks+C[1]))*np.exp(mult_exp))
        dCxdt = (mi - Kd)*C[0]
        dCsdt = (-1/Yxs)*mi*C[0]
        dCpdt = alfa*mi*C[0]+beta*C[0]
        return(dCxdt,dCsdt,dCpdt)
    return(bat_Aiba_et_al)


    

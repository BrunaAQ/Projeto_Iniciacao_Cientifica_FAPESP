                     # MODELO CINÉTICO DE CRESCIMENTO MICROBIANO COM INIBIÇÃO (PRODUTO) - AIBA et al #

# Módulos com as funções de: 
# 1) Entrada dos valores iniciais dos parâmetros cinéticos, concentrações iniciais e tempo total de cultivo;
# 2) Importação dos dados experimentais de Cx, Cs e Cp diretamente de arquivos .xlsx;
# 3) Modelagem (parâmetros cinéticos passam a ser argumentos na função de integração numérica)

# Importação dos pacotes:
import numpy as np
import pandas as pd
import math

# Função 1)
def entr_rand_Aiba_colab():
    def entr_rand_Aiba_colab_gerand():
        mimaximo = 0.5 #unidade 1/hora - taxa específica de crescimento
        Ks = 10 #unidade g/L - constante de semi-saturação
        Kd = 0.089 #unidade de 1/h - constante de morte celular
        Cx0 = 2.5 # unidade g/L - concentração inicial de microrganismo
        Cs0 = 120 # unidade g/L - concentração inicial de substrato
        Cp0 = 0 # unidade g/L - concentração inicial de produto
        tf = 65 # unidade horas - tempo final da integração
        Yxs = 0.65 #unidade g células/g substrato - coeficiente estequiométrico
        alfa = 0.11 # unidade g células/g produto - coeficiente estequiométrico
        beta = 0 
        KIS = 0.6
        return(mimaximo, Ks, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta, KIS)
    mimaximo, Ks, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta, KIS = entr_rand_Aiba_colab_gerand()
    entr_rand_val = [mimaximo, Ks, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta, KIS]
    cond_inic = [Cx0,Cs0,Cp0]
    t = np.arange(0,tf,1.5)
    return(entr_rand_val, cond_inic, t)

# Função 2)
def modelag_bat_Aiba_et_al_dados_conc_sim():
   importado = pd.read_excel("Aiba_bat_gerado_Bruna_param_igual_01.xlsx","C_t_exp") 
   importado_np = importado.values
   t_exp = importado_np[:,0]
   Cx_exp = importado_np [:,1]
   Cs_exp = importado_np [:,2]
   Cp_exp = importado_np [:,3]
   C_exp = np.zeros((len(t_exp),3))
   C_exp[:,0] = Cx_exp
   C_exp[:,1] = Cs_exp
   C_exp[:,2] = Cp_exp
   return(C_exp, t_exp)

# Função 3)
def modelag_bat_Aiba_et_al_func_args():
    def bat_Aiba_colab(C, t, *args):
        mimaximo = args[0]
        Ks = args[1]
        Kd = args[2]
        Yxs = args[3]
        alfa = args[4]
        beta = args[5]
        Kp = args[6]
    
        mult_exp = -Kp*C[2]
        mi=mimaximo*((C[1]/(Ks+C[1]))*math.exp(mult_exp))
        dCxdt=(mi-Kd)*C[0]
        dCsdt=(-1/Yxs)*mi*C[0]
        dCpdt=alfa*mi*C[0]+beta*C[0]
        return(dCxdt,dCsdt,dCpdt)
    return(bat_Aiba_colab)

# Função 4)
def simul_bat_Aiba_et_al():
    def edos_int_bat_Aiba_et_al(C,t):
        Cx,Cs,Cp=C
        mimax_sim = mimax
        Ks_sim = Ks
        Kd_sim = Kd
        Yxs_sim = Yxs
        alfa_sim = alfa
        beta_sim = beta
        Kp_aiba_sim = Kp_aiba
    
        mult_exp = -Cs*Kp_aiba_sim
        mi=mimax_sim*((Cs/(Ks_sim+Cs))*math.exp(mult_exp))
        dCxdt=(mi-Kd_sim)*Cx
        dCsdt=(-1/Yxs_sim)*mi*Cx
        dCpdt=alfa_sim*mi*Cx+beta_sim*Cx
        return(dCxdt,dCsdt,dCpdt)








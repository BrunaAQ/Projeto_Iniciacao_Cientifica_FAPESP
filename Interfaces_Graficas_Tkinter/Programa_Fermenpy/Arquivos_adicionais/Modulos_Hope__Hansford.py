                     # MODELO CINÉTICO DE CRESCIMENTO MICROBIANO COM INIBIÇÃO (PRODUTO) - HOPE & HANSFORD #

# Módulos com as funções de: 
# 1) Entrada dos valores iniciais dos parâmetros cinéticos, concentrações iniciais e tempo total de cultivo;
# 2) Importação dos dados experimentais de Cx, Cs e Cp diretamente de arquivos .xlsx;
# 3) Modelagem (parâmetros cinéticos passam a ser argumentos na função de integração numérica)

# Importação dos pacotes:
import numpy as np
import pandas as pd
import random 

# Função 1)
def entr_rand_Hope_Hansford():
    def entr_rand_Hope_Hansford_gerand():
        mimaximo = random.uniform (0.1 , 0.8) #unidade 1/hora - taxa específica de crescimento
        Ks = random.uniform(0.0 , 10) #unidade g/L - constante de semi-saturação
        Kd = random.uniform(0.0 ,0.4) #unidade de 1/h - constante de morte celular
        Cx0 = random.uniform(0.1, 10) # unidade g/L - concentração inicial de microrganismo
        Cs0 = random.uniform(5.0, 50.0) # unidade g/L - concentração inicial de substrato
        Cp0 = random.uniform(0.0, 10.0)  # unidade g/L - concentração inicial de produto
        tf = random.uniform(5.0, 50.0) # unidade horas - tempo final da integração
        Yxs = random.uniform(0.1, 0.8)#unidade g células/g substrato - coeficiente estequiométrico
        alfa= random.uniform(0.1 , 2) # unidade g células/g produto - coeficiente estequiométrico
        beta = random.uniform(0.0, 1)
        Kp= random.uniform(0.0 , 10)
        return(mimaximo, Ks, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta, Kp)
    mimaximo, Ks, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta, Kp = entr_rand_Hope_Hansford_gerand()
    entr_rand_val = [mimaximo, Ks, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta, Kp]
    cond_inic = [Cx0,Cs0,Cp0]
    t = np.arange(0,tf,0.5)
    return(entr_rand_val, cond_inic, t)

# Função 2)
def modelag_bat_Hope_Hansford_dados_conc_sim():
   importado = pd.read_excel("Dados_conc_sim_bat_Hope_Hansford_modelag.xlsx","C_exp") 
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
def modelag_bat_Hope_Hansford_func_args():
    def bat_Hope_Hansford(C, t, *args):
        mimaximo = args[0]
        Ks = args[1]
        Kd = args[2]
        Yxs = args[3]
        alfa = args[4]
        beta = args[5]
        Kp = args[6]
    
        mi=mimaximo*(C[1]/(Ks+C[1]))*(Kp/(Kp+C[2]))
        dCxdt=(mi-Kd)*C[0]
        dCsdt=(-1/Yxs)*mi*C[0]
        dCpdt=alfa*mi*C[0]+beta*C[0]
        return(dCxdt,dCsdt,dCpdt)
    return(bat_Hope_Hansford)

















                         # MODELO CINÉTICO DE CRESCIMENTO MICROBIANO SEM INIBIÇÃO - CONTOIS #

# Módulos com as funções de: 
# 1) Entrada dos valores iniciais dos parâmetros cinéticos, concentrações iniciais e tempo total de cultivo;
# 2) Importação dos dados experimentais de Cx, Cs e Cp diretamente de arquivos .xlsx;
# 3) Modelagem (parâmetros cinéticos passam a ser argumentos na função de integração numérica)

# Importação dos pacotes:
import numpy as np
import pandas as pd

# Função 1)
def entr_rand_Contois():
    def entr_rand_Contois_gerand():
        mimaximo = 0.7 # unidade 1/hora - taxa específica de crescimento
        KSX = 7.44 # unidade g/L - constante de semi-saturação
        Kd = 0.0146  #unidade de 1/h - constante de morte celular
        Cx0 = 0.85  # unidade g/L - concentração inicial de microrganismo
        Cs0 = 40 # unidade g/L - concentração inicial de substrato
        Cp0 = 0  # unidade g/L - concentração inicial de produto
        tf =  32 # unidade horas - tempo final da integração
        Yxs = 0.5826 #unidade g células/g substrato - coeficiente estequiométrico
        alfa = 0.7778 # unidade g células/g produto - coeficiente estequiométrico
        beta = 0 # unidade g células/g produto . h - coeficiente estequiométrico
        return(mimaximo, KSX, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta)
    mimaximo, KSX, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta = entr_rand_Contois_gerand()
    entr_rand_val = [mimaximo, KSX, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta]
    cond_inic = [Cx0,Cs0,Cp0]
    t = np.arange(0,tf,1.5)
    return(entr_rand_val, cond_inic, t)

# Função 2)
def modelag_bat_Contois_dados_conc_sim():
   importado = pd.read_excel("C_exp_rand_sim_bat_Contois_ref_03.xlsx","C_t_exp") 
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
def modelag_bat_Contois_func_args():
    def bat_Contois(C, t, *args):
        mimaximo = args[0]
        KSX = args[1]
        Kd = args[2]
        Yxs = args[3]
        alfa = args[4]
        beta = args[5]
    
        mi=mimaximo*(C[1]/(KSX*C[0]+C[1]))
        dCxdt=(mi-Kd)*C[0]
        dCsdt=(-1/Yxs)*mi*C[0]
        dCpdt=alfa*mi*C[0]+beta*C[0]
        return(dCxdt,dCsdt,dCpdt)
    return(bat_Contois)

# Função 4)
def simul_bat_Contois():
    def edos_int_bat_Contois(C,t):
        Cx,Cs,Cp=C
        mimax_sim = mimax
        KSX_sim = KSX
        Kd_sim = Kd
        Yxs_sim = Yxs
        alfa_sim = alfa
        beta_sim = beta
        
        mi=mimax_sim*(Cs/((KSX_sim*Cx)+Cs))
        dCxdt=(mi-Kd_sim)*Cx
        dCsdt=(-1/Yxs_sim)*mi*Cx
        dCpdt=alfa_sim*mi*Cx+beta_sim*Cx
        return(dCxdt,dCsdt,dCpdt)
    return(edos_int_bat_Contois)
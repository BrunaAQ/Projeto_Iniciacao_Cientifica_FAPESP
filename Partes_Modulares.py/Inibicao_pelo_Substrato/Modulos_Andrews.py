                # MODELO CINÉTICO DE CRESCIMENTO MICROBIANO COM INIBIÇÃO (SUBSTRATO) - ANDREWS #

# Módulos com as funções de: 
# 1) Entrada dos valores iniciais dos parâmetros cinéticos, concentrações iniciais e tempo total de cultivo;
# 2) Importação dos dados experimentais de Cx, Cs e Cp diretamente de arquivos .xlsx;
# 3) Modelagem (parâmetros cinéticos passam a ser argumentos na função de integração numérica)

# Importação dos pacotes:
import numpy as np
import pandas as pd

# Função 1)
def entr_rand_Andrews():
    def entr_rand_Andrews_gerand():
        mimaximo = 0.45 #unidade 1/h - taxa específica de crescimento
        Ks = 3.14 #unidade g/L - constante de semi-saturação
        Kd = 0.021  #unidade de 1/h - constante de morte celular
        Cx0 = 1.5 # unidade g/L - concentração inicial de microrganismo
        Cs0 = 100  # unidade g/L - concentração inicial de substrato
        Cp0 = 0  # unidade g/L - concentração inicial de produto
        tf = 32 # unidade horas - tempo final da integração
        Yxs = 0.6 # unidade g células/g substrato - coeficiente estequiométrico
        alfa = 0.05 # unidade g produto/g células - coeficiente estequiométrico
        beta = 0 # unidade g produto/g células . h - coeficiente estequiométrico
        KIS = 50 # unidade g/L - constante de inibição pelo substrato
        return(mimaximo, Ks, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta, KIS)
    mimaximo, Ks, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta, KIS = entr_rand_Andrews_gerand()
    entr_rand_val = [mimaximo, Ks, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta, KIS]
    cond_inic = [Cx0,Cs0,Cp0]
    t = np.arange(0,tf,1.5)
    return( entr_rand_val, cond_inic, t)

# Função 2)
def modelag_bat_Andrews_dados_conc_sim():
## Digitar o nome do arquivo acompanhado do da planilha:
   importado = pd.read_excel("Andrews_bat_relat_fapesp.xlsx","C_t_exp") 
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
def modelag_bat_Andrews_func_args():
    def bat_Andrews(C, t, *args):
        mimaximo = args[0]
        Ks = args[1]
        Kd = args[2]
        Yxs = args[3]
        alfa = args[4]
        beta = args[5]
        KIS = args[6]
    
        mi = mimaximo *(C[1]/(Ks + C[1] + ((C[1]**2)/KIS)))
        dCxdt=(mi-Kd)*C[0]
        dCsdt=(-1/Yxs)*mi*C[0]
        dCpdt=alfa*mi*C[0]+beta*C[0]
        return(dCxdt,dCsdt,dCpdt)
    return(bat_Andrews)

# Função 4)
def simul_bat_Andrews():
    def edos_int_bat_Andrews(C,t):
        Cx,Cs,Cp=C
        mimax_sim = mimax
        Ks_sim = Ks
        Kd_sim = Kd
        Yxs_sim = Yxs
        alfa_sim = alfa
        beta_sim = beta
        KIS_sim = KIS
    
        mi=mimax_sim*(Cs/(Ks_sim+Cs+((Cs**2)/KIS_sim)))
        dCxdt=(mi-Kd_sim)*Cx
        dCsdt=(-1/Yxs_sim)*mi*Cx
        dCpdt=alfa_sim*mi*Cx+beta_sim*Cx
        return(dCxdt,dCsdt,dCpdt)

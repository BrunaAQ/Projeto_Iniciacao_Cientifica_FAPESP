                                 # MODELO CINÉTICO DE CRESCIMENTO MICROBIANO SEM INIBIÇÃO - MOSER #

# Módulos com as funções de: 
# 1) Entrada dos valores iniciais dos parâmetros cinéticos, concentrações iniciais e tempo total de cultivo;
# 2) Importação dos dados experimentais de Cx, Cs e Cp diretamente de arquivos .xlsx;
# 3) Modelagem (parâmetros cinéticos passam a ser argumentos na função de integração numérica)

# Importação dos pacotes:
import numpy as np
import pandas as pd

# Função 1)
def entr_rand_Moser():
    def entr_rand_Moser_gerand():
        mimaximo = 0.35 # unidade 1/h - taxa específica de crescimento
        Ks = 9.8 # unidade g/L - constante de semi-saturação
        Kd = 0.0146  # unidade de 1/h - constante de morte celular
        Cx0 = 0.85  # unidade g/L - concentração inicial de microrganismo
        Cs0 = 52 # unidade g/L - concentração inicial de substrato
        Cp0 = 0  # unidade g/L - concentração inicial de produto
        tf =  42 # unidade horas - tempo final da integração
        Yxs = 0.65 #unidade g células/g substrato - coeficiente estequiométrico
        alfa = 0.14 # unidade g produto/g células - coeficiente estequiométrico
        beta = 0 # unidade g produto/g células . h - coeficiente estequiométrico
        u = 2 # adimensional - constante de Moser
        return(mimaximo, Ks, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta, u)
    mimaximo, Ks, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta, u = entr_rand_Moser_gerand()
    entr_rand_val = [mimaximo, Ks, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta, u]
    cond_inic = [Cx0,Cs0,Cp0]
    t = np.arange(0,tf,1.5)
    return(entr_rand_val, cond_inic, t)

# Função 2)
def modelag_bat_Moser_dados_conc_sim():
## Digitar o nome do arquivo acompanhado do da planilha:
   importado = pd.read_excel("C_exp_sim_bat_Moser_gerado_Bruna_param_igual_01.xlsx","C_t_exp") 
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
def modelag_bat_Moser_func_args():
    def bat_Moser(C, t, *args):
        mimaximo = args[0]
        Ks = args[1]
        Kd = args[2]
        Yxs = args[3]
        alfa = args[4]
        beta = args[5]
        u = args[6]
    
        mi=mimaximo*(((C[1])**u)/(Ks+((C[1])**u)))
        dCxdt=(mi-Kd)*C[0]
        dCsdt=(-1/Yxs)*mi*C[0]
        dCpdt=alfa*mi*C[0]+beta*C[0]
        return(dCxdt,dCsdt,dCpdt)
    return(bat_Moser)


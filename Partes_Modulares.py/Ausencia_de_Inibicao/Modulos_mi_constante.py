                     # MODELO CINÉTICO DE CRESCIMENTO MICROBIANO SEM INIBIÇÃO - µ CONSTANTE #

# Módulos com as funções de: 
# 1) Entrada dos valores iniciais dos parâmetros cinéticos, concentrações iniciais e tempo total de cultivo;
# 2) Importação dos dados experimentais de Cx, Cs e Cp diretamente de arquivos .xlsx;
# 3) Modelagem (parâmetros cinéticos passam a ser argumentos na função de integração numérica)

# Importação dos pacotes:
import numpy as np
import pandas as pd

# Função 1)
def entr_rand_mi_const():
    def entr_rand_mi_const_gerand():
        mi = 0.2 #unidade 1/h - taxa específica de crescimento
        Yxs = 0.5  #unidade g células/g substrato - coeficiente estequiométrico
        Kd = 0.04 #unidade de 1/h - constante de morte celular
        Cx0 = 0.2 # unidade g/L - concentração inicial de microrganismo
        Cs0 = 30 # unidade g/L - concentração inicial de substrato
        Cp0 = 0  # unidade g/L - concentração inicial de produto
        tf = 40 # unidade horas - tempo final da integração
        alfa = 0.1  # unidade g produto/g célula - coeficiente estequiométrico
        beta = 0.8 # unidade g produto/g célula . h - coeficiente estequiométrico
        return(mi,Yxs,Kd,Cx0,Cs0,Cp0,tf,alfa,beta)
    mi, Yxs, Kd, Cx0, Cs0, Cp0, tf, alfa, beta = entr_rand_mi_const_gerand()
    entr_rand_val = [mi, Yxs, Kd, Cx0, Cs0, Cp0, tf, alfa, beta]
    cond_inic = [Cx0,Cs0,Cp0]
    t = np.arange(0,tf,0.5)
    return(entr_rand_val,cond_inic,t)

# Função 2)
def modelag_bat_mi_const_dados_conc_sim():
## Digitar o nome do arquivo acompanhado do da planilha:
   importado = pd.read_excel("mi_const_fapesp.xlsx","C_t_exp") 
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
def modelag_bat_mi_const_func_args():
    def mi_constante_bat (C, t, *args):
        mi = args[0]
        Kd = args[1]
        Yxs = args[2]
        alfa = args[3]
        beta = args[4]
        
        dCxdt = (mi-Kd)*C[0]
        dCsdt = - (1/Yxs)*mi*C[0]
        dCpdt = alfa*mi*C[0]+beta*C[0]
        return (dCxdt,dCsdt,dCpdt)
    return(mi_constante_bat)

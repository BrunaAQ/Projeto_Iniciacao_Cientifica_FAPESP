                                  # MODELO CINÉTICO DE CRESCIMENTO MICROBIANO SEM INIBIÇÃO - MONOD #

# Módulos com as funções de: 
# 1) Entrada dos valores iniciais dos parâmetros cinéticos, concentrações iniciais e tempo total de cultivo;
# 2) Importação dos dados experimentais de Cx, Cs e Cp diretamente de arquivos .xlsx;
# 3) Modelagem (parâmetros cinéticos passam a ser argumentos na função de integração numérica)

# Importação dos pacotes:
import numpy as np
import pandas as pd

# Função 1)
def entr_rand_Monod():
    def entr_rand_Monod_gerand():
        mimaximo = 0.46 #0.45 #unidade 1/h - taxa específica de crescimento
        Ks = 8.9 #3.14 #unidade g/L - constante de semi-saturação
        Kd = 0.0074 #0.021  #unidade de 1/h - constante de morte celular
        Cx0 =  0.1 #1.5 # unidade g/L - concentração inicial de microrganismo
        Cs0 = 70 #100  # unidade g/L - concentração inicial de substrato
        Cp0 = 0  # unidade g/L - concentração inicial de produto
        tf = 32 # unidade horas - tempo final da integração
        Yxs = 0.52 #0.6 #unidade g células/g substrato - coeficiente estequiométrico
        alfa = 0.5 #0.05 # unidade g produto/g células - coeficiente estequiométrico
        beta =  0.001 #0 # unidade g produto/g células . h - coeficiente estequiométrico
        return(mimaximo,Ks,Kd,Cx0,Cs0,Cp0,tf,Yxs,alfa,beta)
    mimaximo, Ks, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta = entr_rand_Monod_gerand()
    entr_rand_val = [mimaximo, Ks, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta]
    cond_inic = [entr_rand_val[3],entr_rand_val[4],entr_rand_val[5]]
    t = np.arange(0,tf,1.5)
    return(entr_rand_val,cond_inic,t)

# Função 2)
def modelag_Monod_dados_conc_sim():
## Digitar o nome do arquivo acompanhado do da planilha:
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
def modelag_bat_Monod_func_args():
    def bat_Monod(C, t, *args):
        mimaximo = args[0]
        Ks = args[1]
        Kd = args[2]
        Yxs = args[3]
        alfa = args[4]
        beta = args[5]
        
        mi=mimaximo*(C[1]/(Ks+C[1]))
        dCxdt=(mi-Kd)*C[0]
        dCsdt=(-1/Yxs)*mi*C[0]
        dCpdt=alfa*mi*C[0]+beta*C[0]
        return(dCxdt,dCsdt,dCpdt)
    return(bat_Monod)

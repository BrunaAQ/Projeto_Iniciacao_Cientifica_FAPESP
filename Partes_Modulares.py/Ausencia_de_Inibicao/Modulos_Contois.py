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
        mimaximo = 0.32 # unidade 1/h - taxa específica de crescimento
        KSX = 9.4 # unidade g substrato/g células - constante de semi-saturação (constante de Contois)
        Kd = 0.021  # unidade de 1/h - constante de morte celular
        Cx0 = 0.1  # unidade g/L - concentração inicial de microrganismo
        Cs0 = 80 # unidade g/L - concentração inicial de substrato
        Cp0 = 0  # unidade g/L - concentração inicial de produto
        tf =  70 # unidade horas - tempo final da integração
        Yxs = 0.75 #unidade g células/g substrato - coeficiente estequiométrico
        alfa = 0.51 # unidade g produto/g células - coeficiente estequiométrico
        beta = 0 # unidade g produto/g células . h - coeficiente estequiométrico
        return(mimaximo, KSX, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta)
    mimaximo, KSX, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta = entr_rand_Contois_gerand()
    entr_rand_val = [mimaximo, KSX, Kd, Cx0, Cs0, Cp0, tf, Yxs, alfa, beta]
    cond_inic = [Cx0,Cs0,Cp0]
    t = np.arange(0,tf,1.5)
    return(entr_rand_val, cond_inic, t)

# Função 2)
def modelag_bat_Contois_dados_conc_sim():
## Escrever o nome do arquivo e da planilha; o mesmo deve estar na mesma pasta que o arquivo .py:
   importado = pd.read_excel("Contois_bat_relat_fapesp.xlsx","C_t_exp") 
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



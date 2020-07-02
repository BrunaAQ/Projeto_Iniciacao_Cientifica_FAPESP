                                 # GERAÇÃO DE GRÁFICOS - ADOTADA PARA CÓDIGOS DE SIMULAÇÃO E MODELAGEM#

# Módulos com as funções de: 
# 1) Definição do tamanho da fonte dos eixos;
# 2) Padronização das dimensões e background das figuras geradas.

# Importação dos pacotes:
import matplotlib.pyplot as plt

# Função 1)
def config_plot():
    SMALL_SIZE = 30                       
    MEDIUM_SIZE = 20                       
    BIGGER_SIZE = 20
    plt.rc('font', size=SMALL_SIZE)          
    plt.rc('axes', titlesize=SMALL_SIZE)     
    plt.rc('axes', labelsize=MEDIUM_SIZE)    
    plt.rc('xtick', labelsize=SMALL_SIZE)    
    plt.rc('ytick', labelsize=SMALL_SIZE)    
    plt.rc('legend', fontsize=SMALL_SIZE)    
    plt.rc('figure', titlesize=BIGGER_SIZE)  
    return(config_plot)

# Função 2)
def config_estetica_eixo_unico():
     f = plt.figure()              
     f.set_figheight(5)                                                 
     f.set_figwidth(8)                                                  
     f.patch.set_facecolor('white')                                     
     plt.style.use('default') 
     return(config_estetica_eixo_unico)
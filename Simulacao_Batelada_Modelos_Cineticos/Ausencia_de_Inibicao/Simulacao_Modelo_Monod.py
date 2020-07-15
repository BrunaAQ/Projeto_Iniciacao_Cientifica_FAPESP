# Importação das bibliotecas e módulos necessários:
import Modulos_Monod
import Modulos_configuracao_graficos
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Módulo - geração randômica dos valores de entrada para a simulação
val_ent_rand_Monod = Modulos_Monod.entr_rand_Monod() 

# Modelos matemáticos preditos pelo balanço de massa para batelada com cinética de Monod:
def sim_bat_Monod(C,t):
    Cx,Cs,Cp=C
    sim_bat_Monod_val_entr = val_ent_rand_Monod[0]
    mimaximo = sim_bat_Monod_val_entr[0]
    Ks = sim_bat_Monod_val_entr[1]
    Kd = sim_bat_Monod_val_entr[2]
    Yxs = sim_bat_Monod_val_entr[7]
    alfa = sim_bat_Monod_val_entr[8]
    beta = sim_bat_Monod_val_entr[9]
    
    mi=mimaximo*(Cs/(Ks+Cs))
    dCxdt=(mi-Kd)*Cx
    dCsdt=(-1/Yxs)*mi*Cx
    dCpdt=alfa*mi*Cx+beta*Cx
    return(dCxdt,dCsdt,dCpdt)

# Condições iniciais para integração:
inic_cond = val_ent_rand_Monod[1]
t = val_ent_rand_Monod[2]

# Integrando numericamente:
C = odeint(sim_bat_Monod,inic_cond,t)

#Separando, a partir da matriz Concent, os vetores Cx, Cs e Cp:
Cx = C[:,0]
Cs = C[:,1]
Cp = C[:,2]

# Plotagem gráfica
## Módulos - Funções para definição das dimensões e padrão estético das figuras geradas:
config_eixos = Modulos_configuracao_graficos.config_plot()
config_back = Modulos_configuracao_graficos.config_estetica_eixo_unico()

## Dimensões do gráfico - para aqueles com duplo eixo:
alt = 5
larg = 8

## Função de impressão do gráfico com o perfil das concentrações seguindo o modelo proposto pelo BM:
def imprimir_perfil_concentracao (t_m, Cx_m, Cs_m, Cp_m):
    config_eixos()   
    f = plt.figure() 
    ax = f.add_subplot(111)                                              
    lns1 = ax.plot(t_m,Cx_m,'red',linewidth=3,label='Cx modelo')    
    lns2 = ax.plot(t_m,Cs_m,linestyle=":",color='blue',linewidth=3,label='Cs modelo')  
    ax2 = ax.twinx()
    lns3 = ax2.plot(t_m,Cp_m,linestyle="--",color='green',linewidth=3,label='Cp modelo')     
    ax.set_xlabel('Tempo de cultivo (h)',weight='bold')               
    ax.set_ylabel('Cx, Cs (g/L)', weight='bold')
    ax2.set_ylabel('Cp (g/L)', weight='bold') 
    lns = lns1+lns2+lns3
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.17),ncol=3, fancybox=True, shadow=True )                                              
    ax.grid(True)                                                  
    f.set_figheight(alt)                                                 
    f.set_figwidth(larg)                                                  
    f.patch.set_facecolor('white')                                     
    plt.style.use('default')  
    plt.savefig("Batelada monod simulação.png")
imprimir_perfil_concentracao(t, Cx, Cs, Cp)                            

#Equação que permite calcular a produtividade celular (Px):
Px=Cx[1:]/t[1:]
#Equação que permite calcular a produtividade do produto (Pp):
Pp=Cp[1:]/t[1:] 

## Função para impressão do gráfico com o perfil de produtividade celular e do produto:
def imprimir_produtividade_celular_produto (t_m, Px_m, Pp_m):
    config_eixos() 
    f = plt.figure() 
    ax = f.add_subplot(111)                
    lns1 = ax.plot(t_m,Px_m,'red',linewidth=3,label='Produtividade celular')      
    ax2 = ax.twinx()
    lns2 = ax2.plot(t_m,Pp_m,linestyle='--',color='green',linewidth=4,label='Produtividde metabólito')    
    ax.set_xlabel('Tempo de cultivo (h)',weight='bold')               
    ax.set_ylabel('Produtividade Celular (gx/L.h)', weight='bold')
    ax2.set_ylabel('Produtividade Produto (gp/L.h)', weight='bold') 
    lns = lns1+lns2
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.17),ncol=2, fancybox=True, shadow=True )                                              
    ax.grid(True) 
    f.set_figheight(alt)                                                 
    f.set_figwidth(larg)                                                  
    f.patch.set_facecolor('white')                                     
    plt.style.use('default') 
    plt.show() 
    plt.savefig("Batelada monod simulação produtividade celular e do produto.png")
imprimir_produtividade_celular_produto(t[1:], Px, Pp)

#Equação que permite calcular a produtividade específica (Ppx):
Ppx=Cp*(1/Cx)

## Função para impressão do gráfico com o perfil de produtividade específica:
def imprimir_produtividade_especifica (t_m, Ppx_m):
    config_back()
    config_eixos()                                             
    plt.plot(t_m,Ppx_m,'red',linewidth=4)     
    plt.xlabel('Tempo de cultivo (h)',weight='bold')               
    plt.ylabel('Produtividade Específica (gp/gx)', weight='bold')    
    plt.grid(True)                                                       
    plt.show()      
    plt.savefig("Batelada monod simulação produtividade específica.png")                  
imprimir_produtividade_especifica(t, Ppx)

# Cálculo do valor de mi para cada tempo:
mi=val_ent_rand_Monod[0][0]*(Cs/(val_ent_rand_Monod[0][1]+Cs))

## Função para impressão do gráfico com o perfil da variação temporal da taxa específica de crescimento:
def imprimir_taxa_especifica_crescimento (t_m, mi_m):
    config_back()
    config_eixos()                                              
    plt.plot(t_m,mi_m,'red',linewidth=4)     
    plt.xlabel('Tempo de cultivo (h)',weight='bold')               
    plt.ylabel('Taxa $\mu(h^{-1}$)', weight='bold') 
    plt.grid(True)
    plt.show()     
    plt.savefig("Batelada monod simulação variação mi com o tempo.png")
imprimir_taxa_especifica_crescimento(t, mi)

# Inserindo 0 para o primeiro valor de produtividade:
Px = np.insert(Px,0,Px[0])
Pp = np.insert(Pp,0,Pp[0])

# Criando um vetor concentração único:
C = np.zeros((len(t),3))
C[:,0] = Cx
C[:,1] = Cs
C[:,2] = Cp

## Trecho de código opcional:
'''
# Atribuição de ruídos randômicos:
for i in range(0,3):
    C_i = C[:,i]
    C[:,i] = abs(C_i + np.random.randn(len(C_i)) * 0.5)
'''
#Criando a função que permite a geração do output dos valores de saída:
df_concents_produt = pd.DataFrame({'Tempo(h)': t, 'Cx(g/L)': C[:,0], 'Cs(g/L)': C[:,1], 'Cp(g/L)': C[:,2],'mi(h-¹)':mi,
                           'Px(gcél/L.h)': Px, 'Pp(gprod/L.h)': Pp, 'Ppx(gprod/gcél)':Ppx})
df_params_sim = pd.DataFrame({'mimáx_sim(h-¹)':[val_ent_rand_Monod[0][0]],'Ks_sim(g/L)':[val_ent_rand_Monod[0][1]],
                              'Kd_sim(h-¹)':[val_ent_rand_Monod[0][2]], 'Yxs_sim(gcél/gsubs)':[val_ent_rand_Monod[0][7]],
                              'alfa(gprod/gcél)':[val_ent_rand_Monod[0][8]], 'beta_sim(gprod/gcél.h)':[val_ent_rand_Monod[0][9]]})
df_saida_Monod = pd.concat([df_concents_produt, df_params_sim], axis=1)
with pd.ExcelWriter('Nome_arquivo_output_Monod.xlsx') as writer:
    df_saida_Monod.to_excel(writer, sheet_name="Saída_Monod")
    writer.save()
    

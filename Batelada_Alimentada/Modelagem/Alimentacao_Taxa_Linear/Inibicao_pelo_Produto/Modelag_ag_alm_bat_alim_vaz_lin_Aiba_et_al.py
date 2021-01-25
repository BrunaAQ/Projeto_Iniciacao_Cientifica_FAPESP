# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 10:53:00 2020

@author: Bruna Aparecida
"""

                    ## MODELAGEM BATELADA ALIMENTADA À VAZÃO LINEAR CINÉTICA DE AIBA ET AL ##

# Importação das bibliotecas necessárias para as partes não modulares:
import Modulos_Aiba_et_al_bat_alim
import Modulo_peso_limite_AG
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import differential_evolution
from scipy.optimize import leastsq
import scipy.stats as sc
import time

## Separação do processo em batelada (etapa 1) e batelada alimentada (etapa 2):


                        # PRIMEIRO PASSO: simulação de dados para Cx, Cs e Cp:
        #*ETAPA 1*# - BATELADA
## Módulos:
### Valores dos parâmetros do modelo e condição inicial:
dad_entr_geral = Modulos_Aiba_et_al_bat_alim.entr_Aiba_et_al()
## Valor de entrada dos parâmetros cinéticos
pars_entr = dad_entr_geral[0]
mimaximo = pars_entr[0]
Ks = pars_entr[1]
Yxs = pars_entr[7]
alfa = pars_entr[8]
beta = pars_entr[9]
Kp = pars_entr[10]

## Integração numérica (sistema de EDOs):
def bat_Aiba_et_al(Concent,t_exp_bat):
    Cx,Cs,Cp = Concent
    mult_exp = -Kp*Cp
    mi = mimaximo*((Cs/(Ks+Cs))*np.exp(mult_exp))
    dCxdt = mi*Cx
    dCsdt = (-1/Yxs)*mi*Cx
    dCpdt = alfa*mi*Cx+beta*Cx
    return(dCxdt,dCsdt,dCpdt)
### Condições de integração:
cond_inic_bat = dad_entr_geral[1]
t_exp_bat = dad_entr_geral[2]
### Matriz de retorno:
C_exp_bat = odeint(bat_Aiba_et_al, cond_inic_bat, t_exp_bat)

        #*ETAPA 2*# - BATELADA ALIMENTADA
## Módulos:
### Valores dos parâmetros operacionais e condição inicial:
param_oper_alim = dad_entr_geral[3]
Cs0_corrent_alim = param_oper_alim[0]
V0 = param_oper_alim[2]
Vf = param_oper_alim[3]
Q0 = param_oper_alim[5]
a = param_oper_alim[6]

## Integração numérica (sistema de EDOs):
def bat_alim_Aiba_et_al(Concent,t_exp_alim):
    Cx,Cs,Cp = Concent
    mult_exp = -Kp*Cp
    mi = mimaximo*((Cs/(Ks+Cs))*np.exp(mult_exp))
    D = (Q0*(1 + a*t_exp_alim))/((Q0*(t_exp_alim + (a*t_exp_alim**2))) + V0)
    dCxdt = (mi-D)*Cx
    dCsdt = D*(Cs0_corrent_alim-Cs)-((mi*Cx)/Yxs)
    dCpdt = D*(Cp0_alim-Cp)+Cx*(beta+alfa*mi)
    return(dCxdt,dCsdt,dCpdt)
### Condições de integração:
#### Condição inicial - Valores finais da batelada vão ser os iniciais da batelada alimentada:
Cx0_alim = C_exp_bat[:,0][len(C_exp_bat[:,0])-1]   
Cs0_alim = C_exp_bat[:,1][len(C_exp_bat[:,1])-1]
Cp0_alim = C_exp_bat[:,2][len(C_exp_bat[:,2])-1]   
cond_inic_alim = [Cx0_alim, Cs0_alim, Cp0_alim]
t_exp_alim = dad_entr_geral[4]
### Matriz de retorno:
C_exp_alim = odeint(bat_alim_Aiba_et_al, cond_inic_alim, t_exp_alim)


                # SEGUNDO PASSO: aplicar a modelagem por acoplamento AG-ALM:

# Início da contagem do tempo de convergência computacional:
start_tempo = time.time() 

     #*ETAPA 1*# - BATELADA
  ##*Algoritmo Genético (global)*##
# Módulos
## Função com as equações modelo com os parâmetros atribuídos a argumentos:
func_args_bat = Modulos_Aiba_et_al_bat_alim.modelag_bat_Aiba_et_al_func_args()
## Atribuição de pesos a Cx, Cs e Cp para a modelagem (tendência de convergência - ideia de prioridade):
dpC = Modulo_peso_limite_AG.peso()
## Função objetiva, compara os pontos experimentais com o sistema cinético adotado:
def func_obj_ag_bat(parametros, *dados):
    t_exp,C_exp = dados
    p = tuple(parametros)
    C_sim = odeint(func_args_bat, cond_inic_bat, t_exp_bat, args = p)
    res = C_sim - C_exp
    for i in range(0,3):
        res[:,i] = res[:,i]/dpC[i]
    res = res.flatten()
    res = sum(res**2)
    return res
## Importação dos bounds para aplicação do AG:
limites_Aiba_et_al = Modulo_peso_limite_AG.limites()[5]
# Definição dos argumentos:
args = (t_exp_bat,C_exp_bat)
resultado_ag_bat = differential_evolution(func_obj_ag_bat, limites_Aiba_et_al, args=args, popsize=5,  tol=0.01, mutation=(0.5, 1), recombination=0.7, updating='immediate')
resultado_ag_bat = resultado_ag_bat.x
resultado_ag_bat = tuple(resultado_ag_bat)

  ##*Algoritmo de Levenberg-Marquardt (local)*##
## Função objetiva para o ALM:
def func_obj_alm_bat(p):
    p = tuple(p)
    C_sim_bat = odeint(func_args_bat,cond_inic_bat,t_exp_bat,args=p)
    res = C_sim_bat - C_exp_bat
    for i in range(0,3):
        res[:,i]=res[:,i]/dpC[i]
    return res.flatten()
## Minimização da função objetiva pela função leastsq:
lance_inic_bat = [resultado_ag_bat]
resultado_alm_bat = leastsq(func_obj_alm_bat,lance_inic_bat, args=(), Dfun=None, full_output=1)
param_otim_alm_bat = resultado_alm_bat[0]
'''
## Cálculo do intervalo de confiança (I.C.) correspondente:
res_otimo_bat = resultado_alm_bat[2]['fvec']
sensT_otimo_bat =resultado_alm_bat[2]['fjac']

npar_bat = len(sensT_otimo_bat[:,1])
ndata_bat = len(sensT_otimo_bat[1,:])
invXtX_bat = np.linalg.inv(np.matmul(sensT_otimo_bat,sensT_otimo_bat.transpose()))
sig2y_bat = sum(res_otimo_bat**2) / (ndata_bat-npar_bat)
covparamers_bat = invXtX_bat*sig2y_bat
EPpar_bat = np.sqrt(covparamers_bat.diagonal())
ICpar_bat = EPpar_bat*sc.t.interval(.95, ndata_bat-npar_bat, loc=0, scale=1)[1]
'''
## Armazenamento dos parâmetros otimizados em tuplas:
param_otim_alm_bat = tuple(param_otim_alm_bat)
## Tempo modelo:
t_bat = np.arange(0, t_exp_bat[-1], 0.1)
## Integrando com os valores dos parâmetros ajustados:
C_otim_bat = odeint(func_args_bat, cond_inic_bat, t_bat, args = (param_otim_alm_bat))

    #*ETAPA 2*# - BATELADA ALIMENTADA
  ##*Algoritmo Genético (global)*##
# Função com as equações modelo com os parâmetros atribuídos a argumentos:
def func_args_alim(C, t_exp_alim, *args):
    mimaximo = args[0]
    Ks = args[1]
    Yxs = args[2]
    alfa = args[3]
    beta = args[4]
    Kp = args[5]
        
    mult_exp = -Kp*C[2]
    mi = mimaximo*((C[1]/(Ks + C[1]))*np.exp(mult_exp))
    D = (Q0*(1 + a*t_exp_alim))/((Q0*(t_exp_alim + (a*t_exp_alim**2))) + V0)
    dCxdt = (mi - D)*C[0]
    dCsdt = D*(Cs0_corrent_alim - C[1]) - ((mi*C[0])/Yxs)
    dCpdt = D*(Cp0_alim - C[2]) + C[0]*(beta + alfa*mi)
    return(dCxdt,dCsdt,dCpdt)
# Módulos
## Função objetiva, compara os pontos experimentais com o sistema cinético adotado:
def func_obj_ag_alim(parametros, *dados):
    t_exp_alim,C_exp_alim = dados
    p = tuple(parametros)
    C_sim_alim = odeint(func_args_alim, cond_inic_alim, t_exp_alim, args = p)
    res = C_sim_alim - C_exp_alim
    for i in range(0,3):
        res[:,i] = res[:,i]/dpC[i]
    res = res.flatten()
    res = sum(res**2)
    return res
# Definição dos argumentos:
args = (t_exp_alim,C_exp_alim)
resultado_ag_alim = differential_evolution(func_obj_ag_alim, limites_Aiba_et_al, args = args, popsize=5,  tol=0.01, mutation=(0.5, 1), recombination=0.7, updating='immediate')
resultado_ag_alim = resultado_ag_alim.x
resultado_ag_alim = tuple(resultado_ag_alim)

 ##*Algoritmo de Levenberg-Marquardt (local)*##
## Função objetiva para o ALM:
def func_obj_alm_alim(p):
    p = tuple(p)
    C_sim_alim = odeint(func_args_alim,cond_inic_alim,t_exp_alim,args=p)
    res = C_sim_alim - C_exp_alim
    for i in range(0,3):
        res[:,i]=res[:,i]/dpC[i]
    return res.flatten()
## Minimização da função objetiva pela função leastsq:
lance_inic_alim= [resultado_ag_alim]
resultado_alm_alim = leastsq(func_obj_alm_alim,lance_inic_alim, args=(), Dfun=None, full_output=1)
param_otim_alm_alim = resultado_alm_alim[0]
'''
## Cálculo do intervalo de confiança (I.C.) correspondente:
res_otimo_alim = resultado_alm_alim[2]['fvec']
sensT_otimo_alim =resultado_alm_alim[2]['fjac']

npar_alim = len(sensT_otimo_alim[:,1])
ndata_alim = len(sensT_otimo_alim[1,:])
invXtX_alim = np.linalg.inv(np.matmul(sensT_otimo_alim,sensT_otimo_alim.transpose()))
sig2y_alim = sum(res_otimo_alim**2) / (ndata_alim-npar_alim)
covparamers_alim = invXtX_alim*sig2y_alim
EPpar_alim = np.sqrt(covparamers_alim.diagonal())
ICpar_alim = EPpar_alim*sc.t.interval(.95, ndata_alim-npar_alim, loc=0, scale=1)[1]
'''
## Armazenamento dos parâmetros otimizados em tuplas:
param_otim_alm_alim = tuple(param_otim_alm_alim)
## Tempo modelo:
t_alim = np.arange(dad_entr_geral[0][6], t_exp_alim[-1], 0.1) 
## Integrando com os valores dos parâmetros ajustados:
Cx0_otim_alim = C_otim_bat[:,0][len(C_otim_bat[:,0])-1]   
Cs0_otim_alim = C_otim_bat[:,1][len(C_otim_bat[:,1])-1]
Cp0_otim_alim = C_otim_bat[:,2][len(C_otim_bat[:,2])-1]
cond_inic_alim = [Cx0_otim_alim, Cs0_otim_alim, Cp0_otim_alim]
C_otim_alim = odeint(func_args_alim, cond_inic_alim, t_alim, args = (param_otim_alm_alim))

## Parada da contagem do tempo de convergência total:
fim = time.time()
tempo_converg = fim - start_tempo

                                            ###***Impressão valores de saída***###

print("____________Saída Geral____________")
# Tempo de convergência requerido:
print("Tempo de modelagem:", tempo_converg, "s")
#*ETAPA 1*#
print("____________Resultados para batelada____________")
print("mimaxixo_bat:",resultado_alm_bat[0][0])#,"+/-",ICpar_bat[0],"(h-1)")
print("Ks_bat:",resultado_alm_bat[0][1])#,"+/-",ICpar_bat[1],"(g/l)")
print("Yxs_bat:",resultado_alm_bat[0][2])#,"+/-",ICpar_bat[2],"(gx/gs)")
print("alfa_bat:",resultado_alm_bat[0][3])#,"+/-",ICpar_bat[3],"(gp/gx)")
print("beta_bat:",resultado_alm_bat[0][4])#,"+/-",ICpar_bat[4],"[gp/(gx.h)]")
print("Kp_bat:",resultado_alm_bat[0][5])#,"+/-",ICpar_bat[5],"[l/g]")
#*ETAPA 2*#
print("____________Resultados para batelada alimentada____________")
print("mimaxixo_alim:",resultado_alm_alim[0][0])#,"+/-",ICpar_alim[0],"(h-1)")
print("Ks_alim:",resultado_alm_alim[0][1])#,"+/-",ICpar_alim[1],"(g/l)")
print("Yxs_alim:",resultado_alm_alim[0][2])#,"+/-",ICpar_alim[2],"(gx/gs)")
print("alfa_alim:",resultado_alm_alim[0][3])#,"+/-",ICpar_alim[3],"(gp/gx)")
print("beta_alim:",resultado_alm_alim[0][4])#,"+/-",ICpar_alim[4],"[gp/(gx.h)]")
print("Kp_alim:",resultado_alm_alim[0][5])#"+/-",ICpar_bat[5],"[l/(g)]")

                                                  ###***Impressão gráfica***###

## União das matrizes C_exp_bat e C_exp_alim:
    #*ETAPA 1*# - BATELADA
Cx_exp_bat = C_exp_bat[:,0]
Cx_bat = C_otim_bat[:,0]
Cs_exp_bat = C_exp_bat[:,1]
Cs_bat = C_otim_bat[:,1]
Cp_exp_bat = C_exp_bat[:,2]
Cp_bat = C_otim_bat[:,2]
    #*ETAPA 2*# - BATELADA ALIMENTADA
Cx_exp_alim = C_exp_alim[:,0]
Cx_alim = C_otim_alim[:,0]
Cs_exp_alim = C_exp_alim[:,1]
Cs_alim = C_otim_alim[:,1]
Cp_exp_alim = C_exp_alim[:,2]
Cp_alim = C_otim_alim[:,2]

### Contadores gerais:
    #*ETAPA 1*# - BATELADA
limite_bat_exp = len(C_exp_bat)
limite_alim_exp = len(C_exp_alim)
limite_bat = len(C_otim_bat)
limite_alim = len(C_otim_alim)

Cx_exp = []
Cs_exp = []
Cp_exp = []
Cx = []
Cs = []
Cp = []
bat_exp = 0
alim_exp = 0
bat = 0
alim = 0
while (bat_exp < limite_bat_exp):
    Cx_exp.append(Cx_exp_bat[bat_exp])
    Cs_exp.append(Cs_exp_bat[bat_exp])
    Cp_exp.append(Cp_exp_bat[bat_exp])
    bat_exp = bat_exp + 1     
while (bat < limite_bat):
    Cx.append(Cx_bat[bat])
    Cs.append(Cs_bat[bat])
    Cp.append(Cp_bat[bat]) 
    bat = bat + 1    
while (alim_exp < limite_alim_exp):
    Cx_exp.append(Cx_exp_alim[alim_exp])
    Cs_exp.append(Cs_exp_alim[alim_exp])
    Cp_exp.append(Cp_exp_alim[alim_exp])
    alim_exp = alim_exp + 1
while (alim < limite_alim):
    Cx.append(Cx_alim[alim])
    Cs.append(Cs_alim[alim])
    Cp.append(Cp_alim[alim])
    alim = alim + 1
    
divisor = len(Cx)

## Vetor tempo total do processo:
Ttotal_exp = np.arange(0,param_oper_alim[1],0.5)
divisor = len(Cx)
Ttotal = np.linspace (0,param_oper_alim[1],divisor)

## Conversão das listas para arrays - necessário para operações matemáticas:
Cx_exp = np.asarray(Cx_exp)
Cs_exp = np.asarray(Cs_exp)
Cp_exp = np.asarray(Cp_exp)
Cx = np.asarray(Cx)
Cs = np.asarray(Cs)
Cp = np.asarray(Cp)


def tam_graf():
    # Gráfico batelada e batelada alimentada
    SMALL_SIZE = 20                       
    MEDIUM_SIZE = 24                                             

    ## Comando para determinar o tamanho segundo o qual os textos grafados no gráfico serão impressos na tela:
    plt.rc('font', size=SMALL_SIZE)          
    plt.rc('axes', titlesize=SMALL_SIZE)     
    plt.rc('axes', labelsize=MEDIUM_SIZE)    
    plt.rc('xtick', labelsize=SMALL_SIZE)    
    plt.rc('ytick', labelsize=SMALL_SIZE)    
    plt.rc('legend', fontsize=SMALL_SIZE)      

# Gráfico perfil de concentração:
# Definindo a figura que será gerada - batelada:
tam_graf()
_ = f = plt.figure() 
_ = ax = f.add_subplot(111)    
_ = lns1 = ax.plot(t_bat,C_otim_bat[:,0], color = "red", linewidth = 3,label ='Cx modelo')
_ = lns2 = ax.plot(t_exp_bat,C_exp_bat[:,0],'o',color = "red",markersize = 6, label = 'Cx experimental')
_ = lns3 = ax.plot(t_bat,C_otim_bat[:,1], linestyle="--", color = "green",linewidth = 3,label = 'Cs modelo')  
_ = lns4 = ax.plot(t_exp_bat ,C_exp_bat[:,1],'^',color = "green", markersize = 6,label = 'Cs experimental')
ax2 = ax.twinx()
_ = lns5 = ax2.plot(t_bat,C_otim_bat[:,2],linestyle = ":", color = "blue",linewidth = 3,label = 'Cp modelo') 
_ = lns6 = ax2.plot(t_exp_bat,C_exp_bat[:,2],'s',color = "blue", markersize = 6,label = 'Cp experimental')
_ = ax.set_xlabel('Tempo de cultivo (h)',weight='bold')               
_ = ax.set_ylabel('Cx e Cs (g/L)', weight='bold')
_ = ax2.set_ylabel('Cp (g/L)', weight='bold') 
lns = lns1+lns2+lns3+lns4+lns5+lns6
labs = [l.get_label() for l in lns]
_ = ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.17),ncol=3, fancybox=True, shadow=True)                                                
_ = ax.grid(True)
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)                                                   
_ = f.patch.set_facecolor('white')                                
_ = plt.style.use('default') 

# Definindo a figura que será gerada - batelada alimentada:
tam_graf()
_ = f = plt.figure() 
_ = ax = f.add_subplot(111)    
_ = lns1 = ax.plot(t_alim,C_otim_alim[:,0], color = "red", linewidth = 3,label ='Cx modelo')
_ = lns2 = ax.plot(t_exp_alim,C_exp_alim[:,0],'o',color = "red",markersize = 6, label = 'Cx experimental')
_ = lns3 = ax.plot(t_alim,C_otim_alim[:,1], linestyle="--", color = "green",linewidth = 3,label = 'Cs modelo')  
_ = lns4 = ax.plot(t_exp_alim,C_exp_alim[:,1],'^',color = "green", markersize = 6,label = 'Cs experimental')
ax2 = ax.twinx()
_ = lns5 = ax2.plot(t_alim,C_otim_alim[:,2],linestyle = ":", color = "blue",linewidth = 3,label = 'Cp modelo') 
_ = lns6 = ax2.plot(t_exp_alim,C_exp_alim[:,2],'s',color = "blue", markersize = 6,label = 'Cp experimental')
_ = ax.set_xlabel('Tempo de cultivo (h)',weight='bold')               
_ = ax.set_ylabel('Cx e Cs (g/L)', weight='bold')
_ = ax2.set_ylabel('Cp (g/L)', weight='bold') 
lns = lns1+lns2+lns3+lns4+lns5+lns6
labs = [l.get_label() for l in lns]
_ = ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.17),ncol=3, fancybox=True, shadow=True)                                                
_ = ax.grid(True)
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)                                                   
_ = f.patch.set_facecolor('white')                                
_ = plt.style.use('default') 

# Definindo a figura que será gerada - processos acoplados:
tam_graf()
_ = f = plt.figure() 
_ = ax = f.add_subplot(111)    
_ = lns1 = ax.plot(t_bat,C_otim_bat[:,0], color = "red", linewidth = 3,label ='Cx modelo')
_ = lns2 = ax.plot(t_exp_bat,C_exp_bat[:,0],'o',color = "red",markersize = 6, label = 'Cx experimental')
_ = lns3 = ax.plot(t_bat,C_otim_bat[:,1], linestyle="--", color = "green",linewidth = 3,label = 'Cs modelo')  
_ = lns4 = ax.plot(t_exp_bat ,C_exp_bat[:,1],'^',color = "green", markersize = 6,label = 'Cs experimental')
ax2 = ax.twinx()
_ = lns5 = ax2.plot(t_bat,C_otim_bat[:,2],linestyle = ":", color = "blue",linewidth = 3,label = 'Cp modelo') 
_ = lns6 = ax2.plot(t_exp_bat,C_exp_bat[:,2],'s',color = "blue", markersize = 6,label = 'Cp experimental')
_ = ax.set_xlabel('Tempo de cultivo (h)',weight='bold')               
_ = ax.set_ylabel('Cx e Cs (g/L)', weight='bold')
_ = ax2.set_ylabel('Cp (g/L)', weight='bold') 
lns = lns1+lns2+lns3+lns4+lns5+lns6
labs = [l.get_label() for l in lns]
_ = ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.17),ncol=3, fancybox=True, shadow=True)                                                
_ = ax.grid(True)
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)                                                   
_ = f.patch.set_facecolor('white')                                
_ = plt.style.use('default') 

# Definindo a figura que será gerada - batelada alimentada:
tam_graf()
_ = f = plt.figure() 
_ = ax = f.add_subplot(111)    
_ = lns1 = ax.plot(Ttotal,Cx, color = "red", linewidth = 3,label ='Cx modelo')
_ = lns2 = ax.plot(Ttotal_exp,Cx_exp,'o',color = "red",markersize = 6, label = 'Cx experimental')
_ = lns3 = ax.plot(Ttotal,Cp, linestyle="--", color = "green",linewidth = 3,label = 'Cp modelo')  
_ = lns4 = ax.plot(Ttotal_exp,Cp_exp,'^',color = "green", markersize = 6,label = 'Cp experimental')
ax2 = ax.twinx()
_ = lns5 = ax2.plot(Ttotal,Cs,linestyle = ":", color = "blue",linewidth = 3,label = 'Cs modelo') 
_ = lns6 = ax2.plot(Ttotal_exp,Cs_exp,'s',color = "blue", markersize = 6,label = 'Cs experimental')
_ = ax.axvline(x = dad_entr_geral[0][6], color = "grey", linestyle="dashed", linewidth=3)
_ = ax.set_xlabel('Tempo de cultivo (h)',weight='bold')               
_ = ax.set_ylabel('Cx e Cp (g/L)', weight='bold')
_ = ax2.set_ylabel('Cs (g/L)', weight='bold') 
lns = lns1 + lns2 + lns3 + lns4 + lns5 + lns6
labs = [l.get_label() for l in lns]
_ = ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.17),ncol=3, fancybox=True, shadow=True)                                                
_ = ax.grid(True)
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)                                                   
_ = f.patch.set_facecolor('white')                                
_ = plt.style.use('default') 

## Cálculo produtividade volumétrica modelo e experimental - celular e do produto:
Px_exp = Cx_exp[1:]/Ttotal_exp[1:]
Pp_exp = Cp_exp[1:]/Ttotal_exp[1:]
Px = Cx[1:]/Ttotal[1:]
Pp = Cp[1:]/Ttotal[1:]

## Plotando a figura gráfica - produtividades:
tam_graf()    
f = plt.figure()  
ax = f.add_subplot(111)                                                 
lns1 = ax.plot(Ttotal[1:] ,Px,'red',linewidth=3,label='Produtividade Celular modelo')
lns2 = ax.plot(Ttotal_exp[1:] ,Px_exp,'or',markersize=6, label='Produtividade Celular experimental')
ax2 = ax.twinx()
lns3 = ax2.plot(Ttotal[1:],Pp,linestyle=":", color='blue',linewidth=3,label='Produtividade do Produto modelo') 
lns4 = ax2.plot(Ttotal_exp[1:],Pp_exp,'sb', markersize=6,label='Produtividade do Produto experimental')
ax.set_xlabel('Tempo de cultivo (h)',weight='bold')               
ax.set_ylabel('Produtividade Celular (gx/L.h)', weight='bold')
ax2.set_ylabel('Produtividade Produto (gp/L.h)', weight='bold') 
lns = lns1+lns2+lns3+lns4
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.19),ncol=2, fancybox=True, shadow=True )                                                
ax.grid(True)                     
f.set_figheight(9)                                                 
f.set_figwidth(14)                                                   
f.patch.set_facecolor('white')                                   
plt.style.use('default')    
plt.show()

#Equação que permite calcular a produtividade específica (Ppx) modelo e experimental:
Ppx_exp = Cp_exp*(1/Cx_exp)
Ppx_exp[Ppx_exp<0] = 0

Ppx = Cp*(1/Cx)
Ppx[Ppx<0] = 0 

## Plotando a figura gráfica - produtividade específica:
tam_graf()    
f = plt.figure() 
ax = f.add_subplot(111)  
plt.plot(Ttotal,Ppx,'red',linewidth=3, label='Modelo')
plt.plot(Ttotal_exp,Ppx_exp,'or',markersize=6, label='Experimental')
plt.xlabel('Tempo de cultivo (h)',weight='bold')               
plt.ylabel('Produtividade Específica (gp/gx)', weight='bold')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.17),ncol=2, fancybox=True, shadow=True )
plt.grid(True)  
f.set_figheight(9)                                                 
f.set_figwidth(14)                                                   
f.patch.set_facecolor('white')                                   
plt.style.use('default')                       
plt.show() 

# Calculando a velocidade de crescimento microbiano - experimental e modelada:
#imprimindo os valores dos parâmetros
#param_otim = np.asarray(resultado_alm_alim)

#Calculando os valores de mi - modelo otimizado e experimental
mimaximo_otim = resultado_alm_alim[0][0]
Ks_otim = resultado_alm_alim[0][1]
Kp_otim = resultado_alm_alim[0][5]

mult_exp_exp = -Kp_otim*Cp_exp
mi_exp = mimaximo_otim*((Cs_exp/(Ks_otim + Cs_exp))*np.exp(mult_exp_exp))
mi_exp[mi_exp<0] = 0
mult_exp = -Kp_otim*Cp
mi = mimaximo_otim*((Cs/(Ks_otim + Cs))*np.exp(mult_exp))
mi[mi<0] = 0

## Plotando a figura gráfica - taxa específica de crescimento microbiano:
tam_graf()    
f = plt.figure() 
ax = f.add_subplot(111)  
plt.plot(Ttotal,mi,'red',linewidth=3, label='Modelo')
plt.plot(Ttotal_exp,mi_exp,'or',markersize=6, label='Experimental')
plt.xlabel('Tempo de cultivo (h)',weight='bold')               
plt.ylabel('Taxa $\mu(h^{-1}$)', weight='bold')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.17),ncol=2, fancybox=True, shadow=True )  
plt.grid(True)   
f.set_figheight(9)                                                 
f.set_figwidth(14)                                                   
f.patch.set_facecolor('white')                                   
plt.style.use('default')                       
plt.show() 




import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import pandas as pd

importado = pd.read_excel("Input_batelada_processos_fermentativos_ajuste.xlsx","Operação_batelada")
##Linha de comando que permite a conversão dos dados numéricos extraídos das células do Excel para o formato de vetores Numpy:
importado_np = importado.values
##Concentração celular inicial:
Cx0 = 0.1
print("\nCx0:\n",Cx0)
##Concentração inicial de substrato fornecido às celulas inicial:
Cs0 = 20
print("\nCs0:\n",Cs0)
##Início do cultivo microbiano em batelada:
T0 = 0
print("\nT0:\n",T0)
##Término do cultivo microbiano em batelada:
Tf = 30
print("\nTf:\n",Tf)
##Intervalo de tempo (passo), entre o tempo total de cultivo em batelada,em que o mesmo será analisado matematicamente:
Intervalo = 0.25
print("\nIntervalo:\n",Intervalo)
##Entrada inicial aproximada para a taxa específica de crescimento:
mimaximo =0.45
print("\nmimáx:\n",mimaximo)
##Constante de morte celular Kd:
Kd = 0.08
print("Constante de morte:",Kd)
##Entrada inicial aproximada para a constante Ks:
Ks = 2
print("\nKs:\n",Ks)
##Entrada inicial aproximada para o coeficiente de transferência de substrato para o crescimento celular Yx/s:
Yxs = 0.3
print("\nYxs:\n",Yxs)
##Entrada inicial aproximada para a constante alfa associada à formação de produto pelas células durante a fermentação:


#Definindo as equações diferenciais que descrevem a variação da concentração celular e de substrato em função do tempo:
def modelo_crescimento_sem_Kd (Concentsemkd,t):
    Cx,Cs=Concentsemkd
##Definição das equações diferencias ordinárias que descrevem a variação das concentrações com o tempo, bem como o modelo de Monod: 
    mi=mimaximo*(Cs/(Ks+Cs))
    dCxdt=mi*Cx
    dCsdt=(-1/Yxs)*mi*Cx
    return(dCxdt,dCsdt)
    
#Definindo as condições iniciais para permitir a integração numérica computacional das EDOs definidas no modelo "modeloscrescimento", seguindo a cinética de Monod:
##Lista que contém os valores iniciais de concentração celular, de substrato de produto:
init_concent_sem_kd=[Cx0,Cs0]
##Vetor tempo, do tipo arange, a partir do pacote numérico Numpy:
Tfinalintegracao=Tf-6
t=np.arange(T0,Tfinalintegracao,Intervalo)
##Comando para integrar numericamente as EDOs definidas pelo modelo 'modeloscrescimento':
Concentsemkd=odeint(modelo_crescimento_sem_Kd,init_concent_sem_kd,t)
print("\nConcentrações sem kd:\n",Concentsemkd)
#Separando, a partir da matriz Concent, as vetores Cx, Cs e Cp:
##Matriz concentração celular com os valores calculados através da solução do modelo de EDO por integração numérica computacional:
Cx_sem_kd=Concentsemkd[:,0]
print("Cx sem kd:", Cx_sem_kd)
##Matriz concentração de substrato com os valores calculados através da solução do modelo de EDO por integração numérica computacional:
Cs_sem_kd=Concentsemkd[:,1]
print("Cs sem kd:", Cs_sem_kd)

#Definindo as equações diferenciais que descrevem a variação da concentração celular e de substrato em função do tempo:
def modelo_crescimento_com_Kd (Concentcomkd,t):
    Cx,Cs=Concentcomkd
##Definição das equações diferencias ordinárias que descrevem a variação das concentrações com o tempo, bem como o modelo de Monod: 
    mi=mimaximo*(Cs/(Ks+Cs))
    dCxdt=(mi-Kd)*Cx
    dCsdt=(-1/Yxs)*mi*Cx
    return(dCxdt,dCsdt)

#Definindo as condições iniciais para permitir a integração numérica computacional das EDOs definidas no modelo "modeloscrescimento", seguindo a cinética de Monod:
##Lista que contém os valores iniciais de concentração celular, de substrato de produto:
###Condição de integração:
Cxzero=max(Cx_sem_kd)
Cszero=min(Cs_sem_kd)
init_concent_kd=[Cxzero,Cszero]
##Vetor tempo, do tipo arange, a partir do pacote numérico Numpy:
T=np.arange(Tfinalintegracao,Tf,Intervalo)
##Comando para integrar numericamente as EDOs definidas pelo modelo 'modeloscrescimento':
Concentcomkd=odeint(modelo_crescimento_com_Kd,init_concent_kd,T)
print("\nConcentrações com kd:\n",Concentcomkd)
#Separando, a partir da matriz Concent, as vetores Cx, Cs e Cp:
##Matriz concentração celular com os valores calculados através da solução do modelo de EDO por integração numérica computacional:
Cx_com_kd=Concentcomkd[:,0]
print("Cx com kd:", Cx_com_kd)
##Matriz concentração de substrato com os valores calculados através da solução do modelo de EDO por integração numérica computacional:
Cs_com_kd=Concentcomkd[:,1]
print("Cs com kd:", Cs_com_kd)

#Fase lag:
Tlag=T0+1
Cxlag1=Cx_sem_kd[8]
Cxlag2=Cx_sem_kd[25]
Tlagrafico=T0+5
Tlgraficoplotar1=np.repeat(Tlagrafico, len(Cx_com_kd))
Tlgraficoplotar2=np.repeat(Tlagrafico, len(Cx_sem_kd))

#Fase log:
Tlog=T0+8
Cxlog1=0.60*max(Cx_sem_kd)
Cxlog2=0.80*max(Cx_sem_kd)
Tlografico=T0+11
Tlograficoplotar1=np.repeat(Tlografico, len(Cx_com_kd))
Tlograficoplotar2=np.repeat(Tlografico, len(Cx_sem_kd))

#Fase estacionária:
Testacionaria=T0+18
Cxest1=0.98*max(Cx_sem_kd)
Cxest2=0.62*max(Cx_sem_kd)
Tfinalintegracao=Tf-6
Testgraficoplotar1=np.repeat(Tfinalintegracao, len(Cx_com_kd))
Testgraficoplotar2=np.repeat(Tfinalintegracao, len(Cx_sem_kd))

#Fase morte:
Tmorte=T0+27
Cxmorte1=0.75*max(Cx_sem_kd)
Cxmorte2=0.41*max(Cx_sem_kd)

SMALL_SIZE = 12                        
MEDIUM_SIZE = 12                       
BIGGER_SIZE = 12                      

##Comando para determinar o tamanho segundo o qual os textos grafados no gráfico serão impressos na tela:
plt.rc('font', size=SMALL_SIZE)          
plt.rc('axes', titlesize=SMALL_SIZE)     
plt.rc('axes', labelsize=MEDIUM_SIZE)    
plt.rc('xtick', labelsize=SMALL_SIZE)    
plt.rc('ytick', labelsize=SMALL_SIZE)    
plt.rc('legend', fontsize=SMALL_SIZE)    
plt.rc('figure', titlesize=BIGGER_SIZE)  

f = plt.figure() 
#Definindo os vetores tempo e concentração celular que irão ser plotados, referente a cada uma das taxas de crescimento analisadas, bem como a cor e espessura da linha graficada:                                                    
_ = plt.plot(t,Cx_sem_kd,'darkgrey',linewidth=3)  
#_ = plt.plot(t,Cs_sem_kd,'darkgrey',linewidth=4) 
_ = plt.plot(T,Cx_com_kd,'darkgrey',linewidth=3) 
_ = plt.plot(Tlgraficoplotar1,Cx_com_kd,'dimgrey',linestyle="dashed",linewidth=2)
_ = plt.plot(Tlgraficoplotar2,Cx_sem_kd,'dimgrey',linestyle="dashed",linewidth=2)
_ = plt.plot(Tlograficoplotar1,Cx_com_kd,'dimgrey',linestyle="dashed",linewidth=2)
_ = plt.plot(Tlograficoplotar2,Cx_sem_kd,'dimgrey',linestyle="dashed",linewidth=2)
_ = plt.plot(Testgraficoplotar1,Cx_com_kd,'dimgrey',linestyle="dashed",linewidth=2)
_ = plt.plot(Testgraficoplotar2,Cx_sem_kd,'dimgrey',linestyle="dashed",linewidth=2)
#_ = plt.plot(T,Cs_com_kd,'darkgrey',linewidth=4)    
#Definição do título dos eixos x e y, assim como da formatação do texto a ser utilizada (negrito):
_ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
_ = plt.ylabel('Concentração de células (g/L)', weight='bold') 
#Definição da posição da legenda no interior da área de plotagem, assim como o seu título:        
#Linha de comando que permite a colocação de uma seta para a indicação do perfil linear adotado pelo modelo matemático graficado (cor, tamanho e posição da seta dentro da área de plotagem):                                          
_ = plt.title('Fases do Crescimento Microbiano', weight='bold')
_ = plt.annotate(u'       Lag\n(Adaptação)\n', xy=(Tlag,Cxlag1), xytext=((Tlag-2.2),Cxlag2), arrowprops=dict(facecolor='grey',shrink=0.05),size=10)   
_ = plt.annotate(u'       Log\n(Exponencial)\n', xy=(Tlog,Cxlog1), xytext=((Tlog-2.89),Cxlog2), arrowprops=dict(facecolor='grey',shrink=0.05),size=10)
_ = plt.annotate(u'Estacionária\n (Equilíbrio)\n', xy=(Testacionaria,Cxest1), xytext=((Testacionaria-2.89),Cxest2), arrowprops=dict(facecolor='grey',shrink=0.05),size=10) 
_ = plt.annotate(u'Declínio\n (Morte)\n', xy=(Tmorte,Cxmorte1), xytext=((Tmorte-1),Cxmorte2), arrowprops=dict(facecolor='grey',shrink=0.05),size=10) 
#Comando que habilita a presença da linha de grade ao fundo da área de plotagem:
_ = plt.grid(True)
#Definição das dimensões de comprimento e largura da figura gerada:                                                  
f.set_figheight(5)                                                 
f.set_figwidth(8) 
#Definição da cor de fundo da área de plotagem do gráfico:                                                  
f.patch.set_facecolor('white') 
#Definição do template, disponibilizado pelo pacote matplotlib, para compor a estética da figura:                                          
plt.style.use('default') 
#Comando para o output do gráfico obtido:   
    #plt.show() 
plt.savefig('Gráfico fases do crescimento microbiano batelada.png')    

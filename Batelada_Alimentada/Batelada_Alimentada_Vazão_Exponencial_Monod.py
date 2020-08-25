#Importando as bibliotecas para importação e exportação de dados, realização de operações matemáticas, plotação gráfica de resultados::
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import pandas as pd

##Para o cálculo do produto-atribuir uma varipavel p
###0-associado ao crescimento;1-não associado ao crescimento;2-parcialmente associado ao crescimento

#BATELADA
Cx0batelada = 0.1
Cs0batelada = 30
Cp0batelada = 0
T0batelada= 0
Tfbatelada= 10
Intervalobatelada = 0.5
mimaximo = 0.4
Ks = 2
Yxs = 0.3
alfa = 0.3
beta = 0.8

#BATELADA ALIMENTADA
Cs0alimentacao = 150
T0ba = Tfbatelada
Tfba = 35
Intervaloba = 0.5
V0= 2
Vf=6
Q0=0.252
mimaximo = 0.3
Ks = 3.1
Yxs = 0.3
alfa = 0.3
beta = 0.8
beta_perfil=0.12


                                            ## BATELADA ##
def modeloscrescimentobatelada (Concent,tbatelada):
    Cx,Cs,Cp=Concent
    mi=mimaximo*(Cs/(Ks+Cs))
    dCxdt=mi*Cx
    dCsdt=(-1/Yxs)*mi*Cx
    dCpdt=alfa*mi*Cx+beta*Cx
    return(dCxdt,dCsdt,dCpdt)

init_concent_batelada=[Cx0batelada,Cs0batelada,Cp0batelada]
tbatelada=np.arange(T0batelada,Tfbatelada,Intervalobatelada)
Concentbatelada=odeint(modeloscrescimentobatelada,init_concent_batelada,tbatelada)
print("\nConcentrações:\n",Concentbatelada)

Cxbatelada=Concentbatelada[:,0]
print("Cx:", Cxbatelada)

Csbatelada=Concentbatelada[:,1]
print("Cs:", Csbatelada)

Cpbatelada=Concentbatelada[:,2]
print("Cp:", Cpbatelada)


df_concents= pd.DataFrame({'Tempo(h)':tbatelada,'Cx(g/L)': Cxbatelada, 'Cs(g/L)': Csbatelada, 'Cp(g/L)': Cpbatelada})
with pd.ExcelWriter('Output_batelada_processos_fermentativos.xlsx',engine = 'openpyxl') as writer:
    df_concents.to_excel(writer, sheet_name="Output_concent_batelada")
    writer.save()

                                ## BATELADA ALIMENTADA ##
def modeloscrescimentoalimentada (Concent,tal):
    Cx,Cs,Cp=Concent
    mi=mimaximo*(Cs/(Ks+Cs))
    multiplicacao=beta_perfil*tal
    exponencial=np.exp(multiplicacao)
    D =(Q0*np.exp(beta_perfil*tal))/(((Q0/beta_perfil)*(exponencial-1))+V0)
    dCxdt=(mi-D)*Cx
    dCsdt=D*(Cs0alimentacao-Cs)-((mi*Cx)/Yxs)
    dCpdt=D*(Cp0ba-Cp)+Cx*(beta+alfa*mi)
    return(dCxdt,dCsdt,dCpdt)
    
##Lista que contém os valores iniciais de concentração celular, de substrato de produto:
###Valores finais da batelada vão ser os iniciais da batelada alimentada:
Cx0ba=Cxbatelada[len(Cxbatelada)-1]   
Cs0ba=Csbatelada[len(Csbatelada)-1]
Cp0ba=Cpbatelada[len(Cpbatelada)-1]    
    
init_concent_alimentada=[Cx0ba,Cs0ba,Cp0ba]
tal=np.arange(Tfbatelada,Tfba,Intervaloba)
Concentalimentada=odeint(modeloscrescimentoalimentada,init_concent_alimentada,tal)
print("\nConcentrações:\n",Concentalimentada)

Cxal=Concentalimentada[:,0]
print("Cx:", Cxal)

Csal=Concentalimentada[:,1]
print("Cs:", Csal)

Cpal=Concentalimentada[:,2]
print("Cp:", Cpal)

Csalinit=round(np.float(Csal[0]),2)
print("Concentração de substrato imediatamente depois da alimentação:",Csalinit)

Cxalinit=round(np.float(Cxal[0]),2)
print("Concentração de células ao fim da operação:",Cxalinit)

df_concents= pd.DataFrame({'Tempo(h)':tal,'Cx(g/L)': Cxal, 'Cs(g/L)': Csal, 'Cp(g/L)': Cpal})
with pd.ExcelWriter('Output_batelada_alimentada_processos_fermentativos.xlsx',engine = 'openpyxl') as writer:
    df_concents.to_excel(writer, sheet_name="Output_concent_alimentada")
    writer.save()                                      
 
    #9x14

##Contadores gerais
limitebatelada=len(Concentbatelada)
print("Limite batelada",limitebatelada)
limitealimentada=len(Concentalimentada)
print("Limite batelada alimentada", limitealimentada)

concentotalx=[]
concentotals=[]
concentotalp=[]
bat=0
batal=0
#if (tbatelada[bat]<(Tfbatelada-Intervalobatelada)):
while (bat<limitebatelada):
    concentotalx.append(Cxbatelada[bat])
    concentotals.append(Csbatelada[bat])
    concentotalp.append(Cpbatelada[bat])
    bat=bat+1
        
#if (tal[batal]<Tfba):
while (batal<limitealimentada):
    concentotalx.append(Cxal[batal])
    concentotals.append(Csal[batal])
    concentotalp.append(Cpal[batal])
    batal=batal+1

Ttotal=np.arange(T0batelada,Tfba,Intervalobatelada)

## Conversão das listas para arrays - necessário para operações matemáticas:
concentotalx = np.asarray(concentotalx)
concentotals = np.asarray(concentotals)
concentotalp = np.asarray(concentotalp)

#Gráfico batelada e batelada alimentada
def tam_graf():
    SMALL_SIZE = 20                       
    MEDIUM_SIZE = 24                                          

    ##Comando para determinar o tamanho segundo o qual os textos grafados no gráfico serão impressos na tela:
    plt.rc('font', size=SMALL_SIZE)          
    plt.rc('axes', titlesize=SMALL_SIZE)     
    plt.rc('axes', labelsize=MEDIUM_SIZE)    
    plt.rc('xtick', labelsize=SMALL_SIZE)    
    plt.rc('ytick', labelsize=SMALL_SIZE)    
    plt.rc('legend', fontsize=SMALL_SIZE)    

# Figura gráfica - perfil concentração
tam_graf()
_ = f = plt.figure()   
_ = ax = f.add_subplot(111)                                                
_ = lns1 = ax.plot(Ttotal,concentotalx,'red',linewidth=3,label='Cx modelo')    
_ = lns2 = ax.plot(Ttotal,concentotals,linestyle=':',color='blue',linewidth=3,label='Cs modelo')  
_ = ax2 = ax.twinx()
_ = lns3 = ax2.plot(Ttotal,concentotalp,linestyle='--',color='green',linewidth=3,label='Cp modelo')  
_ = ax.axvline(x = Tfbatelada, color = "grey", linestyle="dashed", linewidth=3)  
_ = ax.set_xlabel('Tempo de cultivo (h)',weight='bold')               
_ = ax.set_ylabel('Cx, Cs (g/L)', weight='bold')
_ = ax2.set_ylabel('Cp (g/L)', weight='bold') 
lns = lns1+lns2+lns3
labs = [l.get_label() for l in lns]
_ = ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.11),ncol=3, fancybox=True, shadow=True )
_ = ax.annotate(u'Alimentação', xy=(Tfbatelada,Csalinit), xytext=((Tfbatelada+2),(Cs0batelada)), arrowprops=dict(facecolor='lightgrey',shrink=0.05),size=18,weight='bold')                                                 
_ = ax.grid(True)                                                 
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)                                                    
_ = f.patch.set_facecolor('white') 
_ = plt.style.use('default') 
plt.show()   

## Cálculo produtividade - celular e do produto:
Px = concentotalx[1:]/Ttotal[1:]
Pp = concentotalp[1:]/Ttotal[1:]

## Plotando a figura gráfica - produtividades:
tam_graf()    
_ = f = plt.figure() 
_ = ax = f.add_subplot(111)  
_ = lns1 = ax.plot(Ttotal[1:], Px, color = "red", linewidth=3, label='Produtividade Celular')
_ = ax2 = ax.twinx()
_ = lns2 = ax2.plot(Ttotal[1:], Pp, linestyle=":", color = "green", linewidth=3,label='Produtividade do Produto') 
_ = ax.axvline(x = Tfbatelada, color = "grey", linestyle="dashed", linewidth=3)
_ = ax.set_xlabel('Tempo de cultivo (h)',weight='bold')               
_ = ax.set_ylabel('Produtividade Celular (gx/L.h)', weight='bold')
_ = ax2.set_ylabel('Produtividade Produto (gp/L.h)', weight='bold') 
lns = lns1 + lns2
labs = [l.get_label() for l in lns]
_ = ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.11),ncol=2, fancybox=True, shadow=True)  
_ = ax.grid(True)
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)
_ = f.patch.set_facecolor('white')                                   
_ = plt.style.use('default')    
plt.show()

## Cálculo produtividade específica:
Ppx = (concentotalp)*(1/concentotalx)
Ppx[Ppx<0] = 0

## Plotando a figura gráfica - produtividades: 
tam_graf()   
_ = f = plt.figure() 
_ = ax = f.add_subplot(111)  
_ = plt.plot(Ttotal, Ppx, color = "purple", linewidth=3, label='Produtividade Específica')
_ = plt.axvline(x = Tfbatelada, color = "grey", linestyle="dashed", linewidth=3)
_ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
_ = plt.ylabel('Produtividade Específica (gp/gx)', weight='bold')
_ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.11),ncol=2, fancybox=True, shadow=True)  
_ = plt.grid(True)
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)
_ = f.patch.set_facecolor('white')                                   
_ = plt.style.use('default')    
plt.show()

## Cálculo mi:
mi = mimaximo*(concentotals/(Ks+concentotals))

## Plotando a figura gráfica - velocidade de crescimento: 
tam_graf()   
_ = f = plt.figure() 
_ = ax = f.add_subplot(111)  
_ = plt.plot(Ttotal, mi, color = "orange", linewidth=3, label='Velocidade de crescimento')
_ = plt.axvline(x = Tfbatelada, color = "grey", linestyle="dashed", linewidth=3)
_ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
_ = plt.ylabel('Taxa $\mu (h^{-1}$)', weight='bold')
_ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.11),ncol=2, fancybox=True, shadow=True)  
_ = plt.grid(True)
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)
_ = f.patch.set_facecolor('white')                                   
_ = plt.style.use('default')    
plt.show()


#Variação do volume reacional em função do tempo:
##Função V(t) integrada:

V=((Q0/beta_perfil)*((np.exp(beta_perfil*tal))-1))+V0

#Gráfico variação de volume x tempo 
tam_graf()
f = plt.figure() 
_ = plt.plot(tal,V,'brown',linewidth=3, label = "Volume")
_ = plt.xlabel("Tempo de cultivo alimentado (h)",weight='bold')
_ = plt.ylabel("Volume do reacional (L)",weight='bold')
_ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.11),ncol=1, fancybox=True, shadow=True )
_ = plt.grid(True)
_ = plt.style.use('default') 
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)
_ = plt.show()


#Variação linear da vazão com o tempo
##Função Q(t) original:
Q=Q0*np.exp(beta_perfil*tal)

#Gráfico variação de volume x tempo 
tam_graf()
_ = f = plt.figure() 
_ = plt.plot(tal,Q,'magenta',linewidth=3, label = "Vazão")
_ = plt.xlabel("Tempo de cultivo alimentado (h)",weight='bold')
_ = plt.ylabel("Vazão de alimentação (L/h)",weight='bold')
_ = plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.11),ncol=1, fancybox=True, shadow=True )
_ = plt.grid(True)
_ = plt.style.use('default') 
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(14)
_ = plt.show()









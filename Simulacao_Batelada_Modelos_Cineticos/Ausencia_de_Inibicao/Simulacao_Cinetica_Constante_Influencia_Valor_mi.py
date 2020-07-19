#Importando as bibliotecas para importação e exportação de dados, realização de operações matemáticas, plotação gráfica de resultados e criação da GUI:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#Definindo os valores da taxa específica de crescimento para determinar a concentração final de células em função do tempo de cultivo:
##Entrada para o primeiro valor da taxa específica de crescimento microbiano:
mi_1 = 0.1
print("\nmi_1:\n",mi_1)
##Entrada para o segundo valor da taxa específica de crescimento microbiano: 
mi_2 = 0.2
print("\nmi_2:\n",mi_2)
##Entrada para o terceiro valor da taxa específica de crescimento microbiano:
mi_3 = 0.3
print("\nmi_3:\n",mi_3)
##Entrada para o quarto valor da taxa específica de crescimento microbiano:
mi_4 = 0.4
print("\nmi_4:\n",mi_4)
##Entrada para o quinto valor da taxa específica de crescimento microbiano:
mi_5 = 0.5
print("\nmi_5:\n",mi_5)
##Entrada da concentração celular inicial:
Cx0 = 0.2
print("\nCx0:\n",Cx0)
##Entrada para o tempo inicial a partir do qual o cultivo e consequente crescimento celular será simulado matematicamente:
t0 = 0
print("\nt0:\n",t0) 
##Entrada para o tempo final de cultivo que será analisado para fins da simulação matemática de cinética microbiana (h):
tf = 8
print("\ntf:\n",tf)
##Entrada para o intervalo de tempo entre o tempo total de cultivo em que as análises serão realizadas durante a efetuação dos cálculos de simulação:
int = 0.5
print("\nint:\n",int)

#Definição do modelo matemático da variação da concentração celular com o tempo de cultivo, considerando uma taxa específica de crescimento constante (mi_1):
def batelconst(Cx,t):                   
    mi= mi_1                             
    dCxdt=mi*Cx                         
    return(dCxdt)                       
#Criação do vetor com as condições iniciais(Cx0 e t0) utilizadas para a solução da EDO anterior por integração numérica computacional: 
init_cond=[Cx0,t0]  
#Criação do vetor tempo do tipo arange com os tempos inicial, final e intervalos do cultivo para a análise matemática:                     
t=np.arange(t0,tf,int) 
#Resolução da equação diferencial ordinária definida no modelo através da utilização das condições iniciais e dos tempos estipulados:                 
Cells1=odeint(batelconst,init_cond,t)    
#print(type(Cells1)) 
#Cells1set=pd.DataFrame({'Column1':Cells1[:,0], 'Column2':Cells2[:,0]})
#print(Cells1set)    
         
#Definição do modelo matemático da variação da concentração celular com o tempo de cultivo, considerando uma taxa específica de crescimento constante (mi_2):
def batelconst(Cx,t):                   
  mi=mi_2                                
  dCxdt=mi*Cx                           
  return(dCxdt)                          
#Criação do vetor com as condições iniciais(Cx0 e t0) utilizadas para a solução da EDO anterior por integração numérica computacional:
init_cond=[Cx0,t0]   
#Criação do vetor tempo do tipo arange com os tempos inicial, final e intervalos do cultivo para a análise matemática:                 
t=np.arange(t0,tf,int)    
#Resolução da equação diferencial ordinária definida no modelo através da utilização das condições iniciais e dos tempos estipulados:            
Cells2=odeint(batelconst,init_cond,t)   
#print(Cells2[:,0])  
       
#Definição do modelo matemático da variação da concentração celular com o tempo de cultivo, considerando uma taxa específica de crescimento constante (mi_3):
def batelconst(Cx,t):                  
    mi=mi_3                              
    dCxdt=mi*Cx                         
    return(dCxdt)                      
#Criação do vetor com as condições iniciais(Cx0 e t0) utilizadas para a solução da EDO anterior por integração numérica computacional:
init_cond=[Cx0,t0]  
#Criação do vetor tempo do tipo arange com os tempos inicial, final e intervalos do cultivo para a análise matemática:                 
t=np.arange(t0,tf,int)  
#Resolução da equação diferencial ordinária definida no modelo através da utilização das condições iniciais e dos tempos estipulados:                
Cells3=odeint(batelconst,init_cond,t)   
#print(Cells3[:,0]) 

Cellsset=pd.DataFrame({'Column1':Cells1[:,0], 'Column2':Cells2[:,0],'Column3':Cells3[:,0]})
#print(Cellsset)                                  

#Definição do modelo matemático da variação da concentração celular com o tempo de cultivo, considerando uma taxa específica de crescimento constante (mi_4):
def batelconst(Cx,t):                   
    mi=mi_4                             
    dCxdt=mi*Cx                         
    return(dCxdt)                       
#Criação do vetor com as condições iniciais(Cx0 e t0) utilizadas para a solução da EDO anterior por integração numérica computacional:
init_cond=[Cx0,t0]  
#Criação do vetor tempo do tipo arange com os tempos inicial, final e intervalos do cultivo para a análise matemática:                  
t=np.arange(t0,tf,int)   
#Resolução da equação diferencial ordinária definida no modelo através da utilização das condições iniciais e dos tempos estipulados:             
Cells4=odeint(batelconst,init_cond,t)  
#print(Cells4[:,0])    

Cellsset=pd.DataFrame({'Column1':Cells1[:,0], 'Column2':Cells2[:,0],'Column3':Cells3[:,0], 'Column4':Cells4[:,0]})                  

#Definição do modelo matemático da variação da concentração celular com o tempo de cultivo, considerando uma taxa específica de crescimento constante (mi_5):
def batelconst(Cx,t):                   
    mi=mi_5                             
    dCxdt=mi*Cx                         
    return(dCxdt)                       
#Criação do vetor com as condições iniciais(Cx0 e t0) utilizadas para a solução da EDO anterior por integração numérica computacional: 
init_cond=[Cx0,t0] 
##Criação do vetor tempo do tipo arange com os tempos inicial, final e intervalos do cultivo para a análise matemática:                    
t=np.arange(t0,tf,int) 
#Resolução da equação diferencial ordinária definida no modelo através da utilização das condições iniciais e dos tempos estipulados:                
Cells5=odeint(batelconst,init_cond,t)   
#print(Cells5[:,0])                      

#Criando a função que permite a geração do output dos valores dos valores de concentração celular para cada taxa específica de crescimento considerada no período de tempo analisado:
Cellsset=pd.DataFrame({'Tempo(h)':t, 'Cx1(g/L)':Cells1[:,0], 'Cx2(g/L)':Cells2[:,0],'Cx3(g/L)':Cells3[:,0], 'Cx4(g/L)':Cells4[:,0], 'Cx5(g/L)':Cells5[:,0]})

# Plotando graficamente os resultados obtidos através da integração numérica para a concentração celular em cada um dos casos de mi estudados:
## Definição das variáveis referentes ao tamanho da fonte encontrada no gráfico:
SMALL_SIZE = 14                        
MEDIUM_SIZE = 20                       
BIGGER_SIZE = 20                       

## Comando para determinar o tamanho segundo o qual os textos encontrados no gráfico serão impressos na tela:
plt.rc('font', size=SMALL_SIZE)          
plt.rc('axes', titlesize=SMALL_SIZE)     
plt.rc('axes', labelsize=MEDIUM_SIZE)    
plt.rc('xtick', labelsize=SMALL_SIZE)    
plt.rc('ytick', labelsize=SMALL_SIZE)    
plt.rc('legend', fontsize=SMALL_SIZE)    
plt.rc('figure', titlesize=BIGGER_SIZE)  

## Algoritmo para plotar e imprimir os dados numéricos graficamente:
#Definindo a figura que irá ser gerada:
f = plt.figure() 
#Definindo os vetores tempo e concentração celular que irão ser plotados, referente a cada uma das taxas de crescimento analisadas, bem como a cor e espessura da linha graficada:                                                    
_ = plt.plot(t,Cells1[:,0],'m',linewidth=4,label= mi_1)    
_ = plt.plot(t,Cells2[:,0],'y',linewidth=4,label= mi_2)    
_ = plt.plot(t,Cells3[:,0],'b',linewidth=4,label= mi_3)    
_ = plt.plot(t,Cells4[:,0],'g',linewidth=4,label= mi_4)    
_ = plt.plot(t,Cells5[:,0],'c',linewidth=4,label= mi_5)  
#Definição do título dos eixos x e y, assim como da formatação do texto a ser utilizada (negrito):
_ = plt.xlabel('Tempo de cultivo (h)',weight='bold')               
_ = plt.ylabel('Concentração de células (g/L)', weight='bold') 
#Definição da posição da legenda no interior da área de plotagem, assim como o seu título:      
_ = plt.legend(loc=0, title = "Valores de $\mu= (h^{-1}$)")    
#Linha de comando que permite a colocação de uma seta para a indicação do perfil linear adotado pelo modelo matemático graficado (cor, tamanho e posição da seta dentro da área de plotagem):                                          
_ = plt.annotate(u'Perfil exponencial de crescimento', xy=(6.8, 3), xytext=(2.2, 4.2), arrowprops=dict(facecolor='grey',shrink=0.05),size=15)   
#Comando que habilita a presença da linha de grade ao fundo da área de plotagem:
_ = plt.grid(True)
#Definição das dimensões de comprimento e largura da figura gerada:                                                  
f.set_figheight(9)                                                 
f.set_figwidth(14) 
#Definição da cor de fundo da área de plotagem do gráfico:                                                  
f.patch.set_facecolor('white') 
#Definição do template, disponibilizado pelo pacote matplotlib, para compor a estética da figura:                                          
plt.style.use('default') 
#Comando para o output do gráfico obtido:   
plt.show()                                            


#O pacote Pandas permite escrever, em Python, em uma planilha Excel, os valores de concentração celular calculados através do algoritmo, por meio de função abaixo:
with pd.ExcelWriter('Dados_mi_saida.xlsx') as writer:
    Cellsset.to_excel(writer, sheet_name="Output")
##O documento, em xlsx, é salvo com o mesmo nome indicado entre aspas na função anterior:
    writer.save()
    

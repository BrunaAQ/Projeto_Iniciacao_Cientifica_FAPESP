# Importação das bibliotecas necessárias para as partes não modulares:
import Modulos_Lee_et_al
import Modulo_peso_limite_AG
import Modulos_configuracao_graficos
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import differential_evolution
from scipy.optimize import leastsq
import scipy.stats as sc
import time

# GERANDO DADOS EXPERIMENTAIS

## Módulos
# Valores dos parâmetros e condição inicial
dad_entr_geral = Modulos_Lee_et_al.entr_rand_Lee_colab()
# Valor de entrada dos parâmetros cinéticos
dad_inic = dad_entr_geral[0]
# Importação valores de concentração gerados por simulação
said_mod = Modulos_Lee_et_al.modelag_bat_Lee_et_al_dados_conc_sim() 

## Saídas
# Valores de C_exp e t_exp 
t_exp = said_mod[1]
C_exp = said_mod[0] 

# Condição inicial - integração numérica
cond_inic = [C_exp[0,0], C_exp[0,1], C_exp[0,2]]

# Trecho de código opcional:
# Gerando ruído aos dados:
for i in range(0,3):
    C_exp_i = C_exp[:,i]
    C_exp[:,i] = C_exp_i + np.random.randn(len(C_exp_i)) * 0.5
    
df_saida_lee_et_al = pd.DataFrame({"t_exp(h)":t_exp, "Cx_exp(g/L)": C_exp[:,0], "Cs_exp(g/L)": C_exp[:,1], "Cp_exp(g/L)": C_exp[:,2]})
with pd.ExcelWriter('Dados_sim_bat_Lee_et_al.xlsx') as writer:
    df_saida_lee_et_al.to_excel(writer, sheet_name="C_t_exp")
    writer.save() 
    
# TÉRMINO DA GERAÇÃO DE DADOS EXPERIMENTAIS
    
#início da contagem do tempo
start = time.time() 

# Função com as equações modelo com os parâmetros atribuídos a argumentos:
func_args = Modulos_Lee_et_al.modelag_bat_Lee_et_al_func_args()

# Função objetiva, compara os pontos experimentais com o modelo
# Módulo para atribuição do peso:
dpC = Modulo_peso_limite_AG.peso()

def func_ob_ag(parametros, *dados):
    # mimax, ks, alfa, Yxs, beta, kd = parametros
    t_exp,C_exp = dados
    p = tuple(parametros)
    C_sim = odeint(func_args, cond_inic, t_exp, args = p)
    res = C_sim - C_exp
    for i in range(0,3):
        res[:,i] = res[:,i]/dpC[i]
    res = res.flatten()
    res = sum(res**2)
    return res

#chutes iniciais para ajuste do parametro
limites = Modulo_peso_limite_AG.limites()[8]
args = (t_exp,C_exp)
resultado_ag = differential_evolution(func_ob_ag, limites, args=args, popsize=5,  tol=0.01, mutation=(0.5, 1), recombination=0.7, updating='immediate')
resultado_ag = resultado_ag.x

#Criação da Função Objetiva do Levemberg-Marquardt
def func_ob_lm(p):
    p=tuple(p)
##Calculando os valores simulados, através dos modelos matemáticos de EDOs (resolvidas por integração numérica computacional),para Cx, Cs e Cp, utilizando os argumentos guardados na tupla: 
    C_sim=odeint(func_args,cond_inic,t_exp,args=p)
##Determinado o erro entre os valores experimentais e calculados pelo método acima para os valores de Cx, Cs e Cp:
    res=C_sim-C_exp
##Para cada uma das três colunas da matriz contendo os valores experimentais, o erro calculado é dividido pelo peso atribuído a Cx, Cs e Cp:
    for i in range(0,3):
        res[:,i]=res[:,i]/dpC[i]
##O que a função retorna é uma matriz unidimensional, pelo uso da função flatten:
    return res.flatten()

#Minimizando a função objetiva pela função leastsq:

##A lista 'initial guess' contém os valores de entrada, portanto, aproximados, para as constantes cinéticas de crescimento microbiano extraídas diretamente da planilha do Excel:
lance_inic = [resultado_ag]
##A função leastsq, a partir da solução da função residuals e dos valores de entrada aproximados anteriores irá definir qual o valor dessas mesmas constantes que minimiza o erro observado entre os valores simulados e modelo para Cx, Cs e Cp:
resultado_lm=leastsq(func_ob_lm,lance_inic, args=(), Dfun=None, full_output=1)

param_otim_lm=resultado_lm[0]

res_otimo =resultado_lm[2]['fvec']
sensT_otimo =resultado_lm[2]['fjac']

npar = len(sensT_otimo[:,1])
ndata = len(sensT_otimo[1,:])
invXtX=np.linalg.inv(np.matmul(sensT_otimo,sensT_otimo.transpose()))
sig2y= sum(res_otimo**2) / (ndata-npar)
covparamers = invXtX*sig2y
EPpar = np.sqrt(covparamers.diagonal())
ICpar = EPpar*sc.t.interval(.95, ndata-npar, loc=0, scale=1)[1]

##As constantes, já com valores otimizados, são armazenadas em uma tupla (lista imutável):
param_otim_lm=tuple(param_otim_lm)
##Agora, a função modeloscrescimento, que contém as EDOs que descrevem o comportamento, em função do tempo, de Cx, Cs e Cp é novamente integrada numericamente utilizando as constantes cinéticas (argumentos) já otimizados (convergidas):

# Criando meu vetor tempo do modelo
t = np.arange(0, t_exp[-1], 0.1)

# Integrando com os valores dos parâmetros ajustados
C_otim = odeint(func_args, cond_inic, t, args = (param_otim_lm))

#Funções de impressão gráfica:
# Módulo para configuração do tamanho das fontes dos eixos:
config_eixos = Modulos_configuracao_graficos.config_plot()
# Módulo para configurar background:
config_back = Modulos_configuracao_graficos.config_estetica_eixo_unico()
# Tamanho das figuras de duplo eixo:
alt = 6
larg = 8

#Função de impressão do gráfico
def imprimir_perfil_concentracao_model_otim_exp (t_ajus, t_m, Cx_ajus, Cs_ajus, Cp_ajus, Cx_m, Cs_m, Cp_m):
    config_eixos()        
    f = plt.figure() 
    ax = f.add_subplot(111) 
    lns1 = ax.plot(t_m ,Cx_m,'red',linewidth=3,label='Cx modelo')
    lns3 = ax.plot(t_m,Cp_m, linestyle="--", color='green',linewidth=3,label='Cp modelo')  
    lns2 = ax.plot(t_ajus ,Cx_ajus,'or',markersize=6, label='Cx experimental')
    lns4 = ax.plot(t_ajus ,Cp_ajus,'^g',markersize=6,label='Cp experimental')
    ax2 = ax.twinx()
    lns5 = ax2.plot(t_m,Cs_m,linestyle=":", color='blue',linewidth=3,label='Cs modelo') 
    lns6 = ax2.plot(t_ajus,Cs_ajus,'sb', markersize=6,label='Cs experimental')
    ax.set_xlabel('Tempo de cultivo (h)',weight='bold')               
    ax.set_ylabel('Cx e Cp (g/L)', weight='bold')
    ax2.set_ylabel('Cs (g/L)', weight='bold') 
    lns = lns1+lns2+lns3+lns4+lns5+lns6
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.21),ncol=3, fancybox=True, shadow=True )                                                
    ax.grid(True)                     
    f.set_figheight(alt)                                                 
    f.set_figwidth(larg)                                                   
    f.patch.set_facecolor('white')                                   
    plt.style.use('default')    
    plt.savefig("Concentrações model acopl bat Lee et al.png")
    plt.show()
#impressão do gráfico
imprimir_perfil_concentracao_model_otim_exp(t_exp, t, C_exp[:,0], C_exp[:,1], C_exp[:,2], C_otim[:,0], C_otim[:,1], C_otim[:,2])

# Cálculo de Produtividade
#PRODUTIVIDADE:
#Calculando Produtividade Celular - Px tanto experimental quanto do modelo
Px_exp = C_exp[1:,0]/t_exp[1:] 
Px_exp[Px_exp<0] = 0 # Se o valor é menor que 0 é substituido por 0

Px = C_otim[1:,0]/t[1:]
Px[Px<0] = 0 # Se o valor é menor que 0 é substituido por 0

#Calculando Produtividade do Produto - Pp tanto experimental quanto do modelo
Pp_exp = C_exp[1:,2]/t_exp[1:]
Pp_exp[Pp_exp<0] = 0 # Se o valor é menor que 0 é substituido por 0

Pp = C_otim[1:,2]/t[1:]
Pp[Pp<0] = 0 # Se o valor é menor que 0 é substituido por 0

#Gráfico de Produtividade
def imprimir_produtividade_celular_produto_model_otim_exp (t_ajus, t_m, Px_ajus, Pp_ajus, Px_m, Pp_m):
    config_eixos()
    f = plt.figure()  
    ax = f.add_subplot(111)                                                 
    lns1 = ax.plot(t_m ,Px_m,'red',linewidth=3,label='Produtividade Celular modelo')
    lns2 = ax.plot(t_ajus ,Px_ajus,'or',markersize=6, label='Produtividade Celular experimental')
    ax2 = ax.twinx()
    lns3 = ax2.plot(t_m,Pp_m,linestyle=":", color='blue',linewidth=3,label='Produtividade do Produto modelo') 
    lns4 = ax2.plot(t_ajus,Pp_ajus,'sb', markersize=6,label='Produtividade do Produto experimental')
    ax.set_xlabel('Tempo de cultivo (h)',weight='bold')               
    ax.set_ylabel('Produtividade Celular (gx/L.h)', weight='bold')
    ax2.set_ylabel('Produtividade Produto (gp/L.h)', weight='bold') 
    lns = lns1+lns2+lns3+lns4
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc='upper center', bbox_to_anchor=(0.5, 1.19),ncol=2, fancybox=True, shadow=True )                                                
    ax.grid(True)                     
    f.set_figheight(alt)                                                 
    f.set_figwidth(larg)                                                   
    f.patch.set_facecolor('white')                                   
    plt.style.use('default')    
    plt.savefig("Produtividades model acopl bat Lee et al.png")
    plt.show()
#impressão do gráfico
imprimir_produtividade_celular_produto_model_otim_exp(t_exp[1:], t[1:],Px_exp, Pp_exp, Px, Pp)

# Calculando a produtividade específica experimental e modelo:
#imprimindo os valores dos parâmetros
param_otim = np.asarray(param_otim_lm)

#Calculando os valores de mi - modelo otimizado e experimental
mimaximo_otim=param_otim[0]
Ks_otim=param_otim[1]
m_otim=param_otim[6]
Cx_estr_otim=param_otim[7]

#mi=mimaximo*((Cs/(Ks+Cs))*((1-(Cx/Cx_estr))**m))
mi_exp = mimaximo_otim*((C_exp[:,1]/(Ks_otim+C_exp[:,1]))*((1-(C_exp[:,0]/Cx_estr_otim))**m_otim))
mi_exp[mi_exp<0] = 0
mi=mimaximo_otim*((C_otim[:,1]/(Ks_otim+C_otim[:,1]))*((1-(C_otim[:,0]/Cx_estr_otim))**m_otim))
mi[mi<0] = 0

def imprimir_taxa_especifica_crescimento (t_ajus,t_m, mi_ajus, mi_m):
    config_back()
    config_eixos()                                              
    plt.plot(t_m,mi_m,'red',linewidth=3, label='Modelo')
    plt.plot(t_ajus,mi_ajus,'or',markersize=6, label='Experimental')
    plt.xlabel('Tempo de cultivo (h)',weight='bold')               
    plt.ylabel('Taxa $\mu(h^{-1}$)', weight='bold')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.17),ncol=2, fancybox=True, shadow=True )  
    plt.grid(True)                   
    plt.show() 
    plt.savefig("Velocidade específica de crescimento model acopl bat Lee et al.png")    
#impressão do gráfico
imprimir_taxa_especifica_crescimento(t_exp,t,mi_exp,mi)

#Equação que permite calcular a produtividade específica (Ppx) modelo e experimental:
Ppx_exp=C_exp[:,2]*(1/C_exp[:,0])
Ppx_exp[Ppx_exp<0] = 0

Ppx=C_otim[:,2]*(1/C_otim[:,0])
Ppx[Ppx<0] = 0

def imprimir_produtividade_especifica_model_otim_exp (t_ajus,t_m, Ppx_ajus, Ppx_m):
    config_back()
    config_eixos()                                          
    plt.plot(t_m,Ppx_m,'red',linewidth=3, label='Modelo')
    plt.plot(t_ajus,Ppx_ajus,'or',markersize=6, label='Experimental')
    plt.xlabel('Tempo de cultivo (h)',weight='bold')               
    plt.ylabel('Produtividade Específica (gp/gx)', weight='bold')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.17),ncol=2, fancybox=True, shadow=True )
    plt.grid(True)                     
    plt.show() 
    plt.savefig("Produtividade específica model acopl bat Lee at al.png")    
#impressão do gráfico
imprimir_produtividade_especifica_model_otim_exp(t_exp,t,Ppx_exp,Ppx)

print("_______________Resultado__________________")

print("O valor de mimaximo é {:.4f}".format(param_otim[0]) +' 1/h')
print("O intervalo de confiança de 95% de mimaximo é {:.4f}".format(ICpar[0]))
print("O valor de Ks é {:.4f}".format(param_otim[1]) + ' g/L')
print("O intervalo de confiança de 95% de Ks é {:.4f}".format(ICpar[1]))
print("O valor de Kd é {:.4f}".format(param_otim[2]) +' 1/h')
print("O intervalo de confiança de 95% de Kd é {:.4f}".format(ICpar[2]))
print("O valor de Yxs é {:.4f}".format(param_otim[3]) +' gx/gs')
print("O intervalo de confiança de 95% de Yxs é {:.4f}".format(ICpar[3]))
print("O valor de alfa é {:.4f}".format(param_otim[4]) + 'gp/gx')
print("O intervalo de confiança de 95% de alfa é {:.4f}".format(ICpar[4]))
print("O valor de beta é {:.4f}".format(param_otim[5]) +' gp/gx.h')
print("O intervalo de confiança de 95% de beta é {:.4f}".format(ICpar[5]))
print("O valor de m é {:.4f}".format(param_otim[6]))
print("O intervalo de confiança de 95% de m é {:.4f}".format(ICpar[6]))
print("O valor de Cx_estr é {:.4f}".format(param_otim[7]) +' g/L')
print("O intervalo de confiança de 95% de Cx_estr é {:.4f}".format(ICpar[7]))

#Inserção do primeiro valor de Px e Pp - 0 para o tempo inicial:
Px = np.insert(Px,0,0)
Pp = np.insert(Pp,0,0)
Px_exp = np.insert(Px_exp,0,0)
Pp_exp = np.insert(Pp_exp,0,0)

print("")
print("________Diferença Ajuste - modelo____________")
#Diferença do valor ajustado menos o valor que gerou os pontos experimentais
print("mimax " + str(param_otim[0]-dad_inic[0]))
print("Ks " + str(param_otim[1]-dad_inic[1]))
print("Kd " + str(param_otim[2]-dad_inic[2]))
print("Yxs " + str(param_otim[3]-dad_inic[7]))
print("alfa " + str(param_otim[4]-dad_inic[8]))
print("beta " + str(param_otim[5]-dad_inic[9]))
print("m " + str(param_otim[6]-dad_inic[10]))
print("Cx_estr " + str(param_otim[7]-dad_inic[11]))
print("___________________________________________")

end = time.time()
elapsed = end - start
print("\nO tempo decorrido do ajuste foi de {:.1f}".format(elapsed)+ " segundos")

# Criação de todos os dataframes que serão utilizados
df_concents= pd.DataFrame({'Tempo(h)': t, 'Cx(g/L)': C_otim[:,0], 'Cs(g/L)': C_otim[:,1], 'Cp(g/L)': C_otim[:,2], 'mi(h-¹)': mi, 'Px(gcél/L.h)': Px, 'Pp(gprod/L.h)': Pp, 'Ppx(gprod/gcél)': Ppx})
df_params_exp=pd.DataFrame({'mimax_exp(h-¹)':[dad_inic[0]], 'Ks_exp(g/L)':[dad_inic[1]],'Kd_exp(h-¹)':[dad_inic[2]],'Yxs_exp(gcél/gsub)':[dad_inic[7]], 'alfa_exp(gprod/gcél)':[dad_inic[8]], 'beta_exp(gprod/gcél.h)':[dad_inic[9]],'m_exp(adim)':[dad_inic[10]],'Cx_estr_exp(g/L)':[dad_inic[11]], 'tempo decorrido(s)':[elapsed]})
df_params =pd.DataFrame({'mimax(h-¹)':[param_otim[0]],'Ks(g/L)':[param_otim[1]],'Kd(h-¹)':[param_otim[2]],'Yxs(gcél/gsub)':[param_otim[3]], 'alfa(gprod/gcél)': [param_otim[4]], 'beta(gprod/gcél.h)':[param_otim[5]], 'm(adim)':[param_otim[6]], 'Cx_estr(g/L)':[param_otim[7]]})
df_icpar =pd.DataFrame({'ICmimax':[ICpar[0]],'ICKs':[ICpar[1]],'ICKd':[ICpar[2]],'ICYxs':[ICpar[3]], 'ICalfa': [ICpar[4]], 'ICbeta':[ICpar[5]], 'ICm':[ICpar[6]], 'ICCx_estr':[ICpar[7]]})   
df_concents_exp= pd.DataFrame({'Tempo_exp(h)': t_exp,'Cx_exp(g/L)': C_exp[:,0],'Cs_exp(g/L)': C_exp[:,1],'Cp_exp(g/L)': C_exp[:,2]})
df_produtiv_exp = pd.DataFrame({'Px_exp(gcél/L.h)': Px_exp, 'Pp_exp(gprod/L.h)': Pp_exp, 'Ppx_exp(gprod/gcél)': Ppx_exp})

## Dataframes para separação dos tempos experimental e modelo
df_teste = pd.DataFrame({'Tempo(h)': t})
df_teste_conc = pd.DataFrame({'Cx(g/L)': C_otim[:,0], 'Cs(g/L)': C_otim[:,1], 'Cp(g/L)': C_otim[:,2]})
df_teste_exp = pd.DataFrame({'Tempo_exp(h)': t_exp})
df_teste_exp_conc = pd.DataFrame({'Cx_exp(g/L)': C_exp[:,0],'Cs_exp(g/L)': C_exp[:,1],'Cp_exp(g/L)': C_exp[:,2]})

# Teste: qual tempo tem o menor intervalo de divisão temporal
control_compar = len(t)
   
## Laço para comparação de tempos iguais (experimental e modelo) 
i_compar_exp = 0
i_compar_model = 0
temp_model=[]
temp_exp=[]
concent_model = []
concent_exp = []
while (i_compar_exp  < control_compar) and (i_compar_model < control_compar):
    exp_teste = df_teste_exp.at[i_compar_exp, 'Tempo_exp(h)']
    model_teste = df_teste.at[i_compar_model, 'Tempo(h)']
    dif = np.round(exp_teste - model_teste,decimals=1)
    if dif != 0:
        i_compar_model = 1 + i_compar_model
    else:
        temp_model.append(model_teste)
        temp_exp.append(exp_teste)
        df_temp_model = pd.DataFrame({"Tempo(h)": temp_model})
        df_temp_exp = pd.DataFrame({"Tempo_exp(h)": temp_exp})
        debitado_model = df_teste_conc.loc[i_compar_model]
        debitado_model = pd.Series(debitado_model).values
        debitado_exp = df_teste_exp_conc.loc[i_compar_exp]
        debitado_exp = pd.Series(debitado_exp).values
        df_conc_model = pd.DataFrame({'Cx(g/L)':[debitado_model[0]],'Cs(g/L)':[debitado_model[1]],'Cp(g/L)':[debitado_model[2]]})
        concent_model.append(df_conc_model)
        df_conc_exp = pd.DataFrame({'Cx_exp(g/L)':[debitado_exp[0]], 'Cs_exp(g/L)':[debitado_exp[1]], 'Cp_exp(g/L)':[debitado_exp[2]]})
        concent_exp.append(df_conc_exp)
        i_compar_model =  1 + i_compar_model
        i_compar_exp =  1 + i_compar_exp   

df_concent_model = pd.concat(concent_model)
df_concent_exp = pd.concat(concent_exp)
df_concent_model.reset_index(drop=True, inplace=True)
df_concent_exp.reset_index(drop=True, inplace=True)

# Cálculo do coeficiente de regressão:
med_conc = df_conc_exp.mean(axis=0)
med_conc_val = pd.Series(med_conc).values

df_med_conc = pd.DataFrame({'Cxexp_med(g/L)':[med_conc_val[0]], 'Csexp_med(g/L)':[med_conc_val[1]],'Cpexp_med(g/L)':[med_conc_val[2]]})
    
df_saida_compar = pd.concat ([df_temp_exp,df_concent_exp, df_temp_model, df_concent_model,df_med_conc], axis=1)
     
## Determinação da soma do quadrado do resíduo:
df_saida_compar['DQres_Cx'] = (df_concent_exp['Cx_exp(g/L)'] - df_concent_model['Cx(g/L)']) ** 2
df_saida_compar['DQres_Cs'] = (df_concent_exp['Cs_exp(g/L)'] - df_concent_model['Cs(g/L)']) ** 2
df_saida_compar['DQres_Cp'] = (df_concent_exp['Cp_exp(g/L)'] - df_concent_model['Cp(g/L)']) ** 2
## Determinação da soma do quadrado do resíduo:

cx_med = np.repeat(med_conc_val[0],len(temp_exp))
cs_med = np.repeat(med_conc_val[1],len(temp_exp))
cp_med = np.repeat(med_conc_val[2],len(temp_exp))
df_SQtotal_cx = pd.DataFrame ({'Cxexp_med(g/L)': cx_med, 'Csexp_med(g/L)': cs_med, 'Cpexp_med(g/L)': cp_med})
df_saida_compar['DQtot_Cx'] = (df_concent_exp['Cx_exp(g/L)'] - df_SQtotal_cx['Cxexp_med(g/L)']) ** 2
df_saida_compar['DQtot_Cs'] = (df_concent_exp['Cs_exp(g/L)'] - df_SQtotal_cx['Csexp_med(g/L)']) ** 2
df_saida_compar['DQtot_Cp'] = (df_concent_exp['Cp_exp(g/L)'] - df_SQtotal_cx['Cpexp_med(g/L)']) ** 2
## Soma SQres e QStot: 
soma_SQres_SQtot = df_saida_compar.sum(axis=0) #pegar 11,12,13,14,15 e 16
soma_SQres_SQtot_val= pd.Series(soma_SQres_SQtot).values
SQres = soma_SQres_SQtot_val[11] + soma_SQres_SQtot_val[12] + soma_SQres_SQtot_val[13]
SQtotal = soma_SQres_SQtot_val[14] + soma_SQres_SQtot_val[15] + soma_SQres_SQtot_val[16]
df_soma_SQres_SQtot = pd.DataFrame({'SQres':[SQres], 'SQtot':[SQtotal]})
## Cálculo do R²:
r2 = 1 - (SQres/SQtotal)
df_r2 = pd.DataFrame({'R²': [r2]})
    
# Saídas para as planilhas:
## Cálculo do R²:
df_saida_compar_comp = pd.concat ([df_temp_exp, df_concent_exp, df_temp_model, df_concent_model, df_med_conc,df_soma_SQres_SQtot, df_r2], axis=1)
with pd.ExcelWriter('Cálculo_R2_model_acopl_bat_Lee_et_al.xlsx') as writer:
    df_saida_compar_comp.to_excel(writer, sheet_name="Lee_et_al")
    writer.save()
## Valores de tempo, concentração, produtividade, parâmetros cinéticos e erros:   
df_concents = pd.concat([df_concents_exp, df_produtiv_exp, df_concents, df_params_exp, df_params, df_icpar, df_r2], axis=1) 
with pd.ExcelWriter('Saída_model_acopl_bat_Lee_et_al.xlsx') as writer:
    df_concents.to_excel(writer, sheet_name="Lee_et_al")
    writer.save()
 
print("R²" , r2)       

# Importação das bibliotecas necessárias e módulos:
import Modulos_Moser
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np


# Módulo - geração randômica dos valores de entrada para a simulação
val_ent_rand_Moser = Modulos_Moser.entr_rand_Moser()

# Modelos matemáticos preditos pelo balanço de massa para batelada com cinética de Moser:
def sim_bat_Moser_01(C,t):
    Cx,Cs,Cp=C
    sim_bat_Moser_val_entr = val_ent_rand_Moser[0]
    mimaximo = sim_bat_Moser_val_entr[0]
    Ks = sim_bat_Moser_val_entr[1]
    Kd = sim_bat_Moser_val_entr[2]
    Yxs = sim_bat_Moser_val_entr[7]
    alfa = sim_bat_Moser_val_entr[8]
    beta = sim_bat_Moser_val_entr[9]
    mi_exp = sim_bat_Moser_val_entr[10]
    
    mi=mimaximo*((Cs**mi_exp)/(Ks+(Cs**mi_exp)))
    dCxdt=(mi-Kd)*Cx
    dCsdt=(-1/Yxs)*mi*Cx
    dCpdt=alfa*mi*Cx+beta*Cx
    return(dCxdt,dCsdt,dCpdt)


def sim_bat_Moser_02(C,t):
    Cx,Cs,Cp=C
    sim_bat_Moser_val_entr = val_ent_rand_Moser[0]
    mimaximo = sim_bat_Moser_val_entr[0]
    Ks = sim_bat_Moser_val_entr[1]
    Kd = sim_bat_Moser_val_entr[2]
    Yxs = sim_bat_Moser_val_entr[7]
    alfa = sim_bat_Moser_val_entr[8]
    beta = sim_bat_Moser_val_entr[9]
    mi_exp = sim_bat_Moser_val_entr[11]
    
    mi=mimaximo*((Cs**mi_exp)/(Ks+(Cs**mi_exp)))
    dCxdt=(mi-Kd)*Cx
    dCsdt=(-1/Yxs)*mi*Cx
    dCpdt=alfa*mi*Cx+beta*Cx
    return(dCxdt,dCsdt,dCpdt)

def sim_bat_Moser_03(C,t):
    Cx,Cs,Cp=C
    sim_bat_Moser_val_entr = val_ent_rand_Moser[0]
    mimaximo = sim_bat_Moser_val_entr[0]
    Ks = sim_bat_Moser_val_entr[1]
    Kd = sim_bat_Moser_val_entr[2]
    Yxs = sim_bat_Moser_val_entr[7]
    alfa = sim_bat_Moser_val_entr[8]
    beta = sim_bat_Moser_val_entr[9]
    mi_exp = sim_bat_Moser_val_entr[12]
    
    mi=mimaximo*((Cs**mi_exp)/(Ks+(Cs**mi_exp)))
    dCxdt=(mi-Kd)*Cx
    dCsdt=(-1/Yxs)*mi*Cx
    dCpdt=alfa*mi*Cx+beta*Cx
    return(dCxdt,dCsdt,dCpdt)

def sim_bat_Moser_04(C,t):
    Cx,Cs,Cp=C
    sim_bat_Moser_val_entr = val_ent_rand_Moser[0]
    mimaximo = sim_bat_Moser_val_entr[0]
    Ks = sim_bat_Moser_val_entr[1]
    Kd = sim_bat_Moser_val_entr[2]
    Yxs = sim_bat_Moser_val_entr[7]
    alfa = sim_bat_Moser_val_entr[8]
    beta = sim_bat_Moser_val_entr[9]
    mi_exp = sim_bat_Moser_val_entr[13]
    
    mi=mimaximo*((Cs**mi_exp)/(Ks+(Cs**mi_exp)))
    dCxdt=(mi-Kd)*Cx
    dCsdt=(-1/Yxs)*mi*Cx
    dCpdt=alfa*mi*Cx+beta*Cx
    return(dCxdt,dCsdt,dCpdt)

def sim_bat_Moser_05(C,t):
    Cx,Cs,Cp=C
    sim_bat_Moser_val_entr = val_ent_rand_Moser[0]
    mimaximo = sim_bat_Moser_val_entr[0]
    Ks = sim_bat_Moser_val_entr[1]
    Kd = sim_bat_Moser_val_entr[2]
    Yxs = sim_bat_Moser_val_entr[7]
    alfa = sim_bat_Moser_val_entr[8]
    beta = sim_bat_Moser_val_entr[9]
    mi_exp = sim_bat_Moser_val_entr[14]
    
    mi=mimaximo*((Cs**mi_exp)/(Ks+(Cs**mi_exp)))
    dCxdt=(mi-Kd)*Cx
    dCsdt=(-1/Yxs)*mi*Cx
    dCpdt=alfa*mi*Cx+beta*Cx
    return(dCxdt,dCsdt,dCpdt)

# Condições iniciais para integração:
inic_cond = val_ent_rand_Moser[1]
t = val_ent_rand_Moser[2]

# Integrando numericamente:
C_1 = odeint(sim_bat_Moser_01,inic_cond,t)
Cs_1 = C_1[:,1]
print(Cs_1)
print(Cs_1)
C_2 = odeint(sim_bat_Moser_02,inic_cond,t)
C_3 = odeint(sim_bat_Moser_03,inic_cond,t)
C_4 = odeint(sim_bat_Moser_04,inic_cond,t)
C_5 = odeint(sim_bat_Moser_05,inic_cond,t)

# Cálculo de mi:
sim_bat_Moser_val_entr = val_ent_rand_Moser[0]
mi_1=sim_bat_Moser_val_entr[0]*((Cs_1**sim_bat_Moser_val_entr[10])/(sim_bat_Moser_val_entr[1]+(Cs_1**sim_bat_Moser_val_entr[10])))
mi_2=sim_bat_Moser_val_entr[0]*((C_2[:,1]**sim_bat_Moser_val_entr[11])/(sim_bat_Moser_val_entr[1]+(C_2[:,1]**sim_bat_Moser_val_entr[11])))
mi_3=sim_bat_Moser_val_entr[0]*((C_3[:,1]**sim_bat_Moser_val_entr[12])/(sim_bat_Moser_val_entr[1]+(C_3[:,1]**sim_bat_Moser_val_entr[12])))
mi_4=sim_bat_Moser_val_entr[0]*((C_4[:,1]**sim_bat_Moser_val_entr[13])/(sim_bat_Moser_val_entr[1]+(C_4[:,1]**sim_bat_Moser_val_entr[13])))
mi_5=sim_bat_Moser_val_entr[0]*((C_5[:,1]**sim_bat_Moser_val_entr[14])/(sim_bat_Moser_val_entr[1]+(C_5[:,1]**sim_bat_Moser_val_entr[14])))

 


'''
Cs_1_rever=[]
i_Cs = (len(Cs_1)-1)
while i_Cs >= 0:
    Cs_rever = Cs_1[i_Cs]
    print(Cs_rever)
    Cs_1_rever.append(Cs_rever)
    i_Cs = i_Cs-1 
Cs_1_rever = np.asarray(Cs_1_rever)

mi_1_rever=[]
i_mi = (len(mi_1)-1)
while i_mi >= 0:
    mi_rever = mi_1[i_mi]
    print(mi_rever)
    mi_1_rever.append(mi_rever)
    i_mi = i_mi-1 
mi_1_rever = np.asarray(mi_1_rever)

x = Cs_1_rever
power = mi_1_rever
x_new = np.linspace(x.min(),x.max(),300)   
spl = make_interp_spline(x, power, k=3) #BSpline object
power_smooth = spl(x_new)  

plt.plot(x_new,power_smooth,'red',linestyle='--',linewidth=5,label=sim_bat_Moser_val_entr[10]) 
plt.plot(x_new,mi_1_rever,'red',linestyle='--',linewidth=5,label=sim_bat_Moser_val_entr[10])                            
'''
# Determinação tamanho eixos gráficos
SMALL_SIZE = 13                        
MEDIUM_SIZE = 16                      
BIGGER_SIZE = 16                      
plt.rc('font', size=SMALL_SIZE)          
plt.rc('axes', titlesize=SMALL_SIZE)     
plt.rc('axes', labelsize=MEDIUM_SIZE)    
plt.rc('xtick', labelsize=SMALL_SIZE)    
plt.rc('ytick', labelsize=SMALL_SIZE)    
plt.rc('legend', fontsize=SMALL_SIZE)    
plt.rc('figure', titlesize=BIGGER_SIZE) 

f = plt.figure()                                               
_ = plt.plot(C_1[:,1],mi_1,'red',linestyle="--", linewidth=5,label='0.6')  
_ = plt.plot(C_2[:,1],mi_2,'lime',linestyle="--", linewidth=5,label='0.8')  
_ = plt.plot(C_3[:,1],mi_3,'purple',linestyle="--",linewidth=5,label='1.0') 
_ = plt.plot(C_4[:,1],mi_4,'yellow',linestyle = "--", linewidth=5,label='1.6') 
_ = plt.plot(C_5[:,1],mi_5,'blue',linestyle = "--",linewidth=5,label='1.8') 
   
_ = plt.xlabel('Cs (g/L)',weight='bold')               
_ = plt.ylabel('Taxa especpifica de crescimento $\mu= (h^{-1}$)', weight='bold')


_ = plt.text(34.5,0.061,"BBBB", fontsize = 72, color = "white",
         bbox={'facecolor': 'white'})
_ = plt.text(35,0.085,'$\mu máx(h^{-1})$    Ks(g/L)', style='oblique', fontsize = 18)
_ = plt.text(37.5,0.055,sim_bat_Moser_val_entr[0], fontsize = 17)
_ = plt.text(47,0.055,sim_bat_Moser_val_entr[1], fontsize = 17)

_ = plt.legend(loc='upper left', bbox_to_anchor=(0.015, 1.0),title = "Adimensional u",fontsize = 14, ncol=1, fancybox=True, shadow=True )   
                                          
_ = plt.grid(True)                                                  
_ = f.set_figheight(9)                                                 
_ = f.set_figwidth(12)                                                  
_ = f.patch.set_facecolor('white')                                     
_ = plt.style.use('default')  
_ = plt.savefig("Batelada Moser simulação.png")





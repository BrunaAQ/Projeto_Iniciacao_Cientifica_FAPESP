# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 14:47:30 2020

@author: Bruna Aparecida
"""


                                          # MODELAGEM - AJUSTE NÃO LINEAR (ALGORITMO GENÉTICO - AG)#

# Módulo com a função para definir:
# - os pesos de Cx, Cs e Cp para o processo de ajuste dos dados experimentais aos modelo;
# - o alcance numérico de busca a ser analisado pelo AG para cada modelo cinético não estruturado estudado.

def peso():
     dpC = [1,1,1]
     return(dpC)

def limites():
    limites_Monod = [(0, 1),(0.01, 100),(0, 1),(0, 10),(0, 1)] #5
    limites_Contois = [(0, 1),(0, 100),(0, 1),(0, 100),(0, 100)] #5
    limites_Moser = [(0, 1),(5, 10),(0.01, 1),(0, 10),(0, 1),(1,2)] #6
    limites_Andrews = [(0, 1),(0, 100),(0.01, 1),(0, 100),(0, 100),(1, 45)] #6
    limites_Hope_Hansford = [(0, 1),(0, 100),(0, 1),(0, 100),(0, 100),(0,100)]#6
    limites_Aiba = [(0, 1),(0, 100),(0, 1),(0, 100),(0, 100),(0.1,2)] #6
    limites_Wu = [(0, 1),(0, 5),(0.01, 10),(0, 10),(0, 10),(1,25),(1,2)]#7
    limites_Levenspiel = [(0, 1),(0, 100),(0.01, 1),(0, 10),(0, 1),(0,3),(1,50)]#7
    limites_Lee = [(0, 1),(0, 100),(0.01, 1),(0, 10),(0, 1),(0,3),(1,57)]#7
    limites_mi_const = [(0, 3),(0, 1),(0, 7),(0, 5)]#4
    return(limites_Monod, limites_Contois, limites_Moser, limites_Andrews, limites_Hope_Hansford,
           limites_Aiba, limites_Wu, limites_Levenspiel, limites_Lee, limites_mi_const)
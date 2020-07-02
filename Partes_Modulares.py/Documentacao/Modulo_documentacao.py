## MÓDULO PARA ESCRITA DA DOCUMENTAÇÃO PARA INTERFACE DE SIMULAÇÃO E MODELAGEM DE PROCESSOS FERMENTATIVOS ##

from tkinter import *
import tkinter as tk
from tkinter import Text

def caixa_texto_batelada(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 10", borderwidth = 3, relief = "sunken", bg = "grey80") 
    tex.configure(state='normal')
    tex_escrito = "A fermentação ocorre com ausência de fluxos de matéria \nexternos ao biorreator." 
    
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')

def caixa_texto_modelo_contois(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 12", borderwidth = 5, relief = "sunken", bg = "grey90") 
    tex.configure(state='normal')
    tex_escrito = "TIPO DE INIBIÇÃO DESCRITA: Nenhum\n\nPONTO CHAVE: Prevê os efeitos da transferência de massa substrato-célula\n\nPARÂMETRO KSX: Quanto mais elevado, mais lento será o crescimento microbiano"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
def caixa_texto_equacao_contois(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 10", borderwidth = 5, relief = "sunken", bg = "grey80") 
    tex.configure(state='normal')
    tex_escrito = u"t = Tempo de cultivo decorrido (tempo)\n\u03bc = Taxa específica de crescimento (tempo\u207b\u00b9)\n\u03bcmáx = Taxa específica máxima de crescimento (tempo\u207b\u00b9)\nCs = Concentração de substrato (massa.volume\u207b\u00b9)\nKSX = Constante de saturação (massa.volume\u207b\u00b9)"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
    
def caixa_texto_modelo_monod(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 12", borderwidth = 5, relief = "sunken", bg = "grey90") 
    tex.configure(state='normal')
    tex_escrito = "TIPO DE INIBIÇÃO DESCRITA: Nenhum\n\nPONTO CHAVE: Considera que as células estão em perfeito estado de equílibrio (fase log ou exponencial)\n\nPARÂMETRO Ks: Quanto mais elevado, mais lento será o crescimento microbiano"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
def caixa_texto_equacao_monod(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 10", borderwidth = 5, relief = "sunken", bg = "grey80") 
    tex.configure(state='normal')
    tex_escrito = u"t = Tempo de cultivo decorrido (tempo)\n\u03bc = Taxa específica de crescimento (tempo\u207b\u00b9)\n\u03bcmáx = Taxa específica máxima de crescimento (tempo\u207b\u00b9)\nCs = Concentração de substrato (massa.volume\u207b\u00b9)\nKs = Constante de saturação (massa.volume\u207b\u00b9)"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
    
def caixa_texto_modelo_moser(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 12", borderwidth = 5, relief = "sunken", bg = "grey90") 
    tex.configure(state='normal')
    tex_escrito = "TIPO DE INIBIÇÃO DESCRITA: Nenhum\n\nPONTO CHAVE: Provê um grau de liberdade adicional ao modelo de Monod\n\nPARÂMETRO u: Quanto mais elevado, mais acentuado será o crescimento microbiano"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
def caixa_texto_equacao_moser(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 10", borderwidth = 5, relief = "sunken", bg = "grey80") 
    tex.configure(state='normal')
    tex_escrito = u"t = Tempo de cultivo decorrido (tempo)\n\u03bc = Taxa específica de crescimento (tempo\u207b\u00b9)\n\u03bcmáx = Taxa específica máxima de crescimento (tempo\u207b\u00b9)\nCs = Concentração de substrato (massa.volume\u207b\u00b9)\nKs = Constante de saturação (massa.volume\u207b\u00b9)\nn = Parâmetro expoente (adimensional)"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')

def caixa_texto_modelo_andrews(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 12", borderwidth = 5, relief = "sunken", bg = "grey90") 
    tex.configure(state='normal')
    tex_escrito = "TIPO DE INIBIÇÃO DESCRITA: Inibição pelo substrato\n\nPONTO CHAVE: Prevê o efeito tóxico de uma substância às células microbianas\n\nPARÂMETRO KIS: Quanto mais baixo, maior a sensibilidade da cultura ao acúmulo de\nsubstrato"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
def caixa_texto_equacao_andrews(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 10", borderwidth = 5, relief = "sunken", bg = "grey80") 
    tex.configure(state='normal')
    tex_escrito = u"t = Tempo de cultivo decorrido (tempo)\n\u03bc = Taxa específica de crescimento (tempo\u207b\u00b9)\n\u03bcmáx = Taxa específica máxima de crescimento (tempo\u207b\u00b9)\nCs = Concentração de substrato (massa.volume\u207b\u00b9)\nKs = Constante de saturação (massa.volume\u207b\u00b9)\nKIS = Parâmetro expoente inibição (massa.volume\u207b\u00b9)"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
    
def caixa_texto_modelo_wu(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 12", borderwidth = 5, relief = "sunken", bg = "grey90") 
    tex.configure(state='normal')
    tex_escrito = "TIPO DE INIBIÇÃO DESCRITA: Inibição pelo substrato\n\nPONTO CHAVE: Traz um grau de liberdade a mais para a predição da inibição\n\nPARÂMETRO Ke: Quanto mais baixo, maior a sensível será a cultura\nPARÂMETRO v: Quanto mais baixo, maior a velocidade de crescimento microbiano"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
def caixa_texto_equacao_wu(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 10", borderwidth = 5, relief = "sunken", bg = "grey80") 
    tex.configure(state='normal')
    tex_escrito = u"t = Tempo de cultivo decorrido (tempo)\nu03bc = Taxa específica de crescimento (tempo\u207b\u00b9)\n\u03bcmáx = Taxa específica máxima de crescimento (tempo\u207b\u00b9)\nCs = Concentração de substrato (massa.volume\u207b\u00b9)\nKs = Constante de saturação (massa.volume\u207b\u00b9)\nKe = Constante inibição por substrato (volume.massa\u207b\u00b9)\nv = Parâmetro expoente de inibição (adimensional)"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')

def caixa_texto_modelo_aiba(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 12", borderwidth = 5, relief = "sunken", bg = "grey90") 
    tex.configure(state='normal')
    tex_escrito = "TIPO DE INIBIÇÃO DESCRITA: Inibição pelo produto\n\nPONTO CHAVE: Propõe uma relação exponencial entre crescimento e inibição\n\nPARÂMETRO Kp: Valores elevados implicam em baixa velocidade de crescimento celular"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
def caixa_texto_equacao_aiba(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 10", borderwidth = 5, relief = "sunken", bg = "grey80") 
    tex.configure(state='normal')
    tex_escrito = u"t = Tempo de cultivo decorrido (tempo)\n\u03bc = Taxa específica de crescimento (tempo\u207b\u00b9)\n\u03bcmáx = Taxa específica máxima de crescimento (tempo\u207b\u00b9)\nCs = Concentração de substrato (massa.volume\u207b\u00b9)\nKs = Constante de saturação (massa.volume\u207b\u00b9)\nKp = Parâmetro expoente de inibição (volume.massa\u207b\u00b9)"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
    
def caixa_texto_modelo_h_h(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 12", borderwidth = 5, relief = "sunken", bg = "grey90") 
    tex.configure(state='normal')
    tex_escrito = "TIPO DE INIBIÇÃO DESCRITA: Inibição pelo produto\n\nPONTO CHAVE: Introduz uma expressão para predição da inibição ao modelo de Monod\n\nPARÂMETRO Kp: Valores elevados implicam em uma maior taxa de crescimento celular"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
def caixa_texto_equacao_h_h(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 10", borderwidth = 5, relief = "sunken", bg = "grey80") 
    tex.configure(state='normal')
    tex_escrito = u"t = Tempo de cultivo decorrido (tempo)\n\u03bc = Taxa específica de crescimento (tempo\u207b\u00b9)\n\u03bcmáx = Taxa específica máxima de crescimento (tempo\u207b\u00b9)\nCs = Concentração de substrato (massa.volume\u207b\u00b9)\nKs = Constante de saturação (massa.volume\u207b\u00b9)\nKp = Parâmetro expoente de inibição (massa.volume\u207b\u00b9)"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
    
def caixa_texto_modelo_levenspiel(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 12", borderwidth = 5, relief = "sunken", bg = "grey90") 
    tex.configure(state='normal')
    tex_escrito = "TIPO DE INIBIÇÃO DESCRITA: Inibição pelo produto\n\nPONTO CHAVE: Traz um parâmetro adicional para a predição da inibição\n\nPARÂMETRO Cp*: Podem apresentar valores extrapolados para experimentos reais\nPARÂMETRO n: Valores mais altos culminam na redução do crescimento microbiano"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
def caixa_texto_equacao_levenspiel(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 10", borderwidth = 5, relief = "sunken", bg = "grey80") 
    tex.configure(state='normal')
    tex_escrito = u"t = Tempo de cultivo decorrido (tempo)\n\u03bc = Taxa específica de crescimento (tempo\u207b\u00b9)\n\u03bcmáx = Taxa específica máxima de crescimento (tempo\u207b\u00b9)\nCs = Concentração de substrato (massa.volume\u207b\u00b9)\nKs = Constante de saturação (massa.volume\u207b\u00b9)\nCp* = Concentração crítica de produto (massa.volume\u207b\u00b9)\nn = Constante de Levenspiel (adimensional)"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
    
def caixa_texto_modelo_lee(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 12", borderwidth = 5, relief = "sunken", bg = "grey90") 
    tex.configure(state='normal')
    tex_escrito = "TIPO DE INIBIÇÃO DESCRITA: Inibição pela biomassa\n\nPONTO CHAVE: Considera o efeito inibitório do acúmulo de biomassa\n\nPARÂMETRO Cx*: Não deve ser superior ao Cx máximo observado no cultivo\nPARÂMETRO m: Quanto mais baixo, menor a velocidade do crescimento microbiano"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
def caixa_texto_equacao_lee(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 10", borderwidth = 5, relief = "sunken", bg = "grey80") 
    tex.configure(state='normal')
    tex_escrito = u"t = Tempo de cultivo decorrido (tempo)\n\u03bc = Taxa específica de crescimento (tempo\u207b\u00b9)\n\u03bcmáx = Taxa específica máxima de crescimento (tempo\u207b\u00b9)\nCs = Concentração de substrato (massa.volume\u207b\u00b9)\nKs = Constante de saturação (massa.volume\u207b\u00b9)\nCx* = Concentração crítica de células (massa.volume\u207b\u00b9)\nm = Constante de Lee at al (adimensional)"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')

def caixa_texto_integ_num(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 12", borderwidth = 5, relief = "sunken", bg = "grey90") 
    tex.configure(state='normal')
    tex_escrito = "MODO DE IMPLEMENTAÇÃO: Módulo odeint (pacote Scipy), que aplica a rotina em \nFortran 77 LSODA\n\nOBJETIVO: Integração numérica do sistema de EDOs pelo método de Runge-Kutta de 2a\nordem, sendo o crescimento microbiano descrito por diferentes modelos cinéticos"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
def caixa_texto_ag(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 12", borderwidth = 5, relief = "sunken", bg = "grey90") 
    tex.configure(state='normal')
    tex_escrito = "MODO DE IMPLEMENTAÇÃO: Módulo Differencial Evolution (pacote Scipy, subpacote\noptmize)\n\nMECANISMO DE CONVERGÊNCIA: Global\n\nPRINCÍPIO DE FUNCIONAMENTO DO ALGORITMO: Geração possíveis de soluções\ncandidatas ao problema de minimização. Por se uma classe de Algoritmo Evolutivo, envolve a\naplicação dos conceitos de bounds, genes, cromossomos, geração, recombinação, mutação e\nreplicação, em um contexto de aleatoriedade e avaliações estatísticas"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')
def caixa_texto_alm(frame, altura, largura, x, y):
    tex = Text(frame, height = altura, width = largura, font = "times 12", borderwidth = 5, relief = "sunken", bg = "grey90") 
    tex.configure(state='normal')
    tex_escrito = "MODO DE IMPLEMENTAÇÃO: Módulo Leastsq (pacote Scipy, subpacote\noptmize)\n\nMECANISMO DE CONVERGÊNCIA: Local\n\nPRINCÍPIO DE FUNCIONAMENTO DO ALGORITMO: Busca de soluções mínimas\nlocais dentro de um intervalo numérico restrito de busca por meio da aplicação de uma\nequação relacional de valores de entrada e modelo única e peculiar"
    tex.place(x = x, y = y)
    tex.insert(tk.END, tex_escrito)
    tex.configure(state='disabled')


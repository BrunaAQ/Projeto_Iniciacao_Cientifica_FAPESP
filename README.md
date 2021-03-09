# 🖥️🔬Projeto de pesquisa Iniciação Científica N°2019/24737-9🧫🦠
As pastas que trazem os arquivos escritos em Python (._py_) ou ainda salvos em outra extensão (._xlsx_ e ._png_) que contemplam os resultados apresentados e discutidos no Relatório Parcial submetido à FAPESP para análise foram criadas seguindo o esquema descrito abaixo (o repositório utilizado na rotina de trabalho para desenvolvimento do projeto, com todos os commits (alterações e versionamentos) realizados, encontra-se nomeado por "Projeto_fermenpy" e associado à mesma conta deste aqui tratado). 

## Pastas inseridas referentes ao Relatório Científico Final:
  - "<i><b>Batelada_Alimentada</i></b>": Traz os códigos .py desenvolvidos para a simulação e modelagem de bioprocessos fermentativos microbianos operados operados com alimentação de substrato (compostos pelas fases de cultivo em batelada e batelada alimentada propriamente dito), assim como os módulos de apoio necessários à correta execução dos algoritmos, considerando todos os perfis de vazão discutidos no relatório submetido;
  - "<i>Continuo_Quimiostato</i>": Comtempla o <i>script</i> Python para a simulação de bioprocessos fermentativos com culturas contínuas em estado estacionário, considerando entrada de substrato e saída de caldo fermentado. O diretório também hospeda os módulos de apoio para a perfeita execução do algoritmo;
  - "<i>Continuo_diferentes_vazoes</i>": Aqui está o <i>notebook</i> contendo o código Python para o estudo <i>in silico</i> de fermentações contínuas em estado não estacinário, conduzido a fim de se avaliar casos de enchimento e esvaziamento do reator frente a valores de vazão para entrada de substrato e saída de material fermentado;
  - *"<i>Interfaces_Graficas_Tkinter</i>"*: Foi adicionado o algoritmo responsável pela geração do programa de apoio Fermenpy BA-I, criado para permitir a simulação e modelagem de fermentações microbianas em batelada alimentada em formato GUI.
 
 ## Pastas que compreendem todo o material submetido ao Relatório Científico Parcial:
- ___"Partes_Modulares.py":___ Guarda os códigos cujas linhas de comandos descrevem funções que permitem a importação automatizada dos valores fornecidos a cada um dos parâmetros cinéticos envolvidos nos equacionamentos cinéticos estudados para a automatização da simulação, bem como a de funções objetivas e dos sistemas de equações não lineares empregados nas etapas de modelagem computacional. Ainda, os módulos atuam na definição dos limites (_bounds_) e pesos necessários à satisfatória definição do algoritmo de evolução diferencial através do _differential evolution_, bem como permitem a construção da documentação que será inserida na interface Fermenpy. São importados para os códigos .py principais, necessitando, para tanto, estarem alocados no mesmo diretório em que os mesmos se encontram armazenados na máquina de operação dos algoritmos;

- ___"Simulacao_Batelada_Modelos_Cineticos":___ Traz os códigos a nível _Back-End_ (aqueles que são executados com apoio do terminal/console fornecido pelos programas editores de texto) responsáveis por realizar a predição matemática dos perfis temporais de concentração, produtividade e taxa específica de crescimento microbiano a partir da importação automatizada dos parâmetros cinéticos e operacionais requeridos pelas leis cinéticas implementadas pelos algoritmos e que é feita diretamente através dos módulos criados em extensão .py e alocados na pasta anterior;

- ___"Modelagem_Batelada_Modelos_Cineticos":___ Traz os códigos a nível _Back-End_ (aqueles que são executados com apoio do terminal/console fornecido pelos programas editores de texto) responsáveis por implementar etapas de otimização computacional, retornando como saídas no console os perfis temporais de concentração, produtividade e taxa específica de crescimento microbiano simulados e modelados, bem como cálculos estatísticos que avaliam a performance do ajuste realizado, sendo a entrada de dados realizada igualmente a partir de módulos. A pasta é composta ainda por diversas planilhas eletrônicas, em formato Excel, elaboradas com o intuito de serem aplicadas nos códigos de estimação de parâmetros cinéticos, além de contar com a disponibilização de documento empregado para a etapa de validação do algoritmo de otimização por alinhamento Algoritmo Genético (AG) - Algoritmo de Levenberg-Marquardt (ALM);

- ___"Interfaces_Graficas_Tkinter":___ Hospeda os códigos-fonte, já com a adição dos comandos necessários à criação das interfaces gráficas de usuário (nível _Front-End_), por auxílio do pacote Python Tkinter, os quais permitem a implementação de algoritmos de regressão linear e, com isso, a construção de curvas de calibração e tratamento de dados a elas relacionados (Calibrapy), bem como de simulação e modelagem (Fermenpy) passíveis de serem executados como arquivos executáveis (.exe), descartando a obrigatoriedade do uso de programas de edição para tanto. O diretório "Arquivos_Adicionais" guarda as figuras e todo o material visual contido nas interfaces desenvolvidas e que devem, por essa razão, serem importados oportunamente em suas linhas de comando, ao passo que aquele nomeado por "Arquivos_para_Calibrar_e_Quantificar_Cx", alocados como uma subpasta relacionada apenas à interface Calibrapy, disponibiliza planilhas previamente preparadas e que contém sugestões de dados que permitem o programa ser executado prontamente e retornar suas saídas ao usuário. Aqui, o programa Fermenpy permite o cálculo do intervalo de confiança associado aos parâmetros estimados;

- ___"Graficos_Documentos_Submetidos":___ Aqui estão os arquivos desenvolvidos em linguagem Python que permitiram a criação, por autoria própria, das figuras gráficas empregadas com fins ilustrativos e demonstrativos das fases do crescimento microbiano (submetido juntamente com o projeto de pesquisa aqui relacionado) e da influência exercida pela constante de Moser "u" na velocidade do crescimento microbiano.

__Importante__: Todos os códigos implementados em linguagem Python de programação contidos neste repositório foram escritos, executados, testados e validados através da utilização e exploração do ambiente de programação científica _Spyder_, acessado por meio do _software open source Anaconda Navigator_.
Os modelos cinéticos encontram-se classificados, no interior das pastas criadas e componentes do repositório, de acordo com a ausência, presença e qual o tipo de inibição que descrevem, seguindo a abordagem levantada no Relatório Parcial e nos documentos a ele anexados por intermédio da plataforma SAGE.


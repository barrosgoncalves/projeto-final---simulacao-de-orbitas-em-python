#!/usr/bin/env python
# coding: utf-8

# T1

# In[2]:


import pandas as pd
from pandas import *

df = pd.read_csv('caracteristicas_corpos.csv')

df


# T2

# In[68]:


from math import *

conjcorpos = ['Terra', 'Marte', 'Urano']
corpo = 'Terra'
def aceleracao_corpo(conjcorpos, corpo):
    global G 
    G = 6.67384E-11

    #recolhe massas corpos em contribuicao
    massascorpos = []
    for nome in conjcorpos:
        massa = df.loc[df['nome'] == nome, 'massa'].iloc[0]
        massascorpos.append(massa)
    
    #recolhe coordenadas corpos em contribuicao
    coordenadascorpos = []
    for nome in conjcorpos:
        c1 = (df.loc[df['nome'] == nome, 'lx'].iloc[0], df.loc[df['nome'] == nome, 'ly'].iloc[0], df.loc[df['nome'] == nome, 'lz'].iloc[0])
        coordenadascorpos.append(c1)
    
    #recolhe coordenadas corpo que sofre aceleracao
    coordenadascorpo = [df.loc[df['nome'] == corpo, 'lx'].iloc[0], df.loc[df['nome'] == corpo, 'ly'].iloc[0], df.loc[df['nome'] == corpo, 'lz'].iloc[0]]
    
    aceleracoes = []
    for i in range(len(massascorpos)):
        if corpo != conjcorpos[i]:#p cada corpo em contribuição
            ac = ((G*massascorpos[i])/((((coordenadascorpo[0]-coordenadascorpos[i][0])**2)+((coordenadascorpo[1]-coordenadascorpos[i][1])**2)+((coordenadascorpo[2]-coordenadascorpos[i][2])**2))**(3/2))*(coordenadascorpos[i][0]-coordenadascorpo[0]), (G*massascorpos[i])/((((coordenadascorpo[0]-coordenadascorpos[i][0])**2)+((coordenadascorpo[1]-coordenadascorpos[i][1])**2)+((coordenadascorpo[2]-coordenadascorpos[i][2])**2))**(3/2))*(coordenadascorpos[i][1]-coordenadascorpo[1]), (G*massascorpos[i])/((((coordenadascorpo[0]-coordenadascorpos[i][0])**2)+((coordenadascorpo[1]-coordenadascorpos[i][1])**2)+((coordenadascorpo[2]-coordenadascorpos[i][2])**2))**(3/2))*(coordenadascorpos[i][2]-coordenadascorpo[2]))
            aceleracoes.append(ac)   

    componentesac = sum(i[0] for i in aceleracoes), sum(i[1] for i in aceleracoes), sum(i[2] for i in aceleracoes)
    
    return componentesac

aceleracao_corpo(conjcorpos, corpo)


# Na busca dos valores, a falta de tempo impediu a implementação de um algoritmo mais geral, que não se focasse nas colunas do dataframe? 
# 
# A utilização de tuplos como estrutura de recolha das coordenadas dos corpos em contribuição prende-se com o facto de atribuir uma forma de leitura tangível e percetível relativamente ao tipo de dado que aquele tuplo alberga (no caso, coordenadas 3D). 
# 
# Teria sido mais fácil simplesmente recolher cada coordenada de cada corpo e anexá-la à lista, fazendo posteriormente a divisão dessas coordenadas em tripletos aquando da computação do valor das componentes da aceleração, mas cremos que a nossa escolha é mais adequada, apesar de adicionar algumas linhas ao código para obter a entrada de índice x do tuplo.
# 
# A inclusão de diversos ciclos para calcular componentes estacionárias numa variável e mutáveis noutra da aceleração, apesar de incluir mais linhas de código, segue uma abordagem mais modular aos diversos cálculos realizados na utilização do método de Euler-Cromer. Apesar de visualmente mais pesada, e de ser possível realizar este cálculo numa série de ciclos "nested", esta abordagem acaba por tornar mais fácil a perceção dos diversos passos a utilizar - tornando a eventual manutenção ou reaproveitamento de código mais fácil e menos interdependente. -- agora compromete-se a modularidade do cálculo dos termos da equação em deterimento da otimização do código.

# In[62]:


# receber o valor da massa ou whatever
#obj1 = 'Sol'
#c = df.loc[df['nome'] == obj1, 'massa'].iloc[0]


# T3

# In[51]:


from math import *

conjcorpos = ['Terra', 'Marte', 'Urano']
deltat = 20
def velocidade_apos_dt(conjcorpos, deltat):
    
    velocidadescorpos = []
    for elem in conjcorpos:
        c1 = (df.loc[df['nome'] == elem, 'vx'].iloc[0], df.loc[df['nome'] == elem, 'vy'].iloc[0], df.loc[df['nome'] == elem, 'vz'].iloc[0])
        velocidadescorpos.append(c1)
    
    aceleracoescorpos = []
    for elem in conjcorpos:
        ac = aceleracao_corpo(conjcorpos, elem)
        aceleracoescorpos.append(ac)
    
    velatualiz = []
    for i in range(len(velocidadescorpos)):
        vel = (velocidadescorpos[i][0] + ((aceleracoescorpos[i][0])*deltat), velocidadescorpos[i][1] + ((aceleracoescorpos[i][1])*deltat), velocidadescorpos[i][2] + ((aceleracoescorpos[i][2])*deltat))
        velatualiz.append(vel)
    
    return velatualiz

#falta implementar os dicionarios que guardam a localizacao atual (? ou so na seguinte, em q guardo simult. pos e loc?)
velocidade_apos_dt(conjcorpos, deltat)


# T4

# In[69]:


from math import *

conjcorpos = ['Terra', 'Marte', 'Urano']
deltat = 20
def posicao_apos_dt(conjcorpos, deltat):

    poscorpos = []
    for elem in conjcorpos:
        pos = (df.loc[df['nome'] == elem, 'lx'].iloc[0], df.loc[df['nome'] == elem, 'ly'].iloc[0], df.loc[df['nome'] == elem, 'lz'].iloc[0])
        poscorpos.append(pos)

    velcorpos = []
    velocidades = velocidade_apos_dt(conjcorpos, deltat)
    velcorpos.append(velocidades)
    
    posatualiz = []
    for i in range(len(poscorpos)):
        coords = (poscorpos[i][0]+(velcorpos[0][i][0]*deltat), poscorpos[i][1]+(velcorpos[0][i][1]*deltat), poscorpos[i][2]+(velcorpos[0][i][2]*deltat))
        posatualiz.append(coords)
    
    dictscorpos = []
    #print(posatualiz[1][0])
    #l = [dict(zip(['lx'],posatualiz[i][j])) for i in range(len(conjcorpos)) j in range(len(velcorpos[0][0]))]
    for i in range(len(poscorpos)):
        dictscorpo = {'lx':posatualiz[i][0], 'ly':posatualiz[i][1], 'lz':posatualiz[i][2], 'vx':velcorpos[0][i][0], 'vy':velcorpos[0][i][1], 'vz':velcorpos[0][i][2]}
        dictscorpos.append(dictscorpo)
        
    histloc = []
    for i in range(len(dictscorpos)):
        histloc.append([[dictscorpos[i]['lx']], [dictscorpos[i]['ly']], [dictscorpos[i]['lz']]])
    
    return histloc

posicao_apos_dt(conjcorpos, deltat)


# T5

# In[75]:


conjcorpos = ['Terra', 'Marte', 'Urano']
deltat = 20
def chama_anteriores(conjcorpos, deltat):
    for elem in conjcorpos:
        velocidade_apos_dt(conjcorpos, deltat)
        posicao_apos_dt(conjcorpos, deltat)
    
    return 3

chama_anteriores(conjcorpos, deltat)


# T6

# In[74]:


conjcorpos = ['Terra', 'Marte', 'Urano']
deltat = 20
ndt = 5

def simulacao(conjcorpos, deltat, ndt):
    for elem in conjcorpos:
        chama_anteriores(conjcorpos, deltat)


# T7

# In[ ]:





# TESTE

# In[157]:


from math import *

conjcorpos = ['Venus', 'Marte']
corpo = 'Terra'
def aceleracao_corpo(conjcorpos, corpo):
    global G 
    G = 6.67384E-11

    #recolhe massas corpos em contribuicao
    massascorpos = []
    for nome in conjcorpos:
        massa = df.loc[df['nome'] == nome, 'massa'].iloc[0]
        massascorpos.append(massa)
    
    print(len(massascorpos))
    
    #recolhe coordenadas corpos em contribuicao
    coordenadascorpos = []
    for nome in conjcorpos:
        c1 = (df.loc[df['nome'] == nome, 'lx'].iloc[0], df.loc[df['nome'] == nome, 'ly'].iloc[0], df.loc[df['nome'] == nome, 'lz'].iloc[0])
        coordenadascorpos.append(c1)
    
    print(len(coordenadascorpos))
    
    #recolhe coordenadas corpo que sofre aceleracao
    coordenadascorpo = [df.loc[df['nome'] == corpo, 'lx'].iloc[0], df.loc[df['nome'] == corpo, 'ly'].iloc[0], df.loc[df['nome'] == corpo, 'lz'].iloc[0]]

    print(len(coordenadascorpo))
    
    cx = [tup[0] for tup in coordenadascorpos] # lista de coords em x dos corpos
    cy = [tup[1] for tup in coordenadascorpos] # lista de coords em y dos corpos
    cz = [tup[2] for tup in coordenadascorpos] # lista de coords em z dos corpos
    
    #calculo dos termos direcionais (xj-xi)
    termosdirecionais = []
    for j in range(len(coordenadascorpos)):
        for i in range(len(coordenadascorpos[0])):
            termo = coordenadascorpos[j][i] - coordenadascorpo[i]
            termosdirecionais.append(termo)
    
    print(len(termosdirecionais))
    
    #cálculo do termo da distancia (xi-xj)**2+(yi-yj)**2+(zi-zj)**2
    termosdist = []
    for j in range(len(coordenadascorpos)):
        for i in range(1):
            termo = ((coordenadascorpo[i] - coordenadascorpos[j][i])**2 + (coordenadascorpo[i+1] - coordenadascorpos[j][i+1])**2 + (coordenadascorpo[i+2] - coordenadascorpos[j][i+2])**2)
            termosdist.append(termo)
            
    print(len(termosdist))
    
    #cálculo do termo comum (G*mj)/(xi-xj)**2+(yi-yj)**2+(zi-zj)**2
    termoscomum = []
    for i in range(len(massascorpos)):
        termo = (G*massascorpos[i])/(termosdist[i])**(3/2)
        termoscomum.append(termo)
        
    print(len(termoscomum))
    
    #calculo das aceleracoes direcionais em x:
    aceleracoesdirecionais = []

    for j in range(len(termoscomum)):
        for i in range(len(termosdirecionais)):
            termo = termoscomum[j]*termosdirecionais[i]
            aceleracoesdirecionais.append(termo)

    print(len(aceleracoesdirecionais))

    #aceleracaox = sum()
    #aceleracaoy = sum()
    #aceleracaoz = sum()
    
    #return aceleracaox, aceleracaoy, aceleracaoz

aceleracao_corpo(conjcorpos, corpo)


# In[ ]:





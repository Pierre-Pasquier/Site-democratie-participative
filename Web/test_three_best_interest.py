# -*- coding: UTF-8 -*-
from sympy import factorint

premiers=[2,3,5,7,11,13,17,19,23,29]
def threeBestInterest(str):
    if type(str) != int:
        raise NameError('Mauvais type')
    if str <= 0:
        raise NameError('Nombre négatif')
    
    L=[0 for k in range(len(premiers))]

    for p in range(len(premiers)):
        s=str
        cpt=0
        while s%premiers[p]==0 and s > 0:
            cpt+=1
            s=s/premiers[p]
        L[p]=cpt
    A=max(L)
    L.remove(A)
    B=max(L)
    L.remove(B)
    C=max(L)
    return [A,B,C]

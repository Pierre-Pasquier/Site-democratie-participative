# -*- coding: UTF-8 -*-
#!/usr/bin/env python3

from sympy import factorint

def threeBestInterest(str):
    premiers=[2,3,5,7,11,13,17,19,23,29]
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


def test_threeBestInterest():
    premiers=[2,3,5,7,11,13,17,19,23,29]
    for n in range(10000):   
        dico = factorint(n)
        ld = [dico.get(k) for k in premiers]
        A = max(ld)
        ld.remove(A)
        B=max(ld)
        ld.remove(B)
        C=max(ld)
        assert threeBestInterest(n) == [A,B,C],"test failed" 
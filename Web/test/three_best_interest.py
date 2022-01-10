from sympy import factorint

def threeBestInterest(str,id_profil): #str représente soit score_dem ou bien score_offre
    db=getdb()
    c=db.cursor()
    c.execute("SELECT ? FROM Utilisateurs WHERE Utilisateurs.id_profil=?",(str,id_profil))
    Score=int(c.fetchall)
    L=[0 for k in range(len(premiers))]
    for p in range(len(premiers)):
        while Score%premiers[p] == 0:
            Score = 
        L[p]=Score%premiers[p]
    A=max(L)
    L.remove(A)
    B=max(L)
    L.remove(B)
    C=max(L)
    return [A,B,C]

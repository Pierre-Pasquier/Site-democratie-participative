def isDivided(k,L):
    for i in L:
        if k%i==0 :
            return True
    return False

def gerere_n_premiers(n):
    L=[]
    for p in range(2,n):
        if not isDivided(p,L):
            L.append(p)
    return L

def add(dico1,dico2,L):
    if dico2!=None:
        for key,value in dico2.items():
                    
            if key in dico1.keys():
                a=dico1.get(key)
                dico1.update({key:a+value})

            else:
                
                dico1.update({key:value})
        return dico1
    else: return dico1


def scoring(score,dico,L): #score >=1
    if score in L:
        a=dico.get(score)
        if not a:
            dico.update({score:1})
            return dico
        else:
            dico.update({score:a+1})
            return dico
    elif score==1:
        return dico

    copy=score




    for k in L:

            if copy%k==0:

                a=dico.get(k)
                if a!=None:
                    dico.update({k:a+1})
                else: 
                    dico.update({k:1})
                copy=copy//k
                dico2=scoring(copy,{},L)
                add(dico,dico2,L)
                return dico
    return dico







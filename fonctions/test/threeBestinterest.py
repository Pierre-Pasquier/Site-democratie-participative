
premiers=[2,3,5,7,11,13,17,19,23,29]
def threeBestInterest(Score): #str représente soit score_dem ou bien score_offre
    cptmax1=0
    cptmax2=0
    cptmax3=0
    max1=0
    max2=0
    max3=0
    for p in range(len(premiers)):
        copy=Score
        cpt=0

        while copy%premiers[p]==0 and copy>0:
            cpt+=1
            copy=copy//premiers[p]
        if cpt>cptmax1:
            if cpt>cptmax2:
                if cpt>cptmax3:
                    cptmax1=cptmax2
                    cptmax2=cptmax3
                    cptmax3=cpt
                    max1=max2
                    max2=max3
                    max3=premiers[p]
                else :
                    cptmax1=cptmax2
                    cptmax2=cpt
                    max1=max2
                    max2=premiers[p]
            else :
                cptmax1=cpt
                max1=premiers[p]
    if cptmax3==0:
        return (2,2,2)
    elif cptmax3!=0 and cptmax2==0:
        return (max3,max3,max3)
    elif cptmax3!=0 and cptmax2!=0 and cptmax1==0:
        return (max2,max2,max3)

    return (max1,max2,max3)
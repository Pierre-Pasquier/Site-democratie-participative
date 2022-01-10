from flask import Flask, Blueprint, render_template, abort, request, redirect,flash
from flask import g
import cryptocode    #installer cryptocode
import smtplib, ssl     #à importer
import random      #à importer
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import string
import random
import re
import datetime

app = Flask(__name__)
database= "db_projetS1.db"


def score(type,id):
    db=getdb()
    c=db.cursor()
    if type == 'demande':   #différenciation selon si offre ou demande
        c.execute("SELECT score_demande FROM Utilisateurs WHERE id_profil=?",(id,))
    else:
        c.execute("SELECT score_offre FROM Utilisateurs WHERE id_profil=?",(id,))
    l = c.fetchall()
    score=int(l[0][0])  #on récupère le score
    return score

dico_filtre = {2:'Jardinage',3:'Bricolage',5:'Déménagement',7:'Formation',11:'Babysitting',13:'Informatique',17:'Autres taches physiques',19:'Autres taches intellectuelles',23: 'Aide aux devoirs',29:'Autre...'}  #pour faire lien entre filtre et leurs nombre premier associé
dico_num = {'Jardinage':2,'Bricolage':3,'Déménagement':5,'Formation':7,'Babysitting':11,'Informatique':13,'Autres taches physiques':17,'Autres taches intellectuelles':19,'Aide aux devoirs':23,'Autre...':29} #pour faire lien entre nombre premier associé aux filtre et les filtres


def isDivided(k,L):     #pour voir si k divisible par un entier de la liste L
    for i in L:
        if k%i==0 :
            return True
    return False

def gerere_n_premiers(n):   #génère les nombres premiers strictement inférieur à n
    L=[]
    for p in range(2,n):
        if not isDivided(p,L):
            L.append(p)
    return L

def add(dico1,dico2,L):     #fusion de dico1 et dico2 en additionnant les valeurs des clés communes
    if dico2!=None:
        for key,value in dico2.items():

            if key in dico1.keys():
                a=dico1.get(key)
                dico1.update({key:a+value})

            else:

                dico1.update({key:value})
        return dico1
    else: return dico1


def scoring(score,dico,L): #score >=1, mets les diviseurs premiers de score et leur valuation p-adique dans dico
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

def threeBestInterest(type,id):     #retourne les 3 filtres préférés de l'utilisateur dont l'id est donnée en entrée pour le type donné (demande ou offre)
    scoree = score(type,id)
    print(scoree)
    L=[2,3,5,7,11,13,17,19,23,29]
    dico={}
    dico2 = scoring(scoree,dico,L)
    l_num = []
    l_num_filtre = []
    for k in dico2.items():     #stock les valeurs du dico dans 2 listes pour le traitement des données
        l_num.append(k[1])
        l_num_filtre.append(k[0])
    copy = [k for k in l_num]   #copie car l_num va être modifié
    if l_num == []:
        return ['Autre ...','Autre ...','Autre ...']
    else:           #stock les 3 plus grands éléments de l_num
        A = max(l_num)
        l_num.remove(A)
    if l_num == []:
        B = A
        C = A
    else:
        B = max(l_num)
        l_num.remove(B)
        if l_num == []:
            C = B
        else:
            C = max(l_num)
            l_num.remove(C)
    A = l_num_filtre[copy.index(A)]     #récupère les filtres associés aux 3 plus grands élément de l_num
    B = l_num_filtre[copy.index(B)]
    C = l_num_filtre[copy.index(C)]
    dico_filtre = {2:'Jardinage',3:'Bricolage',5:'Déménagement',7:'Formation',11:'Babysitting',13:'Informatique',17:'Autres taches physiques',19:'Autres taches intellectuelles',23: 'Aide aux devoirs',29:'Autre...'}
    A = dico_filtre[A]   #récupère les noms des 3 filtres préférés
    B = dico_filtre[B]
    C = dico_filtre[C]
    return [A,B,C]




def envoi_mail(email_receiver):         #pour envoyer un mail
    # on rentre les renseignements pris sur le site du fournisseur
    smtp_address = 'smtp.gmail.com'
    smtp_port = 465

    # on rentre les informations sur notre adresse e-mail
    email_address = 'helpnngo@gmail.com'
    email_password = 'tncytncy'

    # on crée un e-mail
    message = MIMEMultipart("alternative")
    # on ajoute un sujet
    message["Subject"] = "Vérification de votre adresse mail"
    # un émetteur
    message["From"] = email_address
    # un destinataire
    message["To"] = email_receiver

    #on génere un code
    code_1 = str(random.randint(0,9))
    code_2 = str(random.randint(0,9))
    code_3 = str(random.randint(0,9))
    code_4 = str(random.randint(0,9))
    code = code_1 + code_2 + code_3 + code_4

    # on crée un texte et sa version HTML
    texte = '''
    Bonjour 
    Voici votre code de vérification de votre adresse mail :
    ''' + code + '''
    '''

    html = '''
    <html>
    <body>
    <h1>Bonjour</h1>
    <p>Voici votre code de vérification de votre adresse mail :</p>
    <h2>''' + code + '''</h2>
    </body>
    </html>
    '''

    # on crée deux éléments MIMEText 
    texte_mime = MIMEText(texte, 'plain')
    html_mime = MIMEText(html, 'html')

    # on attache ces deux éléments 
    message.attach(texte_mime)
    message.attach(html_mime)

    # on crée la connexion
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
        # connexion au compte
        server.login(email_address, email_password)
        # envoi du mail
        server.sendmail(email_address, email_receiver, message.as_string())
    return code



def getdb():     #pour ouvrir la base de donnée
    db = getattr(g, '_database', None)
    db = g._database = sqlite3.connect(database)
    return db

def close_connection():  # pour fermer la connexion proprement
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def liste(l):
    #prends en entrée une liste en chaine de caractère et retourne cette liste
    if l == '[]':
        return []
    l = list(l)
    n = len(l)
    c = 0 #compteur
    lf = [] #liste finale
    while c < n:
        li = []     #liste intermédiaire    
        while c < n and l[c] != ',' :    #parcours l'élément jusqu'à rencontrer une ','
            li.append(l[c])
            c+=1
        lf.append(li)
        c += 1
    for k in range(len(lf)):
        x = lf[k][0]
        for j in range(len(lf[k])):
            if j !=0:
                x += lf[k][j]
        lf[k] = int(x)
    return lf




@app.route('/')      #redirection vers page d'accueil
def redirection():
    return redirect('/home')


@app.route('/à_propos')      #page à propos
def apropos():
    id = request.args.get('id')
    return render_template('apropos.html',id_user=id)


@app.route('/contactez_nous')   #page contactez nous
def contactez():
    id = request.args.get('id')
    return render_template('contacteznous.html',id_user=id)


@app.route('/home')     #page d'accueil
def home():
    id=request.args.get('id')
    if id is None or id=='':
        return render_template('home.html') 
    return render_template('home_connect.html',id_user=id)


@app.route('/connexion', methods=["GET", "POST"])   #page de connexion
def connex():
    erreur = False
    if request.form.get("mail") and request.form.get("mdp"):    #si les champs sont remplis
        mdp = request.form.get("mdp")
        db = getdb()
        c = db.cursor()
        c.execute("SELECT id_profil,mdp FROM Utilisateurs WHERE mail = ?",(request.form.get("mail"),))  #on récupère id et mdp associé à l'adresse mail donnée
        l = c.fetchall()
        
        if l == []:     #si pas inscrit
            return render_template('connexion.html',erreur=erreur,pas_inscrit=True)
        close_connection()
        bon_mdp = l[0][1]
        id = l[0][0]
        bon_mdp_decrypte = cryptocode.decrypt(bon_mdp,'tncy')   #on décrypte le mot de passe de la base de donnée pour le comparer à celui donné
        if bon_mdp_decrypte != mdp:   #si mauvais mot de passe
            erreur = True
        else:
            return redirect('/'+str(id)+'/mc/profil')   #si bon mot de passe, on redirige
    return render_template('connexion.html',erreur=erreur,pas_inscrit=False)    #on affiche la page

@app.route('/inscription', methods=["GET", "POST"])     #page d'inscription
def inscription():
    global mail
    mail = request.form.get("mail")     #on récupère les informations données
    global numtel
    numtel = str('' if request.form.get("numTel") is None else request.form.get("numTel"))
    erreur_tel = len(numtel) != 10 and len(numtel) != 14 and numtel != ''
    global pseudo
    pseudo = str('' if request.form.get("pseudo") is None else request.form.get("pseudo"))
    erreur_pseudo = ((len(pseudo) < 4 or len(pseudo)>20) and pseudo != '')
    global description
    description = request.form.get("description")
    global mdp
    mdp = str('' if request.form.get("mdp") is None else request.form.get("mdp"))
    erreur_mdp = ((len(mdp) < 4 or len(mdp) > 20) and mdp != '')
    mdpverif = request.form.get("mdpverif")
    global mairie
    mairie=request.form.get('isMairie')
    egal = (mdp == mdpverif or mdp == '')
    db = getdb()
    c = db.cursor()
    c.execute("SELECT MAX(id_profil) FROM Utilisateurs")    #on récupère l'id maximum deja présent
    a=c.fetchall()[0][0]
    global id
    if not a:
        id =1
    else : 
        id= a+1     #on crée l'id du nouvel utilisateur
    close_connection()
    db = getdb()
    d = db.cursor()
    d.execute("SELECT mail FROM Utilisateurs")  #on récupère les mails et pseudo deja existants
    m = d.fetchall()
    close_connection()
    db = getdb()
    p = db.cursor()
    p.execute("SELECT pseudo FROM Utilisateurs")
    pl = p.fetchall()
    close_connection()
    for k in range(len(m)):
        m[k] = m[k][0]
        pl[k] = pl[k][0]
    pseudo_pris = (pseudo in pl)    #si ce pseudo est deja pris
    inscrit = (mail in m)    #si ce mail est deja pris donc que cet utilisateur est deja inscrit
    complet = True
    if not erreur_pseudo and not erreur_mdp and not erreur_tel:
        if not pseudo_pris and not inscrit:
            if mail != None and mail != '' and pseudo != None and pseudo != '' and description != None and description != '' and mdp != None and mdp != '' and mdpverif != None and mdpverif != '' and egal == True:
                if (numtel == None or numtel == ''):    #si numtel vide
                    numtel = '0606060606'
                url = f'{mail}/{pseudo}/{mdp}/{description}/{numtel}/{id}/{mairie}' #on enregistre toutes les infos pour les faire passer à la page verification par l'url
                url_chiffre = cryptocode.encrypt(url,'urltncy')     #on chiffre l'url
                for k in range(len(url_chiffre)):
                    if url_chiffre[k] == '/':
                        url_chiffre = url_chiffre[:k] + 'telecom' + url_chiffre[k+1:]   #on remplace les '/' par 'telecom' pour éviter les problèmes dans l'url
                return redirect('/verification/'+url_chiffre)
            elif (mail == None or mail == '') and (numtel == None or numtel == '') and (pseudo == None or pseudo == '') and (description == None or description == '') and (mdp == None or mdp == '') and (mdpverif == None or mdpverif == ''):     #si tous les champs sont vides (à l'arrivée sur la page)
                complet = True
            else:
                complet = False
        else:
            complet = True
    return render_template('inscription.html',egal=egal,complet=complet,pris=pseudo_pris,inscrit=inscrit,erreur_tel=erreur_tel,erreur_mdp=erreur_mdp,erreur_pseudo=erreur_pseudo)



@app.route('/verification/<url_chiffre>', methods=["GET", "POST"])  #page de vérification de l'adresse mail
def verification(url_chiffre):
    url_split = url_chiffre.split('telecom')    #on enleve les 'telecom' de l'url
    url = ''
    for k in url_split:
        url += k + '/'  #on rajoute les anciens '/'
    url = url[:-1]
    bon_url = cryptocode.decrypt(url,'urltncy')     #on déchiffre l'url
    lurl = bon_url.split('/')
    mail = lurl[0]  #on récupère les infos
    pseudo = lurl[1]
    mdp = lurl[2]
    description = lurl[3]
    numtel = lurl[4]
    id = lurl[5]
    mairie = lurl[6]    
    if request.form.get("code") == None:    #en arrivant sur la page
        global code
        code = envoi_mail(mail)     #on envoie un mail de notification
    code_donne = str('' if request.form.get("code") is None else request.form.get("code"))  #pour donner type str à code_donne
    if code_donne == code:  #si le code est bon
        mdp_crypte = cryptocode.encrypt(mdp,'tncy')
        db = getdb()
        c = db.cursor()
        c.execute("INSERT INTO Utilisateurs VALUES(?,'1','1',?,?,?,?,?)",(id,pseudo,mail,numtel,mdp_crypte,description,))   #on rentre les infos de l'utilisateur dans la table utilisateur
        db.commit()
        close_connection()
        db = getdb()
        d = db.cursor()
        d.execute("INSERT INTO Notation VALUES(?,0,0,'[]')",(id,))  #on le rajoute dans la table notation
        db.commit()
        close_connection()
        db=getdb()
        mai=db.cursor()
        text="INSERT INTO Mairie VALUES(?,?)"   #et dans la table mairie
        mai.execute(text,(id,mairie,))
        db.commit()
        close_connection()
        complet = True
        return redirect('/'+str(id)+'/mc/profil')   #et on redirige l'utilisateur vers son profil fraichement créé
    elif code_donne != '':
        return render_template('verification.html',erreur=True)     #si le code n'est pas le bon, on affiche l'erreur
    else:
        return render_template('verification.html',erreur=False)    #on arrivant sur la page, on lui affiche la page sans erreur

@app.route('/<id>/demande/encours', methods=["GET", "POST"])    #page pour afficher les demandes
def encours(id):
    filtre = request.form.get("filtre")     #on récupère le filtre et ce qui est entré dans la barre de recherche
    recherche = request.form.get("recherche")
    if filtre == None:  #pour afficher quelque chose en arrivant sur la page
        filtre = 'Filtre'
    if recherche == None:  #pour afficher quelque chose en arrivant sur la page
        recherche = ''
    pref = threeBestInterest('demande',id)  #on récupère les 3 filtres préférés de l'utilisateur
    db = getdb()
    c = db.cursor()
    if filtre != 'Filtre' and filtre != None :  #si l'utilisateur a rentrer un filtre
        db = getdb()
        c = db.cursor()
        c.execute("SELECT id_dem,titre,filtre,pseudo FROM Demandes d, Utilisateurs u WHERE d.id_auteur_dem = u.id_profil AND filtre = ? AND titre LIKE ? AND etat='en attente'",(filtre,'%'+str(recherche)+'%',))   #on récupère les infos des demandes contenant le filtre demandé et les mots clés entrés sans teniir compte des préférences
        paspref = c.fetchall()
        close_connection()
        l = ['' for k in range(len(paspref))]
        for k in range(len(paspref)):
            l[k] = [k for k in paspref[k]]   #pour donner type liste et pouvoir assigner l[k][0][0]
            l[k][0] = "/"+str(id)+"/d/"+str(l[k][0])+"/ld"      #liste des liens pour rediriger l'utilisateurs quand il aura cliqué sur une demande
        return render_template("encours.html",pref=False,l=l,vide=(l==[]),Annonce='Demandes')
    else:   #si il ne rentre pas de filtre : affichage préférentiel
        p1l = []    #on fait une liste pour chacun des 3 filtres préférés
        p2l = []
        p3l = []
        db = getdb()
        diff = db.cursor()
        diff.execute("SELECT id_dem,titre,filtre,pseudo FROM Demandes d, Utilisateurs u WHERE d.id_auteur_dem = u.id_profil AND filtre != ? AND filtre != ? AND filtre != ? AND titre LIKE ? AND etat='en attente'",(pref[0],pref[1],pref[2],'%'+str(recherche)+'%',))  #on récupère les infos des demandes ne contenat pas ces filtres
        diffl = diff.fetchall()
        close_connection()
        if pref[1] != pref[0]:  #si il y a moins 2 filtres différents
            db = getdb()
            p1 = db.cursor()
            p1.execute("SELECT id_dem,titre,filtre,pseudo FROM Demandes d, Utilisateurs u WHERE d.id_auteur_dem = u.id_profil AND filtre = ? AND titre LIKE ? AND etat='en attente'",(pref[0],'%'+str(recherche)+'%',))
            p1l = p1.fetchall()
            close_connection()
        if pref[2] != pref[0] and pref[2] != pref[1]:   #si les 3 filtres sont différents
            db = getdb()
            p2 = db.cursor()
            p2.execute("SELECT id_dem,titre,filtre,pseudo FROM Demandes d, Utilisateurs u WHERE d.id_auteur_dem = u.id_profil AND filtre = ? AND titre LIKE ? AND etat='en attente'",(pref[1],'%'+str(recherche)+'%',))
            p2l = p2.fetchall()
            close_connection()
        db = getdb()
        p3 = db.cursor()
        p3.execute("SELECT id_dem,titre,filtre,pseudo FROM Demandes d, Utilisateurs u WHERE d.id_auteur_dem = u.id_profil AND filtre = ? AND titre LIKE ? AND etat='en attente'",(pref[2],'%'+str(recherche)+'%',))
        p3l = p3.fetchall()
        close_connection()
        m = max( max(len(diffl),len(p1l)) , max(len(p2l),len(p3l)))
        l = [['','','',''] for k in range(m)]
        for k in range(len(p1l)):
            l[k][0] = [k for k in p1l[k]]   #pour donner type liste et pouvoir assigner l[k][0][0]
            l[k][0][0] = "/"+str(id)+"/d/"+str(l[k][0][0])+"/ld"    #on crée les listes pour pouvoir rediriger l'utilisateur sur la demande qu'il aura choisi
        for k in range(len(p2l)):
            l[k][1] = [k for k in p2l[k]]
            l[k][1][0] = "/"+str(id)+"/d/"+str(l[k][1][0])+"/ld"
        for k in range(len(p3l)):
            l[k][2] = [k for k in p3l[k]]
            l[k][2][0] = "/"+str(id)+"/d/"+str(l[k][2][0])+"/ld"
        for k in range(len(diffl)):
            l[k][3] = [k for k in diffl[k]]
            l[k][3][0] = "/"+str(id)+"/d/"+str(l[k][3][0])+"/ld"
        return render_template("encours.html",pref=True,l=l,vide=(l==[]),Annonce='Demandes',id_user=id)

@app.route('/<id>/offre/encours', methods=["GET", "POST"])  #fonction pour afficher les offres
def encours_offre(id):      #même principe que pour afficher les demandes
    filtre = request.form.get("filtre")
    recherche = request.form.get("recherche")
    if filtre == None:  #pour afficher quelque chose en arrivant sur la page
        filtre = 'Filtre'
    if recherche == None:  #pour afficher quelque chose en arrivant sur la page
        recherche = ''
    pref = threeBestInterest('offre',id)
    print(pref)
    db = getdb()
    c = db.cursor()
    if filtre != 'Filtre' and filtre != None :
        db = getdb()
        c = db.cursor()
        c.execute("SELECT id_offre,titre,filtre,pseudo FROM Offres d, Utilisateurs u WHERE d.id_auteur_off = u.id_profil AND filtre = ? AND titre LIKE ? AND etat='en attente'",(filtre,'%'+str(recherche)+'%',))
        paspref = c.fetchall()
        close_connection()
        l = ['' for k in range(len(paspref))]
        for k in range(len(paspref)):
            l[k] = [k for k in paspref[k]]   #pour donner type liste et pouvoir assigner l[k][0][0]
            l[k][0] = "/"+str(id)+"/o/"+str(l[k][0])+'/lo'
        return render_template("encours.html",pref=False,l=l,vide=(l==[]),Annonce='Offres')
    else:
        p1l = []
        p2l = []
        p3l = []
        db = getdb()
        diff = db.cursor()
        diff.execute("SELECT id_offre,titre,filtre,pseudo FROM Offres d, Utilisateurs u WHERE d.id_auteur_off = u.id_profil AND filtre != ? AND filtre != ? AND filtre != ? AND titre LIKE ? AND etat='en attente'",(pref[0],pref[1],pref[2],'%'+str(recherche)+'%',))
        diffl = diff.fetchall()
        close_connection()
        if pref[1] != pref[0]:
            db = getdb()
            p1 = db.cursor()
            p1.execute("SELECT id_offre,titre,filtre,pseudo FROM Offres d, Utilisateurs u WHERE d.id_auteur_off = u.id_profil AND filtre = ? AND titre LIKE ? AND etat='en attente'",(pref[0],'%'+str(recherche)+'%',))
            p1l = p1.fetchall()
            close_connection()
        if pref[2] != pref[0] and pref[2] != pref[1]:
            db = getdb()
            p2 = db.cursor()
            p2.execute("SELECT id_offre,titre,filtre,pseudo FROM Offres d, Utilisateurs u WHERE d.id_auteur_off = u.id_profil AND filtre = ? AND titre LIKE ? AND etat='en attente'",(pref[1],'%'+str(recherche)+'%',))
            p2l = p2.fetchall()
            close_connection()
        db = getdb()
        p3 = db.cursor()
        p3.execute("SELECT id_offre,titre,filtre,pseudo FROM Offres d, Utilisateurs u WHERE d.id_auteur_off = u.id_profil AND filtre = ? AND titre LIKE ? AND etat='en attente'",(pref[2],'%'+str(recherche)+'%',))
        p3l = p3.fetchall()
        close_connection()
        m = max( max(len(diffl),len(p1l)) , max(len(p2l),len(p3l)))
        l = [['','','',''] for k in range(m)]
        for k in range(len(p1l)):
            l[k][0] = [k for k in p1l[k]]   #pour donner type liste et pouvoir assigner l[k][0][0]
            l[k][0][0] = "/"+str(id)+"/o/"+str(l[k][0][0])+"/lo"
        for k in range(len(p2l)):
            l[k][1] = [k for k in p2l[k]]
            l[k][1][0] = "/"+str(id)+"/o/"+str(l[k][1][0])+"/lo"
        for k in range(len(p3l)):
            l[k][2] = [k for k in p3l[k]]
            l[k][2][0] = "/"+str(id)+"/o/"+str(l[k][2][0])+"/lo"
        for k in range(len(diffl)):
            l[k][3] = [k for k in diffl[k]]
            l[k][3][0] = "/"+str(id)+"/o/"+str(l[k][3][0])+"/lo"
        return render_template("encours.html",pref=True,l=l,vide=(l==[]),Annonce='Offres',id_user=id)

@app.route('/<id_noteur>/<id_note>/notation', methods=["GET", "POST"])
def notation(id_noteur,id_note):    #fonction pour noter un utilisateur
    if id_noteur == id_note:     #pour afficher une erreur si un utilisateur se note lui même
        return render_template('notation.html',autonote=True)
    db = getdb()
    c = db.cursor()
    c.execute("SELECT pseudo FROM Utilisateurs WHERE id_profil=?",(int(id_note),))  #on récupère le nom de l'utilisateur noté pour l'afficher
    l = c.fetchall()
    nom = l[0][0]
    close_connection()
    note_donnee = int(0 if request.form.get("note") is None else request.form.get("note"))  #pour donner type int à note_donnee
    db = getdb()
    d = db.cursor()
    d.execute("SELECT note,nb_note,note_par FROM Notation WHERE id=?",(int(id_note),))  #on récupère l'ancienne note de l'utilisateur noté, le nombre de note pour recalculer sa nouvelle note et les utilisateurs qui l'ont déja noté
    dl = d.fetchall()
    close_connection()
    if dl == []:    #si l'utilisateur n'a jamais été noté (ne devrait plus être le cas maintenant)
        db = getdb()
        n = db.cursor()
        n.execute("INSERT INTO Notation VALUES(?,0,0,'[]')",(id_note,))
        db.commit()
        close_connection()
    db = getdb()
    d = db.cursor()
    d.execute("SELECT note,nb_note,note_par FROM Notation WHERE id=?",(int(id_note),)) 
    dl = d.fetchall()
    note = dl[0][0]
    nb_note = dl[0][1]
    note_par = liste(dl[0][2][1:-1])
    if int(id_noteur) in note_par:  #si cet utilisateur a deja donné une note
        deja_note = True    #pour renvoyer une erreur
        return render_template('notation.html',id_noteur=id_noteur,id_note=id_note,nom=nom,deja_note=deja_note,autonote=False,id_user=id_noteur)
    elif note_donnee == 0 : #en arrivant sur la page
        deja_note = False
        return render_template('notation.html',id_noteur=id_noteur,id_note=id_note,nom=nom,deja_note=deja_note,autonote=False,id_user=id_noteur)
    else:
        deja_note = False
        nouvelle_note = (note * nb_note + note_donnee)/(nb_note+1)  #on calcule la nouvelle note
        note_par.append(int(id_noteur))  #on ajoute l'utilisateur qui note a la liste des utilisateurs ayant donné une note à celui qui est noté
        db = getdb()
        a = db.cursor()
        a.execute("UPDATE Notation SET note_par = ? WHERE id = ?",(str(note_par),int(id_note),))    #on met à jour les valeurs
        db.commit()
        close_connection()
        db = getdb()
        e = db.cursor()
        e.execute("UPDATE Notation SET nb_note = ? WHERE id = ?",(nb_note+1,int(id_note),))
        db.commit()
        close_connection()
        db = getdb()
        f = db.cursor()
        f.execute("UPDATE Notation SET note = ? WHERE id = ?",(nouvelle_note,int(id_note),))
        db.commit()
        close_connection()
        return render_template('notation.html',id_noteur=id_noteur,id_note=id_note,nom=nom,deja_note=True,id_user=id_noteur)





@app.route('/<idd>/mes_offres', methods=['GET'])    #pour afficher mes offres en récupérant la liste 
def mesoffres(idd):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT etat,lieu,datedeb,titre,id_offre,filtre,dateservice FROM Offres WHERE id_auteur_off = ?', (idd,)) 
    tab = cur.fetchall()
    con.close()
    return render_template("mesoffres.html",liste=tab,id_user=idd)



@app.route('/<idd>/mes_demandes', methods=['GET']) #pour afficher mes demandes en récupérant la liste
def mesdemandes(idd):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT etat,lieu,datedeb,titre,filtre,id_dem,dateservice FROM Demandes WHERE id_auteur_dem = ?', (idd,)) 
    tab = cur.fetchall()
    con.close()
    return render_template("mesdemandes.html",liste=tab,id_user=idd) 


@app.route('/<idd>/mes_demandes/<idd_dem>',methods=['GET'])     #pour afficher une de mes demandes
def mademandelà(idd,idd_dem):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT id_auteur_dem,etat,lieu,description,datedeb,titre,filtre,dateservice FROM Demandes WHERE id_dem= ?', (idd_dem,)) ###ajout de id_accepteur quand table ~complète
    tab = cur.fetchall()
    con.close()
    if tab == []:
        return redirect('/PageInexistante')
    if int(idd)!=int(tab[0][0]):
        return redirect('/PageInexistante')
        ###en gros la page lui appartient pas, donc redirection vers erreur
    else:
        enattente=(tab[0][1]=='en attente')
        print(enattente)
        con = sqlite3.connect(database)
        cur=con.cursor()
        cur.execute('SELECT Bool FROM Mairie WHERE id_utilisateur=?',(idd,))
        mairietab=cur.fetchall()
        con.close()
        isattmair=((mairietab[0][0]=='True') and enattente) ###pas besoin de vérif si non vide car si l'utilisateur est là c'est que c'est non vide
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute('SELECT Bool FROM isSondage WHERE type="demande" AND id_annonce=?',(idd_dem,))
        sondtab = cur.fetchall()
        con.close()
        if not sondtab:
            db=getdb()
            c = db.cursor()
            c.execute("INSERT INTO isSondage VALUES('demande',?,'False','[]')",(idd_dem,))
            db.commit()
            close_connection()
            issond = False
        else:
            issond = (sondtab[0][0]=='False') ###pas besoin de vérif si non vide, car si l'utilisateur est sur cette page le poste existe
        return render_template("mademandelà.html",liste=tab,id_user=idd,iddem=idd_dem,boolmair=isattmair,boolsond=issond)


@app.route('/<idd>/mes_demandes/<idd_dem>/postulants',methods=['GET'])
def voirpostulants(idd,idd_dem):
    con = sqlite3.connect(database) #on récupère la liste des demandeurs qui y ont postulé
    cur = con.cursor()
    cur.execute('SELECT id_post,id_postulant,message_postulant,pseudo,mail FROM Postulants AS P JOIN Utilisateurs AS U ON P.id_postulant=U.id_profil WHERE P.id_post= ?', (idd_dem,)) 
    tabpostul = cur.fetchall()
    con.close()
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT id_auteur_dem FROM Demandes WHERE id_dem= ?', (idd_dem,)) 
    tabauteur = cur.fetchall()
    con.close()
    con = sqlite3.connect(database)
    cur=con.cursor()
    cur.execute('SELECT id_dem FROM Demandes WHERE id_dem=?',(idd_dem,))
    verif = cur.fetchall()
    if verif == []:
        return redirect('/PageInexistante') 
    if int(idd)!=int(tabauteur[0][0]):
        return redirect('/PageInexistante')
        ###en gros la page ne lui appartient pas, donc il va pas voir les demandeurs
    return render_template("postulants.html",liste=tabpostul,id_user=idd,iddem=idd_dem)


@app.route('/<idd>/mes_demandes/<idd_dem>/postulants/selection',methods=['GET','POST'])
def selectpostulant(idd,idd_dem): #on vérif si postulants non déjà choisi, si poste en attente, et on lors de methode
    if request.method=='POST': #POST on update car l'utilisateur a submit
        pol = request.form.get('postulant')
        con = sqlite3.connect(database) 
        cur = con.cursor()
        cur.execute('SELECT etat FROM Demandes WHERE id_dem= ?',(idd_dem,))
        tab=cur.fetchall()
        con.close()
        if tab==[]:
            return redirect('/PageInexistante')
        else:
            if tab[0][0]=='en attente': 
                if not(pol is None):
                    con = sqlite3.connect(database)
                    cur = con.cursor()
                    cur.execute('UPDATE Demandes SET id_accepteur=? WHERE id_dem= ?', (pol,idd_dem)) 
                    cur.execute('UPDATE Demandes SET etat="en cours" WHERE id_dem=?', (idd_dem,))
                    con.commit()
                    con.close()
                    con = sqlite3.connect(database)
                    cur = con.cursor()
                    cur.execute('SELECT pseudo FROM Utilisateurs WHERE id_profil=?',(pol,))
                    tabuser=cur.fetchall()[0][0]
                    con.close()
                else:
                    tabuser=[]
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute('SELECT titre FROM Demandes WHERE id_dem=?',(idd_dem,))
                tabtitre=cur.fetchall()
                con.close()
                return render_template("postulantchoisi.html",id_user=idd,iddem=idd_dem,pseudo=tabuser,titre=tabtitre[0][0])
            else:
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute('SELECT pseudo FROM Utilisateurs AS U JOIN Demandes AS D ON U.id_profil=D.id_accepteur WHERE D.id_dem=?',(idd_dem,))
                pseutab = cur.fetchall()
                con.close()
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute('SELECT titre FROM Demandes WHERE id_dem=?',(idd_dem,))
                titab=cur.fetchall()
                con.close()
                return render_template("postulantchoisi.html",id_user=idd,iddem=idd_dem,pseudo=pseutab[0][0],titre=titab[0][0])
    else: 
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute('SELECT etat FROM Demandes WHERE id_dem= ?',(idd_dem,))
        tab=cur.fetchall()
        con.close()
        if tab==[]:
            return redirect('/PageInexistante')
        else:
            if tab[0][0]=='en attente':
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute('SELECT id_post,id_postulant,pseudo FROM Postulants AS P JOIN Utilisateurs AS U ON P.id_postulant=U.id_profil WHERE P.id_post= ?', (idd_dem,)) 
                tabpostulant = cur.fetchall()
                con.close()
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute('SELECT id_auteur_dem FROM Demandes WHERE id_dem= ?', (idd_dem,)) 
                tabauteur = cur.fetchall()
                con.close()
                con = sqlite3.connect(database)
                cur=con.cursor()
                cur.execute('SELECT id_dem FROM Demandes WHERE id_dem=?',(idd_dem,))
                verif = cur.fetchall()
                if verif == []:
                    return redirect('/PageInexistante')
                if int(idd)!=int(tabauteur[0][0]):
                    return "cpaàtoidoncpagenormale"
                    ###en gros la page lui appartient pas, donc redirection page normale
                return render_template("selectpostulant.html",liste=tabpostulant,id_user=idd,iddem=idd_dem)
            else:
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute('SELECT pseudo FROM Utilisateurs AS U JOIN Demandes AS D ON U.id_profil=D.id_accepteur WHERE D.id_dem=?',(idd_dem,))
                pseutab = cur.fetchall()
                con.close()
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute('SELECT titre FROM Demandes WHERE id_dem=?',(idd_dem,))
                titab=cur.fetchall()
                con.close()
                if pseutab==[]:
                    return render_template("postulantchoisi.html",id_user=idd,iddem=idd_dem,pseudo=[],titre=titab[0][0])
                return render_template("postulantchoisi.html",id_user=idd,iddem=idd_dem,pseudo=pseutab[0][0],titre=titab[0][0])




@app.route('/<idd>/mes_offres/<idd_off>',methods=['GET']) #même chose que mademandelà
def monoffrelà(idd,idd_off):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT id_auteur_off,etat,lieu,description,datedeb,titre,filtre,dateservice FROM Offres WHERE id_offre= ?', (idd_off,)) ###ajout de id_demandeur quand table ~complète
    tab = cur.fetchall()
    con.close()
    if tab == []:
        return redirect('/PageInexistante')
    if int(idd)!=int(tab[0][0]):
        return "cpaàtoidoncpagenormale"
        ###en gros la page lui appartient pas, donc redirection vers la page de manière normale?
    else:
        enattente=(tab[0][1]=='en attente')
        con = sqlite3.connect(database)
        cur=con.cursor()
        cur.execute('SELECT Bool FROM Mairie WHERE id_utilisateur=?',(idd,))
        mairietab=cur.fetchall()
        con.close()
        isattmair=((mairietab[0][0]=='True') and enattente) ###pas besoin de vérif si non vide, si t'es là, c'est qu'elle n'est pas vide
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute('SELECT Bool FROM isSondage WHERE type="offre" AND id_annonce=?',(idd_off,))
        sondtab = cur.fetchall()
        con.close()
        if not sondtab:
            db=getdb()
            c = db.cursor()
            c.execute("INSERT INTO isSondage VALUES('offre',?,'False','[]')",(idd_off,))
            db.commit()
            close_connection()
            issond = False
        else:
            issond = (sondtab[0][0]=='False') ###pas besoin de vérif si non vide, car si t'es là, le poste existe
        return render_template("monoffrelà.html",liste=tab,id_user=idd,idof=idd_off,boolmair=isattmair,boolsond=issond)


@app.route('/<idd>/mes_offres/<idd_off>/demandeurs',methods=['GET']) #pareil que voirpostulants
def voirdemandeurs(idd,idd_off):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT id_offre_dem,id_demandeur,message_demandeur,pseudo,mail FROM Demandeurs AS D JOIN Utilisateurs AS U ON D.id_demandeur=U.id_profil WHERE D.id_offre_dem= ?', (idd_off,)) 
    tabdemandeur = cur.fetchall()
    con.close()
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT id_auteur_off FROM Offres WHERE id_offre= ?', (idd_off,)) 
    tabauteur = cur.fetchall()
    con.close()
    con = sqlite3.connect(database)
    cur=con.cursor()
    cur.execute('SELECT id_offre FROM Offres WHERE id_offre=?',(idd_off,))
    verif = cur.fetchall()
    if verif == []:
        return redirect('/PageInexistante')
    if int(idd)!=int(tabauteur[0][0]):
        return "cpaàtoidoncpagenormale"
        ###en gros la page lui appartient pas, donc il va pas voir les demandeurs
    return render_template("demandeurs.html",liste=tabdemandeur,id_user=idd,idoff=idd_off)


@app.route('/<idd>/mes_offres/<idd_off>/demandeurs/selection',methods=['GET','POST'])
def selectdemandeur(idd,idd_off): #pareil que pour selectpostulant
    if request.method=='POST':
        dem = request.form.get('demandeur')
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute('SELECT etat FROM Offres WHERE id_offre= ?',(idd_off,))
        tab=cur.fetchall()
        con.close()
        if tab==[]:
            return redirect('/PageInexistante')
        else:
            if tab[0][0]=='en attente':
                if not(dem is None):
                    con = sqlite3.connect(database)
                    cur = con.cursor()
                    cur.execute('UPDATE Offres SET id_demandeur=? WHERE id_offre= ?', (dem,idd_off)) 
                    cur.execute('UPDATE Offres SET etat="en cours" WHERE id_offre=?', (idd_off,))
                    con.commit()
                    con.close()
                    con = sqlite3.connect(database)
                    cur = con.cursor()
                    cur.execute('SELECT pseudo FROM Utilisateurs WHERE id_profil=?',(dem,))
                    tabuser=cur.fetchall()[0][0]
                    con.close()
                else:
                    tabuser=[]
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute('SELECT titre FROM Offres WHERE id_offre=?',(idd_off,))
                tabtitre=cur.fetchall()
                con.close()
                return render_template("demandeurchoisi.html",id_user=idd,idoff=idd_off,pseudo=tabuser,titre=tabtitre[0][0])
            else:
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute('SELECT pseudo FROM Utilisateurs AS U JOIN Offres AS O ON U.id_profil=O.id_demandeur WHERE O.id_offre=?',(idd_off,))
                pseutab = cur.fetchall()
                con.close()
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute('SELECT titre FROM Offres WHERE id_offre=?',(idd_off,))
                titab=cur.fetchall()
                con.close()
                return render_template("demandeurchoisi.html",id_user=idd,idoff=idd_off,pseudo=pseutab[0][0],titre=titab[0][0])
    else: 
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute('SELECT etat FROM Offres WHERE id_offre= ?',(idd_off,))
        tab=cur.fetchall()
        con.close()
        if tab==[]:
            return redirect('/PageInexistante')
        else:
            if tab[0][0]=='en attente':
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute('SELECT id_offre_dem,id_demandeur,pseudo FROM Demandeurs AS D JOIN Utilisateurs AS U ON D.id_demandeur=U.id_profil WHERE D.id_offre_dem= ?', (idd_off,)) 
                tabdemandeur = cur.fetchall()
                con.close()
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute('SELECT id_auteur_off FROM Offres WHERE id_offre= ?', (idd_off,)) 
                tabauteur = cur.fetchall()
                con.close()
                con = sqlite3.connect(database)
                cur=con.cursor()
                cur.execute('SELECT id_offre FROM Offres WHERE id_offre=?',(idd_off,))
                verif = cur.fetchall()
                if verif == []:
                    return redirect('/PageInexistante')
                if int(idd)!=int(tabauteur[0][0]):
                    return "cpaàtoidoncpagenormale"
                    ###en gros la page lui appartient pas, donc redirection page normale
                return render_template("selectdemandeur.html",liste=tabdemandeur,id_user=idd,idoff=idd_off)
            else:
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute('SELECT pseudo FROM Utilisateurs AS U JOIN Offres AS O ON U.id_profil=O.id_demandeur WHERE O.id_offre=?',(idd_off,))
                pseutab = cur.fetchall()
                con.close()
                con = sqlite3.connect(database)
                cur = con.cursor()
                cur.execute('SELECT titre FROM Offres WHERE id_offre=?',(idd_off,))
                titab=cur.fetchall()
                con.close()
                return render_template("demandeurchoisi.html",id_user=idd,idoff=idd_off,pseudo=pseutab[0][0],titre=titab[0][0])


@app.route("/PageInexistante") #permet d'éviter que l'utilisateur joue avec l'url
def error404():
    id=request.args.get('id')
    if id is None or id=='':
        return render_template('error404.html') 
    return render_template('error404.html',id_user=id) 


@app.route("/<idd>/cloturer_demande/<idd_dem>") #permet de fixer l'état en 'terminée'
def cloturer_demande(idd,idd_dem): 
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT id_auteur_dem FROM Demandes WHERE id_dem=?',(idd_dem,))
    tab = cur.fetchall()
    con.close()
    if int(idd)==int(tab[0][0]): ###pour vérifier si la page appartient bien à l'utilisateur
        con = sqlite3.connect(database)
        cur=con.cursor()
        cur.execute('UPDATE Demandes SET etat="terminé" WHERE id_dem=?',(idd_dem,))
        con.commit()
        con.close()
        con = sqlite3.connect(database)
        cur=con.cursor()
        cur.execute('SELECT id_accepteur FROM Demandes WHERE id_dem=?',(idd_dem,))
        tabcepteur= cur.fetchall()
        if tabcepteur[0][0]!=0:
            return redirect(f'/{idd}/{tabcepteur[0][0]}/notation')
    return redirect(f'/{idd}/mes_demandes/{idd_dem}')


@app.route("/<idd>/cloturer_offre/<idd_off>")
def cloturer_offre(idd,idd_off): #même chose qu'au dessus
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT id_auteur_off FROM Offres WHERE id_offre=?',(idd_off,))
    tab = cur.fetchall()
    con.close()
    if int(idd)==int(tab[0][0]):
        con = sqlite3.connect(database)
        cur=con.cursor()
        cur.execute('UPDATE Offres SET etat="terminé" WHERE id_offre=?',(idd_off,))
        con.commit()
        con.close()
        con = sqlite3.connect(database)
        cur=con.cursor()
        cur.execute('SELECT id_demandeur FROM Offres WHERE id_offre=?',(idd_off,))
        tabcepteur= cur.fetchall()
        con.close()
        if tabcepteur[0][0]!=0:
            return redirect(f'/{idd}/{tabcepteur[0][0]}/notation')
    return redirect(f'/{idd}/mes_offres/{idd_off}')


@app.route("/<idd>/supprimer_demande/<idd_dem>")
def supprimer_demande(idd,idd_dem): #on reprend le même principe que cloture, mais on supprime la valeur
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT id_auteur_dem FROM Demandes WHERE id_dem=?',(idd_dem,))
    tab = cur.fetchall()
    con.close()
    if int(idd)==int(tab[0][0]):
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute('DELETE FROM Demandes WHERE id_dem=?',(idd_dem,))
        con.commit()
        con.close()
    return redirect(f'/{idd}/mes_demandes')


@app.route("/<idd>/supprimer_offre/<idd_off>")
def supprimer_offre(idd,idd_off):  #même chose qu'au dessus 
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT id_auteur_off FROM Offres WHERE id_offre=?',(idd_off,))
    tab = cur.fetchall()
    con.close()
    if tab != [] and int(idd)==int(tab[0][0]):
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute('DELETE FROM Offres WHERE id_offre=?',(idd_off,))
        con.commit()
        close_connection()
        con = sqlite3.connect(database)
        cur3 = con.cursor()
        cur3.execute('DELETE FROM isSondage WHERE id_annonce = ?',(idd_off,))
        con.commit()
        close_connection()
    return redirect(f'/{idd}/mes_offres')


@app.route("/<id>/<type>/<typeid>/<idsondage>", methods=['GET','POST'])
def affichSondage(idsondage,id,type,typeid): #on récupère toute les données du sondage pour l'afficher
        db = getdb()
        d = db.cursor()
        d.execute("SELECT repondu_par FROM isSondage i, Sondages s WHERE i.id_annonce=s.typeid AND s.id_sondage =?",(int(idsondage),))
        dl = d.fetchall()
        close_connection()
        print(dl[0][0])
        repondu_par = dl[0][0][1:-1].split(', ')
        #repondu_par=re.sub("\[|\]|'","",str(dl)).split(', ')
        deja_repondu = (id in repondu_par)
        print(repondu_par,id)
        if  request.method!='POST' and not deja_repondu:
            db=getdb()
            c=db.cursor()
            c.execute("Select questions,reponses,type_rep From Sondages Where Sondages.id_sondage= ? and type=? and typeid=?",(str(idsondage),str(type),str(typeid)))
            x=c.fetchall()
            print('x :',x)
            liste_questions=[x[k][0] for k in range (len(x))][0]
            liste_questions=liste_questions[1:len(liste_questions)-1].split(',')
        
            
            liste_reponses=[x[k][1] for k in range(len(x))][0] #on décompose le varchar en récupérant la liste à l'intèrieur
            liste_reponses=liste_reponses[1:len(liste_reponses)-1].split('], [')
            liste_reponses=[liste_reponses[k][1:].split(', ') for k in range(len(liste_reponses)-1)]+[liste_reponses[len(liste_reponses)-1].split(', ')]
            for i in range(len(liste_reponses)):
                for j in range(len(liste_reponses[i])):
                    liste_reponses[i][j]=re.sub("\]|\[|'","",liste_reponses[i][j])
            liste_typerep=[x[k][2] for k in range(len(x))][0]
            liste_typerep=liste_typerep[1:len(liste_typerep)-1].split(',')
            for k in range(len(liste_typerep)):
                liste_typerep[k]=re.sub("\]|\[|'| ","",liste_typerep[k])
            return render_template("afffichSondage.html",liste_questions=liste_questions,liste_reponses=liste_reponses,liste_typerep=liste_typerep,nb_questions=len(liste_questions),id_user=id,deja_repondu=False)

        elif not deja_repondu :
            repondu_par.append(int(id))
            db = getdb()
            r = db.cursor()
            r.execute("UPDATE isSondage SET repondu_par = ? WHERE id_annonce = ? AND type = ?",(str(repondu_par),typeid,type,))
            db.commit()
            close_connection()
            return redirect(f'/{id}/{type[0]}/{typeid}/l{type[0]}') #on retournera sur la page de l'annonce en question, en prenant soin de mettre que l'utilisateur a bien répondu au sondage  
        
        else:
            return render_template("afffichSondage.html",liste_questions=[],liste_reponses=[],liste_typerep=[],nb_questions=0,id_user=id,deja_repondu=True)



@app.route("/<id>/<type>/<typeid>/newsondage1", methods=['GET','POST'])

def creeSondage1(id,type,typeid): #on affiche la page de création de sondage, et on insère dans la table si la methode est POST
    if request.method=="POST":
        nbQ=int(request.form.get('nbQ'))
        db=getdb()
        c=db.cursor()
        text='Select MAX(id_sondage) FROM Sondages'
        c.execute(text)
        a=c.fetchall()
        if a[0][0] == None:
            id_sondage=1
        else:
            id_sondage=int(a[0][0])+1

        exec='Insert into Sondages values(?,?,?,?,"","","")'
        c.execute(exec,(id,type,typeid,int(id_sondage)))
        db.commit()
        db.close()
        return redirect(f'/{id}/{type}/{typeid}/newsondage2?nbQ={nbQ}')

    else:
        return render_template('ask-creeSondage.html',id_user=id)

@app.route("/<id>/<type>/<typeid>/newsondage2", methods=['GET','POST']) #on continue de compléter le sondage en insérant dans
def creeSondage2(id,type,typeid): #la table les questions et leur réponse possible si methode est POST
    if request.method=='POST':
        
        nbQ=int(request.args.get('nbQ'))
        list_nbR=[request.form.get('nbR'+str(k)) for k in range(0,nbQ)]
        type_rep=[request.form.get('tr'+str(k)) for k in range(0,nbQ)]

        db=getdb()
        c=db.cursor()
        c.execute("Update Sondages set type_rep=? Where id=? and typeid=?",(str(type_rep),str(id),str(typeid)))
        db.commit()
        return redirect(f'/{id}/{type}/{typeid}/newsondage3?nbQ={nbQ}&lR={list_nbR}&tr={type_rep}')
    else:
        nbQ=int(request.args.get('nbQ'))
        t='ask-creeSondage2.html'
        return render_template(t,nb_questions=nbQ,id_user=id)


@app.route("/<id>/<type>/<typeid>/newsondage3", methods=['GET','POST'])
def creeSondage3(id,type,typeid): #finalisation de la création du sondage
    if request.method=='POST':
        nbQ=int(request.args.get('nbQ'))
        list_nbR=request.args.get('lR')
        type_rep=request.args.get('tr')
        list_nbR=list_nbR[1:len(list_nbR)-1].split(',')
        list_nbr=[list_nbR[k][1:len(list_nbR[k])-1] for k in range(nbQ)]
        list_nbr=[int(list_nbr[0])]+[int(list_nbr[k][1:]) for k in range(1,nbQ)]
        type_rep=type_rep[1:len(type_rep)-1].split(',')
        type_rep=[type_rep[k][1:len(type_rep[k])-1] for k in range(nbQ)]
        type_rep=[type_rep[0]]+[type_rep[k][1:] for k in range(1,nbQ)]

        questions=[request.form.get('q'+str(k)) for k in range(1,nbQ+1)]
        reponses=[[request.form.get(str(k)+'r'+str(j)) for j in range(1,int(list_nbr[k-1])+1)] for k in range(1,nbQ+1)]
        db=getdb()
        c=db.cursor()
        c.execute("Update Sondages Set questions= ? where id= ? and typeid=? ",(str(questions),str(id),str(typeid)))
        db.commit()
        c=db.cursor()
        c.execute("Update Sondages Set reponses=? where id=? and typeid=?",(str(reponses),str(id),str(typeid)))
        db.commit()
        db.close()
        db=getdb()
        c=db.cursor()
        c.execute(("Update isSondage Set Bool='True' Where id_annonce= ? AND type=?"),(str(typeid),type))
        db.commit()
        db.close()
        if type=='demande':
            return redirect(f'/{id}/mes_demandes/{typeid}') #une fois sondage créé on redirige vers le type d'annonce où il a été créé
        elif type=='offre':
            return redirect(f'/{id}/mes_offres/{typeid}')
    else:
        nbQ=int(request.args.get('nbQ'))
        list_nbR=request.args.get('lR')
        list_nbR=list_nbR[1:len(list_nbR)-1].split(',')
        list_nbr=[list_nbR[k][1:len(list_nbR[k])-1] for k in range(nbQ)]
        #list_nbr=[int(list_nbr[0])]+[int(list_nbr[k][1:]) for k in range(1,nbQ)]
        list_nbr=[int(re.sub("\[|\]|'","",list_nbr[k])) for k in range(nbQ) ]
        type_rep=request.args.get('tr')
        type_rep=type_rep[1:len(type_rep)-1].split(',')
        type_rep=[type_rep[k][1:len(type_rep[k])-1] for k in range(nbQ)]
        type_rep=[type_rep[0]]+[type_rep[k][1:] for k in range(1,nbQ)]
        return render_template('ask-creeSondage3.html',nb_questions=nbQ,nb_reponses=list_nbr,type_rep=type_rep,id_user=id)




@app.route('/<id>/demande/creationd', methods=['GET', 'POST'])
def creationd(id):  #création d'une nouvelle demande
    Titre=request.form.get('titre')
    if Titre is None :
        return render_template('ADemandeBD.html',id_user=id)
    
    time = str('' if request.form.get('time') is None else request.form.get('time'))
    time = time[-2:] + '/' + time[5:7] + '/' + time[:4] #pour mettre bon format de date
    Objet=request.form.get('objet')
    if request.method=="POST":
        Adresse=request.form.get('ville')
        Type=str('' if request.form.get('filtre') is None else request.form.get('filtre'))  #
        if Type == 'Choix du type':    #on remplace 'choix du type' car ça correspond à une fonction
            Type = 'Autre...'
        conn=getdb()
        cursor1= conn.cursor()
        cursor1.execute('SELECT MAX(id_dem) FROM Demandes') #on récupère le pls grand id des demandes pour créer le nouveau
        l = cursor1.fetchall()
        close_connection()
        if not l:   #si l est vide c'est qu'il n'y a aucune demande pour l'instant
            id_dem = '1'
        else:
            id_dem = str(int(l[0][0]) + 1)  #on prend l'id suivant
        conn=getdb()
        cursor2= conn.cursor()
        cursor2.execute('INSERT INTO Demandes (id_dem,id_auteur_dem,etat,id_accepteur,lieu,description,titre,filtre,dateservice) VALUES(?,?,?,0,?,?,?,?,?)', (id_dem,id,'en attente',Adresse,Objet,Titre,Type,time))     # ajout de tous les éléments dans la BDD
        conn.commit()  
        close_connection()
        db = getdb()
        c = db.cursor()
        c.execute("INSERT INTO isSondage VALUES('demande',?,'False','[]')",(id_dem,))      #on ajoute à la demande le sondage voulu
        db.commit()
        close_connection()
        return redirect(f"/{id}/mes_demandes")                                                                                      
    return render_template('ADemandeBD.html',id_user=id)




@app.route("/<id>/mc/profil", methods=['GET', 'POST'])
def profil(id):   #consulation des informations de l'utilisateur
    db=getdb()
    c = db.cursor() 
    c.execute(("SELECT * FROM Utilisateurs WHERE id_profil = ? "),(id,))  # on prend toutes les informations de l'utilisateur
    listeutilisateurs=c.fetchall()
    close_connection()
    return render_template('Profil.html',listeutilisateurs=listeutilisateurs,id=id)

    
@app.route("/<id>/mc/Modifprofil", methods=['GET', 'POST'])
def Modifprofil(id):  #  on donne la capacité une fois le profil créé de pouvoir le modifier
    db=getdb()
    c = db.cursor()
    c.execute(("SELECT * FROM Utilisateurs WHERE id_profil = ? "),(id,))  
    listeutilisateurs=c.fetchall()
    close_connection()
    mail = request.form.get("mail")     #on récupère les informations
    numtel = request.form.get("numTel")
    pseudo = request.form.get("pseudo")
    description = request.form.get("description")
    db = getdb()
    d = db.cursor()
    d.execute("SELECT mail FROM Utilisateurs WHERE id_profil != ?",(id,))   #on récupère les mail deja existant pour voir si le nouveau mail est deja pris ou non
    m = d.fetchall()
    close_connection()
    db = getdb()
    e = db.cursor()
    e.execute("SELECT mail,numTel,description,pseudo FROM Utilisateurs WHERE id_profil = ?",(id,))   # cette ligne nous permet par la suite de récupérer les élements du profil et donc d'éviter à l'utilisateur de resaisir ses informations
    el = e.fetchall()
    ancien_mail = el[0][0]  #on récupère les anciennes informations pour voir si elles changent
    ancien_numtel = el[0][1]
    ancien_description = el[0][2]
    ancien_pseudo = el[0][3]
    close_connection()
    db = getdb()
    p = db.cursor()
    p.execute("SELECT pseudo FROM Utilisateurs WHERE id_profil != ?",(id,))     #on récupère les pseudo deja existant pour voir si le nouveau pseudo est deja pris ou non
    pl = p.fetchall()
    close_connection()
    for k in range(len(m)):
        m[k] = m[k][0]
        pl[k] = pl[k][0]
    pseudo_pris = (pseudo in pl)     #on vérifie si le pseudo ou le mail est deja pris
    MailDPris = (mail in m)
    print(MailDPris,pseudo_pris)
    if (pseudo == ancien_pseudo and mail == ancien_mail and description == ancien_description and numtel == ancien_numtel) or (pseudo == None and mail == None and description == None and numtel == None):     #si aucun changement ou en arrivant sur la page
        return render_template('Modifprofil.html',listeutilisateurs=listeutilisateurs,succes=False,erreur=False,id_user=id)
    else:
        if not pseudo_pris and not MailDPris:  # si pseudo et mail pas deja pris
            if pseudo != ancien_pseudo and pseudo != None:
                print('pseudo oui')
                db = getdb()
                a = db.cursor()
                a.execute("UPDATE Utilisateurs SET pseudo = ? WHERE id_profil= ?",(str(pseudo),int(id),))   #on met à jour le pseudo
                db.commit()
                close_connection()
            if numtel != ancien_numtel and numtel != None:
                print('numtel oui')
                db = getdb()
                a = db.cursor()
                a.execute("UPDATE Utilisateurs SET numTel = ? WHERE id_profil= ?",(str(numtel),int(id),))   #on met à jour le numéro de téléphone
                db.commit()
                close_connection()
            if description != ancien_description and description != None:
                print('description oui')
                db = getdb()
                a = db.cursor()
                a.execute("UPDATE Utilisateurs SET description = ? WHERE id_profil= ?",(str(description),int(id),))     #on met à jour la description
                db.commit()
                close_connection()
            db=getdb()
            c = db.cursor() 
            c.execute(("SELECT * FROM Utilisateurs WHERE id_profil = ? "),(id,))  #on redemande les info pour les afficher une fois modifiée
            listeutilisateurs=c.fetchall()
            close_connection()
            return render_template('Modifprofil.html',listeutilisateurs=listeutilisateurs,succes=True,erreur=True,id_user=id)
        elif pseudo != None and mail != None :
            db=getdb()
            c = db.cursor() 
            c.execute(("SELECT * FROM Utilisateurs WHERE id_profil = ? "),(id,))    #on récupère les infos pour les afficher
            listeutilisateurs=c.fetchall()
            close_connection()
            return render_template('Modifprofil.html',listeutilisateurs=listeutilisateurs,succes=False,erreur=True,id_user=id)
        else :
            db=getdb()
            c = db.cursor() 
            c.execute(("SELECT * FROM Utilisateurs WHERE id_profil = ? "),(id,)) 
            listeutilisateurs=c.fetchall()
            close_connection()
            return render_template('Modifprofil.html',listeutilisateurs=listeutilisateurs,succes=False,erreur=False,id_user=id)




@app.route("/<id>/d/<id_dem>/ld", methods=['GET', 'POST'])
def Dencours(id,id_dem):   #on consulte une demande spécifique et on choisit si oui ou non on veut la réaliser
    db=getdb()
    c = db.cursor() 
    c.execute("SELECT * FROM Demandes WHERE id_dem = ? ",(id_dem,)) #on récupère toutes les infos de la demande
    listedemande=c.fetchall()
    close_connection()
    db=getdb()
    s = db.cursor() 
    s.execute("SELECT id_sondage FROM Sondages WHERE type = 'demande' AND typeid = ?",(id_dem,))    #on récupère l'id du sondage associé
    ls = s.fetchall()
    close_connection()
    db=getdb()
    f = db.cursor() 
    f.execute("SELECT filtre FROM Demandes WHERE id_dem = ?",(id_dem,))     #on récupère le filtre pour modifier le score
    lf = f.fetchall()
    print(lf)
    filtre = lf[0][0]
    close_connection()
    score_demande = score('demande',id)
    x = dico_num[filtre]    #on récupère le nombre associé au filtre de la demande
    print(x,filtre)
    score_demande *= x  #on multiplie le score par ce nombre
    db=getdb()
    u = db.cursor() 
    u.execute("UPDATE Utilisateurs SET score_demande = ? WHERE id_profil = ?",(str(score_demande),id,))     #on met à jour la valeur du
    db.commit()
    close_connection()
    if not ls:
        sondage = False
        id_sondage = 0
    else:
        sondage = True
        id_sondage = ls[0][0]
    choix = int(0 if request.form.get('choix') is None else request.form.get('choix'))
    print(choix)
    if choix==1:  #si l'utilisateur veut réaliser la demande on a choix==1 et on ajoute donc l'id de la demande dans la table postulant au postulant
        db = getdb()
        c = db.cursor()
        c.execute("SELECT id_postulant FROM Postulants WHERE id_post= ? ",(id_dem,))
        dl = c.fetchall()
        db.close()
        postulant = [ i[0] for i in dl]
        if int(id) in postulant:
            return render_template("CDemandes.html",listedemande=listedemande,deja_postule=True,sondage=sondage,id_sondage=id_sondage,id_user=id,id_dem=id_dem)
        else:
            score_demande = score('demande',id)
            x = dico_num[filtre]
            score_demande *= x**3
            db=getdb()
            u = db.cursor() 
            u.execute("UPDATE Utilisateurs SET score_demande = ? WHERE id_profil = ?",(str(score_demande),id,))
            db.commit()
            close_connection()
            db = getdb()
            a = db.cursor()
            a.execute("INSERT INTO Postulants VALUES(?,?,'')",(id_dem,id))
            db.commit()
            db.close()
        return redirect('/'+str(id)+'/demande/encours')
    elif request.form.get('choix') == None:
        return render_template("CDemandes.html",listedemande=listedemande,sondage=sondage,id_sondage=id_sondage,id_user=id,id_dem=id_dem)
    else:
        return redirect('/'+str(id)+'/demande/encours')



@app.route("/<id>/o/<id_offre>/lo",  methods=['GET', 'POST'])
def Oencours(id,id_offre):   #même principe de fonctionnement que Dencours
    db=getdb()
    c = db.cursor()
    c.execute("SELECT * FROM Offres WHERE id_offre = ? ",(id_offre)) 
    listeoffre=c.fetchall()
    close_connection()
    db=getdb()
    s = db.cursor() 
    s.execute("SELECT id_sondage FROM Sondages WHERE type = 'offre' AND typeid = ?",(id_offre,))
    ls = s.fetchall()
    close_connection()
    db=getdb()
    f = db.cursor() 
    f.execute("SELECT filtre FROM Offres WHERE id_offre = ?",(id_offre,))
    filtre = f.fetchall()[0][0]
    close_connection()
    score_offre = score('offre',id)
    x = dico_num[filtre]
    print(x,filtre)
    score_offre *= x
    db=getdb()
    u = db.cursor() 
    u.execute("UPDATE Utilisateurs SET score_offre = ? WHERE id_profil = ?",(str(score_offre),id,))
    db.commit()
    close_connection()
    if not ls:
        sondage = False
        id_sondage = 0
    else:
        sondage = True
        id_sondage = ls[0][0]
    choix = int(0 if request.form.get('choix') is None else request.form.get('choix'))
    if choix==1:
        db = getdb()
        c = db.cursor()
        c.execute("SELECT id_demandeur FROM Demandeurs WHERE id_offre_dem= ? ",(id_offre,))
        dl = c.fetchall()
        db.close()
        demandeur = [ i[0] for i in dl]
        if int(id) in demandeur:
            return render_template("COffres.html",listeoffre=listeoffre,deja_postule=True,sondage=sondage,id_sondage=id_sondage,id_user=id,id_offre=id_offre)
        else:
            score_offre = score('offre',id)
            x = dico_num[filtre]
            score_offre *= x**3
            db=getdb()
            u = db.cursor() 
            u.execute("UPDATE Utilisateurs SET score_offre = ? WHERE id_profil = ?",(str(score_offre),id,))
            db.commit()
            close_connection()
            db = getdb()
            a = db.cursor()
            a.execute("INSERT INTO Demandeurs VALUES(?,?,'')",(id_offre,id))
            db.commit()
            db.close()
        return redirect('/'+str(id)+'/offre/encours')
    elif request.form.get('choix') == None:
        return render_template("COffres.html",listeoffre=listeoffre,sondage=sondage,id_sondage=id_sondage,id_user=id,id_offre=id_offre)
    else:
        return redirect('/'+str(id)+'/offre/encours')


@app.route('/<id>/offre/creationo', methods=['GET', 'POST'])
def creationo(id):   #même principe de fonctionnement que creationd
    Titre=request.form.get('titre')
    if Titre is None :
        return render_template('AOffreBD.html',id_user=id)
    
    time = str('' if request.form.get('time') is None else request.form.get('time'))
    time = time[-2:] + '/' + time[5:7] + '/' + time[:4]     #pour mettre bon format de date
    Objet=request.form.get('objet')
    if request.method=="POST":
        Adresse=request.form.get('ville')
        Type=str('' if request.form.get('filtre') is None else request.form.get('filtre'))
        if Type == 'Choix du type':
            Type = 'Autre...'
        conn=getdb()
        cursor1= conn.cursor()
        cursor1.execute('SELECT MAX(id_offre) FROM Offres')
        l = cursor1.fetchall()
        conn.close()
        if not l:
            id_offre = '1'
        else:
            id_offre = str(int(l[0][0]) + 1)
        conn=getdb()
        cursor1=conn.cursor()
        cursor1.execute('INSERT INTO Offres (id_offre,id_auteur_off,etat,id_demandeur,lieu,description,titre,filtre,dateservice) VALUES(?,?,?,0,?,?,?,?,?) ', (id_offre,id,'en attente',Adresse,Objet,Titre,Type,time))     # ajout dans la BDD
        conn.commit()  
        close_connection()
        db = getdb()
        c = db.cursor()
        c.execute("INSERT INTO isSondage VALUES('offre',?,'False','[]')",(id_offre,))
        db.commit()
        close_connection()        
        return redirect(f"/{id}/mes_offres")                                                                               
    return render_template('AOffreBD.html',id_user=id)



@app.route('/<idd>/messondages')
def messondages(idd):
    db=getdb()
    c=db.cursor()
    c.execute("SELECT Bool from Mairie Where id_utilisateur= ?",(idd,))
    value=c.fetchall()
    if not value:
        db.close()
        return render_template("messondages.html", test=False, vide=False, list=[],id_user=idd)
    else : 
        test=('True' in value[0][0])
        if  not test:
            db.close()
            return render_template('messondages.html',test=test,vide=False,list=[],id_user=idd)
        else:
            a=db.cursor()
            a.execute(("Select type,typeid from Sondages where Sondages.id= ?"),(idd))
            l=a.fetchall()

            if not l:
                return render_template('messondages.html', test=test, vide=True, list=[],id_user=idd)
            else: #Si l'user est un compte mairie et qu'il a fait des sondages
                l_type=[l[k][0] for k in range(len(l))]
                l_typeid=[l[k][1] for k in range(len(l))]
                ell=[]
                s=""
                for k in range(len(l)):
                    db=getdb()
                    b=db.cursor()
                    cur=b
                    
                    if l_type[k]=='demande':  
                        b.execute(("Select titre From Demandes Where id_dem= ? "),(l_typeid[k],))
                        value=b.fetchall()
                        ell.append(value[0][0])
                        s+=str(value)
                    else:
                        b.execute(("Select titre From Offres Where id_offre= ?"),(l_typeid[k],))
                        value=b.fetchall()
                        ell.append(value[0][0])
                        s+=str(value)
                    b.close()

                return render_template('messondages.html',test=test,vide=False,list=ell,listType=l_type,id_user=idd) 





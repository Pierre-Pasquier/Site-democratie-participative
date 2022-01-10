DROP TABLE IF EXISTS Demandes CASCADE;
DROP TABLE IF EXISTS Postulants CASCADE;
DROP TABLE IF EXISTS Offres CASCADE;
DROP TABLE IF EXISTS Demandeurs CASCADE;
DROP TABLE IF EXISTS Utilisateurs CASCADE;


CREATE TABLE Demandes(
	id_dem int primary key check (id_dem > 0) NOT NULL,
	id_auteur_dem int check (id_auteur_dem > 0) NOT NULL,
	etat varchar check (etat in ('en attente','en cours','terminé')) NOT NULL,
	id_accepteur int DEFAULT 0,
	lieu varchar NOT NULL,
	description varchar,
	datedeb datetime default CURRENT_TIMESTAMP,
	titre varchar,
	filtre varchar check (filtre in ('Jardinage','Bricolage','Déménagement','Formation','Babysitting','Informatique','Autres taches physiques','Aide aux devoirs','Autres taches intellectuelles','Autre...')),
	dateservice datetime);;


CREATE TABLE Offres(
	id_offre int primary key check (id_offre > 0),
	id_auteur_off int check (id_auteur_off > 0) NOT NULL,
	etat varchar check (etat in ('en attente','en cours','terminé')) NOT NULL,
	id_demandeur int DEFAULT 0,
	lieu varchar NOT NULL,
	description varchar,
	datedeb datetime DEFAULT CURRENT_TIMESTAMP,
	titre varchar,
	filtre varchar check (filtre in ('Jardinage','Bricolage','Déménagement','Formation','Babysitting','Informatique','Autres taches physiques','Aide aux devoirs','Autres taches intellectuelles','Autre...')),
	dateservice datetime);;


CREATE TABLE Postulants(
	id_post int references Demandes (id_dem) check (id_post > 0) NOT NULL,
	id_postulant int check (id_postulant > 0) NOT NULL,
	message_postulant varchar DEFAULT '',
	primary key(id_post,id_postulant));

CREATE TABLE Demandeurs(
	id_offre_dem int references Offres (id_offre) check (id_offre_dem > 0) NOT NULL,
	id_demandeur int check (id_demandeur > 0) NOT NULL,
	message_demandeur varchar DEFAULT '',
	primary key(id_offre_dem,id_demandeur));


CREATE TABLE Utilisateurs(
	id_profil int primary key check (id_profil > 0) NOT NULL,
	score_demande varchar default '1',
	score_offre varchar default '1',
	pseudo varchar check (length(pseudo) >= 4),
	mail varchar check (mail LIKE '%@%') default '@',
	numTel varchar check (length(numTel) = 10 or length(numTel) = 14 ) default '00 00 00 00 00',
	mdp varchar check (length(mdp) >= 4) default 'tncy',
	description varchar default '');

CREATE TABLE Notation(
	id int primary key check (id>0) NOT NULL,
	note int check (1<note<5),
	nb_note int check (nb_note >= 0),
	note_par varchar);

CREATE TABLE Mairie(
	id_utilisateur int primary key check (id_utilisateur>0) not null,
	Bool varchar check (Bool in 
	('True','False')
	) 
	);

CREATE TABLE Sondages(
	id integer not null,
	type varchar check (type in ('offre','demande')),
	typeid integer not null,
	id_sondage integer primary key not null check (id_sondage>=1),
	questions varchar,
	reponses varchar,
	type_rep varchar,
	UNIQUE(id,typeid,id_sondage)
	);

CREATE TABLE isSondage(
	type varchar references Sondages (type) check (type in ('offre','demande')),
	id_annonce int references Sondages (typeid) check (id_annonce>0),
	Bool varchar check (Bool in ('True','False')),
	repondu_par varchar DEFAULT '[]' ,
	primary key(type,id_annonce)
	);


INSERT INTO Utilisateurs VALUES(1,1,1,'Mairie de Nancy','nancymairie@test.com', '0606060606','jiFOsg==*p97SKNoPgahT33gDhwgYTg==*4koNRqJLQCDpzDNkhK74uA==*jnJqZZfOrxFNWFvdHO9J2w==',"Mairie non officielle de nancy parce que c'est un test.");


INSERT INTO Utilisateurs VALUES(2,1,1,'Jean','jeanmichel08@gmail.com','0651998019','jiFOsg==*p97SKNoPgahT33gDhwgYTg==*4koNRqJLQCDpzDNkhK74uA==*jnJqZZfOrxFNWFvdHO9J2w==',"Bonjour j’aime le bricolage");

INSERT INTO Utilisateurs VALUES(3,1,1,'Gauthier','Gauthierdu77@hotmail.com','0667985478','jiFOsg==*p97SKNoPgahT33gDhwgYTg==*4koNRqJLQCDpzDNkhK74uA==*jnJqZZfOrxFNWFvdHO9J2w==', "agriculteur à mes heures perdues");

INSERT INTO Utilisateurs VALUES(4,1,1,'Michael','michealfrog@gmail.com','0606060806','jiFOsg==*p97SKNoPgahT33gDhwgYTg==*4koNRqJLQCDpzDNkhK74uA==*jnJqZZfOrxFNWFvdHO9J2w==', "j'ai souvent besoin d’aide pour des travaux");

INSERT INTO Utilisateurs VALUES(5,1,1,'Kevin','kevindbz@gmail.com','0609060606','jiFOsg==*p97SKNoPgahT33gDhwgYTg==*4koNRqJLQCDpzDNkhK74uA==*jnJqZZfOrxFNWFvdHO9J2w==', "j'aime beaucoup les motos");

INSERT INTO Utilisateurs VALUES(6,1,1,'Carole','carolejohn@gmail.com','0651795019','jiFOsg==*p97SKNoPgahT33gDhwgYTg==*4koNRqJLQCDpzDNkhK74uA==*jnJqZZfOrxFNWFvdHO9J2w==',"J'aime beaucoup l’idée de pouvoir compter sur mes voisins");

INSERT INTO Utilisateurs VALUES(7,1,1,'Marine','marinefete@test.com','0606360606','jiFOsg==*p97SKNoPgahT33gDhwgYTg==*4koNRqJLQCDpzDNkhK74uA==*jnJqZZfOrxFNWFvdHO9J2w==', 'Ensemble rendons notre ville meilleur !');

INSERT INTO Utilisateurs VALUES(8,1,1,'Carole','carole@gmail.com','0706060606','jiFOsg==*p97SKNoPgahT33gDhwgYTg==*4koNRqJLQCDpzDNkhK74uA==*jnJqZZfOrxFNWFvdHO9J2w==', "je suis très forte en langue et j adore aider les autres à s améliorer");

INSERT INTO Utilisateurs VALUES(9,1,1,"Manon","manonkleiner@test.com","0645060606","jiFOsg==*p97SKNoPgahT33gDhwgYTg==*4koNRqJLQCDpzDNkhK74uA==*jnJqZZfOrxFNWFvdHO9J2w==", "j ai des difficultés aux lycée c est pourquoi j aimerais voir si des personnes ici ne pourraient pas m aider");



INSERT INTO Mairie VALUES(1,'True');
INSERT INTO Mairie VALUES(2,'False');
INSERT INTO Mairie VALUES(3,'False');
INSERT INTO Mairie VALUES(4,'False');
INSERT INTO Mairie VALUES(5,'False');
INSERT INTO Mairie VALUES(6,'False');
INSERT INTO Mairie VALUES(7,'False');
INSERT INTO Mairie VALUES(8,'False');
INSERT INTO Mairie VALUES(9,'False');

INSERT INTO Notation VALUES(1,0,0,'[]');
INSERT INTO Notation VALUES(2,0,0,'[]');
INSERT INTO Notation VALUES(3,0,0,'[]');
INSERT INTO Notation VALUES(4,0,0,'[]');
INSERT INTO Notation VALUES(5,0,0,'[]');
INSERT INTO Notation VALUES(6,0,0,'[]');
INSERT INTO Notation VALUES(7,0,0,'[]');
INSERT INTO Notation VALUES(8,0,0,'[]');
INSERT INTO Notation VALUES(9,0,0,'[]');

INSERT INTO Demandes VALUES(1,1,'en attente',0,'Nancy',"Bonjour, je cherche quelqu'un qui aurait un pneu en rab","01/01/22",'Besoin de pneu svp','Bricolage','10/01/22');

INSERT INTO Demandes VALUES(2,4,'en attente',0,'Nancy',"Bonjour, j'aurai besoin d'une formation en Latex","01/01/22",'Latex : besoin forma','Formation','01/01/22');

INSERT INTO Demandes VALUES(3,5,'en attente',0,'Nancy',"Bonjour, êtes vous intéressé par venir repeindre nos trams?","04/01/22",'Peinture Tram','Bricolage','05/01/22');

INSERT INTO Demandes VALUES(4,2,'en attente',0,'Nancy',"Bonjour j aurai besoin de quelqu un pour venir arroser mon jardin pendant mes vacances. J ai 200 mètres carré et j habite à Villers","04/01/22","Besoin de quelqu un pour arroser mon jardin pendant mes vacances",'Jardinage','28/01/22');

INSERT INTO Demandes VALUES(5,7,'en attente',0,'Nancy',"Bonjour, j aurai besoin d aide pour débarrasser mon apartement de 25 mètres carrés le 20/01/2022 ","04/01/22",'Besoin d aide pour déménager','Déménagement','20/01/22');

INSERT INTO Demandes VALUES(6,8,'en attente',0,'Nancy',"Bonjour, je suis en 3ème et j aurai besoin d aide en maths. Je pense que 2h par semaine suffirait","04/01/22","Besoin d aide en maths (niveau 3ème)",'Aide aux devoirs','10/01/22');

INSERT INTO Demandes VALUES(7,9,'en attente',0,'Nancy',"Bonjour, j aurai besoin de quelqu un qui puisse garder mes enfants durant la soirée du 15/01/22","04/01/22",'Garde de 2 enfants durant une soirée','Babysitting','15/01/22');

INSERT INTO Demandes VALUES(8,5,'en attente',0,'Nancy',"Bonjour, j aurai besoin d aide pour sortir un meuble de chez moi et le charger dans ma remorque afin de l amener à la déchetterie","04/01/22",'Besoin d aide pour charger un meuble lourd dans ma remorque','Autres taches physiques','18/01/22');

INSERT INTO Demandes VALUES(9,6,'en attente',0,'Nancy',"Bonjour, j aurai besoin de quelqu un qui puisse me concevoir un site internet pour mon commerce","04/01/22","Besoin d un site internet pour mon commerce",'Autres taches intellectuelles','20/01/22');

INSERT INTO Demandes VALUES(10,7,'en attente',0,'Nancy',"Bonjour, je suis une personne agée et j aurai besoin d'aide en informatique pour envoyer des mails à mes petits-enfants","04/01/22",'Aide à personne agée pour informatique','Formation','16/01/22');

INSERT INTO Demandes VALUES(11,4,'en attente',0,'Nancy',"Bonjour, j aurai besoin de quelqu un à qui je puisse parler de mes problèmes","04/01/22",'Besoin de quelqu un pour parler','Autre...','10/01/22');



INSERT INTO Offres VALUES(1,2,'en attente',0,'Nancy',"Bonjour j aide à faire des sondages",'02/01/22','Création de sondages','Formation','01/01/22');

INSERT INTO Offres VALUES(2,3,'en attente',0,'Nancy',"Bonjour, j offre des oeufs, qui en veut?",'01/01/22',"J offre des oeufs",'Autre...','16/12/21');

INSERT INTO Offres VALUES(3,5,'en attente',0,'Nancy',"Bonjour, vous voulez plus de trams ?",'01/01/22',"Nouveaux trams",'Bricolage','05/01/22');

INSERT INTO Offres VALUES(4,9,'en attente',0,'Nancy',"Bonjour je peux vous aider à faire vos devoirs",'02/01/22','Aide pour les études','Aide aux devoirs','01/01/22');

INSERT INTO Offres VALUES(5,6,'en attente',0,'Nancy',"Bonjour, je peux vous aider à  vous occuper de vos plantes",'01/01/22',"Je m occupe de vos plantes",'Jardinage','12/12/21');

INSERT INTO Offres VALUES(6,4,'en attente',0,'Nancy',"Bonjour, je peux vous aider à déménager si vous voulez",'01/01/22',"Aide aux déménagement",'Déménagement','11/01/22');

INSERT INTO Offres VALUES(7,3,'en attente',0,'Nancy',"Bonjour, je fais des études de coaching en sport et je peux vous aider à faire du sport. Cela me permettrait de m exercer à ce métier",'02/01/22','Coaching de sport','Autres taches physiques','10/01/22');

INSERT INTO Offres VALUES(8,7,'en attente',0,'Nancy',"Bonjour, je peux essayer de vous aider pour des taches intellectuelles quelconques",'01/01/22',"Aide pour taches intellectuelles quelconques",'Autres taches intellectuelles','16/12/21');

INSERT INTO Offres VALUES(9,5,'en attente',0,'Nancy',"Bonjour, je peux garder vos enfants ou vos animaux de compagnie",'01/01/22',"Garde d enfants ou d animaux de companie",'Babysitting','05/01/22');

INSERT INTO Offres VALUES(10,8,'en attente',0,'Nancy',"Bonjour, je peux aider pour des problèmes d informatique",'02/01/22','Création de sondages','Informatique','28/02/22');


INSERT INTO isSondage VALUES('demande',1,'False','[]');
INSERT INTO isSondage VALUES('demande',2,'False','[]');
INSERT INTO isSondage VALUES('demande',3,'False','[]');
INSERT INTO isSondage VALUES('demande',4,'False','[]');
INSERT INTO isSondage VALUES('demande',5,'False','[]');
INSERT INTO isSondage VALUES('demande',6,'False','[]');
INSERT INTO isSondage VALUES('demande',7,'False','[]');
INSERT INTO isSondage VALUES('demande',8,'False','[]');
INSERT INTO isSondage VALUES('demande',9,'False','[]');
INSERT INTO isSondage VALUES('demande',10,'False','[]');
INSERT INTO isSondage VALUES('demande',11,'False','[]');

INSERT INTO isSondage VALUES('offre',1,'False','[]');
INSERT INTO isSondage VALUES('offre',2,'False','[]');
INSERT INTO isSondage VALUES('offre',3,'False','[]');
INSERT INTO isSondage VALUES('offre',4,'False','[]');
INSERT INTO isSondage VALUES('offre',5,'False','[]');
INSERT INTO isSondage VALUES('offre',6,'False','[]');
INSERT INTO isSondage VALUES('offre',7,'False','[]');
INSERT INTO isSondage VALUES('offre',8,'False','[]');
INSERT INTO isSondage VALUES('offre',9,'False','[]');
INSERT INTO isSondage VALUES('offre',10,'False','[]');























DROP TABLE IF EXISTS Demandes CASCADE;
DROP TABLE IF EXISTS Postulants CASCADE;
DROP TABLE IF EXISTS Offres CASCADE;
DROP TABLE IF EXISTS Demandeurs CASCADE;
DROP TABLE IF EXISTS Utilisateurs CASCADE;


CREATE TABLE Demandes(
	id_dem int primary key check (id_dem > 0) NOT NULL,
	id_auteur_dem int check (id_auteur_dem > 0) NOT NULL,
	etat varchar check (etat in ('en attente','en cours','terminé')) NOT NULL,
	id_accepteur int check(id_accepteur>0),
	lieu varchar NOT NULL,
	description varchar,
	datedeb datetime default CURRENT_TIMESTAMP,
	titre varchar,
	filtre varchar check (filtre in ('Jardinage','Bricolage','Demenagement','Formation','Babysitting','Informatique','Autres taches physiques','Aide aux devoirs','Autres taches intellectuelles','Autre')),
	dateservice datetime);;


CREATE TABLE Offres(
	id_offre int primary key check (id_offre > 0),
	id_auteur_off int check (id_auteur_off > 0) NOT NULL,
	etat varchar check (etat in ('en attente','en cours','terminé')) NOT NULL,
	id_demandeur int check(id_demandeur>0),
	lieu varchar NOT NULL,
	description varchar,
	datedeb datetime DEFAULT CURRENT_TIMESTAMP,
	titre varchar,
	filtre varchar check (filtre in ('Jardinage','Bricolage','Demenagement','Formation','Babysitting','Informatique','Autres taches physiques','Autres taches intellectuelles', 'Aide aux devoirs','Autre')),
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
	score_demande int check (score_demande >=1) default 1,
	score_offre int check (score_offre >=1) default 1,
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
	repondu_par varchar)
	);


INSERT INTO Utilisateurs VALUES(1,1,1,'Piero','pierrepasquier63@gmail.com','0651798019','tncy','bonjour je m appelle Pierre');

INSERT INTO Utilisateurs VALUES(2,1,1,'FLexThomas','sondageLover@test.com','0606060606','tncy',"bonjour j'adore créer mes sondages");

INSERT INTO Utilisateurs VALUES(3,1,1,'LifteurNathan','jepousseàlasalle@test.com','0606060606','tncy',"bonjour, j'adore pousser à la salle");

INSERT INTO Utilisateurs VALUES(4,1,1,'EurobeatJulien','àfondsurlautoroute@test.com','0606060606','tncy',"bonjour, j'adore écouter de l'eurobeat");

INSERT INTO Utilisateurs VALUES(5,1,1,'Mairie de Nancy','nancymairie@test.com','0606060606','tncy',"Mairie non officielle de nancy parce que c'est un test.");

INSERT INTO Mairie VALUES(1,'False');
INSERT INTO Mairie VALUES(2,'False');
INSERT INTO Mairie VALUES(3,'False');
INSERT INTO Mairie VALUES(4,'False');
INSERT INTO Mairie VALUES(5,'True');

INSERT INTO Notation VALUES(1,0,0,'[]');
INSERT INTO Notation VALUES(2,0,0,'[]');
INSERT INTO Notation VALUES(3,0,0,'[]');
INSERT INTO Notation VALUES(4,0,0,'[]');
INSERT INTO Notation VALUES(5,0,0,'[]');

INSERT INTO Demandes VALUES(1,1,'en attente','[]','Nancy',"Bonjour, je cherche quelqu'un qui aurait un pneu en rab","01/01/22",'Besoin de pneu svp','Bricolage','10/01/22');

INSERT INTO Demandes VALUES(2,4,'en attente','[]','Nancy',"Bonjour, j'aurai besoin d'une formation en Latex plz","01/01/22",'Latex : besoin forma','Formation','01/01/22');

INSERT INTO Demandes VALUES(3,5,'en attente','[]','Nancy',"Bonjour, êtes vous intéressé par venir repeindre nos trams?","04/01/22",'Peinture Tram','Bricolage','05/01/22');

INSERT INTO Offres VALUES(1,2,'en attente','[]','Nancy','Bonjour jaide à faire des sondages','02/01/22','Création de sondages','Formation','01/01/22');

INSERT INTO Offres VALUES(2,3,'en attente','[]','Nancy',"Bonjour, j'offre des oeufs, qui veut?",'01/01/22',"Trop d'oeufs!",'Autre','16/12/21');

INSERT INTO Offres VALUES(3,5,'en attente','[]','Nancy',"Bonjour, vous voulez des trams moins chiants?",'01/01/22',"Nouveaux trams",'Bricolage','05/01/22');

INSERT INTO isSondage VALUES('demande',1,'False');
INSERT INTO isSondage VALUES('demande',2,'False');
INSERT INTO isSondage VALUES('demande',3,'False');
INSERT INTO isSondage VALUES('offre',1,'False');
INSERT INTO isSondage VALUES('offre',2,'False');
INSERT INTO isSondage VALUES('offre',3,'False');

INSERT INTO Demandeurs VALUES(2,1,"oh cool des oeufs, j'arrive à TN les récupérer");

INSERT INTO Demandeurs VALUES(2,2,"pourquoi pas, ça sera surement utile");

INSERT INTO Demandeurs VALUES(3,1,"j'aime bien peindre, je suis dispo");
INSERT INTO Demandeurs VALUES(3,2,"je me sens l'âme d'un artiste");
INSERT INTO Postulants VALUES(3,3,"jvous les lève vos trams là");
INSERT INTO Postulants VALUES(3,4,"j'avoue les trams sont chiants");





















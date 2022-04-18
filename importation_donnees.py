# IMPORTATION DES DONNÉES ET CREATION DU TABLEAU
import sqlite3, csv
import pandas as pd

conn = sqlite3.connect('db_tables_v1')
print("La connexion avec la base de donnée est bien ouverte.")

#conn.execute("CREATE TABLE sondage(id INT, titre VARCHAR(50), PRIMARY KEY(id));")

#conn.execute("CREATE TABLE matching_questions(id INT, type VARCHAR(10), theme VARCHAR(30), title VARCHAR(50), PRIMARY KEY(id));")

#conn.execute("CREATE TABLE users(id INT, code_postal INT, commune VARCHAR(30), type_commune VARCHAR(20), nom_departement VARCHAR(30), departement INT, genre VARCHAR(20), tranche_age VARCHAR(15), formation VARCHAR(30), profession VARCHAR(30), taille_org VARCHAR(30), position_gj VARCHAR(30), PRIMARY KEY(id));")

#conn.execute("CREATE TABLE questions_posees(Sid INT, MQid INT, ordre INT, FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(MQid) REFERENCES matching_questions(id), PRIMARY KEY(Sid, MQid));")

#conn.execute("CREATE TABLE matching_answers_qcm(id INT, MQid INT, title TEXT, FOREIGN KEY(MQid) REFERENCES matching_questions(id), PRIMARY KEY(id, MQid));")

#conn.execute("CREATE TABLE answers_qcm(Sid INT, Uid INT, MQid INT, MAid INT, FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(Uid) REFERENCES users(id), FOREIGN KEY(MQid) REFERENCES matching_questions(id), FOREIGN KEY(MAid) REFERENCES matching_answers_qcm(id), PRIMARY KEY(Sid, Uid, MQid, MAid));")

#conn.execute("CREATE TABLE answers_free(Sid INT, Uid INT, MQid INT, answer TEXT, FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(Uid) REFERENCES users(id), FOREIGN KEY(MQid) REFERENCES matching_questions(id), PRIMARY KEY(Sid, Uid, MQid));")

# Importation des donnees dans la table

chemin_fichier = "./bdd/users.csv"
with open(chemin_fichier, 'r', encoding="utf-8") as csvfile:
    fichier_lu = csv.reader(csvfile, delimiter=";")
    liste_lignes = []
    for row in fichier_lu:
        liste_lignes.append(row)
    # supprime la première ligne correspondant au titre
    liste_lignes.pop(0)
    print(liste_lignes[1])
    for ind_ligne in range(0, len(liste_lignes)):
        id = liste_lignes[ind_ligne][0]
        code_postal = liste_lignes[ind_ligne][1]
        commune = liste_lignes[ind_ligne][2]
        type_commune = liste_lignes[ind_ligne][3]
        nom_departement = liste_lignes[ind_ligne][4]
        departement = liste_lignes[ind_ligne][5]
        genre = liste_lignes[ind_ligne][6]
        tranche_age = liste_lignes[ind_ligne][7]
        formation = liste_lignes[ind_ligne][8]
        profession = liste_lignes[ind_ligne][9]
        taille_org = liste_lignes[ind_ligne][10]
        position_gj = liste_lignes[ind_ligne][11]
        conn.execute('INSERT INTO users VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(id, code_postal, commune, type_commune, nom_departement, departement, genre, tranche_age, formation, profession, taille_org, position_gj))
    resultat = conn.execute("SELECT * FROM users")
    liste = resultat.fetchall()
    for li in liste:
        print(li)
import sqlite3
import csv

conn = sqlite3.connect('db_tables_v1')
print("La connexion avec la base de donnée est bien ouverte.")

# Création des tables
# conn.execute("CREATE TABLE sondage(id INT, titre VARCHAR(50), PRIMARY KEY(id));")
#
# conn.execute("CREATE TABLE matching_questions(id INT, type VARCHAR(10), theme VARCHAR(30), title VARCHAR(50), PRIMARY KEY(id));")
#
# conn.execute("CREATE TABLE users(id INT, code_postal INT, commune VARCHAR(30), type_commune VARCHAR(20), nom_departement VARCHAR(30), departement INT, genre VARCHAR(20), tranche_age VARCHAR(15), formation VARCHAR(30), profession VARCHAR(30), taille_org VARCHAR(30), position_gj VARCHAR(30), PRIMARY KEY(id));")
#
# conn.execute("CREATE TABLE questions_posees(Sid INT, MQid INT, ordre INT, FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(MQid) REFERENCES matching_questions(id), PRIMARY KEY(Sid, MQid));")
#
# conn.execute("CREATE TABLE matching_answers_qcm(id INT, MQid INT, title TEXT, FOREIGN KEY(MQid) REFERENCES matching_questions(id), PRIMARY KEY(id, MQid));")
#
# conn.execute("CREATE TABLE answers_qcm(Sid INT, Uid INT, MQid INT, MAid INT, FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(Uid) REFERENCES users(id), FOREIGN KEY(MQid) REFERENCES matching_questions(id), FOREIGN KEY(MAid) REFERENCES matching_answers_qcm(id), PRIMARY KEY(Sid, Uid, MQid, MAid));")
#
# conn.execute("CREATE TABLE answers_free(Sid INT, Uid INT, MQid INT, answer TEXT, FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(Uid) REFERENCES users(id), FOREIGN KEY(MQid) REFERENCES matching_questions(id), PRIMARY KEY(Sid, Uid, MQid));")

# Importation des donnees dans la table
conn.execute("INSERT INTO sondage VALUES('001', 'Entendre_la_France')")
chemin_fichier = "./bdd/users.csv"

with open(chemin_fichier, "r", encoding="utf-8") as csvfile:
    fichier_lu = csv.reader(csvfile, delimiter=";")
    liste_lignes = []
    for row in fichier_lu:
        liste_lignes.append(row)
    # supprime la première ligne correspondant au titre
    liste_lignes.pop(0)
    for ind_ligne in range(0, len(liste_lignes)):
        id = ind_ligne+1
        type = liste_lignes[ind_ligne][1]
        theme = liste_lignes[ind_ligne][2]
        title = liste_lignes[ind_ligne][3]
        conn.execute('INSERT INTO matching_questions VALUES("{}", "{}", "{}", "{}")'.format(id, type, theme, title))
    resultat = conn.execute("SELECT * FROM matching_questions")
    liste = resultat.fetchall()
    for li in liste:
        print(li)
chemin_fichier = "./bdd/users.csv"
with open(chemin_fichier, 'r', encoding="utf-8") as csvfile:
    fichier_lu = csv.reader(csvfile, delimiter=";")
    liste_lignes = []
    for row in fichier_lu:
        liste_lignes.append(row)
    # supprime la première ligne correspondant au titre
    liste_lignes.pop(0)
    print(liste_lignes[1])
    for ind_ligne in range(0, len(liste_lignes)):
        id = liste_lignes[ind_ligne][0]
        code_postal = liste_lignes[ind_ligne][1]
        commune = liste_lignes[ind_ligne][2]
        type_commune = liste_lignes[ind_ligne][3]
        nom_departement = liste_lignes[ind_ligne][4]
        departement = liste_lignes[ind_ligne][5]
        genre = liste_lignes[ind_ligne][6]
        tranche_age = liste_lignes[ind_ligne][7]
        formation = liste_lignes[ind_ligne][8]
        profession = liste_lignes[ind_ligne][9]
        taille_org = liste_lignes[ind_ligne][10]
        position_gj = liste_lignes[ind_ligne][11]
        conn.execute('INSERT INTO users VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(id, code_postal, commune, type_commune, nom_departement, departement, genre, tranche_age, formation, profession, taille_org, position_gj))
    resultat = conn.execute("SELECT * FROM users")
    liste = resultat.fetchall()
    for li in liste:
        print(li)
# Importation des donnees dans la table
conn.execute("INSERT INTO sondage VALUES('001', 'Entendre_la_France')")
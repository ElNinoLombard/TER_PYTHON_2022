# --- Les imports
import sqlite3
import csv
import demoji

# --- Ouverture connexion à la BDD
conn = sqlite3.connect('db_tables_v1')
cur = conn.cursor()


# --- Les fonctions
# Fonction utile pour matching_answers_qcm
def is_integer(n):
   try:
       float(n)
   except ValueError:
       return False
   else:
       return float(n).is_integer()


# -- Création des tables
cur.execute("CREATE TABLE IF NOT EXISTS sondage(id INT, titre VARCHAR(50), PRIMARY KEY(id));")
cur.execute(
   "CREATE TABLE IF NOT EXISTS matching_questions(id INT, type VARCHAR(10), theme VARCHAR(30), "
   "title VARCHAR(50), PRIMARY KEY(id));")
cur.execute(
   "CREATE TABLE IF NOT EXISTS users(id INT, code_postal INT, commune VARCHAR(30), type_commune VARCHAR(20), "
   "nom_departement VARCHAR(30), departement INT, genre VARCHAR(20), tranche_age VARCHAR(15), formation VARCHAR(30), "
   "profession VARCHAR(30), taille_org VARCHAR(30), position_gj VARCHAR(30), PRIMARY KEY(id));")
cur.execute(
   "CREATE TABLE IF NOT EXISTS questions_posees(Sid INT, ordre INT, MQid INT, "
   "FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(MQid) REFERENCES matching_questions(id), "
   "PRIMARY KEY(Sid, ordre));")
cur.execute(
   "CREATE TABLE IF NOT EXISTS matching_answers_qcm(id INT, MQid INT, title TEXT, "
   "FOREIGN KEY(MQid) REFERENCES matching_questions(id), PRIMARY KEY(id, MQid));")
cur.execute(
   "CREATE TABLE IF NOT EXISTS answers_qcm(Sid INT, Uid INT, MQid INT, MAid INT, "
   "FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(Uid) REFERENCES users(id), "
   "FOREIGN KEY(MQid) REFERENCES matching_questions(id), FOREIGN KEY(MAid) REFERENCES matching_answers_qcm(id), "
   "PRIMARY KEY(Sid, Uid, MQid, MAid));")
cur.execute(
   "CREATE TABLE IF NOT EXISTS answers_free(Sid INT, Uid INT, MQid INT, answer TEXT, "
   "FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(Uid) REFERENCES users(id), FOREIGN KEY(MQid) "
   "REFERENCES matching_questions(id), PRIMARY KEY(Sid, Uid, MQid));")

# -- Remplissage des tables

#  Table sondage - Une seule entité à créer
id_ = 1
titre = "Entendre la France"
cur.execute('INSERT INTO sondage VALUES("{}", "{}")'.format(id_, titre))

# Table matching_questions
chemin_fichier = "./Data_entendre_la_france/matching_questions.csv"

# Lecture du fichier
with open(chemin_fichier, "r", encoding="utf-8") as csvfile:
   fichier_lu = csv.reader(csvfile, delimiter=";")
   liste_lignes = []
   for row in fichier_lu:
       liste_lignes.append(row)
   # supprime la première ligne correspondant au titre
   liste_lignes.pop(0)

   correspondance_question_id = {}  # utile pour matching_answers_qcm,
   for ind_ligne in range(0, len(liste_lignes)):
       id_ = ind_ligne + 1
       correspondance_question_id[liste_lignes[ind_ligne][0]] = id_  # sauvegarde de l'association id et id dans le doc
       if liste_lignes[ind_ligne][1] == "QCM":
           type_ = "QCU"
       else:
           type_ = liste_lignes[ind_ligne][1]
       theme = liste_lignes[ind_ligne][2]
       title = liste_lignes[ind_ligne][3]
       cur.execute('INSERT INTO matching_questions VALUES("{}", "{}", "{}", "{}")'.format(id_, type_, theme, title))

# Table questions_posees
Sid = 1
resultat = cur.execute("SELECT id FROM matching_questions")
liste = resultat.fetchall()
compteur = 0
for li in liste:
   compteur += 1
   cur.execute('INSERT INTO questions_posees VALUES("{}", "{}", "{}")'.format(1, compteur, li[0]))

# Table users
chemin_fichier = "./Data_entendre_la_france/users.csv"

with open(chemin_fichier, 'r', encoding="utf-8") as csvfile:
   fichier_lu = csv.reader(csvfile, delimiter=";")
   liste_lignes = []
   for row in fichier_lu:
       liste_lignes.append(row)
   # supprime la première ligne correspondant au titre
   liste_lignes.pop(0)
   for ind_ligne in range(0, len(liste_lignes)):
       id_ = liste_lignes[ind_ligne][0]
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
       cur.execute(
           'INSERT INTO users VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
               id_, code_postal, commune, type_commune, nom_departement, departement, genre, tranche_age, formation,
               profession, taille_org, position_gj))

# Table matching_answers_qcm
chemin_fichier = "./Data_entendre_la_france/matching_answers_qcm.csv"

with open(chemin_fichier, 'r', encoding="utf-8") as csvfile:
   fichier_lu = csv.reader(csvfile, delimiter=";")
   liste_lignes = []
   for row in fichier_lu:
       liste_lignes.append(row)
   # supprime la première ligne correspondant au titre
   liste_lignes.pop(0)

   id_max = 0

   correspondance_question_max = {}  # Utilisé pour answers_qcm
   for ind_ligne in range(0, len(liste_lignes)):
       MQid = correspondance_question_id[liste_lignes[ind_ligne][0]]
       title = liste_lignes[ind_ligne][2]

       # Conversion de l'emoji en id
       emoji_code = demoji.findall(liste_lignes[ind_ligne][1])

       for code_emo in emoji_code.values():
           if is_integer(code_emo.split(":")[-1]):
               id_max += 1
               id_ = int(code_emo.split(":")[-1])
           else:
               correspondance_question_max[MQid] = id_max  # Utilisé pour answers_qcm
               id_ = id_max + 1
               id_max = 0
       cur.execute('INSERT INTO matching_answers_qcm VALUES("{}", "{}", "{}")'.format(id_, MQid, title))

# Table answers_free
chemin_fichier = "./Data_entendre_la_france/answers_free.csv"

with open(chemin_fichier, 'r', encoding="utf-8") as csvfile:
   fichier_lu = csv.reader(csvfile, delimiter=";")
   liste_lignes = []
   for row in fichier_lu:
       liste_lignes.append(row)
   # supprime la première ligne correspondant au titre
   liste_lignes.pop(0)

   for ind_ligne in range(0, len(liste_lignes)):
       Uid = liste_lignes[ind_ligne][0]
       MQid = correspondance_question_id[liste_lignes[ind_ligne][1]]
       answer = liste_lignes[ind_ligne][2]
       cur.execute(
           'INSERT INTO answers_free VALUES("{}", "{}", "{}", "{}")'.format(1, Uid, MQid, answer.replace("\"", "'")))

# Table answers_qcm
chemin_fichier = "./Data_entendre_la_france/answers_qcm.csv"

with open(chemin_fichier, 'r', encoding="utf-8") as csvfile:
   fichier_lu = csv.reader(csvfile, delimiter=";")
   liste_lignes = []
   for row in fichier_lu:
       liste_lignes.append(row)
   # supprime la première ligne correspondant au titre
   liste_lignes.pop(0)

   for ind_ligne in range(0, len(liste_lignes)):
       Uid = liste_lignes[ind_ligne][0]
       MQid = correspondance_question_id[liste_lignes[ind_ligne][1]]
       MAid = 0

       emoji_code = demoji.findall(liste_lignes[ind_ligne][2])

       for code_emo in emoji_code.values():
           if is_integer(code_emo.split(":")[-1]):
               MAid = int(code_emo.split(":")[-1])
           else:
               MAid = correspondance_question_max[MQid] + 1
       cur.execute('INSERT INTO answers_qcm VALUES("{}", "{}", "{}", "{}")'.format(1, Uid, MQid, MAid))

# -- Création d'un sondage comportant des QCU, QCM et questions libres
cur.execute('INSERT INTO sondage VALUES("2", "Sondage de test")')

# Question 100 posée en première
cur.execute('INSERT INTO matching_questions VALUES("100", "QCM", "Sports et Loisirs", '
           '"Parmi les activités suivantes, la.les.quelle.s avez-vous déjà effectuée.s ?")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("1", "100", "Du kayak")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("2", "100", "Du foot")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("3", "100", "Des échecs")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("4", "100", "Des trucs de gamers")')

# Question 101 posée en deuxième
cur.execute('INSERT INTO matching_questions VALUES("101", "QCU", "Sports et Loisirs", '
           '"Avez-vous déjà pratiqué de la planche à voile ?")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("1", "101", "Oui")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("2", "101", "Non")')

# Question 102 posée en quatrième
cur.execute('INSERT INTO matching_questions VALUES("102", "QCU", "Santé", '
           '"Combien d\'heure dormez-vous en moyenne par nuit depuis un mois ?")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("1", "102", "0-1 heure")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("2", "102", "2 heures")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("3", "102", "3 heures")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("4", "102", "4 heures")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("5", "102", "5 heures")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("6", "102", "6 heures")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("7", "102", "7 heures")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("8", "102", "8 heures")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("9", "102", "9 heures")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("10", "102", "10 heures")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("11", "102", "11 heures")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("12", "102", "12 heures")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("13", "102", "Plus de 12 heures")')

# Question 103 posée en cinquième
cur.execute('INSERT INTO matching_questions VALUES("103", "QCU", "Santé", '
           '"Êtes-vous vacciné.e contre la COVID-19 ?")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("1", "103", "Oui")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("2", "103", "Non")')
cur.execute('INSERT INTO matching_answers_qcm VALUES("3", "103", "Je ne souhaite pas répondre")')

# Question 104 posée en troisième
cur.execute('INSERT INTO matching_questions VALUES("104", "Libre", "Achats", '
           '"Dans quel magasin faites-vous le plus souvent vos courses ?")')

cur.execute('INSERT INTO questions_posees VALUES("2", "1", "100")')
cur.execute('INSERT INTO questions_posees VALUES("2", "2", "101")')
cur.execute('INSERT INTO questions_posees VALUES("2", "3", "104")')
cur.execute('INSERT INTO questions_posees VALUES("2", "4", "102")')
cur.execute('INSERT INTO questions_posees VALUES("2", "5", "103")')

# -- Création de quelques utilisateurs n'ayant répondu à aucun sondage
cur.execute('INSERT INTO users VALUES("50000", "", "", "", "", "", "", "", "", "", "", "")')
cur.execute('INSERT INTO users VALUES("50001", "", "", "", "", "", "", "", "", "", "", "")')
cur.execute('INSERT INTO users VALUES("50002", "", "", "", "", "", "", "", "", "", "", "")')
cur.execute('INSERT INTO users VALUES("50003", "", "", "", "", "", "", "", "", "", "", "")')
cur.execute('INSERT INTO users VALUES("50004", "", "", "", "", "", "", "", "", "", "", "")')
cur.execute('INSERT INTO users VALUES("50005", "", "", "", "", "", "", "", "", "", "", "")')
cur.execute('INSERT INTO users VALUES("50006", "", "", "", "", "", "", "", "", "", "", "")')
cur.execute('INSERT INTO users VALUES("50007", "", "", "", "", "", "", "", "", "", "", "")')
cur.execute('INSERT INTO users VALUES("50008", "", "", "", "", "", "", "", "", "", "", "")')
cur.execute('INSERT INTO users VALUES("50009", "", "", "", "", "", "", "", "", "", "", "")')
cur.execute('INSERT INTO users VALUES("50010", "", "", "", "", "", "", "", "", "", "", "")')

# -- Les tests

# - Tests remplissage tables

# Pour sondage :
# resultat = cur.execute("SELECT * FROM sondage")
# liste = resultat.fetchall()
# for li in liste:
#     print(li)

# Pour matching_questions :
# resultat = cur.execute("SELECT * FROM matching_questions")
# liste = resultat.fetchall()
# for li in liste:
#     print(li)

# Pour questions_posees :
# resultat = cur.execute("SELECT qp.ordre, mq.title FROM questions_posees qp "
#                        "JOIN matching_questions mq ON mq.id = qp.MQid")
# liste = resultat.fetchall()
# for li in liste:
#     print(li)

# Pour users :
# resultat = cur.execute("SELECT * FROM users")
# liste = resultat.fetchall()
# for li in liste:
#     print(li)

# Pour answers_qcm :
# resultat = cur.execute("SELECT * FROM answers_qcm")
# liste = resultat.fetchall()
# for li in liste:
#     print(li)

# Pour matching_answers_qcm :
# resultat = cur.execute("SELECT * FROM matching_answers_qcm")
# liste = resultat.fetchall()
# for li in liste:
#     print(li)

# Pour answers_free :
# resultat = cur.execute("SELECT * FROM answers_free")
# liste = resultat.fetchall()
# for li in liste:
#     print(li)

# Pour answers_qcm :
# resultat = cur.execute("SELECT * FROM answers_qcm aq "
#                        "JOIN matching_answers_qcm ma ON aq.MAid = ma.id AND ma.MQid = aq.MQid LIMIT 32")
# liste = resultat.fetchall()
# for li in liste:
#     print(li)

# --- Sauvegarde et fermeture de la connexion et fin du programme
conn.commit()
conn.close()


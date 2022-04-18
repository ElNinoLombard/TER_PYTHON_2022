import sqlite3
import csv
import demoji

# Fonction utile pour matching_answers_qcm
def is_integer(n):
   try:
       float(n)
   except ValueError:
       return False
   else:
       return float(n).is_integer()

# --- Connection à la base de données
conn = sqlite3.connect('db_tables_v1')
print("La connexion avec la base de donnée est bien ouverte.")

# --- Création des tables
conn.execute("CREATE TABLE IF NOT EXISTS sondage(id INT, titre VARCHAR(50), PRIMARY KEY(id));")
conn.execute("CREATE TABLE IF NOT EXISTS matching_questions(id INT, type VARCHAR(10), theme VARCHAR(30), title VARCHAR(50), PRIMARY KEY(id));")
conn.execute("CREATE TABLE IF NOT EXISTS users(id INT, code_postal INT, commune VARCHAR(30), type_commune VARCHAR(20), nom_departement VARCHAR(30), departement INT, genre VARCHAR(20), tranche_age VARCHAR(15), formation VARCHAR(30), profession VARCHAR(30), taille_org VARCHAR(30), position_gj VARCHAR(30), PRIMARY KEY(id));")
conn.execute("CREATE TABLE IF NOT EXISTS questions_posees(Sid INT, MQid INT, ordre INT, FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(MQid) REFERENCES matching_questions(id), PRIMARY KEY(Sid, MQid));")
conn.execute("CREATE TABLE IF NOT EXISTS matching_answers_qcm(id INT, MQid INT, title TEXT, FOREIGN KEY(MQid) REFERENCES matching_questions(id), PRIMARY KEY(id, MQid));")
conn.execute("CREATE TABLE IF NOT EXISTS answers_qcm(Sid INT, Uid INT, MQid INT, MAid INT, FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(Uid) REFERENCES users(id), FOREIGN KEY(MQid) REFERENCES matching_questions(id), FOREIGN KEY(MAid) REFERENCES matching_answers_qcm(id), PRIMARY KEY(Sid, Uid, MQid, MAid));")
conn.execute("CREATE TABLE IF NOT EXISTS answers_free(Sid INT, Uid INT, MQid INT, answer TEXT, FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(Uid) REFERENCES users(id), FOREIGN KEY(MQid) REFERENCES matching_questions(id), PRIMARY KEY(Sid, Uid, MQid));")

# --- Remplissage des tables

#  Table sondage
id = 1
titre = "Entendre la France"
conn.execute('INSERT INTO sondage VALUES("{}", "{}")'.format(id, titre))

# Table matching_questions
chemin_fichier = "../Data_entendre_la_france/matching_questions.csv"

with open(chemin_fichier, "r", encoding="utf-8") as csvfile:
   fichier_lu = csv.reader(csvfile, delimiter=";")
   liste_lignes = []
   for row in fichier_lu:
       liste_lignes.append(row)
   # supprime la première ligne correspondant au titre
   liste_lignes.pop(0)

   correspondance_question_id = {}  # utile pour matching_answers_qcm
   for ind_ligne in range(0, len(liste_lignes)):
       id = ind_ligne+1
       correspondance_question_id[liste_lignes[ind_ligne][0]] = id  # sauvegarde de l'association id et id dans le doc
       type = liste_lignes[ind_ligne][1]
       theme = liste_lignes[ind_ligne][2]
       title = liste_lignes[ind_ligne][3]
       conn.execute('INSERT INTO matching_questions VALUES("{}", "{}", "{}", "{}")'.format(id, type, theme, title))

# Table questions_posees
Sid = 1
resultat = conn.execute("SELECT id FROM matching_questions")
liste = resultat.fetchall()
compteur = 0
for li in liste:
   compteur += 1
   conn.execute('INSERT INTO questions_posees VALUES("{}", "{}", "{}")'.format(1, li[0], compteur))

# Table users
chemin_fichier = "../Data_entendre_la_france/users.csv"

with open(chemin_fichier, 'r', encoding="utf-8") as csvfile:
   fichier_lu = csv.reader(csvfile, delimiter=";")
   liste_lignes = []
   for row in fichier_lu:
       liste_lignes.append(row)
   # supprime la première ligne correspondant au titre
   liste_lignes.pop(0)
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

# Table matching_answers_qcm
chemin_fichier = "../Data_entendre_la_france/matching_answers_qcm.csv"

with open(chemin_fichier, 'r', encoding="utf-8") as csvfile:
   fichier_lu = csv.reader(csvfile, delimiter=";")
   liste_lignes = []
   for row in fichier_lu:
       liste_lignes.append(row)
   # supprime la première ligne correspondant au titre
   liste_lignes.pop(0)

   id_max = 0
   for ind_ligne in range(0, len(liste_lignes)):
       MQid = correspondance_question_id[liste_lignes[ind_ligne][0]]
       title = liste_lignes[ind_ligne][2]

       # Conversion de l'emoji en id
       emoji_code = demoji.findall(liste_lignes[ind_ligne][1])

       for code_emo in emoji_code.values():
           if is_integer(code_emo.split(":")[-1]):
               id_max += 1
               id = int(code_emo.split(":")[-1])
           else:
               id = id_max+1
               id_max = 0
       conn.execute('INSERT INTO matching_answers_qcm VALUES("{}", "{}", "{}")'.format(id, MQid, title))


# --- Les tests

# -- Test création table

# Pour sondage :
# resultat = conn.execute("SELECT * FROM sondage")
# liste = resultat.fetchall()
# for li in liste:
#     print(li)

# Pour matching_questions :
# resultat = conn.execute("SELECT * FROM matching_questions")
# liste = resultat.fetchall()
# for li in liste:
#     print(li)

# Pour questions_posees :
# resultat = conn.execute("SELECT qp.ordre, mq.title FROM questions_posees qp JOIN matching_questions mq ON mq.id = qp.MQid")
# liste = resultat.fetchall()
# for li in liste:
#     print(li)

# Pour users :
# resultat = conn.execute("SELECT * FROM users")
# liste = resultat.fetchall()
# for li in liste:
#     print(li)

# Pour answers_qcm :
# resultat = conn.execute("SELECT * FROM answers_qcm")
# liste = resultat.fetchall()
# for li in liste:
#     print(li)

# Pour matching_answers_qcm :
# resultat = conn.execute("SELECT * FROM matching_answers_qcm")
# liste = resultat.fetchall()
# for li in liste:
#     print(li)

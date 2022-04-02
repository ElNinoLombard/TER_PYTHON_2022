# IMPORTATION DES DONNÉES ET CREATION DU TABLEAU
import sqlite3

conn = sqlite3.connect('db_tables_v1')
print("La connexion avec la base de donnée est bien ouverte.")

conn.execute("CREATE TABLE sondage(id INT, titre VARCHAR(50), PRIMARY KEY(id));")

conn.execute("CREATE TABLE matching_questions(id INT, type VARCHAR(10), theme VARCHAR(30), title VARCHAR(50), PRIMARY KEY(id));")

conn.execute("CREATE TABLE users(id INT, code_postal INT, commune VARCHAR(30), type_commune VARCHAR(20), nom_departement VARCHAR(30), departement INT, genre VARCHAR(20), tranche_age VARCHAR(15), formation VARCHAR(30), profession VARCHAR(30), taille_org VARCHAR(30), position_gj VARCHAR(30), PRIMARY KEY(id));")

conn.execute("CREATE TABLE questions_posees(Sid INT, MQid INT, ordre INT, FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(MQid) REFERENCES matching_questions(id), PRIMARY KEY(Sid, MQid));")

conn.execute("CREATE TABLE matching_answers_qcm(id INT, MQid INT, title TEXT, FOREIGN KEY(MQid) REFERENCES matching_questions(id), PRIMARY KEY(id, MQid));")

conn.execute("CREATE TABLE answers_qcm(Sid INT, Uid INT, MQid INT, MAid INT, FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(Uid) REFERENCES users(id), FOREIGN KEY(MQid) REFERENCES matching_questions(id), FOREIGN KEY(MAid) REFERENCES matching_answers_qcm(id), PRIMARY KEY(Sid, Uid, MQid, MAid));")

conn.execute("CREATE TABLE answers_free(Sid INT, Uid INT, MQid INT, answer TEXT, FOREIGN KEY(Sid) REFERENCES sondage(id), FOREIGN KEY(Uid) REFERENCES users(id), FOREIGN KEY(MQid) REFERENCES matching_questions(id), PRIMARY KEY(Sid, Uid, MQid));")
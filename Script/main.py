# --- Les imports
import sqlite3

# --- Ouverture connexion à la BDD
conn = sqlite3.connect('db_tables_v1')
cur = conn.cursor()


# --- Les classes
class AnswerQCM:
   def __init__(self, question_brute, num_uti):
       self.Sid = question_brute[0]
       self.Uid = num_uti
       self.MQid = question_brute[2]
       self.MAid = None
       self.ordre = question_brute[3]
       self.type = question_brute[4]
       self.theme = question_brute[5]
       self.title = question_brute[6]
       self.propositions = self.lister_propositions()

   # Retourne une liste des propositions associées à la question
   def lister_propositions(self):
       resultat = cur.execute(
           "SELECT ma.id, ma.title FROM matching_answers_qcm ma WHERE ma.MQid = {}".format(self.MQid))
       propositions = resultat.fetchall()
       return propositions

   # Pose la question dans la console et stocke la réponse dans MAid - Return False si retour
   def poser_question(self):
       if self.type == "QCM":
           complement = "Plusieurs réponses possibles (exemple : \"1/3/4\")"
       else:
           complement = "Une seule réponse possible (exemple : \"2\")"

       print("\n\nQuestion {} - Theme {} : {}\n"
             "{}\n".format(self.ordre, self.theme, complement, self.title))
       print("0 - Retour à la question précédente")
       for proposition in self.propositions:
           print("{} - {}".format(proposition[0], proposition[1]))
       print("")
       reponse = self.attendre_reponse()

       # Réponse incorrecte -> -1 | Retour -> 0 | Réponse correcte -> la réponse
       if reponse == -1:
           return -1

       elif reponse == 0:
           return 0

       else:
           self.MAid = reponse
           return 1

   # Renvoie False si la réponse donnée ne correspond pas au format attendu
   def attendre_reponse(self):
       reponse_brute = input()
       if reponse_brute == "0":
           return 0

       elif self.type == "QCM":
           reponse_separee = reponse_brute.split("/")
           liste_reponses = []
           for reponse_courante in reponse_separee:
               try:
                   reponse_courante = int(reponse_courante)
                   if reponse_courante <= 0 or reponse_courante > self.propositions[-1][0]:
                       print("Une des réponses choisies ne correspond à aucune proposition. Veuillez réessayer.")
                       return -1
                   else:
                       liste_reponses.append(reponse_courante)
               except ValueError:
                   print("Le format de la réponse est incorrect. Veuillez réessayer.")
                   return -1

           print("Vous avez choisi la ou les réponses : {}".format(liste_reponses))
           return liste_reponses

       else:
           try:
               reponse = int(reponse_brute)
               if reponse <= 0 or reponse > self.propositions[-1][0]:
                   print("Le numéro choisi ne correspond à aucune proposition. Veuillez réessayer.")
                   return -1
               else:
                   print("Vous avez choisi la réponse : {}".format(reponse))
                   return reponse

           except ValueError:
               print("Le format de la réponse est incorrect. Veuillez réessayer.")
               return -1

   def exporter_reponse(self):
       return [self.type, self.Sid, self.Uid, self.MQid, self.MAid]


class AnswerFREE:
   def __init__(self, question_brute, num_uti):
       self.Sid = question_brute[0]
       self.Uid = num_uti
       self.MQid = question_brute[2]
       self.answer = 0
       self.ordre = question_brute[3]
       self.type = question_brute[4]
       self.theme = question_brute[5]
       self.title = question_brute[6]

   # Pose la question dans la console et stocke la réponse dans answer - Return False si retour
   def poser_question(self):
       print("\n\nRépondez \"0\" pour revenir à la question précédente.")
       print("Question {} - Theme {} : Réponse libre (pas de format attendu)\n"
             "{}\n".format(self.ordre, self.theme, self.title))
       reponse = input()

       if reponse.lower() == "0":
           return False

       else:
           print("Vous avez entré la réponse : \"{}\".".format(reponse))
           self.answer = reponse
           return True

   def exporter_reponse(self):
       return self.type, self.Sid, self.Uid, self.MQid, self.answer


# --- Les fonctions

# Demande à la personne utilisatrice de saisir son numéro client composé de 5 chiffres
def saisir_id_client():
   print("Veuillez rentrer votre identifiant de connection (il doit être composé de 5 chiffres) :")
   id_client = 0
   while id_client < 10000:

       id_client = input()

       try:
           id_client = int(id_client)
           if id_client < 10000 or id_client >= 100000:
               print("Votre numéro client doit être composé de 5 chiffres.")
       except ValueError:
           print("Votre numéro client doit être uniquement composé de chiffres.")
           id_client = 0

   return id_client


# Retourne vrai si le numéro client existe dans la base "users"
def verif_id_client(num):
   resultat = cur.execute("SELECT id FROM users")
   liste_fetch = resultat.fetchall()
   liste_num = []
   for elm in liste_fetch:
       liste_num.append(elm[0])
   return num in liste_num


# Retourne les informations de la personne dont le numéro client est celui de la BDD
def recuperer_info_client(num):
   resultat = cur.execute("SELECT * FROM users WHERE id={}".format(num))
   liste = resultat.fetchall()
   return liste[0]


# Retourne une liste des sondages avec leurs titres
def lister_sondages():
   resultat = cur.execute("SELECT * FROM sondage")
   liste = resultat.fetchall()
   return liste


# Retourne une liste des sondages qui ont déjà été faits
def lister_sondages_faits(num_client):
   resultat = cur.execute(
       "SELECT DISTINCT s.id, s.titre FROM sondage s JOIN answers_qcm aq ON aq.Sid = s.id WHERE aq.Uid = {}".format(
           num_client))
   return resultat.fetchall()


# Retourne une liste des sondages qui n'ont pas été faits
def lister_sondages_non_faits(num_client):
   liste_sondages = lister_sondages()
   liste_sondages_faits = lister_sondages_faits(num_client)
   liste_indices_faits = []
   for sondage_fait in liste_sondages_faits:
       liste_indices_faits.append(sondage_fait[0])

   liste_sondages_non_faits = []
   for sondage in liste_sondages:
       if not sondage[0] in liste_indices_faits:
           liste_sondages_non_faits.append(sondage)
   return liste_sondages_non_faits


def choix_numero():
   choix = ""
   while choix.__class__ != int:
       choix = input()
       try:
           choix = int(choix)
       except ValueError:
           print("Veuillez choisir un numéro.")
   return choix


# Permet de choisir et retourne un numéro client
def connexion():
   id_client = saisir_id_client()
   while not verif_id_client(id_client):
       print("Le code client n'existe pas.")
       id_client = saisir_id_client()
   return recuperer_info_client(id_client)


# Permet de choisir un sondage et retourne l'id du sondage choisi
def choix_sondage(info_client):
   print("\n\nListe des sondages effectués :")
   for sondage in lister_sondages_faits(info_client[0]):
       print("{} - {}".format(sondage[0], sondage[1]))
   print("\nListe des sondages non effectués :")
   if len(lister_sondages_non_faits(info_client[0])) == 0:
       print("Aucun sondage n'a pas été effectué. Vous ne pouvez donc plus répondre.")
       return -1
   else:
       for sondage in lister_sondages_non_faits(info_client[0]):
           print("{} - {}".format(sondage[0], sondage[1]))
       # Choix du sondage par la personne utilisatrice
       liste_sondage = lister_sondages_non_faits(info_client[0])
       print("\nVeuillez choisir un numéro de sondage parmi ceux jamais effectués :")
       numero_sondage = choix_numero()
       liste_dict_sondages = {}
       for sondage in liste_sondage:
           liste_dict_sondages[sondage[0]] = sondage[1]
       while numero_sondage not in liste_dict_sondages.keys():
           print("Le numéro ne correspond à aucun sondage. Voici un rappel des sondages existants :")
           for sondage in lister_sondages_non_faits(info_client[0]):
               print("{} - {}".format(sondage[0], sondage[1]))
           numero_sondage = choix_numero()
       print("Vous avez choisis le sondage {} : {}".format(numero_sondage, liste_dict_sondages[numero_sondage]))
   return numero_sondage


# Affiche une présentation du sondage choisi et retourne une liste brute des questions du sondage
def presenter_sondage(numero):
   resultat = cur.execute(
       "SELECT so.id, so.titre, mq.id, qp.ordre, mq.type, mq.theme, mq.title "
       "FROM sondage AS so JOIN questions_posees AS qp ON qp.Sid = so.id "
       "                   JOIN matching_questions AS mq ON mq.id = qp.MQid "
       "WHERE so.id = {}".format(numero))
   liste_questions = resultat.fetchall()

   liste_themes = []
   for question in liste_questions:
       if question[5] not in liste_themes:
           liste_themes.append(question[5])

   print(
       "\n\nLe sondage {} est composé de {} questions et de {} themes.".format(liste_questions[0][0],
                                                                               len(liste_questions),
                                                                               len(liste_themes)))
   print("Les themes sont les suivants :")
   for theme in liste_themes:
       print("- {}".format(theme))
   print(
       '\nVous allez être redirigé.e pour répondre au sondage... '
       'Marquez "retour" pour revenir au choix du sondage. \n')
   return liste_questions


# Construit une liste composée de la liste des objets questions qui seront posées
def construction_questions(liste_questions_brutes, num_utilisateur):
   liste_questions = [None] * len(liste_questions_brutes)
   for question_brute in liste_questions_brutes:
       if question_brute[4] == 'QCU' or question_brute[4] == 'QCM':
           question_posee = AnswerQCM(question_brute, num_utilisateur)
           liste_questions[question_brute[3] - 1] = question_posee
       else:
           liste_questions[question_brute[3] - 1] = AnswerFREE(question_brute, num_utilisateur)
   return liste_questions


# Pose la liste de question en entrée et renvoie cette même liste avec les réponses choisies
def poser_questions(liste_questions):
   indice = 0
   while indice < len(liste_questions):
       retour_question = liste_questions[indice].poser_question()
       if retour_question == 1:
           indice += 1
       elif retour_question == 0:
           if indice == 0:
               print("Impossible de revenir à la réponse précédente.")
           else:
               indice -= 1

   print("Vous avez fini de répondre au questionnaire, merci de votre participation. Les réponses vont être "
         "enregistrées et le programme prendra fin.")
   return liste_questions


# Sauvegarde les reponses données à la liste de questions
def sauvegarder_reponses(liste_reponses):
   for reponse in liste_reponses:
       reponse_texte_eportation = reponse.exporter_reponse()
       if reponse_texte_eportation[0] == "QCM":
           for answer_id in reponse_texte_eportation[4]:
               cur.execute('INSERT INTO answers_qcm VALUES("{}", "{}", "{}", "{}")'.format(reponse_texte_eportation[1],
                                                                                           reponse_texte_eportation[2],
                                                                                           reponse_texte_eportation[3],
                                                                                           answer_id))

       elif reponse_texte_eportation[0] == "QCU":
           cur.execute(
               'INSERT INTO answers_qcm VALUES("{}", "{}", "{}", "{}")'.format(reponse_texte_eportation[1],
                                                                               reponse_texte_eportation[2],
                                                                               reponse_texte_eportation[3],
                                                                               reponse_texte_eportation[4]))

       else:
           cur.execute(
               'INSERT INTO answers_free VALUES("{}", "{}", "{}", "{}")'.format(reponse_texte_eportation[1],
                                                                                reponse_texte_eportation[2],
                                                                                reponse_texte_eportation[3],
                                                                                reponse_texte_eportation[4].replace(
                                                                                    "\"", "'")))


# Affiche les réponses d'un certain utilisateur à un certain sondage
def affichage_reponses(num_utilisateur, num_sondage):
   print("Voici un affiche des réponses de l'utilisateur {} au sondage {} :".format(num_utilisateur, num_sondage))

   resultat = cur.execute("SELECT qp.ordre, mq.title, ma.title "
                          "FROM sondage so JOIN questions_posees qp ON so.id = qp.Sid"
                          "                JOIN matching_questions mq ON qp.MQid = mq.id"
                          "                JOIN matching_answers_qcm ma ON ma.MQid = mq.id"
                          "                JOIN answers_qcm aq ON aq.MQid = mq.id AND aq.MAid = ma.id "
                          "WHERE aq.Uid = {} AND so.id = {} ".format(num_utilisateur, num_sondage))
   liste_reponses_qcm = resultat.fetchall()

   resultat = cur.execute("SELECT qp.ordre, mq.title, af.answer "
                          "FROM sondage so JOIN questions_posees qp ON so.id = qp.Sid"
                          "                JOIN matching_questions mq ON qp.MQid = mq.id"
                          "                JOIN answers_free af ON af.MQid = mq.id  "
                          "WHERE af.Uid = {} AND so.id = {} ".format(num_utilisateur, num_sondage))
   liste_reponses_libres = resultat.fetchall()

   liste_reponses = []

   for reponse in liste_reponses_qcm:
       liste_reponses.append(reponse)
   for reponse in liste_reponses_libres:
       liste_reponses.append(reponse)
   print(liste_reponses)


def main():
   info_client = connexion()
   numero_choisi = choix_sondage(info_client)
   if numero_choisi != -1:
       liste_questions_brutes = presenter_sondage(numero_choisi)
       while input().lower() == "retour":
           numero_choisi = choix_sondage(info_client)
           liste_questions_brutes = presenter_sondage(numero_choisi)
       liste_questions_posees = construction_questions(liste_questions_brutes, info_client[0])
       liste_reponses = poser_questions(liste_questions_posees)
       sauvegarder_reponses(liste_reponses)
       affichage_reponses(info_client[0], numero_choisi)


# --- Les tests
# -- Une liste de codes utilisateurs afin de tester :

# N'ont répondu qu'au premier sondage :
# 17469 - 17767 - 17816 - 17941 - 17942 - 17943 - 17947 - 17948 - 17951 - 17952 - 17953

# N'ont répondu à aucun sondage :
# 50000 - 50001 - 50002 - 50003 - 50004 - 50005 - 50006 - 50007 - 50008 - 50009 - 50010

# Pour lancer le programme :
main()

# Pour afficher les réponses d'un utilisateur :
# num_utilisateur_test = 17767
# num_sondage_test = 1
# affichage_reponses(num_utilisateur_test, num_sondage_test)

# Fin du programme
conn.commit()
conn.close()

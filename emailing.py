import smtplib
from email.message import EmailMessage
import os
import csv
from time import sleep



# Fonction pour créer l'objet Email avec le contenu HTML et les pièces jointes
# !! Ici, piece_jointe est une liste contenant toutes les pièces jointes à ajouter
def creer_email(sender_email_adress, reicever_email_adress=None, email_brut="", email_html=None, subject=None, piece_jointe=None):
    
  email=EmailMessage()
  email['From'] = sender_email_adress
  email['To']= reicever_email_adress
  email['Subject'] = subject
      
  #contenu de l'email
  email.set_content(email_brut)
  email.add_alternative(email_html, subtype='html')

  #Insertion pièce jointe du CV
  if piece_jointe is not None:
    for i in range(len(piece_jointe)):
        if piece_jointe[i] is not None:
            with open(piece_jointe[i], 'rb') as f:
                email.add_attachment(f.read(),
                maintype='application',
                subtype='pdf',
                filename=os.path.basename(piece_jointe[i]))
  
  return email

# Fonction pour extraire une liste d'emails depuis un fichier csv contenant une colonne "Email"
def add_receiver_from_csv(receivers_emails_adresses, csv_file):

  # Lecture du fichier CSV
  with open(csv_file, mode='r', encoding='utf-8') as f:
      lecteur = csv.DictReader(f)
      
      # Retrouver la bonne colonne "Email" du CSV
      nom_column_email = None
      for nom in lecteur.fieldnames:
          if nom.lower() in ["email", "email address", "emails", "e-mail", "e-mails"]:
              nom_column_email = nom
              break

      for ligne in lecteur:
          email = ligne.get(nom_column_email)
          if email:  # Ignorer les valeurs vides
              receivers_emails_adresses.append(email)

# Fonction pour envoyer un email
def send_email(sender_email_adress, application_password, email) : 
   with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
      smtp.login(sender_email_adress, application_password)
      smtp.send_message(email)

# Fonction pour envoyer un email à plusieurs destinataires individuellement
def send_multi_emails(liste_emails_adresses, email, sender_email_adress, application_password):
    for email_adress in liste_emails_adresses:
        del email['To']
        email['To'] = email_adress
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email_adress, application_password)
            smtp.send_message(email)
            print(f"Email envoyé à {email_adress} avec succès")
            sleep(0.8) 



"""    MAIN    """


# informations de l'expéditeur

sender_email_adress ="example@email.com"
application_password = "abcd efgh ijkl mnop" # Mot de passe de l'application, à générer dans les paramètres de sécurité du compte Google


#liste des destinataires à mettre en cc
receivers_emails = []
add_receiver_from_csv(receivers_emails, "exemple.csv") 

# Modèle de l'email brut et avec mise en forme HTML

email_brut = """\
  Lorem ipsum,

  dolor sit amet, consectetur adipiscing elit.
  Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

  Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
  Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
  Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

  Cordialement,
  L'expéditeur
  """
email_html = """\
  <html>   
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
      <p><strong>Lorem ipsum</strong>,</p>

      <p><u>Dolor</u> sit amet, <strong>consectetur</strong> adipiscing elit.<br>
      Sed do <strong>eiusmod tempor</strong> incididunt ut labore et dolore magna aliqua.</p>

      <p>Ut enim ad minim veniam, quis <strong>nostrud exercitation</strong> ullamco laboris nisi ut aliquip ex ea commodo consequat.<br>
      <strong>Duis aute irure dolor</strong> in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.</p>

      <p><strong>Excepteur sint occaecat</strong> cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>

      <p>Cordialement,<br>
      <strong>L'expéditeur</strong></p>

    </body>
  </html>
  """

send_multi_emails(liste_emails_adresses=receivers_emails, 
                  email=creer_email(sender_email_adress, email_brut=email_brut, email_html=email_html, subject="Test Email", piece_jointe=None),
                  sender_email_adress=sender_email_adress, 
                  application_password=application_password)


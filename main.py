import json

from bottle import route, run, template, post, request, get
import sqlite3

# setup database
db = sqlite3.connect('iso21827.db')
c = db.cursor()

c.execute('DROP TABLE IF EXISTS question')
c.execute('''CREATE TABLE question (
    IdQuestion int,
    IdNiveau int,
    Question text,
    Valeur int
)''')
c.execute(''' INSERT INTO question VALUES
(1,1,"Adhérence au système d'information : Comment jugez-vous l'importance de votre système d'information dans l'accomplissement de vos missions ?",0),
(2,1,"Niveau des impacts internes : Quelles sont les conséquences internes (perturbations du fonctionnement, impacts financiers, impacts juridiques…) d'un sinistre touchant la sécurité de votre système d’information (ex : déni de service, perte d’informations, attaque virale…) ?",0),
(3,1,"Niveau des impacts externes : Quelles sont les conséquences externes (image, sécurité de l'environnement, relations contractuelles, sécurité des personnes…) d'un sinistre touchant la sécurité de votre système d’information ?",0),
(4,2,"Besoins de disponibilité (propriété d'accessibilité au moment voulu par des personnes autorisées) : Dans quelle mesure la disponibilité du(des) système(s) informatique(s) est-elle importante ?",0),
(5,2,"Besoins d'intégrité (propriété d'exactitude et de complétude) : Dans quelle mesure l'intégrité des données manipulées ou manipulables dans le cadre de l'activité est-elle importante ?",0),
(6,2,"Besoins de confidentialité (propriété de n'être accessible qu'aux personnes autorisées) : Dans quelle mesure la confidentialité des informations exploitées ou exploitables dans le cadre de l'activité est-elle importante ?",0),
(7,3,"Fréquence des sinistres SSI : Quelle est la fréquence estimée des sinistres SSI dans l’organisme ?",0),
(8,3,"Degré de motivation des attaquants : Quel est le degré de motivation des attaquants potentiels ?",0),
(9,3,"Moyens des attaquants : Quels sont les compétences et les ressources des attaquants potentiels ?",0),
(10,4,"Hétérogénéité du système d'information : Quel est le niveau d’hétérogénéité du système d’information ?",0),
(11,4,"Ouverture du système d'information : Quel est le degré d’ouverture du système d’information ?",0),
(12,4,"Variabilité du système d'information : Quel est le niveau de variabilité des composants du système d'information (matériels, logiciels, réseaux, organisations, locaux, personnel…) et du contexte dans lequel il opère (contraintes, exigences réglementaires, menaces…) ?",0)
''')

c.execute('DROP TABLE IF EXISTS reponse')
c.execute('''CREATE TABLE reponse (
    IdQuestion int,
    IdReponse int,
    Reponse text,
    Valeur int
)''')
c.execute(''' INSERT INTO reponse VALUES
(1,0,"Le système d’information est accessoire à l'accomplissement des missions",3),
(1,1,"Le système d’information est utile à l'accomplissement des missions",1),
(1,2,"Le système d’information est nécessaire à l'accomplissement des missions",2),
(1,3,"Le système d’information est vital à l'accomplissement des missions",3),
(2,0,"Les conséquences internes d’un sinistre SSI ne peuvent qu'être négligeables",1),
(2,1,"Les conséquences internes d’un sinistre SSI peuvent être significatives",1),
(2,2,"Les conséquences internes d’un sinistre SSI peuvent être graves",2),
(2,3,"Les conséquences internes d’un sinistre SSI peuvent être fatales",3),
(3,0,"Les conséquences externes d’un sinistre SSI ne peuvent qu'être négligeables",0),
(3,1,"Les conséquences externes d’un sinistre SSI peuvent être significatives",1),
(3,2,"Les conséquences externes d’un sinistre SSI peuvent être graves",2),
(3,3,"Les conséquences externes d’un sinistre SSI peuvent être catastrophiques",3),
(4,0,"L'inaccessibilité du(des) système(s) informatique(s) ne gêne quasiment pas l'activité",0),
(4,1,"L'inaccessibilité du(des) système(s) informatique(s) perturbe l'activité de manière significative",1),
(4,2,"L'inaccessibilité du(des) système(s) informatique(s) est jugée comme grave pour l'activité",2),
(4,3,"L'inaccessibilité du(des) système(s) informatique(s) peut être fatale pour l'activité",3),
(5,0,"L'altération des données ne gêne quasiment pas l'activité",0),
(5,1,"L'altération des données perturbe l'activité de manière significative",1),
(5,2,"L'altération des données est jugée comme grave pour l'activité",2),
(5,3,"L'altération des données peut être fatale pour l'activité",3),
(6,0,"La compromission d’informations ne gêne quasiment pas l'activité",0),
(6,1,"La compromission d’informations perturbe l'activité de manière significative",1),
(6,2,"La compromission d’informations est jugée comme grave pour l'activité",2),
(6,3,"La compromission d’informations peut être fatale pour l'activité",3),
(7,0,"Les sinistres SSI (vécus ou imaginables) sont rarissimes (moins d'une fois par an)",0),
(7,1,"Plusieurs sinistres SSI dans l'année",1),
(7,2,"Plusieurs sinistres SSI par trimestre",2),
(7,3,"Plusieurs sinistres SSI par mois",3),
(8,0,"Une attaque SSI ciblée sur le périmètre est relativement inimaginable",0),
(8,1,"La motivation des attaquants potentiels est jugée faible",1),
(8,2,"La motivation des attaquants potentiels peut être forte",2),
(8,3,"La motivation des attaquants potentiels peut être très importante",3),
(9,0,"Les attaquants potentiels ne disposent que de faibles moyens",0),
(9,1,"Les attaquants peuvent disposer de moyens significatifs",1),
(9,2,"Les attaquants peuvent disposer de moyens importants",2),
(9,3,"Les attaquants peuvent disposer de moyens potentiellement illimités",3),
(10,0,"Le système d’information est jugé comme homogène",0),
(10,1,"Le système d’information est jugé comme faiblement hétérogène",1),
(10,2,"Le système d’information est jugé comme fortement hétérogène",2),
(10,3,"Le système d’information est jugé comme extrêmement hétérogène",3),
(11,0,"Le système d’information n’est pas ouvert",0),
(11,1,"Le système d’information n'est ouvert qu'à des systèmes internes",1),
(11,2,"Le système d’information est ouvert à des systèmes externes mais sous contrôle",2),
(11,3,"Le système d’information est ouvert à des systèmes externes hors de contrôle",3),
(12,0,"Le système d’information et son contexte sont jugés stables",0),
(12,1,"Le système d’information et son contexte changent peu",1),
(12,2,"Le système d’information et son contexte changent relativement souvent",2),
(12,3,"Le système d’information et son contexte change très souvent",3)
''')
c.execute('DROP TABLE IF EXISTS maturite')
c.execute('''CREATE TABLE maturite (
    IdMaturite int,
    InferieurA int,
    SuperieurA int,
    Maturite text
)''')
c.execute('''INSERT INTO maturite (IdMaturite,InferieurA,SuperieurA,Maturite) VALUES
('1','0','2','Pratique informelle'),
('2','3','5','Pratique répétable et suivie'),
('3','6','8','Processus définis'),
('4','9','10','Processus contrôlés'),
('5','11','12','Processus continuellement optimisés')''')
c.execute('DROP TABLE IF EXISTS niveau')
c.execute('''CREATE TABLE niveau (
    IdNiveau int,
    NIveau text,
    MaxNiveau int
)''')
c.execute('''INSERT INTO niveau ('IdNiveau','NIveau','MaxNiveau') VALUES
('1',"Trois questions pour estimer le niveau des conséquences potentielles",'0'),
('2',"Trois questions pour estimer la sensibilité du patrimoine informationnel",'0'),
('3',"Trois questions pour estimer le degré d'exposition aux menaces",'0'),
('4',"Trois questions pour estimer l'importance des vulnérabilités",'0')
''')
db.commit()
db.close

@route('/iso21827/question/<numero:int>')
def question(numero):
    db = sqlite3.connect('iso21827.db')
    c = db.cursor()
    c.execute('SELECT question FROM question WHERE IdQuestion = ?', (numero,))
    return json.dumps(c.fetchone())

# @route('/iso21827/Q/<numero:int>')
# def question(numero):
#     db = sqlite3.connect('iso21827.db')
#     c = db.cursor()
#
#     # Recupere la question dans la base de données
#     c.execute('SELECT question FROM question WHERE IdQuestion = ?', (numero,))
#     questiontext = c.fetchone()[0]
#
#     # Recupere les propositions dans la base de données
#     c.execute('SELECT reponse FROM reponse WHERE IdQuestion = ?', (numero,))
#     [ch1, ch2, ch3, ch4] = [row[0] for row in c.fetchall()];
#
#     db.close()
#
#     return template('''
#         Question : <i>{{question}}</i>
#         <form method="POST" action="../R/{{numero}}">
#         <ol>
#             <li><label><input type="radio" name="choice" value="1"/>{{ch1}}</label></li>
#             <li><label><input type="radio" name="choice" value="2"/>{{ch2}}</label></li>
#             <li><label><input type="radio" name="choice" value="3"/>{{ch3}}</label></li>
#             <li><label><input type="radio" name="choice" value="4"/>{{ch4}}</label></li>
#         </ol>
#         <input type="submit"/>
#         </form>
#         ''', question=questiontext, numero=numero, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4)
#
#
# @post('/iso21827/R/<numero:int>')
# def response(numero):
#     choice = request.forms.get('choice')
#
#     # Update la question selectionnée dans la base de données
#     db = sqlite3.connect('iso21827.db')
#     c = db.cursor()
#     c.execute('UPDATE question SET valeur=? WHERE IdQuestion = ?', (choice, numero,))
#     db.commit()
#     db.close()
#     return template(''' Successfully answered question {{number}} with choice {{ch}}''',number=numero, ch=choice)
#
#
# @get('/iso21827/R/<numero:int>')
# def response(numero):
#
#     # recupere la reponse a la question selectionnée depuis la base de données
#     db = sqlite3.connect('iso21827.db')
#     c = db.cursor()
#     c.execute('SELECT valeur FROM  question WHERE IdQuestion = ?', (numero,))
#     choice = c.fetchone()[0];
#     db.close()
#     return template(''' Question {{number}} was answered whith choice {{ch}}''',number=numero, ch=choice)
#
#
#
#
# @get('/iso21827/M')
# def response():
#
#     # recupere la reponse a la question selectionnée depuis la base de données
#     db = sqlite3.connect('iso21827.db')
#     c = db.cursor()
#     c.execute('''
#         SELECT SUM(valeur) AS score,"" AS result_text
#         FROM  question
#     ''')
#     [score,text] = c.fetchone();
#     db.close()
#     return template(''' Your score is {{score}} : {{text}}''',score=score, text=text)
#



run(host='localhost', port=8080)

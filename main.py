from logging import info
import sys
from typing import Tuple

import mysql.connector
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

mybd = mysql.connector.connect(
    host="localhost",
    user="JoeDever",
    password="GaryChalk",
    database="vous_etes_le_heros"
)

mon_curseur = mybd.cursor(prepared = True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.id_partie = None
        self.chapitre = None
        # print(self.combo_box.itemData(self.combo_box.currentIndex()))
    
    def initUI(self):
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("Dont Vous Êtes le Héros")
        self.setFixedSize(640, 480)
        connexion_tab = self.connexionTabUI()
        creer_tab = self.creerPartieTabUI()
        wid = QWidget(self)
        self.setCentralWidget(wid)
        layout = QVBoxLayout()
        wid.setLayout(layout)
        self.tabs = QTabWidget()
        self.tabs.addTab(connexion_tab, "Connexion")
        self.tabs.addTab(creer_tab, 'Créer partie')
        layout.addWidget(self.tabs)

    def connexionTabUI(self) -> QWidget:
        connexion_tab = QWidget()
        layout = QVBoxLayout()
        self.combo_box = QComboBox()
        valeurs = self.requetePersonnage()
        for i in range(0, len(valeurs['titre'])):
            self.combo_box.addItem(valeurs['titre'][i], valeurs['id'][i])
        bouton_selection_partie = QPushButton("Sélectionner cette partie")
        bouton_selection_partie.clicked.connect(self.soumissionSelectionPartie)
        layout.addWidget(self.combo_box)
        layout.addWidget(bouton_selection_partie)
        connexion_tab.setLayout(layout)
        return connexion_tab
    
    def creerPartieTabUI(self) -> QWidget:
        creer_tab = QWidget()
        layout = QVBoxLayout()

        layout_nom_partie = QHBoxLayout()
        label_nom_partie = QLabel()
        self.entre_nom_partie = QLineEdit()
        label_nom_partie.setText("Entrez le nom de la partie : ")
        layout_nom_partie.addWidget(label_nom_partie)
        layout_nom_partie.addWidget(self.entre_nom_partie)

        layout_choix_livre = QHBoxLayout()
        label_choix_livre = QLabel()
        self.combo_box_choix_livre = QComboBox()
        valeurs = self.requeteLivre()
        for i in range(0, len(valeurs['titre'])):
            self.combo_box_choix_livre.addItem(valeurs['titre'][i], valeurs['id'][i])
        label_choix_livre.setText("Choisissez le livre : ")
        layout_choix_livre.addWidget(label_choix_livre)
        layout_choix_livre.addWidget(self.combo_box_choix_livre)
        
        bouton_soummission_partie = QPushButton("Créer la partie")
        bouton_soummission_partie.clicked.connect(self.soumissionCreationPartie)

        layout.addLayout(layout_nom_partie)
        layout.addLayout(layout_choix_livre)
        layout.addWidget(bouton_soummission_partie)
        creer_tab.setLayout(layout)
        return creer_tab

    def pageTabUI(self) -> QWidget:
        page_tab = QWidget()
        outer_layout = QVBoxLayout()
        top_layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()
        label = QLabel(self.requeteTextePage(self.id_partie))
        label.setWordWrap(True)
        top_layout.addWidget(label)

        boutons = self.requeteChoix(self.chapitre)
        for bouton in boutons:
            bouton.clicked.connect(self.changementPage)
            bottom_layout.addWidget(bouton)
        
        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(bottom_layout)
        page_tab.setLayout(outer_layout)
        return page_tab

    def requeteLivre(self) -> dict[str, int]:
        mon_curseur.execute("SELECT titre, id FROM livre order by titre;")
        resultat = mon_curseur.fetchall()
        livres = {}
        titres = []
        ids = []
        for titre, id in resultat:
            titres.append(titre)
            ids.append(id)
        livres['titre'] = titres
        livres['id'] = ids
        return livres

    def personnageTabUI(self) -> QWidget:
        personnage_tab = QWidget()
        outer_layout = QVBoxLayout()
        outer_layout.addLayout(self.infoPersonnage())
        outer_layout.addLayout(self.inventairePersonnage())
        personnage_tab.setLayout(outer_layout)
        return personnage_tab
    
    def objetTabUI(self, text_bouton:str, ajout:bool = True) -> QWidget:
        objet_tab = QWidget()
        outer_layout = QVBoxLayout()
        self.choix_objet = QComboBox()
        objets = self.requeteObjets()
        for i in range(0, len(objets['nom'])):
            self.choix_objet.addItem(objets['nom'][i], objets['id'][i])
        bouton_action = QPushButton(text_bouton)
        if ajout:
            bouton_action.clicked.connect(self.ajouterObjetInventaire)
        else:
            bouton_action.clicked.connect(self.modifierObjetInventaire)
        outer_layout.addWidget(self.choix_objet, stretch=1)
        outer_layout.addWidget(bouton_action, stretch=1)
        objet_tab.setLayout(outer_layout)
        return objet_tab

    def ajouterObjetInventaire(self):
        data = (self.id_partie,)
        sql = 'SELECT id FROM personnage WHERE id_partie = %s;'
        mon_curseur.execute(sql, data)
        resultat = mon_curseur.fetchall()
        id_joueur:str
        for id in resultat:
            id_joueur = id[0]
        id_objet = self.choix_objet.itemData(self.choix_objet.currentIndex())
        data = (id_objet, id_joueur)
        sql = 'INSERT INTO objet_personnage(id_objet, id_personnage) VALUES(%s, %s);'
        mon_curseur.execute(sql, data)
        mybd.commit()
        self.tabs.removeTab(1)
        page_personnage = self.personnageTabUI()
        self.tabs.addTab(page_personnage, 'Personnage')
        self.tabs.setCurrentIndex(1)

    def modifierObjetInventaire(self):
        data = (self.choix_objet.itemData(self.choix_objet.currentIndex()), self.list_objets.itemData(self.list_objets.currentIndex()))
        sql = 'UPDATE objet_personnage SET id_objet = %s WHERE id = %s;'
        mon_curseur.execute(sql, data)
        mybd.commit()
        self.tabs.removeTab(1)
        page_personnage = self.personnageTabUI()
        self.tabs.addTab(page_personnage, 'Personnage')
        self.tabs.setCurrentIndex(1)
    
    def supprimerObjetInventaire(self):
        data = (self.list_objets.itemData(self.list_objets.currentIndex()),)
        sql = 'DELETE FROM objet_personnage WHERE id = %s;'
        mon_curseur.execute(sql, data)
        mybd.commit()
        self.tabs.removeTab(1)
        page_personnage = self.personnageTabUI()
        self.tabs.addTab(page_personnage, 'Personnage')
        self.tabs.setCurrentIndex(1)

    def inventairePersonnage(self) -> QVBoxLayout:
        outer_layout = QVBoxLayout()
        label_objet = QLabel("Objets:")
        outer_layout.addWidget(label_objet)
        layout_objet = QHBoxLayout()
        self.list_objets = QComboBox()
        bouton_ajouter = QPushButton('Ajouter')
        bouton_ajouter.clicked.connect(self.boutonAjouterObjet)
        bouton_modifier = QPushButton('Modifier')
        bouton_modifier.clicked.connect(self.boutonModifierObjet)
        bouton_supprimer = QPushButton('Supprimer')
        bouton_supprimer.clicked.connect(self.supprimerObjetInventaire)
        objets = self.requeteObjetsPersonnage()
        for i in range(0, len(objets['nom'])):
            self.list_objets.addItem(objets['nom'][i], objets['id'][i])
        layout_objet.addWidget(self.list_objets, stretch=2)
        if (self.list_objets.count() < 8):
            layout_objet.addWidget(bouton_ajouter, stretch=1)
        if (len(self.list_objets.currentText()) >= 1):
            layout_objet.addWidget(bouton_modifier, stretch=1)
            layout_objet.addWidget(bouton_supprimer, stretch=1)
        outer_layout.addLayout(layout_objet)
        return outer_layout

    def infoPersonnage(self) -> QVBoxLayout:
        layout_attributs = QHBoxLayout()
        attributs = self.requeteInfoPersonnage()
        text_endurance = QLineEdit(str(attributs['endurance']))
        text_endurance.textChanged.connect(self.modifierEndurance)
        text_habilete = QLineEdit(str(attributs['habilete']))
        text_or = QLineEdit(str(attributs['or']))
        layout_attributs.addWidget(QLabel("Endurance:"))
        layout_attributs.addWidget(text_endurance)
        layout_attributs.addWidget(QLabel("Habileté:"))
        layout_attributs.addWidget(text_habilete)
        layout_attributs.addWidget(QLabel("Or:"))
        layout_attributs.addWidget(text_or)
        return layout_attributs
    
    def modifierEndurance(self):
        endurance = str(self.sender().text())
        if (endurance.isdigit()):
            endurance = str(int(endurance))
        else:
            endurance = '0'
        self.sender().setText(endurance)

    def requetePersonnage(self) -> dict[str, int]:
        mon_curseur.execute("SELECT nom, titre, partie.id as id_livre FROM partie INNER JOIN livre ON id_livre = livre.id ORDER BY nom;")
        resultat = mon_curseur.fetchall()
        parties = {}
        titres = []
        ids = []
        for nom, titre, id_livre in resultat:
            titres.append(F"{nom} : {titre}")
            ids.append(id_livre)
        parties['titre'] = titres
        parties['id'] = ids
        return parties
    
    def requeteInfoPersonnage(self) -> dict:
        sql = "SELECT endurance, habilete, `or` as or_perso FROM personnage WHERE id_partie = %s;"
        data = (self.id_partie,)
        mon_curseur.execute(sql, data)
        resultat = mon_curseur.fetchall()
        infos = {}
        for endurance, habilete, or_perso in resultat:
            infos['endurance'] = endurance
            infos['habilete'] = habilete
            infos['or'] = or_perso
        return infos

    def requeteObjetsPersonnage(self) -> dict:
        data  = (self.id_partie,)
        sql = """SELECT CONCAT(nom, ' - ', type) as nom, objet_personnage.id as id_objet FROM personnage INNER JOIN objet_personnage ON id_personnage = personnage.id 
                INNER JOIN objet ON id_objet = objet.id WHERE id_partie = %s;"""
        mon_curseur.execute(sql, data)
        resultat = mon_curseur.fetchall()
        objets = {}
        nom_objet = []
        ids = []
        for nom, id_objet in resultat:
            nom_objet.append(nom)
            ids.append(id_objet)
        objets['nom'] = nom_objet
        objets['id'] = ids 
        return objets
    
    def requeteObjets(self) -> dict:
        sql = "SELECT CONCAT(nom, ' - ', type) as nom_objet, id FROM objet ORDER BY objet.nom;"
        mon_curseur.execute(sql)
        resultat = mon_curseur.fetchall()
        objets = {}
        nom_objet = []
        id_objet = []
        for nom, id in resultat:
            nom_objet.append(nom)
            id_objet.append(id)
        objets['nom'] = nom_objet
        objets['id'] = id_objet
        return objets

    def boutonAjouterObjet(self):
        page_ajout = self.objetTabUI('Ajouter Objet')
        self.tabs.removeTab(1)
        self.tabs.addTab(page_ajout, 'Ajout Objet')
        self.tabs.setCurrentIndex(1)
    
    def boutonModifierObjet(self):
        page_modif = self.objetTabUI('Modifier Objet', False)
        self.tabs.removeTab(1)
        self.tabs.addTab(page_modif, 'Modifier Objet')
        self.tabs.setCurrentIndex(1)

    def requeteTextePage(self, id_partie:int) -> str:
        data = (id_partie,)
        sql = "SELECT texte AS texte_chapitre, id_chapitre FROM partie INNER JOIN chapitre ON chapitre.id = id_chapitre WHERE partie.id = %s;"
        mon_curseur.execute(sql, data)
        resultats = mon_curseur.fetchall()
        texte = ""
        for texte_chapitre, id_chapitre in resultats:
            texte = texte_chapitre
            self.chapitre = id_chapitre
        return texte

    def requeteChoix(self, id_chapitre:int) -> QPushButton:
        data = (id_chapitre,)
        sql = "SELECT numero_chapitre_destination FROM choix_page WHERE id_chapitre = %s;"
        mon_curseur.execute(sql, data)
        resultats = mon_curseur.fetchall()
        boutons = []
        for numero_chapitre_destination in resultats:
            boutons.append(QPushButton(str(numero_chapitre_destination[0])))
        return boutons

    def soumissionCreationPartie(self):
        id_livre = self.combo_box_choix_livre.itemData(self.combo_box_choix_livre.currentIndex())
        nom = self.entre_nom_partie.text()
        data = (nom, id_livre, id_livre)
        sql = "INSERT INTO partie (`nom`, id_chapitre, id_livre) VALUES ( %s, premier_chapitre_id(%s), %s);"
        mon_curseur.execute(sql, data)
        mybd.commit()

        self.id_partie = mon_curseur.lastrowid
        page_tab = self.pageTabUI()
        self.tabs.addTab(page_tab, "Page")

        self.tabs.removeTab(0)
        self.tabs.removeTab(0)

    def soumissionSelectionPartie(self):
        self.id_partie = self.combo_box.itemData(self.combo_box.currentIndex())
        page_tab = self.pageTabUI()
        personnage_tab = self.personnageTabUI()
        self.tabs.addTab(page_tab, "Page")
        self.tabs.addTab(personnage_tab, "Personnage")
        self.tabs.removeTab(0)
        self.tabs.removeTab(0)
    
    def changementPage(self):
        destination = int(self.sender().text())
        data = (destination, self.id_partie)
        sql = "SELECT chapitre.id as id_chapitre FROM chapitre INNER JOIN livre l ON chapitre.id_livre = l.id INNER JOIN partie p ON l.id = p.id_livre WHERE numero_chapitre = %s AND p.id = %s;"
        mon_curseur.execute(sql, data)
        resultats = mon_curseur.fetchall()
        for id_chapitre in resultats:
            self.chapitre = id_chapitre[0]
        data = (self.chapitre, self.id_partie)
        sql = "UPDATE partie SET id_chapitre = %s WHERE id = %s;"
        mon_curseur.execute(sql, data)
        page_tab = self.pageTabUI()
        self.tabs.removeTab(0)
        self.tabs.insertTab(0, page_tab, "Page")
        self.tabs.setCurrentIndex(0)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec()
   mon_curseur.close()

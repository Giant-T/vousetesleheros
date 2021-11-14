import sys
from typing import Tuple
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import mysql.connector

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

    
    def requetePersonnage(self) -> dict[str, int]:
        mon_curseur.execute("SELECT nom, titre, partie.id as id_livre FROM partie INNER JOIN livre ON id_livre = livre.id order by nom;")
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

    def requeteTextePage(self, id:int) -> str:
        data = (id,)
        sql = "SELECT texte AS texte_chapitre, id_chapitre FROM partie INNER JOIN chapitre ON chapitre.id = id_chapitre WHERE partie.id = %s;"
        mon_curseur.execute(sql, data)
        resultats = mon_curseur.fetchall()
        texte = ""
        for texte_chapitre, id_chapitre in resultats:
            texte = texte_chapitre
            self.chapitre = id_chapitre
        return texte

    def requeteChoix(self, id:int) -> QPushButton:
        data = (id,)
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
        self.tabs.addTab(page_tab, "Page")

        self.tabs.removeTab(0)
        self.tabs.removeTab(0)
    
    def changementPage(self):
        destination = int(self.sender().text())
        data = (self.chapitre, destination)
        sql = "SELECT id as id_chapitre FROM chapitre WHERE id = %s AND numero_chapitre = %s;"
        mon_curseur.execute(sql, data)
        resultats = mon_curseur.fetchall()
        for id_chapitre in resultats:
            self.chapitre = id_chapitre[0]
        data = (destination, self.id_partie)
        sql = "UPDATE partie SET id_chapitre = %s WHERE id = %s;"
        mon_curseur.execute(sql, data)
        page_tab = self.pageTabUI()
        self.tabs.removeTab(0)
        self.tabs.insertTab(0, page_tab, "Page")

if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec()
   mon_curseur.close()

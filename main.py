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
        """
        Initialise le ui de base du programme
        """
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
        """
        Crée la page de connexion du jeu
        returns: la page de connexion
        """
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
        outer_layout.addLayout(self.disciplinesPersonnage())
        outer_layout.addLayout(self.armesPersonnage())
        outer_layout.addLayout(self.equipementsPersonnage())
        outer_layout.addLayout(self.inventairePersonnage())
        personnage_tab.setLayout(outer_layout)
        return personnage_tab
    
    def objetTabUI(self, text_bouton:str, ajout:bool = True) -> QWidget:
        objet_tab = QWidget()
        outer_layout = QVBoxLayout()
        self.choix_item = QComboBox()
        objets = self.requeteObjets()
        for i in range(0, len(objets['nom'])):
            self.choix_item.addItem(objets['nom'][i], objets['id'][i])
        bouton_action = QPushButton(text_bouton)
        if ajout:
            bouton_action.clicked.connect(self.ajouterObjetInventaire)
        else:
            bouton_action.clicked.connect(self.modifierObjetInventaire)
        outer_layout.addWidget(self.choix_item, stretch=1)
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
        id_objet = self.choix_item.itemData(self.choix_item.currentIndex())
        data = (id_objet, id_joueur)
        sql = 'INSERT INTO objet_personnage(id_objet, id_personnage) VALUES(%s, %s);'
        mon_curseur.execute(sql, data)
        mybd.commit()
        self.tabs.removeTab(1)
        page_personnage = self.personnageTabUI()
        self.tabs.addTab(page_personnage, 'Personnage')
        self.tabs.setCurrentIndex(1)

    def modifierObjetInventaire(self):
        data = (self.choix_item.itemData(self.choix_item.currentIndex()), self.list_objets.itemData(self.list_objets.currentIndex()))
        sql = 'UPDATE objet_personnage SET id_objet = %s WHERE id = %s;'
        mon_curseur.execute(sql, data)
        mybd.commit()
        self.tabs.removeTab(1)
        page_personnage = self.personnageTabUI()
        self.tabs.addTab(page_personnage, 'Personnage')
        self.tabs.setCurrentIndex(1)
    
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
        layout_objet.addLayout(self.boutonsPersonnage(2, self.list_objets, bouton_ajouter, bouton_modifier, bouton_supprimer))
        outer_layout.addLayout(layout_objet)
        return outer_layout

    def armeTabUI(self, text_bouton:str, ajout:bool = True) -> QWidget:
        arme_tab = QWidget()
        outer_layout = QVBoxLayout()
        self.choix_item = QComboBox()
        armes = self.requeteArmes()
        for i in range(0, len(armes['nom'])):
            self.choix_item.addItem(armes['nom'][i], armes['id'][i])
        bouton_action = QPushButton(text_bouton)
        if ajout:
            bouton_action.clicked.connect(self.ajouterArmeInventaire)
        else:
            bouton_action.clicked.connect(self.modifierArmeInventaire)
        outer_layout.addWidget(self.choix_item, stretch=1)
        outer_layout.addWidget(bouton_action, stretch=1)
        arme_tab.setLayout(outer_layout)
        return arme_tab
    
    def ajouterArmeInventaire(self):
        data = (self.id_partie,)
        sql = 'SELECT id FROM personnage WHERE id_partie = %s;'
        mon_curseur.execute(sql, data)
        resultat = mon_curseur.fetchall()
        id_joueur:str
        for id in resultat:
            id_joueur = id[0]
        id_arme = self.choix_item.itemData(self.choix_item.currentIndex())
        data = (id_arme, id_joueur)
        sql = 'INSERT INTO arme_personnage(id_arme, id_personnage) VALUES(%s, %s);'
        mon_curseur.execute(sql, data)
        mybd.commit()
        self.tabs.removeTab(1)
        page_personnage = self.personnageTabUI()
        self.tabs.addTab(page_personnage, 'Personnage')
        self.tabs.setCurrentIndex(1)
    
    def modifierArmeInventaire(self):
        data = (self.choix_item.itemData(self.choix_item.currentIndex()), self.list_armes.itemData(self.list_armes.currentIndex()))
        sql = 'UPDATE arme_personnage SET id_arme = %s WHERE id = %s;'
        mon_curseur.execute(sql, data)
        mybd.commit()
        self.tabs.removeTab(1)
        page_personnage = self.personnageTabUI()
        self.tabs.addTab(page_personnage, 'Personnage')
        self.tabs.setCurrentIndex(1)

    def boutonAjouterArme(self):
        page_ajout = self.armeTabUI('Ajouter Arme')
        self.tabs.removeTab(1)
        self.tabs.addTab(page_ajout, 'Ajout Arme')
        self.tabs.setCurrentIndex(1)

    def boutonModifierArme(self):
        page_modif = self.armeTabUI('Modifier Arme', False)
        self.tabs.removeTab(1)
        self.tabs.addTab(page_modif, 'Modifier Arme')
        self.tabs.setCurrentIndex(1)
    
    def supprimerArmeInventaire(self):
        data = (self.list_armes.itemData(self.list_armes.currentIndex()),)
        sql = 'DELETE FROM arme_personnage WHERE id = %s;'
        mon_curseur.execute(sql, data)
        mybd.commit()
        self.tabs.removeTab(1)
        page_personnage = self.personnageTabUI()
        self.tabs.addTab(page_personnage, 'Personnage')
        self.tabs.setCurrentIndex(1)

    def armesPersonnage(self) -> QVBoxLayout:
        outer_layout = QVBoxLayout()
        label_arme = QLabel("Armes:")
        outer_layout.addWidget(label_arme)
        layout_arme = QHBoxLayout()
        self.list_armes = QComboBox()
        armes = self.requeteArmesPersonnage()
        for i in range(0, len(armes['nom'])):
            self.list_armes.addItem(armes['nom'][i], armes['id'][i])
        bouton_ajouter = QPushButton("Ajouter")
        bouton_ajouter.clicked.connect(self.boutonAjouterArme)
        bouton_modifier = QPushButton("Modifier")
        bouton_modifier.clicked.connect(self.boutonModifierArme)
        bouton_supprimer = QPushButton("Supprimer")
        bouton_supprimer.clicked.connect(self.supprimerArmeInventaire)
        layout_arme.addWidget(self.list_armes, stretch=2)
        layout_arme.addLayout(self.boutonsPersonnage(2, self.list_armes, bouton_ajouter, bouton_modifier, bouton_supprimer))
        outer_layout.addLayout(layout_arme)
        return outer_layout

    def disciplineTabUI(self, text_bouton:str, ajout:bool = True) -> QWidget:
        """
        Tab qui s'occupe de l'ajout et de la modification des disciplines
        text_bouton:str -- Le texte qui sera afficher sur le bouton
        ajout:bool -- True l'action du bouton sera d'ajouter une discipline | False le bouton servira a la modification de la discipline\n
        returns -> La tab de discipline
        """
        discipline_tab = QWidget()
        outer_layout = QVBoxLayout()
        self.choix_item = QComboBox()
        disciplines = self.requeteDisciplines()
        for i in range(0, len(disciplines['nom'])):
            self.choix_item.addItem(disciplines['nom'][i], disciplines['id'][i])
        bouton_action = QPushButton(text_bouton)
        if ajout:
            bouton_action.clicked.connect(self.ajouterDisciplineInventaire)
        else:
            bouton_action.clicked.connect(self.modifierDisciplineInventaire)
        outer_layout.addWidget(self.choix_item, stretch=1)
        outer_layout.addWidget(bouton_action, stretch=1)
        discipline_tab.setLayout(outer_layout)
        return discipline_tab
    
    def ajouterDisciplineInventaire(self):
        data = (self.id_partie,)
        sql = 'SELECT id FROM personnage WHERE id_partie = %s;'
        mon_curseur.execute(sql, data)
        resultat = mon_curseur.fetchall()
        id_joueur:str
        for id in resultat:
            id_joueur = id[0]
        id_discipline = self.choix_item.itemData(self.choix_item.currentIndex())
        data = (id_discipline, id_joueur)
        sql = 'INSERT INTO discipline_kai_personnage(id_discipline_kai, id_personnage) VALUES(%s, %s);'
        mon_curseur.execute(sql, data)
        mybd.commit()
        self.tabs.removeTab(1)
        page_personnage = self.personnageTabUI()
        self.tabs.addTab(page_personnage, 'Personnage')
        self.tabs.setCurrentIndex(1)
    
    def modifierDisciplineInventaire(self):
        data = (self.choix_item.itemData(self.choix_item.currentIndex()), self.list_disciplines.itemData(self.list_disciplines.currentIndex()))
        sql = 'UPDATE discipline_kai_personnage SET id_discipline_kai = %s WHERE CONCAT(id_personnage, id_discipline_kai) = %s;'
        mon_curseur.execute(sql, data)
        mybd.commit()
        self.tabs.removeTab(1)
        page_personnage = self.personnageTabUI()
        self.tabs.addTab(page_personnage, 'Personnage')
        self.tabs.setCurrentIndex(1)

    def boutonAjouterDiscipline(self):
        page_ajout = self.disciplineTabUI('Ajouter Discipline')
        self.tabs.removeTab(1)
        self.tabs.addTab(page_ajout, 'Ajout Discipline')
        self.tabs.setCurrentIndex(1)

    def boutonModifierDiscipline(self):
        page_modif = self.disciplineTabUI('Modifier Discipline', False)
        self.tabs.removeTab(1)
        self.tabs.addTab(page_modif, 'Modifier Discipline')
        self.tabs.setCurrentIndex(1)

    def supprimerDisciplineInventaire(self):
        data = (self.list_disciplines.itemData(self.list_disciplines.currentIndex()),)
        sql = 'DELETE FROM discipline_kai_personnage WHERE CONCAT(id_personnage, id_discipline_kai) = %s;'
        mon_curseur.execute(sql, data)
        mybd.commit()
        self.tabs.removeTab(1)
        page_personnage = self.personnageTabUI()
        self.tabs.addTab(page_personnage, 'Personnage')
        self.tabs.setCurrentIndex(1)

    def disciplinesPersonnage(self) -> QVBoxLayout:
        outer_layout = QVBoxLayout()
        label_disciplines = QLabel('Disciplines Kai:')
        outer_layout.addWidget(label_disciplines)
        layout_disciplines = QHBoxLayout()
        self.list_disciplines = QComboBox()
        disciplines = self.requeteDisciplinesPersonnage()
        for i in range(0, len(disciplines['nom'])):
            self.list_disciplines.addItem(disciplines['nom'][i], disciplines['id'][i])
        bouton_ajouter = QPushButton('Ajouter')
        bouton_ajouter.clicked.connect(self.boutonAjouterDiscipline)
        bouton_modifier = QPushButton('Modifier')
        bouton_modifier.clicked.connect(self.boutonModifierDiscipline)
        bouton_supprimer = QPushButton('Supprimer')
        bouton_supprimer.clicked.connect(self.supprimerDisciplineInventaire)
        layout_disciplines.addWidget(self.list_disciplines, stretch=2)
        layout_disciplines.addLayout(self.boutonsPersonnage(6, self.list_disciplines, bouton_ajouter, bouton_modifier, bouton_supprimer))
        outer_layout.addLayout(layout_disciplines)
        return outer_layout
    
    def equipementTabUI(self, text_bouton:str, ajout:bool = True) -> QWidget:
        """
        Tab qui s'occupe de l'ajout et de la modification des equipements
        text_bouton:str -- Le texte qui sera afficher sur le bouton
        ajout:bool -- True l'action du bouton sera d'ajouter un equipement | False le bouton servira a la modification de l'equipement'\n
        returns -> La tab d'equipement
        """
        equipement_tab = QWidget()
        outer_layout = QVBoxLayout()
        self.choix_item = QComboBox()
        equipements = self.requeteEquipements()
        for i in range(0, len(equipements['nom'])):
            self.choix_item.addItem(equipements['nom'][i], equipements['id'][i])
        bouton_action = QPushButton(text_bouton)
        if ajout:
            bouton_action.clicked.connect(self.ajouterEquipementInventaire)
        else:
            bouton_action.clicked.connect(self.modifierEquipementInventaire)
        outer_layout.addWidget(self.choix_item, stretch=1)
        outer_layout.addWidget(bouton_action, stretch=1)
        equipement_tab.setLayout(outer_layout)
        return equipement_tab

    def ajouterEquipementInventaire(self):
        data = (self.id_partie,)
        sql = 'SELECT id FROM personnage WHERE id_partie = %s;'
        mon_curseur.execute(sql, data)
        resultat = mon_curseur.fetchall()
        id_joueur:str
        for id in resultat:
            id_joueur = id[0]
        id_equipement = self.choix_item.itemData(self.choix_item.currentIndex())
        data = (id_equipement, id_joueur)
        sql = 'INSERT INTO equipement_personnage(id_equipement, id_personnage) VALUES(%s, %s);'
        mon_curseur.execute(sql, data)
        mybd.commit()
        self.tabs.removeTab(1)
        page_personnage = self.personnageTabUI()
        self.tabs.addTab(page_personnage, 'Personnage')
        self.tabs.setCurrentIndex(1)
    
    def modifierEquipementInventaire(self):
        data = (self.choix_item.itemData(self.choix_item.currentIndex()), self.list_equipements.itemData(self.list_equipements.currentIndex()))
        sql = 'UPDATE equipement_personnage SET id_equipement = %s WHERE CONCAT(id_personnage, id_equipement) = %s;'
        mon_curseur.execute(sql, data)
        mybd.commit()
        self.tabs.removeTab(1)
        page_personnage = self.personnageTabUI()
        self.tabs.addTab(page_personnage, 'Personnage')
        self.tabs.setCurrentIndex(1)

    def boutonAjouterEquipement(self):
        page_ajout = self.equipementTabUI('Ajouter Equipement')
        self.tabs.removeTab(1)
        self.tabs.addTab(page_ajout, 'Ajout Equipement')
        self.tabs.setCurrentIndex(1)

    def boutonModifierEquipement(self):
        page_modif = self.equipementTabUI('Modifier Equipement', False)
        self.tabs.removeTab(1)
        self.tabs.addTab(page_modif, 'Modifier Equipement')
        self.tabs.setCurrentIndex(1)

    def supprimerEquipementInventaire(self):
        data = (self.list_equipements.itemData(self.list_equipements.currentIndex()),)
        sql = 'DELETE FROM equipement_personnage WHERE CONCAT(id_personnage, id_equipement) = %s;'
        mon_curseur.execute(sql, data)
        mybd.commit()
        self.tabs.removeTab(1)
        page_personnage = self.personnageTabUI()
        self.tabs.addTab(page_personnage, 'Personnage')
        self.tabs.setCurrentIndex(1)

    def equipementsPersonnage(self) -> QVBoxLayout:
        outer_layout = QVBoxLayout()
        label_equipements = QLabel('Équipement:')
        outer_layout.addWidget(label_equipements)
        layout_equipements = QHBoxLayout()
        self.list_equipements = QComboBox()
        equipements = self.requeteEquipementsPersonnage()
        for i in range(0, len(equipements['nom'])):
            self.list_equipements.addItem(equipements['nom'][i], equipements['id'][i])
        bouton_ajouter = QPushButton('Ajouter')
        bouton_ajouter.clicked.connect(self.boutonAjouterEquipement)
        bouton_modifier = QPushButton('Modifier')
        bouton_modifier.clicked.connect(self.boutonModifierEquipement)
        bouton_supprimer = QPushButton('Supprimer')
        bouton_supprimer.clicked.connect(self.supprimerEquipementInventaire)
        layout_equipements.addWidget(self.list_equipements, stretch=2)
        layout_equipements.addLayout(self.boutonsPersonnage(2, self.list_equipements, bouton_ajouter, bouton_modifier, bouton_supprimer))
        outer_layout.addLayout(layout_equipements)
        return outer_layout

    def boutonsPersonnage(self, max_length:int, combo_box_item:QComboBox, bouton_ajouter:QPushButton, bouton_modifier:QPushButton, bouton_supprimer:QPushButton) -> QHBoxLayout:
        layout_item = QHBoxLayout()
        if (combo_box_item.count() < max_length):
            layout_item.addWidget(bouton_ajouter, stretch=1)
        if (len(combo_box_item.currentText()) > 0):
            layout_item.addWidget(bouton_modifier, stretch=1)
            layout_item.addWidget(bouton_supprimer, stretch=1)
        return layout_item

    def infoPersonnage(self) -> QVBoxLayout:
        layout_attributs = QHBoxLayout()
        attributs = self.requeteInfoPersonnage()
        text_endurance = QLineEdit(str(attributs['endurance']))
        text_endurance.textChanged.connect(self.formaterNombre)
        text_endurance.editingFinished.connect(self.majPersonnageEndurance)
        text_habilete = QLineEdit(str(attributs['habilete']))
        text_habilete.textChanged.connect(self.formaterNombre)
        text_habilete.editingFinished.connect(self.majPersonnageHabilete)
        text_or = QLineEdit(str(attributs['or']))
        text_or.textChanged.connect(self.formaterNombre)
        text_or.editingFinished.connect(self.majPersonnageOr)
        layout_attributs.addWidget(QLabel("Endurance:"))
        layout_attributs.addWidget(text_endurance)
        layout_attributs.addWidget(QLabel("Habileté:"))
        layout_attributs.addWidget(text_habilete)
        layout_attributs.addWidget(QLabel("Or:"))
        layout_attributs.addWidget(text_or)
        return layout_attributs

    def formaterNombre(self):
        nombre = str(self.sender().text())
        if (nombre.isdigit()):
            nombre = str(int(nombre))
        else:
            nombre = '0'
        self.sender().setText(nombre)

    def majPersonnageEndurance(self):
        nouvelleValeur = str(self.sender().text())
        if nouvelleValeur.isdigit() and self.sender().isModified:
            data = (nouvelleValeur, self.id_partie)
            sql = "UPDATE personnage SET endurance = %s WHERE id_partie = %s;"
            mon_curseur.execute(sql, data)
            mybd.commit()

    def majPersonnageHabilete(self):
        nouvelleValeur = str(self.sender().text())
        if nouvelleValeur.isdigit() and self.sender().isModified:
            data = (nouvelleValeur, self.id_partie)
            sql = "UPDATE personnage SET habilete = %s WHERE id_partie = %s;"
            mon_curseur.execute(sql, data)
            mybd.commit()

    def majPersonnageOr(self):
        nouvelleValeur = str(self.sender().text())
        if nouvelleValeur.isdigit() and self.sender().isModified:
            if int(nouvelleValeur) > 50:
                nouvelleValeur = '50'
                self.sender().setText(nouvelleValeur)
            data = (nouvelleValeur, self.id_partie)
            sql = "UPDATE personnage SET `or` = %s WHERE id_partie = %s;"
            mon_curseur.execute(sql, data)
            mybd.commit()

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
                INNER JOIN objet ON id_objet = objet.id WHERE id_partie = %s ORDER BY nom;"""
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

    def requeteArmesPersonnage(self) -> dict:
        data  = (self.id_partie,)
        sql = "SELECT nom, ap.id as id_arme FROM personnage INNER JOIN arme_personnage ap ON personnage.id = ap.id_personnage INNER JOIN arme a ON ap.id_arme = a.id WHERE id_partie = %s ORDER BY nom;"
        mon_curseur.execute(sql, data)
        resultat = mon_curseur.fetchall()
        armes = {}
        nom_arme = []
        ids = []
        for nom, id_arme in resultat:
            nom_arme.append(nom)
            ids.append(id_arme)
        armes['nom'] = nom_arme
        armes['id'] = ids 
        return armes

    def requeteDisciplinesPersonnage(self) -> dict:
        data  = (self.id_partie,)
        sql = "SELECT nom, CONCAT(id_personnage, id_discipline_kai) as id_discipline FROM personnage INNER JOIN discipline_kai_personnage dkp ON personnage.id = dkp.id_personnage INNER JOIN discipline_kai dk ON dkp.id_discipline_kai = dk.id WHERE id_partie = %s ORDER BY nom;"
        mon_curseur.execute(sql, data)
        resultat = mon_curseur.fetchall()
        disciplines = {}
        nom_disciplines = []
        ids = []
        for nom, id_discipline in resultat:
            nom_disciplines.append(nom)
            ids.append(id_discipline)
        disciplines['nom'] = nom_disciplines
        disciplines['id'] = ids 
        return disciplines

    def requeteEquipementsPersonnage(self) -> dict:
        data  = (self.id_partie,)
        sql = "SELECT nom, CONCAT(id_personnage, id_equipement) as id_equipement FROM personnage INNER JOIN equipement_personnage ep ON personnage.id = ep.id_personnage INNER JOIN equipement eq ON ep.id_equipement = eq.id WHERE id_partie = %s ORDER BY nom;"
        mon_curseur.execute(sql, data)
        resultat = mon_curseur.fetchall()
        equipements = {}
        nom_equipements = []
        ids = []
        for nom, id_equipement in resultat:
            nom_equipements.append(nom)
            ids.append(id_equipement)
        equipements['nom'] = nom_equipements
        equipements['id'] = ids 
        return equipements

    
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

    def requeteArmes(self) -> dict:
        """
        Sélectionne les armes
        returns -> dict ['nom'] -- Le nom de l'arme | ['id'] -- L'id de l'arme
        """
        sql = "SELECT nom, id FROM arme ORDER BY nom;"
        mon_curseur.execute(sql)
        resultat = mon_curseur.fetchall()
        armes = {}
        nom_arme = []
        id_arme = []
        for nom, id in resultat:
            nom_arme.append(nom)
            id_arme.append(id)
        armes['nom'] = nom_arme
        armes['id'] = id_arme
        return armes

    def requeteDisciplines(self) -> dict:
        """
        Sélectionne les disciplines non acquises par le joueur
        returns -> dict ['nom'] -- Le nom de la discipline | ['id'] -- L'id de la discipline
        """
        data = (self.id_partie,)
        sql = 'SELECT id FROM personnage WHERE id_partie = %s;'
        mon_curseur.execute(sql, data)
        resultat = mon_curseur.fetchall()
        id_joueur:str
        for id in resultat:
            id_joueur = id[0]
        data = (id_joueur,)
        sql = "SELECT nom, id FROM discipline_kai WHERE id NOT IN (SELECT id_discipline_kai AS id FROM discipline_kai_personnage WHERE id_personnage = %s);"
        mon_curseur.execute(sql, data)
        resultat = mon_curseur.fetchall()
        disciplines = {}
        nom_discipline = []
        id_discipline = []
        for nom, id in resultat:
            nom_discipline.append(nom)
            id_discipline.append(id)
        disciplines['nom'] = nom_discipline
        disciplines['id'] = id_discipline
        return disciplines

    def requeteEquipements(self) -> dict:
        """
        Sélectionne les equipements non acquis par le joueur
        returns -> dict ['nom'] -- Le nom de l'equipement | ['id'] -- L'id de l'equipement
        """
        data = (self.id_partie,)
        sql = 'SELECT id FROM personnage WHERE id_partie = %s;'
        mon_curseur.execute(sql, data)
        resultat = mon_curseur.fetchall()
        id_joueur:str
        for id in resultat:
            id_joueur = id[0]
        data = (id_joueur,)
        sql = "SELECT nom, id FROM equipement WHERE id NOT IN (SELECT id_equipement AS id FROM equipement_personnage WHERE id_personnage = %s);"
        mon_curseur.execute(sql, data)
        resultat = mon_curseur.fetchall()
        equipements = {}
        nom_equipement = []
        id_equipement = []
        for nom, id in resultat:
            nom_equipement.append(nom)
            id_equipement.append(id)
        equipements['nom'] = nom_equipement
        equipements['id'] = id_equipement
        return equipements

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
        data = (self.id_partie,)
        sql = "INSERT INTO personnage (id_partie) VALUES (%s);"
        mon_curseur.execute(sql, data)
        mybd.commit()
        page_tab = self.pageTabUI()
        perso_tab = self.personnageTabUI()
        self.tabs.addTab(page_tab, "Page")
        self.tabs.addTab(perso_tab, "Personnage")
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
        mybd.commit()
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

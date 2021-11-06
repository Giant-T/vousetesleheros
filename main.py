import sys
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
    
    def initUI(self) -> QVBoxLayout:
        outer_layout = QVBoxLayout()
        top_layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()
        texte = QLabel("texte random pour test")
        top_layout.addWidget(texte)

        boutons = [QPushButton("1"), QPushButton("2"), QPushButton("3"), QPushButton("4"), QPushButton("5"), QPushButton("6")]
        for bouton in boutons:
            bottom_layout.addWidget(bouton)
        
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("Dont Vous Êtes le Héros")
        self.setFixedSize(640, 480)
        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(bottom_layout)
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(outer_layout)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec()
   mon_curseur.close()

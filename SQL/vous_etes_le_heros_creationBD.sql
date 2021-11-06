DROP DATABASE IF EXISTS vous_etes_le_heros;
CREATE DATABASE vous_etes_le_heros;
USE vous_etes_le_heros;

CREATE TABLE livre
(
    id     INT PRIMARY KEY AUTO_INCREMENT,
    titre  VARCHAR(255) NOT NULL,
    auteur VARCHAR(255) NOT NULL
);

CREATE TABLE chapitre
(
    id              INT PRIMARY KEY AUTO_INCREMENT,
    id_livre        INT  NOT NULL,
    numero_chapitre INT  NOT NULL,
    texte           TEXT NOT NULL,
    FOREIGN KEY (id_livre) REFERENCES livre (id)
);

CREATE TABLE choix_page
(
    id                          INT PRIMARY KEY AUTO_INCREMENT,
    id_livre                    INT NOT NULL,
    id_chapitre                 INT NOT NULL,
    numero_chapitre_destination INT NOT NULL,
    FOREIGN KEY (id_livre) REFERENCES livre (id),
    FOREIGN KEY (id_chapitre) REFERENCES chapitre (id)
);

CREATE TABLE partie
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    nom         VARCHAR(255) NOT NULL,
    id_chapitre INT          NOT NULL,
    id_livre    INT          NOT NULL,
    FOREIGN KEY (id_chapitre) REFERENCES chapitre (id),
    FOREIGN KEY (id_livre) REFERENCES livre (id)
);

CREATE TABLE personnage
(
    id        INT PRIMARY KEY AUTO_INCREMENT,
    id_partie INT NOT NULL,
    endurance INT NOT NULL,
    habilete  INT NOT NULL,
    `or`      INT NOT NULL DEFAULT 12,
    FOREIGN KEY (id_partie) REFERENCES partie (id)
);

CREATE TABLE discipline_kai
(
    id          INT PRIMARY KEY AUTO_INCREMENT,
    nom         VARCHAR(255) NOT NULL,
    description TEXT         NOT NULL
);

CREATE TABLE objet
(
    id   INT PRIMARY KEY AUTO_INCREMENT,
    nom  VARCHAR(255)                                NOT NULL,
    type ENUM ('objet','objet spécial','nourriture') NOT NULL
);

CREATE TABLE arme
(
    id  INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255) NOT NULL
);

CREATE TABLE equipement
(
    id  INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255) NOT NULL
);

CREATE TABLE equipement_personnage
(
    id_equipement INT NOT NULL,
    id_personnage INT NOT NULL,
    FOREIGN KEY (id_equipement) REFERENCES equipement (id),
    FOREIGN KEY (id_personnage) REFERENCES personnage (id),
    PRIMARY KEY (id_personnage, id_equipement)
);

CREATE TABLE arme_personnage
(
    id            INT PRIMARY KEY AUTO_INCREMENT,
    id_arme       INT NOT NULL,
    id_personnage INT NOT NULL,
    FOREIGN KEY (id_arme) REFERENCES arme (id),
    FOREIGN KEY (id_personnage) REFERENCES personnage (id)
);

CREATE TABLE objet_personnage
(
    id            INT PRIMARY KEY AUTO_INCREMENT,
    id_objet      INT NOT NULL,
    id_personnage INT NOT NULL,
    FOREIGN KEY (id_objet) REFERENCES objet (id),
    FOREIGN KEY (id_personnage) REFERENCES personnage (id)
);

CREATE TABLE discipline_kai_personnage
(
    id_discipline_kai INT NOT NULL,
    id_personnage     INT NOT NULL,
    FOREIGN KEY (id_discipline_kai) REFERENCES discipline_kai (id),
    FOREIGN KEY (id_personnage) REFERENCES personnage (id),
    PRIMARY KEY (id_personnage, id_discipline_kai)
);




# Exemple Fonction
DROP FUNCTION IF EXISTS no_name_function;
DELIMITER $$
CREATE FUNCTION no_name_function(_pin VARCHAR(100), _classe_id INT) RETURNS BOOLEAN
    READS SQL DATA NOT DETERMINISTIC
BEGIN
    DECLARE _return BOOLEAN DEFAULT FALSE;

    RETURN _return;
END; $$
DELIMITER ;


# Exemple Procédure
DROP PROCEDURE IF EXISTS no_name;
DELIMITER $$
CREATE PROCEDURE no_name(IN _date DATE)
BEGIN

END; $$
DELIMITER ;

# question 2
DROP TRIGGER IF EXISTS no_name_trigger;
DELIMITER $$
CREATE TRIGGER no_name_trigger
    BEFORE INSERT
    ON personnage
    FOR EACH ROW
BEGIN

END; $$
DELIMITER ;
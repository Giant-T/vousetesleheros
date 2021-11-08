USE vous_etes_le_heros;

# Retroune le numero du chapitre dans le livre relié à l'id du chapitre
DROP FUNCTION IF EXISTS numero_id_chapitre;
DELIMITER $$
CREATE FUNCTION numero_id_chapitre(_id_chapitre INT) RETURNS INT
    READS SQL DATA NOT DETERMINISTIC
BEGIN
    RETURN (SELECT numero_chapitre FROM chapitre WHERE id = _id_chapitre);
END;
$$
DELIMITER ;

# Retroune le nombre de disciplines-kai du personnage
DROP FUNCTION IF EXISTS compte_disciplines;
DELIMITER $$
CREATE FUNCTION compte_disciplines(_id_personnage INT) RETURNS INT
    READS SQL DATA NOT DETERMINISTIC
BEGIN
    RETURN (SELECT count(id_discipline_kai) AS nombre_disciplines FROM discipline_kai_personnage WHERE id_personnage = _id_personnage);
END;
$$
DELIMITER ;

# Retroune le nombre d'objets du personnage (objets spéciaux exclu)
DROP FUNCTION IF EXISTS compte_objets;
DELIMITER $$
CREATE FUNCTION compte_objets(_id_personnage INT) RETURNS INT
    READS SQL DATA NOT DETERMINISTIC
BEGIN
    RETURN (SELECT count(op.id) AS nombre_objets FROM objet_personnage op INNER JOIN objet o ON op.id_objet = o.id WHERE op.id_personnage = _id_personnage AND o.type IN('objet','nourriture'));
END;
$$
DELIMITER ;

# Retroune le nombre d'armes portées par le joueur
DROP FUNCTION IF EXISTS compte_armes;
DELIMITER $$
CREATE FUNCTION compte_armes(_id_personnage INT) RETURNS INT
    READS SQL DATA NOT DETERMINISTIC
BEGIN
    RETURN (SELECT count(ap.id) AS nombre_armes FROM arme_personnage ap INNER JOIN arme a ON ap.id_arme = a.id WHERE ap.id_personnage = _id_personnage);
END;
$$
DELIMITER ;

# Retroune vrai si le joueur peut porter plus d'objets
DROP FUNCTION IF EXISTS peut_transporter_objet;
DELIMITER $$
CREATE FUNCTION peut_transporter_objet(_id_personnage INT) RETURNS BOOLEAN
    READS SQL DATA NOT DETERMINISTIC
BEGIN
    RETURN compte_objets(_id_personnage) < 8;
END;
$$
DELIMITER ;

# Retroune vrai si le joueur peut porter plus d'armes
DROP FUNCTION IF EXISTS peut_transporter_arme;
DELIMITER $$
CREATE FUNCTION peut_transporter_arme(_id_personnage INT) RETURNS BOOLEAN
    READS SQL DATA NOT DETERMINISTIC
BEGIN
    RETURN compte_armes(_id_personnage) < 2;
END;
$$
DELIMITER ;


# Procédure qui liste les disciplines kai d'un personnage
DROP PROCEDURE IF EXISTS liste_disciplines_kai;
DELIMITER $$
CREATE PROCEDURE liste_disciplines_kai(IN _id_personnage INT)
BEGIN
    SELECT nom FROM discipline_kai dk INNER JOIN discipline_kai_personnage dkp ON dk.id = dkp.id_discipline_kai LIMIT 5;
END;
$$
DELIMITER ;

# Procédure qui liste les objets d'un personnage
DROP PROCEDURE IF EXISTS liste_objets;
DELIMITER $$
CREATE PROCEDURE liste_objets(IN _id_personnage INT)
BEGIN
    SELECT nom FROM objet o INNER JOIN objet_personnage op ON o.id = op.id_objet ORDER BY type DESC LIMIT 8 ;
END;
$$
DELIMITER ;

# Procédure qui affiche les armes équipées par un personnage
DROP PROCEDURE IF EXISTS liste_armes;
DELIMITER $$
CREATE PROCEDURE liste_armes(IN _id_personnage INT)
BEGIN
    SELECT nom FROM arme a INNER JOIN arme_personnage ap ON a.id = ap.id_arme LIMIT 2;
END;
$$
DELIMITER ;

# Trigger qui s'assure que le chapitre actuel n'est pas le chapitre de destination avant l'insertion.
DROP TRIGGER IF EXISTS destination_differente;
DELIMITER $$
CREATE TRIGGER destination_differente
    BEFORE INSERT
    ON choix_page
    FOR EACH ROW
BEGIN
    IF new.numero_chapitre_destination = numero_id_chapitre(new.id_chapitre) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Le chapitre de destination de doit pas être identique au chapitre';
    END IF;
END;
$$
DELIMITER ;

# Trigger qui s'assure que le personnage peut transporter l'arme avant de l'inserer dans la table arme_personnage
DROP TRIGGER IF EXISTS trigger_peut_transporter_arme;
DELIMITER $$
CREATE TRIGGER trigger_peut_transporter_arme
    BEFORE INSERT
    ON arme_personnage
    FOR EACH ROW
BEGIN
    IF NOT peut_transporter_arme(NEW.id_personnage) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Ce personnage ne peut plus transporter d\'armes';
    END IF;
END;
$$
DELIMITER ;

# Trigger qui s'assure que le personnage peut transporter l'objet avant de l'inserer dans la table objet_personnage
DROP TRIGGER IF EXISTS trigger_peut_transporter_objet;
DELIMITER $$
CREATE TRIGGER trigger_peut_transporter_objet
    BEFORE INSERT
    ON objet_personnage
    FOR EACH ROW
BEGIN
    IF NOT peut_transporter_objet(NEW.id_personnage) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Ce personnage ne peut plus transporter d\'objets';
    END IF;
END;
$$
DELIMITER ;
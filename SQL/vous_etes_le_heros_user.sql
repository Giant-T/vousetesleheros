
CREATE USER IF NOT EXISTS 'JoeDever'@'localhost' IDENTIFIED BY 'GaryChalk';
GRANT SELECT, INSERT, UPDATE, DELETE ON vous_etes_le_heros.partie TO 'JoeDever'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON vous_etes_le_heros.personnage TO 'JoeDever'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON vous_etes_le_heros.arme_personnage TO 'JoeDever'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON vous_etes_le_heros.equipement_personnage TO 'JoeDever'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON vous_etes_le_heros.objet_personnage TO 'JoeDever'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON vous_etes_le_heros.discipline_kai_personnage TO 'JoeDever'@'localhost';
GRANT SELECT ON vous_etes_le_heros.livre TO 'JoeDever'@'localhost';
GRANT SELECT ON vous_etes_le_heros.chapitre TO 'JoeDever'@'localhost';
GRANT SELECT ON vous_etes_le_heros.choix_page TO 'JoeDever'@'localhost';
GRANT EXECUTE ON FUNCTION premier_chapitre_id TO 'JoeDever'@'localhost';
GRANT SELECT ON vous_etes_le_heros.objet TO 'JoeDever'@'localhost';
GRANT SELECT ON vous_etes_le_heros.arme TO 'JoeDever'@'localhost';
GRANT SELECT ON vous_etes_le_heros.discipline_kai TO 'JoeDever'@'localhost';

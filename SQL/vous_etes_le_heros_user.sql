

CREATE USER IF NOT EXISTS 'JoeDever'@'localhost' IDENTIFIED BY 'GaryChalk';
GRANT SELECT, INSERT, UPDATE, DELETE ON vous_etes_le_heros.partie TO 'JoeDever'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON vous_etes_le_heros.personnage TO 'JoeDever'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON vous_etes_le_heros.arme_personnage TO 'JoeDever'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON vous_etes_le_heros.equipement_personnage TO 'JoeDever'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON vous_etes_le_heros.objet_personnage TO 'JoeDever'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON vous_etes_le_heros.discipline_kai_personnage TO 'JoeDever'@'localhost';
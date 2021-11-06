USE vous_etes_le_heros;

INSERT INTO livre (id, titre, auteur)
VALUES (1, 'Lorem Ipsum - Prepare to Die Edition ft. Dante from Devil May Cry', 'Ranus Pockus');

INSERT INTO chapitre (id, id_livre, numero_chapitre, texte)
VALUES (1, 1, 1, 'William, violets are red roses are true, you came out of the blue, and lost no nut november.');
INSERT INTO chapitre (id, id_livre, numero_chapitre, texte)
VALUES (2, 1, 2,
        'Si vis pacem para belum. Lorem Ipsum. haaaaaaaaahahahahahhaaaaaaaaaaaaaaaaaaaaaaahahahahahahh faudrait pt je fasse l\'effort d\'aller chercher tu vrai lorem ipsum');
INSERT INTO chapitre (id, id_livre, numero_chapitre, texte)
VALUES (3, 1, 3,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Astral Souls sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.');

INSERT INTO choix_page(id, id_livre, id_chapitre, numero_chapitre_destination)
VALUES (1, 1, 1, 2);
INSERT INTO choix_page(id, id_livre, id_chapitre, numero_chapitre_destination)
VALUES (2, 1, 1, 3);
INSERT INTO choix_page(id, id_livre, id_chapitre, numero_chapitre_destination)
VALUES (4, 1, 2, 3);
INSERT INTO choix_page(id, id_livre, id_chapitre, numero_chapitre_destination)
VALUES (5, 1, 3, 1);
INSERT INTO choix_page(id, id_livre, id_chapitre, numero_chapitre_destination)
VALUES (6, 1, 3, 2);
INSERT INTO choix_page(id, id_livre, id_chapitre, numero_chapitre_destination)
VALUES (6, 1, 3, 3);

INSERT INTO partie (id, nom, id_chapitre, id_livre) VALUES (1, 'William Boudro', 1, 1);
INSERT INTO personnage(id, id_partie, endurance, habilete) VALUES (1, 1, 20, 8);
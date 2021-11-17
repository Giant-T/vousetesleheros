USE vous_etes_le_heros;

# /////////////////    Première partie    ///////////////////////////////////////////
INSERT INTO livre (id, titre, auteur)
VALUES (1, 'Lorem Ipsum - Prepare to Die Edition ft. Dante from Devil May Cry', 'Ranus Pockus');

INSERT INTO chapitre (id, id_livre, numero_chapitre, texte)
VALUES (1, 1, 1, 'William, violets are red roses are true, you came out of the blue, and lost no nut november.'),
       (2, 1, 2,
        'Si vis pacem para belum. Lorem Ipsum. haaaaaaaaahahahahahhaaaaaaaaaaaaaaaaaaaaaaahahahahahahh faudrait pt je fasse l\'effort d\'aller chercher tu vrai lorem ipsum'),
       (3, 1, 3,
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Astral Souls sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.');

INSERT INTO choix_page(id, id_livre, id_chapitre, numero_chapitre_destination)
VALUES (1, 1, 1, 2),
       (2, 1, 1, 3),
       (4, 1, 2, 3),
       (5, 1, 3, 1),
       (6, 1, 3, 2);

INSERT INTO partie (id, nom, id_chapitre, id_livre)
VALUES (1, 'William Boudro', 1, 1);

INSERT INTO personnage(id, id_partie, endurance, habilete)
VALUES (1, 1, 20, 8);

# /////////////////    Deuxième partie    ///////////////////////////////////////////

INSERT INTO livre (id, titre, auteur)
VALUES (2, 'All Too Well', 'Taylor Swift');

INSERT INTO chapitre (id_livre, numero_chapitre, texte)
VALUES (2, 1,
        'J\'ai franchi la porte avec toi l\'air était froid mais quelque chose à ce sujet se sentait comme à la maison en quelque sorte et moi, j\'ai laissé mon écharpe chez ta soeur et tu l\'as toujours dans ton tiroir même maintenant'),
       (2, 2,
        'Oh, ta douce disposition et mes yeux écarquillés, nous chantons dans la voiture, nous perdons les feuilles d\'automne du nord de l\'État qui tombent comme des morceaux en place et je peux l\'imaginer après tous ces jours'),
       (2, 3,
        'Et je sais que c\'est parti depuis longtemps et que la magie n\'est plus là et je pourrais être bien mais je ne vais pas bien du tout'),
       (2, 4,
        'Parce que nous sommes de nouveau dans cette petite rue de la ville tu as presque couru le rouge parce que tu me regardais le vent dans mes cheveux, j\'étais là je m\'en souviens trop bien'),
       (2, 5,
        'Album photo sur le comptoir tes joues devenaient rouges tu étais un petit enfant avec des lunettes dans un lit simple et ta mère racontait des histoires sur toi dans l\'équipe de tee-ball tu m\'as parlé de ton passé en pensant que ton avenir était moi'),
       (2, 6,
        'Et je sais que c\'est révolu depuis longtemps et qu\'il n\'y avait rien d\'autre que je puisse faire et je t\'oublie assez longtemps pour oublier pourquoi j\'avais besoin de'),
       (2, 7, 'Parce que nous sommes encore au milieu de la nuit, nous dansons autour de la cuisine dans la lumière du réfrigérateur en bas des escaliers, j\'étais là,
        je m\'en souviens trop bien, ouais'),
       (2, 8,
        'Et peut-être que nous nous sommes perdus dans la traduction, peut-être que j\'en ai trop demandé mais peut-être que cette chose était un chef-d\'œuvre jusqu\'à ce que tu la déchires de peur, j\'étais là, je m\'en souviens trop bien'),
       (2, 9,
        'Et tu m\'appelles à nouveau juste pour me briser comme une promesse si cruelle au nom de l\'honnêteté, je suis un morceau de papier chiffonné étendu ici parce que je me souviens de tout, de tout, trop bien');

INSERT INTO choix_page(id_livre, id_chapitre, numero_chapitre_destination)
VALUES (2, id_numero_chapitre(2, 1), 2),
       (2, id_numero_chapitre(2, 2), 1),
       (2, id_numero_chapitre(2, 2), 3),
       (2, id_numero_chapitre(2, 3), 2),
       (2, id_numero_chapitre(2, 3), 4),
       (2, id_numero_chapitre(2, 4), 3),
       (2, id_numero_chapitre(2, 4), 5),
       (2, id_numero_chapitre(2, 5), 4),
       (2, id_numero_chapitre(2, 5), 6),
       (2, id_numero_chapitre(2, 6), 5),
       (2, id_numero_chapitre(2, 6), 7),
       (2, id_numero_chapitre(2, 7), 6),
       (2, id_numero_chapitre(2, 7), 8),
       (2, id_numero_chapitre(2, 8), 7),
       (2, id_numero_chapitre(2, 8), 9),
       (2, id_numero_chapitre(2, 9), 8),
       (2, id_numero_chapitre(2, 9), 1);


INSERT INTO discipline_kai(nom, description)
VALUES ('Camouflage', 'Cette  technique  permet  au  Seigneur  Kaï  de  se  fondre  dans  le paysage. A la  campagne, il peut se cacher parmi les arbres  et les rochers et se rendre de cette façon invisible à l\'ennemi même s\'il passe  tout  près  de  lui.  Dans  une  ville,  cette  discipline  donnera  à celui qui l\'utilise la faculté d\'avoir l\'air d\'un habitant du cru, tant par  l\'apparence  que  par  l\'accent  ou  la  langue  employée.  On  peut ainsi trouver un abri où se cacher en toute sécurité.
Si vous choisissez cette technique, inscrivez Camouflage sur votreFeuille d\'Aventure.'),
       ('Chasse',
        'Cette   discipline   donne   au   Seigneur   Kaï   l\'assurance   qu\'il   ne mourra    jamais    de    faim    même    s\'il    se    trouve    dans    un environnement  hostile.  Il  aura  toujours  la  possibilité  de  chasser pour  se  procurer  de  la  nourriture,  sauf  dans  les  déserts  et  les autres  régions  arides.  Cette  technique  permet  également  de  se déplacer sans bruit en pistant une proie.Si  vous  choisissez  cette  discipline,  inscrivez  sur  votre Feuille d\'Aventure  :Chasse  ;  vous  êtes  dispensé  de  Repas  chaque  fois qu\'il  est  obligatoire  de  manger  (voir  plus  loin  le  paragraphe Nourriture).'),
       ('Sixième Sens',
        'Grâce  à  cette  technique,  le  Seigneur  Kaï  devine  les  dangers imminents  qui  le  menacent.  Ce  Sixième  Sens  peut  également  lui révéler  les  intentions  véritables  d\'un  inconnu  ou  la  nature  d\'un objet   étrange   rencontré   au   cours   d\'une   aventure.   Si   vous choisissez  cette  discipline,  inscrivez  :  Sixième  Sens  sur  votreFeuille d\'Aventure.'),
       ('Orientation',
        'Chaque  fois  qu\'il  se  trouvera  dans  l\'obligation  de  décider  quelle direction  il  doit  prendre,  le  Seigneur  Kaï  fera  toujours  le  bon choix  grâce  à  cette  technique.  Il  saura  ainsi  quel  chemin  il convient d\'emprunter dans une forêt et il pourra également, dans une ville, découvrir l\'endroit  où sont cachés une personne ou un objet.  Par  ailleurs,  il  saura  interpréter  chaque  trace  de  pas, chaque  empreinte  qui  pourrait  lui  permettre  de  remonter  une piste.Si  vous  choisissez  cette  discipline,  inscrivez  :  Orientation  sur votreFeuille d\'Aventure.'),
       ('Guérison',
        'Cette   discipline   donne   la   faculté   de   récupérer   des   points d\'ENDURANCE perdus lors d\'un combat. Si vous maîtrisez cette technique,  vous  pourrez  ajouter  1  point  d\'ENDURANCE  à  votre total  à  chaque  fois  qu\'il  vous  sera  possible  d\'aller  d\'un  bout  à l\'autre d\'un paragraphe sans avoir à combattre un ennemi. (Vous n\'aurez droit d\'utiliser cette technique de la Guérison que lorsque vos  points  d\'ENDURANCE  seront  tombés  au-dessous  de  votre total  initial.  Rappelez-vous  que  vos  points  d\'ENDURANCE  ne peuvent  en  aucun  cas  excéder  votre  total  de  départ).  Si  vous choisissez  cette  discipline,  inscrivez  sur  votreFeuille  d\'Aventure :Guérison  ;  1  point  d\'ENDURANCE  pour  chaque  paragraphe parcouru sans combat.'),
       ('Maîtrise Épée', '2 points d\'habileté supplémentaire avec l\'épée'),
       ('Maîtrise Glaive', '2 points d\'habileté supplémentaire avec la glaive');

INSERT INTO objet(nom, type)
VALUES ('macaroni', 'nourriture'),
       ('spagatt', 'nourriture'),
       ('lasagne', 'nourriture'),
       ('clef squelette', 'objet'),
       ('Emeraude', 'objet'),
       ('miroir de poche', 'objet'),
       ('coupe de vin', 'objet'),
       ('plume d\'autruche', 'objet'),
       ('carapace de tortue', 'objet'),
       ('défense d\'éléphant', 'objet'),
       ('bidon d\'huile', 'objet');

INSERT INTO arme(nom)
VALUES ('Épée'),
       ('Glaive'),
       ('Lance'),
       ('Masse'),
       ('Sabre'),
       ('Marteau'),
       ('Hache'),
       ('Baton');

INSERT INTO equipement(nom)
VALUES ('casque carapace'),
       ('cotte éléphant'),
       ('cape autruche');

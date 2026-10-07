\set ON_ERROR_STOP off

\echo 'Note invalide : doit violer avis_note_check'
INSERT INTO avis (reservation_id, note, commentaire)
VALUES (1, 6, 'Note hors limites');

\echo 'Deux avis pour une réservation : doit violer avis_reservation_id_key'
INSERT INTO avis (reservation_id, note, commentaire)
VALUES (1, 5, 'Premier avis valide');
INSERT INTO avis (reservation_id, note, commentaire)
VALUES (1, 4, 'Deuxième avis interdit');

\echo 'Deux tags de même libellé : doit violer tags_libelle_key'
INSERT INTO tags (libelle) VALUES ('velo');
INSERT INTO tags (libelle) VALUES ('velo');

\echo 'Avis sur une réservation inexistante : doit violer avis_reservation_id_fkey'
INSERT INTO avis (reservation_id, note, commentaire)
VALUES (999999, 5, 'Réservation inconnue');

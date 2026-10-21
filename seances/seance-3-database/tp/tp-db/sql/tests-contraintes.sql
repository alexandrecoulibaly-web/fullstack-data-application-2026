

-- 'Note invalide : viole avis_note_check'
INSERT INTO avis (reservation_id, note, commentaire)
VALUES (1, 6, 'Note hors limites');

-- 'Deux avis pour une réservation : viole avis_reservation_id_key'
INSERT INTO avis (reservation_id, note, commentaire)
VALUES (1, 5, 'Premier avis valide');
INSERT INTO avis (reservation_id, note, commentaire)
VALUES (1, 4, 'Deuxième avis interdit');

-- 'Deux tags de même libellé : viole tags_libelle_key'
INSERT INTO tags (libelle) VALUES ('velo');
INSERT INTO tags (libelle) VALUES ('velo');

-- 'Avis sur une réservation inexistante : viole avis_reservation_id_fkey'
INSERT INTO avis (reservation_id, note, commentaire)
VALUES (999999, 5, 'Réservation inconnue');

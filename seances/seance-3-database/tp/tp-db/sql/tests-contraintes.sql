

-- 'Note invalide : viole avis_note_check'
INSERT INTO avis (reservation_id, note, commentaire)
VALUES (1, 6, 'Note hors limites');
-- ERROR: new row for relation "avis" violates check constraint "avis_note_check"

-- 'Deux avis pour une réservation : viole avis_reservation_id_key'
INSERT INTO avis (reservation_id, note, commentaire)
VALUES (1, 5, 'Premier avis valide');
INSERT INTO avis (reservation_id, note, commentaire)
VALUES (1, 4, 'Deuxième avis interdit');
-- ERROR: duplicate key value violates unique constraint "avis_reservation_id_key"

-- 'Avis sur une réservation active : viole avis_reservation_terminee'
INSERT INTO avis (reservation_id, note, commentaire)
VALUES (2, 5, 'Avis prématuré');
-- ERROR: avis_reservation_terminee: un avis doit concerner une réservation terminée

-- 'Deux tags de même libellé : viole tags_libelle_key'
INSERT INTO tags (libelle) VALUES ('velo');
-- First insert succeeds.
INSERT INTO tags (libelle) VALUES ('velo');
-- ERROR: violates unique constraint "tags_libelle_key"

-- 'Avis sur une réservation inexistante : viole avis_reservation_id_fkey'
INSERT INTO avis (reservation_id, note, commentaire)
VALUES (999999, 5, 'Réservation inconnue');
-- ERROR: violates foreign key constraint "avis_reservation_id_fkey"

-- 'Deux réservations actives qui se chevauchent : viole reservations_active_no_overlap'
INSERT INTO reservations
    (item_id, borrower_id, date_debut, date_fin, statut)
VALUES
    (3, 3, DATE '2026-09-11', DATE '2026-09-13', 'active');
-- ERROR: violates exclusion constraint "reservations_active_no_overlap"

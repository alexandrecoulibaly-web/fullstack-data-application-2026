\set ON_ERROR_STOP off

\echo '1. Email duplicate : doit violer users_email_key'
INSERT INTO users (email, password_hash, display_name)
VALUES ('alice@esiee.fr', 'fake', 'Alice duplicate');

\echo '2. Propriétaire inexistant : doit violer items_owner_id_fkey'
INSERT INTO items (owner_id, titre, tarif_jour)
VALUES (999, 'Item impossible', 1.00);

\echo '3. Tarif négatif : doit violer items_tarif_jour_check'
INSERT INTO items (owner_id, titre, tarif_jour)
VALUES (1, 'Item gratuit impossible', -1.00);

\echo '4. Dates inversées : doit violer reservations_dates_check'
INSERT INTO reservations (item_id, borrower_id, date_debut, date_fin)
VALUES (1, 2, DATE '2026-11-04', DATE '2026-11-01');

\echo '5. Statut inconnu : doit violer reservations_statut_check'
INSERT INTO reservations (item_id, borrower_id, date_debut, date_fin, statut)
VALUES (1, 2, DATE '2026-11-01', DATE '2026-11-04', 'en_attente_peut_etre');

\echo '6. Suppression de Bob : doit être refusée par reservations_borrower_id_fkey'
SELECT COUNT(*) AS bob_items_before
FROM items
WHERE owner_id = 2;
DELETE FROM users WHERE id = 2;
SELECT COUNT(*) AS bob_items_after_failed_delete
FROM items
WHERE owner_id = 2;

-- Expérience demandée : à exécuter seulement après restauration du schéma de base.
-- ALTER TABLE reservations DROP CONSTRAINT reservations_borrower_id_fkey;
-- ALTER TABLE reservations
--     ADD CONSTRAINT reservations_borrower_id_fkey
--     FOREIGN KEY (borrower_id) REFERENCES users(id) ON DELETE CASCADE;
-- DELETE FROM users WHERE id = 2;
-- SELECT * FROM reservations ORDER BY id;

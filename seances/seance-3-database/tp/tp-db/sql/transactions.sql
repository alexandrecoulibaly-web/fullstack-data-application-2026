-- Étape 4 : exécuter les blocs A et B dans deux sessions psql séparées.

-- Session A : isolation, puis annulation.
BEGIN;
UPDATE items SET tarif_jour = 99.00 WHERE id = 1;
SELECT id, titre, tarif_jour FROM items WHERE id = 1;
-- Session B, avant le ROLLBACK de A :
-- SELECT id, titre, tarif_jour FROM items WHERE id = 1;
ROLLBACK;
-- Relire dans A et B : le tarif doit être 8.50.

-- Refaire le même scénario avec COMMIT au lieu de ROLLBACK :
-- BEGIN;
-- UPDATE items SET tarif_jour = 99.00 WHERE id = 1;
-- COMMIT;
-- Relire dans B : le tarif doit être 99.00.

-- Atomicité : l'erreur met la transaction entière dans l'état aborted.
BEGIN;
INSERT INTO reservations (item_id, borrower_id, date_debut, date_fin, statut)
VALUES (1, 3, DATE '2026-11-01', DATE '2026-11-04', 'active');
UPDATE items SET disponible = FALSE WHERE id = 1;
INSERT INTO reservations (item_id, borrower_id, date_debut, date_fin, statut)
VALUES (1, 999, DATE '2026-11-10', DATE '2026-11-12', 'active');
-- Toute commande suivante, y compris COMMIT, doit signaler l'état aborted.
COMMIT;

-- Vérification après l'échec : aucune des deux premières opérations ne doit persister.
SELECT COUNT(*) AS november_reservations
FROM reservations
WHERE date_debut = DATE '2026-11-01';
SELECT disponible FROM items WHERE id = 1;

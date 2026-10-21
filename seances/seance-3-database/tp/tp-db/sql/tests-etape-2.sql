
-- '1. Email duplicate : viole users_email_key'
INSERT INTO users (email, password_hash, display_name)
VALUES ('alice@esiee.fr', 'fake', 'Alice duplicate');
-- Résultat attendu :
-- ERROR:  duplicate key value violates unique constraint "users_pkey"
-- DETAIL:  Key (id)=(1) already exists.


-- '2. Propriétaire inexistant : viole items_owner_id_fkey'
INSERT INTO items (owner_id, titre, tarif_jour)
VALUES (999, 'Lampe', 1.00);
-- Résultat attendu :
-- ERROR: ERROR:  insert or update on table "items" violates foreign key constraint "items_owner_id_fkey"
-- DETAIL:  Key (owner_id)=(999) is not present in table "users".


-- '3. Tarif négatif : viole items_tarif_jour_check'
INSERT INTO items (owner_id, titre, tarif_jour)
VALUES (1, 'Lampe', -1.00);
-- Résultat attendu :
-- ERROR:  new row for relation "items" violates check constraint "items_tarif_jour_check"
-- DETAIL:  Failing row contains (1, Lampe, -1.00).

-- '4. Dates inversées : viole reservations_dates_check'
INSERT INTO reservations
    (item_id, borrower_id, date_debut, date_fin, statut)
VALUES
    (1, 2, '2026-10-10', '2026-10-05', 'active');
-- Résultat attendu :
-- ERROR:  new row for relation "reservations" violates check constraint "dates_coherentes"
-- DETAIL:  Failing row contains (4, 1, 2, 2026-10-10, 2026-10-05, active).


-- '5. Statut inconnu : viole reservations_statut_check'
INSERT INTO reservations
    (item_id, borrower_id, date_debut, date_fin, statut)
VALUES
    (1, 2, '2026-10-10', '2026-10-15', 'en_attente_peut_etre');
-- Résultat attendu :
-- ERROR:  new row for relation "reservations" violates check constraint "statut_valide"
-- DETAIL:  Failing row contains (5, 1, 2, 2026-10-10, 2026-10-15, en_attente_peut_etre).


-- '6. Suppression de Bob : refusée par reservations_borrower_id_fkey'
DELETE FROM users
WHERE id = 2;
-- Résultat attendu :
-- ERROR:  update or delete on table "users" violates foreign key constraint "reservations_borrower_id_fkey" on table "reservations"
-- DETAIL:  Key (id)=(2) is still referenced from table "reservations".

-- Etape 1 :Effacer la contrainte
-- Etape 2 : Mettre nouvelle contrainte
-- Etape 3 : Supprimer Bob
ALTER TABLE reservations
DROP CONSTRAINT reservations_borrower_id_fkey;

ALTER TABLE reservations
ADD CONSTRAINT reservations_borrower_id_fkey
FOREIGN KEY (borrower_id)
REFERENCES users(id)
ON DELETE CASCADE;

DELETE FROM users
WHERE id = 2;

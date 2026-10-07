-- 1. Items disponibles à moins de 10 EUR/jour.
SELECT id, titre, tarif_jour
FROM items
WHERE disponible AND tarif_jour < 10
ORDER BY tarif_jour ASC;
-- Résultat attendu :
-- 2 | Perceuse       | 5.00
-- 1 | Vélo de ville  | 8.50

-- 2. Recherche insensible à la casse. ILIKE ne neutralise pas les accents.
SELECT id, titre
FROM items
WHERE titre ILIKE '%velo%';
-- Résultat attendu : aucune ligne (le titre contient "é", pas "e").

-- 3. Chaque item avec son propriétaire.
SELECT i.id, i.titre, u.display_name AS proprietaire
FROM items AS i
JOIN users AS u ON u.id = i.owner_id
ORDER BY i.id;
-- Résultat attendu :
-- 1 | Vélo de ville  | Alice
-- 2 | Perceuse       | Alice
-- 3 | Tente 2 places | Bob
-- 4 | Appareil photo | Bob

-- 4. LEFT JOIN pour conserver les items jamais réservés.
SELECT i.id, i.titre, COUNT(r.id) AS nombre_reservations
FROM items AS i
LEFT JOIN reservations AS r ON r.item_id = i.id
GROUP BY i.id, i.titre
ORDER BY i.id;
-- Résultat attendu :
-- 1 | Vélo de ville  | 1
-- 2 | Perceuse       | 0
-- 3 | Tente 2 places | 1
-- 4 | Appareil photo | 1

-- 5. Utilisateurs ayant publié au moins un item.
SELECT u.display_name,
       COUNT(i.id) AS nombre_items,
       ROUND(AVG(i.tarif_jour), 2) AS tarif_moyen
FROM users AS u
JOIN items AS i ON i.owner_id = u.id
GROUP BY u.id, u.display_name
ORDER BY u.id;
-- Résultat attendu :
-- Alice | 2 | 6.75
-- Bob   | 2 | 16.00

-- 6. Réservations actives débutant après le 1er septembre 2026.
SELECT r.id, i.titre, u.display_name AS emprunteur,
       r.date_debut, r.date_fin
FROM reservations AS r
JOIN items AS i ON i.id = r.item_id
JOIN users AS u ON u.id = r.borrower_id
WHERE r.statut = 'active'
  AND r.date_debut > DATE '2026-09-01'
ORDER BY r.date_debut;
-- Résultat attendu :
-- 2 | Tente 2 places | Alice | 2026-09-10 | 2026-09-12
-- 3 | Appareil photo | Chloé | 2026-09-15 | 2026-09-20

-- 7. Deux items les plus chers en sautant le premier.
SELECT id, titre, tarif_jour
FROM items
ORDER BY tarif_jour DESC
OFFSET 1 LIMIT 2;
-- Résultat attendu :
-- 3 | Tente 2 places | 12.00
-- 1 | Vélo de ville  | 8.50

-- 8. Chiffre d'affaires potentiel des réservations actives.
SELECT r.id, i.titre,
       i.tarif_jour * (r.date_fin - r.date_debut) AS chiffre_affaires_potentiel
FROM reservations AS r
JOIN items AS i ON i.id = r.item_id
WHERE r.statut = 'active'
ORDER BY r.id;
-- Résultat attendu :
-- 2 | Tente 2 places | 24.00
-- 3 | Appareil photo | 100.00

# Revue du schéma GearShare

| Point de contrôle | OK / KO | Ce que j'ai corrigé |
|---|---|---|
| Chaque table a une clé primaire | OK | PK sur `users`, `items`, `reservations`, `avis`, `tags` et PK composite sur `item_tags`. |
| Les clés étrangères sont déclarées avec `REFERENCES` | OK | Toutes les relations sont déclarées explicitement. |
| Les `ON DELETE` sont explicites et cohérents avec le métier | OK | Cascade pour le matériel dépendant et les avis/tags de liaison ; emprunteur sans cascade. |
| Un seul avis par réservation via `UNIQUE` | OK | `avis_reservation_id_key`. |
| Note bornée par `CHECK (note BETWEEN 1 AND 5)` | OK | `avis_note_check`. |
| Table item/tag avec clé primaire composite | OK | `PRIMARY KEY (item_id, tag_id)`. |
| Libellé de tag `UNIQUE` | OK | `tags_libelle_key`, avec contrôle complémentaire des minuscules. |
| Contraintes nommées | OK | Les contraintes métier ont toutes un nom explicite. |
| Index sur les clés étrangères | OK | Index ajoutés sur les FK utilisées pour les jointures. |
| Non-chevauchement réellement garanti | OK | `reservations_active_no_overlap` utilise `EXCLUDE USING gist` et `daterange`. |
| Aucun flottant pour un montant, aucun `TIMESTAMP` sans fuseau | OK | `NUMERIC` pour les montants et `TIMESTAMPTZ` pour les horodatages. |

## Décision métier sur la suppression d'un utilisateur

Un compte ne doit pas effacer l'historique des prêts effectués sur son matériel : la FK
`reservations.borrower_id` reste donc restrictive (comportement PostgreSQL par défaut). Les items
du propriétaire sont supprimés en cascade, mais cette suppression est volontairement bloquée s'ils
ont encore des réservations ; l'application devra proposer une désactivation plutôt qu'une
suppression physique dans ce cas. Les avis suivent la réservation et sont supprimés avec elle.

## Mécanismes par règle

1. Avis : FK vers `reservations`, `UNIQUE` sur `reservation_id`, `CHECK` sur la note ; le statut
   `terminee` reste une règle métier à contrôler par l'application ou un trigger.
2. Tags : table `tags` unique et table de liaison `item_tags` à clé primaire composite.
3. Libellés : `UNIQUE` et `CHECK (libelle = LOWER(libelle))`.
4. Réservations actives qui se chevauchent : contrainte PostgreSQL `EXCLUDE` avec `btree_gist`.

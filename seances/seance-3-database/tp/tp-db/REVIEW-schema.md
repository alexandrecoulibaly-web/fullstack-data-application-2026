# Revue du schéma GearShare

| Point de contrôle | OK / KO | Ce que j'ai corrigé |
|---|---|---|
| Chaque table a une clé primaire | OK | Primary Key sur `users`, `items`, `reservations`, `avis`, `tags` et Primary Key composite sur `item_tags`. |
| Les clés étrangères sont déclarées avec `REFERENCES` | OK | Toutes les relations sont déclarées explicitement. |
| Les `ON DELETE` sont explicites et cohérents avec le métier | OK | Cascade pour le matériel dépendant et les avis/tags de liaison ; emprunteur sans cascade. |
| Un seul avis par réservation via `UNIQUE` | OK | `avis_reservation_id_key`. |
| Note bornée par `CHECK (note BETWEEN 1 AND 5)` | OK | `avis_note_check`. |
| Table item/tag avec clé primaire composite | OK | `PRIMARY KEY (item_id, tag_id)`. |
| Libellé de tag `UNIQUE` | OK | `tags_libelle_key`, avec contrôle complémentaire des minuscules. |
| Contraintes nommées | OK | Les contraintes métier ont toutes un nom explicite, y compris le trigger `avis_reservation_terminee`. |
| Index sur les clés étrangères | OK | Index ajoutés sur les FK utilisées pour les jointures. |
| Non-chevauchement réellement garanti | OK | `reservations_active_no_overlap` utilise `EXCLUDE USING gist` et `daterange`. |
| Aucun flottant pour un montant, aucun `TIMESTAMP` sans fuseau | OK | `NUMERIC` pour les montants et `TIMESTAMPTZ` pour les horodatages. |

## Décision métier sur la suppression d'un utilisateur

Pour GearShare, je choisirais de ne pas supprimer automatiquement l'historique des prêts lors de la suppression d'un compte. Un utilisateur peut être propriétaire de matériel emprunté par d'autres personnes, mais également avoir lui-même emprunté du matériel. Supprimer toutes les réservations avec ON DELETE CASCADE ferait perdre une partie de l'historique de ces autres utilisateurs. Je préférerais donc conserver les réservations historiques et gérer la suppression du compte autrement, par exemple en désactivant ou anonymisant l'utilisateur. Les cascades sont adaptées aux données qui n'ont plus de sens sans leur parent, mais l'historique des prêts peut conserver une valeur indépendamment de l'existence du compte.

## Mécanismes par règle

1. Avis : FK vers `reservations`, `UNIQUE` sur `reservation_id`, `CHECK` sur la note et trigger
   `avis_reservation_terminee`. L'emprunteur est identifié sans ambiguïté par
   `reservations.borrower_id` ; l'application doit utiliser cette relation comme auteur de l'avis.
2. Tags : table `tags` unique et table de liaison `item_tags` à clé primaire composite.
3. Libellés : `UNIQUE` et `CHECK (libelle = LOWER(libelle))`.
4. Réservations actives qui se chevauchent : contrainte PostgreSQL `EXCLUDE` avec `btree_gist`.

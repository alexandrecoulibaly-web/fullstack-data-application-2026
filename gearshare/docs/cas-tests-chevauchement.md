# Cas de tests des chevauchements

La règle utilisée est :

```text
date_debut_existante < date_fin_demandee
ET
date_fin_existante > date_debut_demandee
```

Les bornes sont donc ouvertes : deux réservations jointives ne sont pas en
conflit. Chaque test utilise `item_id=1`, `borrower_id=1` et une réservation
existante `2026-01-10` → `2026-01-20`.

| Cas | Créneau demandé | Conflit attendu | Code attendu | Résultat |
|---|---|---:|---:|---|
| Avant | 2026-01-01 → 2026-01-05 | Non | 201 | 201 |
| Après | 2026-01-25 → 2026-01-30 | Non | 201 | 201 |
| Chevauchement au début | 2026-01-05 → 2026-01-12 | Oui | 409 | 409 |
| Chevauchement à la fin | 2026-01-18 → 2026-01-25 | Oui | 409 | 409 |
| Englobant | 2026-01-01 → 2026-01-30 | Oui | 409 | 409 |
| Jointif avant | 2025-12-20 → 2026-01-10 | Non | 201 | 201 |
| Jointif après | 2026-01-20 → 2026-01-25 | Non | 201 | 201 |

Une date inversée ou égale (`date_fin <= date_debut`) est rejetée par le
schéma avec un code 422. L'annulation d'une réservation active renvoie 200 ;
l'annulation d'une réservation déjà annulée renvoie 409.

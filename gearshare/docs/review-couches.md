
| Point de contrôle | OK / KO | Ce que j'ai corrigé |
|---|---|---|
| Aucun SQL ni requête SQLAlchemy dans le router | OK | Le router appelle uniquement `ReservationService`. |
| Aucune `HTTPException` dans le service | OK | Le service lève uniquement les exceptions métier. |
| Aucun `commit()` dans le repository | OK | La transaction reste gérée par `get_db`. |
| `response_model` sur les 4 routes | OK | Les quatre routes déclarent `ReservationRead` ou sa liste. |
| Schéma de lecture construit depuis SQLAlchemy, sans champ interne | OK | `ReservationRead` et `ItemSummary` utilisent `from_attributes`. |
| Requête de chevauchement couvrant les cinq cas et l'englobant | OK | Deux comparaisons ouvertes couvrent les trois conflits. |
| Pas de f-string dans une requête SQL | OK | Les filtres passent par SQLAlchemy et la migration utilise des SQL statiques. |
| Pas de N+1 sur `GET /reservations` | OK | `joinedload(Reservation.item)` charge l'item avec la liste. |
| Migration relue, `downgrade()` testé | OK | La migration initiale a été relue et son cycle est validé avec PostgreSQL. |
| Aucune dépendance ajoutée sans justification | OK | Aucune nouvelle dépendance n'a été ajoutée. |


### 6.3. Reviewez

Remplissez ce tableau dans un fichier `REVIEW.md` :

| Point de contrôle | OK / KO | Ce que j'ai corrigé |
|---|---|---|
| Les codes de statut correspondent à la spec (201, 404, 409) | OK | Aucune correction nécessaire : création en 201, 404 pour absence, 409 pour réservation déjà annulée. |
| `response_model` présent sur les 4 routes | OK | Les routes de lecture, liste, création et annulation exposent bien le modèle de sortie attendu. |
| La validation `date_fin > date_debut` est bien dans le schéma Pydantic | OK | J’ai mis la validation dans `ReservationCreate` avec un `model_validator` pour éviter la logique dans le router. |
| Le router n'accède pas au stockage de `items` | OK | Le stockage est isolé dans `FAKE_DB` du router `reservations`, sans accès au dictionnaire des `items`. |
| Pas d'`async def` sans `await` | OK | Aucun endpoint asynchrone n’a été ajouté, donc pas de faux `async def` inutile. |
| Aucune dépendance ajoutée dans `requirements.txt` (ou justifiée) | OK | Aucune dépendance externe n’a été requise pour cette ressource. |
| Les routes littérales sont déclarées avant les routes paramétrées | KO | La route `GET /{reservation_id}` est déclarée avant `GET ""`; il faut placer les routes littérales avant les routes paramétrées pour respecter la convention de la spec. |
| Le code renvoie une réponse cohérente pour `POST /reservations/999/annuler` | OK | Le code renvoie bien 404 si la réservation n’existe pas et 409 si elle est déjà annulée. |
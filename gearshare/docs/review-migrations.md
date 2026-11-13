# Revue des migrations et de l'étape 4

## Migration initiale

La migration `c1c722c2828c_schema_initial.py` crée les tables dans l'ordre
`users`, `items`, puis `reservations`. Elle contient les deux contraintes de
`items` et les deux contraintes de `reservations`, les clés étrangères avec
leurs actions `ondelete`, ainsi que les index sur les clés étrangères. Son
`downgrade()` supprime les index et les tables dans l'ordre inverse.

Le modèle `Item` utilise `Numeric(8, 2)` pour `tarif_jour`, et les dates et
contraintes sont reproduites dans la migration. La migration est donc prête
pour un test `upgrade`/`downgrade`; ce test doit être exécuté avec PostgreSQL.

## Piège du renommage

Une autogénération Alembic ne connaît pas l'intention d'un renommage : elle
peut produire la suppression de `tarif_jour` suivie de la création de
`prix_jour`. Appliquer cette migration ferait perdre les valeurs existantes.
La correction attendue est `op.alter_column("items", "tarif_jour",
new_column_name="prix_jour")`, avec l'opération inverse dans `downgrade()`.
La migration d'exercice est ensuite supprimée et le modèle conserve
`tarif_jour`.

## Traduction des exceptions

Un gestionnaire global dans `app/main.py` traduit les exceptions métier en
réponses HTTP. Ce choix évite de répéter le même `try/except` dans chaque
route, tout en laissant les services indépendants de FastAPI.

## Étape 5 — N+1 sur le propriétaire

Le schéma `OwnerRead` expose uniquement `id` et `display_name`. Il n'expose
ni `email` ni `password_hash`. Le repository charge la relation `Item.owner`
avec `joinedload`, avant la sérialisation Pydantic.

Avec `SQL_ECHO=true`, une page contrôlée de 20 items mesurait auparavant
**21 requêtes `SELECT`** : une requête pour les items, puis une requête par
propriétaire lors de la sérialisation. Après l'ajout de `joinedload`, la même
page mesure **1 requête `SELECT`**, car les propriétaires sont récupérés dans
la requête initiale.

La mesure a été faite avec une base PostgreSQL locale Docker et la requête
`GET /items?limit=50`. La réponse contient bien le propriétaire public de
chaque item et les logs ne contiennent qu'une requête `SELECT` pour la liste.
Le test contrôlé de 20 items a donné les chiffres ci-dessus. `SQL_ECHO` a été
remis à `false` après la vérification.

## Modifications du frontend à l'étape 6.4

Le contrat de création d'un item exige désormais `owner_id`, et le contrat de
création d'une réservation exige `borrower_id`. Le frontend envoie donc
provisoirement `owner_id=1` et `borrower_id=1` depuis ses routes de création,
avec la valeur signalée par `TODO séance 5`; ces identifiants correspondent à
l'utilisateur de démonstration inséré dans PostgreSQL.

Le frontend conserve le traitement des erreurs `422` de validation pour la
création d'un item et affiche aussi les `409` du backend sur le formulaire de
réservation. Il affiche ainsi le message métier en cas de créneau déjà
réservé, au lieu de renvoyer vers la page d'erreur générique.

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

## État des vérifications

Les comptages N+1, les tests HTTP avec Docker et les modifications du frontend
appartiennent aux étapes 5 et 6 ; ils ne sont pas déclarés comme effectués
dans ce livrable.

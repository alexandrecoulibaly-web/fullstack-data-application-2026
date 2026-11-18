# Choix de migration au démarrage

## Option retenue

Nous retenons l'option 2 : un service Compose `migrate`, construit depuis la
même image que le backend, exécute `alembic upgrade head`. Le service `db`
doit être `healthy` avant son démarrage et le service `backend` attend que
`migrate` se termine avec succès.

Le service `frontend` ne reçoit pas `env_file`. Il utilise uniquement
`API_BASE_URL`, car il ne se connecte pas directement à PostgreSQL.

## Réponses aux questions

1. Au deuxième `docker compose up`, Alembic lit la table
   `alembic_version`, constate que la base est déjà à `head` et termine sans
   modifier les tables. Le service `migrate` sort avec le code 0, puis le
   backend démarre.
2. Si une migration échoue, `migrate` sort avec un code différent de 0 et ses
   logs contiennent l'erreur Alembic. La condition
   `service_completed_successfully` n'est pas satisfaite : le backend ne
   démarre pas.
3. Avec plusieurs instances, chaque processus pourrait tenter la migration.
   Alembic et PostgreSQL doivent alors sérialiser l'opération, mais cette
   course n'est pas une stratégie de déploiement suffisante. En production,
   les migrations doivent être exécutées par une étape de déploiement unique
   avant de lancer les instances applicatives.
4. Le `--reload` du backend ne relance pas le service `migrate` : il ne
   concerne que le processus Uvicorn du backend. Le service de migration
   termine avant le premier démarrage de celui-ci.

Cette option sépare clairement la migration et empêche l'API de démarrer si le schéma n'est
pas prêt.

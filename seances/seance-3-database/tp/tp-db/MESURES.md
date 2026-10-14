# Mesures `EXPLAIN ANALYZE`

Les valeurs ci-dessous sont à remplir après exécution dans PostgreSQL 16. Les temps dépendent de
la machine et du cache, donc on conserve le plan et le `Execution Time` réellement observés.

## Génération du volume

```sql
INSERT INTO items (owner_id, titre, description, tarif_jour)
SELECT 1,
       'Item de test ' || n,
       NULL,
       ROUND((1 + random() * 50)::numeric, 2)
FROM generate_series(1, 200000) AS n;

ANALYZE items;
```

## Recherche exacte avant et après index

À exécuter avant l'index, puis après `CREATE INDEX items_titre_idx ON items (titre);` et
`ANALYZE items;`.

```sql
EXPLAIN ANALYZE
SELECT * FROM items WHERE titre = 'Item de test 123456';
```

| Mesure | Avant index | Après index |
|---|---:|---:|
| Execution Time (ms) | 11.747 ms | 0.061 ms |

Facteur d'accélération : `temps_avant / temps_après = ...`.

## Cas subtils

```sql
EXPLAIN ANALYZE
SELECT * FROM items WHERE titre LIKE '%123456';

CREATE INDEX items_disponible_idx ON items (disponible);
ANALYZE items;

EXPLAIN ANALYZE
SELECT * FROM items WHERE disponible = TRUE;

EXPLAIN ANALYZE
SELECT * FROM items WHERE disponible = FALSE;
```

- Le `LIKE '%123456'` ne bénéficie généralement pas d'un B-tree sur `titre`, car le joker en
  tête empêche de chercher un préfixe trié.
- Un index booléen peut être ignoré pour `disponible = TRUE` si presque toutes les lignes sont
  vraies : un parcours séquentiel peut coûter moins cher.
- Le plan de `disponible = FALSE` dépend de la sélectivité réellement observée ; si les lignes
  fausses sont rares, l'index peut être choisi.

Question bonus : mesurez aussi `titre LIKE 'Item de test 123456%'` et comparez avec le cas du
joker en tête.

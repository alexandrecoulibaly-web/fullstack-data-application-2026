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

```sql
EXPLAIN ANALYZE
SELECT * FROM items WHERE titre = 'Item de test 123456';
```

| Mesure | Avant index | Après index |
|---|---:|---:|
| Execution Time (ms) | 11.747 ms | 0.061 ms |

Facteur d'accélération : `temps_avant / temps_après = 192,57`.

## Cas subtils

(a)
```sql
EXPLAIN ANALYZE
SELECT * FROM items WHERE titre LIKE '%123456';

CREATE INDEX items_disponible_idx ON items (disponible);
ANALYZE items;
```
Résultat : 
```
 Gather  (cost=1000.00..7211.29 rows=40 width=74) (actual time=25.273..27.578 rows=2 loops=1)
   Workers Planned: 2
   Workers Launched: 2
   ->  Parallel Seq Scan on items  (cost=0.00..6207.29 rows=17 width=74) (actual time=16.083..21.830 rows=1 loops=3)
         Filter: ((titre)::text ~~ '%123456'::text)
         Rows Removed by Filter: 133334
 Planning Time: 1.050 ms
 Execution Time: 27.614 ms
```

==> Le noeud principal est Parallel Seq Scan. Le `LIKE '%123456'` ne bénéficie généralement pas d'un B-tree sur `titre`, car le joker en
  tête empêche de chercher un préfixe trié. Alors il parcourt toute la table d'où l'Execution Time conséquent. 

(b)  
```sql
EXPLAIN ANALYZE
SELECT * FROM items WHERE disponible = TRUE;

EXPLAIN ANALYZE
SELECT * FROM items WHERE disponible = FALSE;
```
Résultat : 
```
TRUE :  Seq Scan on items  (cost=0.00..8124.04 rows=400004 width=82) (actual time=0.040..50.964 rows=400004 loops=1)
   Filter: disponible
 Planning Time: 0.252 ms
 Execution Time: 65.337 ms
(4 rows)

FALSE :  Index Scan using items_disponible_idx on items  (cost=0.42..4.44 rows=1 width=82) (actual time=0.149..0.150 rows=0 loops=1)
   Index Cond: (disponible = false)
 Planning Time: 0.092 ms
 Execution Time: 0.170 ms
(4 rows)
```

==> Presque toutes les lignes sont vraies, alors l'index coûterait plus cher que parcourir toutes les lignes. A l'inverse, si presque aucune ligne n'est fausse, alors l'utilisation de l'index est pertinent. 

CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE avis (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    reservation_id BIGINT NOT NULL,
    note INTEGER NOT NULL,
    commentaire TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT avis_pkey PRIMARY KEY (id),
    CONSTRAINT avis_reservation_id_key UNIQUE (reservation_id),
    CONSTRAINT avis_note_check CHECK (note BETWEEN 1 AND 5),
    CONSTRAINT avis_reservation_id_fkey
        FOREIGN KEY (reservation_id) REFERENCES reservations(id) ON DELETE CASCADE
);

CREATE INDEX avis_reservation_id_idx ON avis (reservation_id);

CREATE TABLE tags (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    libelle VARCHAR(80) NOT NULL,
    CONSTRAINT tags_pkey PRIMARY KEY (id),
    CONSTRAINT tags_libelle_key UNIQUE (libelle),
    CONSTRAINT tags_libelle_lowercase_check CHECK (libelle = LOWER(libelle))
);

CREATE TABLE item_tags (
    item_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,
    CONSTRAINT item_tags_pkey PRIMARY KEY (item_id, tag_id),
    CONSTRAINT item_tags_item_id_fkey
        FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    CONSTRAINT item_tags_tag_id_fkey
        FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE INDEX item_tags_tag_id_idx ON item_tags (tag_id);

ALTER TABLE reservations
    ADD CONSTRAINT reservations_active_no_overlap
    EXCLUDE USING gist (
        item_id WITH =,
        daterange(date_debut, date_fin, '[)') WITH &&
    )
    WHERE (statut = 'active');

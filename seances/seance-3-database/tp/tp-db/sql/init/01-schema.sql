CREATE TABLE users (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    email VARCHAR(255) NOT NULL,
    password_hash TEXT NOT NULL,
    display_name VARCHAR(80) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email)
);

CREATE TABLE items (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    owner_id BIGINT NOT NULL,
    titre VARCHAR(120) NOT NULL,
    description TEXT,
    tarif_jour NUMERIC(10, 2) NOT NULL,
    disponible BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT items_pkey PRIMARY KEY (id),
    CONSTRAINT items_tarif_jour_check CHECK (tarif_jour > 0),
    CONSTRAINT items_owner_id_fkey
        FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX items_owner_id_idx ON items (owner_id);

CREATE TABLE reservations (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    item_id BIGINT NOT NULL,
    borrower_id BIGINT NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    statut VARCHAR(20) NOT NULL DEFAULT 'active',
    CONSTRAINT reservations_pkey PRIMARY KEY (id),
    CONSTRAINT reservations_dates_check CHECK (date_fin > date_debut),
    CONSTRAINT reservations_statut_check
        CHECK (statut IN ('active', 'annulee', 'terminee')),
    CONSTRAINT reservations_item_id_fkey
        FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    CONSTRAINT reservations_borrower_id_fkey
        FOREIGN KEY (borrower_id) REFERENCES users(id)
);

CREATE INDEX reservations_item_id_idx ON reservations (item_id);
CREATE INDEX reservations_borrower_id_idx ON reservations (borrower_id);

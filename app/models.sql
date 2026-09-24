-- Criação das tabelas do Agro Zap em PostgreSQL + PostGIS.

CREATE TABLE IF NOT EXISTS messages (
    message_id TEXT PRIMARY KEY,
    sender TEXT NOT NULL,
    sent_at TIMESTAMPTZ NOT NULL,
    received_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    message_type TEXT NOT NULL,
    text_body TEXT NULL,
    payload JSONB NOT NULL
);



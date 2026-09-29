-- Criação das tabelas do Agro Zap em PostgreSQL + PostGIS.

CREATE TABLE messages (
    message_id TEXT PRIMARY KEY,
    sender TEXT NOT NULL,
    sent_at TIMESTAMPTZ NOT NULL,
    received_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    message_type TEXT NOT NULL,
    text_body TEXT NULL,
    payload JSONB NOT NULL
);

CREATE TABLE message_media (
    message_id TEXT PRIMARY KEY,
    media_id TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    file_path TEXT,
    download_status TEXT NOT NULL DEFAULT 'pending' 
    CHECK(download_status IN ('pending', 'downloaded', 'downloading', 'error')),
    download_started_at TIMESTAMPTZ NULL,
    transcription_text TEXT,
    transcription_status TEXT NOT NULL DEFAULT 'pending'
    CHECK(transcription_status IN ('pending', 'processing', 'completed', 'error')),
    transcription_started_at TIMESTAMPTZ NULL,
    CONSTRAINT fk_message FOREIGN KEY (message_id)
    REFERENCES messages(message_id)
);

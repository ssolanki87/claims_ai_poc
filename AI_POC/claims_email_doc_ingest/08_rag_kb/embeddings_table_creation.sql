-- SQL to create embeddings table for RAG KB
CREATE TABLE kb_embeddings (
    id INT IDENTITY(1,1) PRIMARY KEY,
    text NVARCHAR(MAX),
    embedding VARBINARY(MAX),
    created_at DATETIME DEFAULT GETDATE()
);

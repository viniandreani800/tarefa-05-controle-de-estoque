PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS produtos (
    codigo TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    categoria TEXT,
    preco REAL NOT NULL CHECK(preco >= 0),
    quantidade INTEGER NOT NULL DEFAULT 0 CHECK(quantidade >= 0),
    estoque_minimo INTEGER NOT NULL DEFAULT 5 CHECK(estoque_minimo >= 0)
);

CREATE TABLE IF NOT EXISTS movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_codigo TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('entrada', 'saida')),
    quantidade INTEGER NOT NULL CHECK(quantidade > 0),
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_codigo) REFERENCES produtos (codigo)
);
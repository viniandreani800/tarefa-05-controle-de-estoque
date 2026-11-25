# Sistema de Controle de Estoque com GUI e SQLite (INE5201)

**Disciplina:** INE5201 - Introdução à Ciência da Computação com Python (UFSC)  
**Aluno:** Vinicius Andreani  

## Descrição do Projeto
Aplicação desktop modular em Python com interface gráfica em `tkinter` (`ttk`) e banco de dados relacional `SQLite` para gerenciar o controle de estoque. O sistema integra cadastro de produtos, registro de entradas e saídas com controle automático de saldo e bloqueio de saída acima do estoque disponível, consulta com filtros, alertas de estoque baixo, cálculo de valor total em estoque, histórico de movimentações, relatórios e exportação para CSV.

## Diagrama e Esquema do Banco de Dados
Relacionamento entre as tabelas `produtos` e `movimentacoes` (`1:N`, onde cada produto pode ter várias movimentações registradas):

```text
+-----------------------------------+          1          +-----------------------------------+
|             produtos              |<>-------------------|           movimentacoes           |
+-----------------------------------+          N          +-----------------------------------+
| PK codigo (TEXT)                  |                     | PK id (INTEGER AUTOINCREMENT)     |
|    nome (TEXT NOT NULL)           |                     | FK produto_codigo (TEXT) -------->|
|    categoria (TEXT)               |                     |    tipo (TEXT: 'entrada'|'saida') |
|    preco (REAL NOT NULL)          |                     |    quantidade (INTEGER NOT NULL)  |
|    quantidade (INTEGER DEFAULT 0) |                     |    data (TIMESTAMP DEFAULT NOW)   |
|    estoque_minimo (INT DEFAULT 5)|                     +-----------------------------------+
+-----------------------------------+
```

Script SQL principal (`banco.sql`):

```sql
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
```

## Estrutura do Projeto
* `banco.sql` — Script de criação das tabelas e restrições de integridade.
* `conexao.py` — Conexão SQLite com `PRAGMA foreign_keys = ON` e inicialização do banco.
* `validacoes.py` — Validação de campos obrigatórios, valores numéricos não negativos e quantidades.
* `produtos.py` — Operações CRUD, consulta filtrada, alerta de estoque baixo e cálculo de valor total.
* `movimentacoes.py` — Registro de entradas e saídas, verificação de saldo disponível e histórico.
* `exportacao.py` — Exportação de relatórios de estoque e histórico para CSV e geração de resumo textual.
* `menu_principal.py` — Janela principal com indicadores em tempo real e navegação entre módulos.
* `cadastro_produtos.py` — Interface gráfica de cadastro, edição e exclusão de produtos.
* `registro_movimentacao.py` — Interface gráfica para lançar entradas e saídas e acompanhar movimentações.
* `consulta_estoque.py` — Consulta de estoque por categoria/alerta, histórico e exportação CSV.
* `relatorios.py` — Visualização de indicadores, alertas de estoque baixo e exportação.
* `main.py` — Ponto de entrada da aplicação.

## Funcionalidades Implementadas
* Menu principal com indicadores em tempo real e navegação entre telas.
* Cadastro de produtos com validação de código único e preço/estoque mínimo não negativos.
* Registro de entradas e saídas com atualização de saldo e bloqueio quando a saída excede o estoque atual.
* Consulta de estoque atual, filtro por categoria, alerta de estoque baixo e cálculo de valor total em estoque (`preco * quantidade`).
* Histórico de movimentações e exportação para `.csv`.

## Como Executar
1. Tenha o Python 3 instalado.
2. Abra o terminal na pasta do projeto e execute:
   ```bash
   python main.py
   ```

## Capturas de Tela
* Menu Principal: `tela-menu.png`
* Cadastro de Produtos: `tela-produtos.png`
* Registro de Movimentações: `tela-movimentacoes.png`
* Consulta de Estoque e Relatórios: `tela-consulta.png`

## Relato Detalhado de Uso do GitHub Copilot
O GitHub Copilot foi utilizado no VS Code durante o desenvolvimento modular do sistema para acelerar a escrita de trechos repetitivos de interface em `tkinter`/`ttk`, sugerir estruturas de consultas SQL parametrizadas com `sqlite3` e apoiar na organização de funções auxiliares e validações de entrada. Todas as regras de negócio — como a exigência de `PRAGMA foreign_keys = ON`, o bloqueio de saídas maiores que o saldo disponível, a separação em módulos e os testes na interface gráfica — foram revisadas, testadas e ajustadas manualmente para atender integralmente aos requisitos da disciplina.

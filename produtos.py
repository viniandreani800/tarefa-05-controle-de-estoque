from conexao import conectar


def criar_produto(codigo, nome, categoria, preco, estoque_minimo):
    with conectar() as conn:
        existente = conn.execute(
            "SELECT codigo FROM produtos WHERE codigo = ?", (codigo,)
        ).fetchone()
        if existente:
            return False, f"Já existe um produto com o código '{codigo}'."

        conn.execute(
            """
            INSERT INTO produtos (codigo, nome, categoria, preco, quantidade, estoque_minimo)
            VALUES (?, ?, ?, ?, 0, ?)
            """,
            (codigo, nome, categoria, preco, estoque_minimo),
        )
        conn.commit()
    return True, "Produto cadastrado com sucesso."


def atualizar_produto(codigo, nome, categoria, preco, estoque_minimo):
    with conectar() as conn:
        cur = conn.execute(
            """
            UPDATE produtos
               SET nome = ?, categoria = ?, preco = ?, estoque_minimo = ?
             WHERE codigo = ?
            """,
            (nome, categoria, preco, estoque_minimo, codigo),
        )
        conn.commit()
        if cur.rowcount == 0:
            return False, "Produto não encontrado."
    return True, "Produto atualizado com sucesso."


def excluir_produto(codigo):
    with conectar() as conn:
        tem_mov = conn.execute(
            "SELECT 1 FROM movimentacoes WHERE produto_codigo = ? LIMIT 1", (codigo,)
        ).fetchone()
        if tem_mov:
            return False, "Não é possível excluir produto que já possui movimentações."

        cur = conn.execute("DELETE FROM produtos WHERE codigo = ?", (codigo,))
        conn.commit()
        if cur.rowcount == 0:
            return False, "Produto não encontrado."
    return True, "Produto excluído com sucesso."


def listar_produtos(categoria=None, apenas_baixo_estoque=False):
    sql = """
        SELECT codigo, nome, categoria, preco, quantidade, estoque_minimo,
               (preco * quantidade) AS valor_total
          FROM produtos
         WHERE 1=1
    """
    params = []

    if categoria and categoria != "Todas":
        sql += " AND categoria = ?"
        params.append(categoria)

    if apenas_baixo_estoque:
        sql += " AND quantidade <= estoque_minimo"

    sql += " ORDER BY nome ASC"

    with conectar() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


def listar_categorias():
    with conectar() as conn:
        rows = conn.execute(
            "SELECT DISTINCT categoria FROM produtos WHERE categoria IS NOT NULL AND categoria != '' ORDER BY categoria"
        ).fetchall()
    return ["Todas"] + [r["categoria"] for r in rows]


def resumo_estoque():
    with conectar() as conn:
        row = conn.execute(
            """
            SELECT COUNT(*) AS total_produtos,
                   COALESCE(SUM(quantidade), 0) AS total_itens,
                   COALESCE(SUM(preco * quantidade), 0.0) AS valor_total,
                   SUM(CASE WHEN quantidade <= estoque_minimo THEN 1 ELSE 0 END) AS alertas_baixo
              FROM produtos
            """
        ).fetchone()
    return {
        "total_produtos": row["total_produtos"] or 0,
        "total_itens": row["total_itens"] or 0,
        "valor_total": float(row["valor_total"] or 0.0),
        "alertas_baixo": row["alertas_baixo"] or 0,
    }
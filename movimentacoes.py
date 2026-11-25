from conexao import conectar


def registrar_movimentacao(codigo, tipo, quantidade):
    with conectar() as conn:
        prod = conn.execute(
            "SELECT codigo, nome, quantidade FROM produtos WHERE codigo = ?", (codigo,)
        ).fetchone()
        if not prod:
            return False, f"Produto com código '{codigo}' não encontrado."

        qtd_atual = prod["quantidade"]
        if tipo == "saida" and quantidade > qtd_atual:
            return (
                False,
                f"Estoque insuficiente para '{prod['nome']}'. Disponível: {qtd_atual}, solicitado: {quantidade}.",
            )

        nova_qtd = qtd_atual + quantidade if tipo == "entrada" else qtd_atual - quantidade

        conn.execute(
            "INSERT INTO movimentacoes (produto_codigo, tipo, quantidade) VALUES (?, ?, ?)",
            (codigo, tipo, quantidade),
        )
        conn.execute(
            "UPDATE produtos SET quantidade = ? WHERE codigo = ?",
            (nova_qtd, codigo),
        )
        conn.commit()

    rotulo = "Entrada" if tipo == "entrada" else "Saída"
    return True, f"{rotulo} registrada com sucesso. Novo saldo de '{prod['nome']}': {nova_qtd}."


def listar_movimentacoes(codigo_produto=None):
    sql = """
        SELECT m.id,
               m.data,
               m.produto_codigo,
               p.nome AS produto_nome,
               m.tipo,
               m.quantidade
          FROM movimentacoes m
          JOIN produtos p ON p.codigo = m.produto_codigo
         WHERE 1=1
    """
    params = []
    if codigo_produto:
        sql += " AND m.produto_codigo = ?"
        params.append(codigo_produto)

    sql += " ORDER BY m.id DESC"

    with conectar() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]
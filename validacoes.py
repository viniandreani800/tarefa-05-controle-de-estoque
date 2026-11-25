def validar_produto(codigo, nome, categoria, preco_str, estoque_min_str):
    codigo = (codigo or "").strip()
    nome = (nome or "").strip()
    categoria = (categoria or "Geral").strip() or "Geral"

    if not codigo:
        return False, "O código do produto é obrigatório.", None
    if not nome:
        return False, "O nome do produto é obrigatório.", None

    try:
        preco = float(str(preco_str).replace(",", ".").strip())
        if preco < 0:
            return False, "O preço não pode ser negativo.", None
    except ValueError:
        return False, "Informe um preço numérico válido.", None

    try:
        estoque_min = int(str(estoque_min_str).strip())
        if estoque_min < 0:
            return False, "O estoque mínimo não pode ser negativo.", None
    except ValueError:
        return False, "Informe um estoque mínimo inteiro válido.", None

    return True, "", {
        "codigo": codigo,
        "nome": nome,
        "categoria": categoria,
        "preco": preco,
        "estoque_minimo": estoque_min,
    }


def validar_movimentacao(codigo, tipo, qtd_str):
    codigo = (codigo or "").strip()
    if not codigo:
        return False, "Selecione ou informe o código do produto.", 0
    if tipo not in ("entrada", "saida"):
        return False, "Tipo de movimentação inválido.", 0
    try:
        qtd = int(str(qtd_str).strip())
        if qtd <= 0:
            return False, "A quantidade deve ser maior que zero.", 0
    except ValueError:
        return False, "Informe uma quantidade inteira válida.", 0
    return True, "", qtd
import csv
from pathlib import Path
from produtos import listar_produtos, resumo_estoque
from movimentacoes import listar_movimentacoes


def exportar_estoque_csv(caminho_arquivo=None, categoria=None, apenas_baixo_estoque=False):
    destino = Path(caminho_arquivo) if caminho_arquivo else Path(__file__).resolve().parent / "relatorio_estoque.csv"
    produtos = listar_produtos(categoria=categoria, apenas_baixo_estoque=apenas_baixo_estoque)

    with open(destino, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Código", "Nome", "Categoria", "Preço (R$)", "Quantidade", "Estoque Mínimo", "Valor Total (R$)"])
        for p in produtos:
            writer.writerow([
                p["codigo"],
                p["nome"],
                p["categoria"] or "",
                f"{p['preco']:.2f}",
                p["quantidade"],
                p["estoque_minimo"],
                f"{p['valor_total']:.2f}",
            ])
    return str(destino)


def exportar_movimentacoes_csv(caminho_arquivo=None):
    destino = Path(caminho_arquivo) if caminho_arquivo else Path(__file__).resolve().parent / "historico_movimentacoes.csv"
    movs = listar_movimentacoes()

    with open(destino, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["ID", "Data", "Código Produto", "Produto", "Tipo", "Quantidade"])
        for m in movs:
            writer.writerow([
                m["id"],
                m["data"],
                m["produto_codigo"],
                m["produto_nome"],
                m["tipo"],
                m["quantidade"],
            ])
    return str(destino)


def gerar_texto_relatorio():
    resumo = resumo_estoque()
    alertas = listar_produtos(apenas_baixo_estoque=True)
    linhas = [
        "=== RELATÓRIO GERAL DE ESTOQUE ===",
        f"Total de produtos cadastrados: {resumo['total_produtos']}",
        f"Total de unidades em estoque: {resumo['total_itens']}",
        f"Valor total em estoque: R$ {resumo['valor_total']:.2f}",
        f"Produtos em estoque baixo: {resumo['alertas_baixo']}",
        "",
        "--- ALERTA DE ESTOQUE BAIXO ---",
    ]
    if not alertas:
        linhas.append("Nenhum produto abaixo ou no estoque mínimo.")
    else:
        for item in alertas:
            linhas.append(
                f"[{item['codigo']}] {item['nome']} ({item['categoria']}) -> "
                f"Qtd: {item['quantidade']} | Mín: {item['estoque_minimo']}"
            )
    return "\n".join(linhas)
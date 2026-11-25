import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from produtos import listar_produtos, listar_categorias
from movimentacoes import listar_movimentacoes
from exportacao import exportar_estoque_csv, exportar_movimentacoes_csv


class TelaConsultaEstoque(tk.Toplevel):
    def __init__(self, master, on_atualizar=None):
        super().__init__(master)
        self.title("Consulta de Estoque e Histórico")
        self.geometry("880x540")
        self.on_atualizar = on_atualizar
        self._montar_ui()
        self._carregar_dados()

    def _montar_ui(self):
        filtros = ttk.LabelFrame(self, text="Filtros e Exportação", padding=10)
        filtros.pack(fill="x", padx=10, pady=8)

        ttk.Label(filtros, text="Categoria:").pack(side="left", padx=(0, 4))
        self.cmb_cat = ttk.Combobox(filtros, values=["Todas"], width=18, state="readonly")
        self.cmb_cat.set("Todas")
        self.cmb_cat.pack(side="left", padx=(0, 10))
        self.cmb_cat.bind("<<ComboboxSelected>>", lambda _e: self._carregar_dados())

        self.var_baixo = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            filtros,
            text="Apenas estoque baixo (<= mínimo)",
            variable=self.var_baixo,
            command=self._carregar_dados,
        ).pack(side="left", padx=8)

        ttk.Button(filtros, text="Exportar Estoque CSV", command=self._exp_estoque).pack(side="right", padx=4)
        ttk.Button(filtros, text="Exportar Mov. CSV", command=self._exp_movs).pack(side="right", padx=4)

        self.lbl_resumo = ttk.Label(self, text="", font=("Segoe UI", 10, "bold"))
        self.lbl_resumo.pack(fill="x", padx=12, pady=(0, 6))

        ttk.Label(self, text="Estoque Atual", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=12)
        cols_p = ("codigo", "nome", "categoria", "preco", "quantidade", "estoque_minimo", "valor_total", "status")
        self.tree_prod = ttk.Treeview(self, columns=cols_p, show="headings", height=9)
        tit_p = {
            "codigo": "Código",
            "nome": "Nome",
            "categoria": "Categoria",
            "preco": "Preço (R$)",
            "quantidade": "Qtd",
            "estoque_minimo": "Mínimo",
            "valor_total": "Valor Total (R$)",
            "status": "Status",
        }
        for c in cols_p:
            self.tree_prod.heading(c, text=tit_p[c])
            self.tree_prod.column(c, width=100, anchor="center")
        self.tree_prod.column("nome", width=170, anchor="w")
        self.tree_prod.pack(fill="both", expand=True, padx=10, pady=(2, 8))

        ttk.Label(self, text="Histórico de Movimentações", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=12)
        cols_m = ("id", "data", "codigo", "produto", "tipo", "quantidade")
        self.tree_mov = ttk.Treeview(self, columns=cols_m, show="headings", height=7)
        tit_m = {
            "id": "ID",
            "data": "Data/Hora",
            "codigo": "Código",
            "produto": "Produto",
            "tipo": "Tipo",
            "quantidade": "Quantidade",
        }
        for c in cols_m:
            self.tree_mov.heading(c, text=tit_m[c])
            self.tree_mov.column(c, width=110, anchor="center")
        self.tree_mov.column("data", width=160)
        self.tree_mov.column("produto", width=210, anchor="w")
        self.tree_mov.pack(fill="both", expand=True, padx=10, pady=(2, 10))

    def _carregar_dados(self):
        cat_atual = self.cmb_cat.get() or "Todas"
        categorias = listar_categorias()
        self.cmb_cat["values"] = categorias
        self.cmb_cat.set(cat_atual if cat_atual in categorias else "Todas")

        cat = self.cmb_cat.get()
        apenas_baixo = self.var_baixo.get()
        prods = listar_produtos(categoria=cat, apenas_baixo_estoque=apenas_baixo)

        for item in self.tree_prod.get_children():
            self.tree_prod.delete(item)

        valor_filtro = 0.0
        alertas = 0
        for p in prods:
            baixo = p["quantidade"] <= p["estoque_minimo"]
            if baixo:
                alertas += 1
            valor_filtro += float(p["valor_total"])
            status = "ESTOQUE BAIXO" if baixo else "OK"
            self.tree_prod.insert(
                "",
                "end",
                values=(
                    p["codigo"],
                    p["nome"],
                    p["categoria"],
                    f"{p['preco']:.2f}",
                    p["quantidade"],
                    p["estoque_minimo"],
                    f"{p['valor_total']:.2f}",
                    status,
                ),
            )

        self.lbl_resumo.config(
            text=f"Produtos exibidos: {len(prods)}  |  Valor total filtrado: R$ {valor_filtro:.2f}  |  Alertas de estoque baixo: {alertas}"
        )

        for item in self.tree_mov.get_children():
            self.tree_mov.delete(item)
        for m in listar_movimentacoes():
            self.tree_mov.insert(
                "",
                "end",
                values=(m["id"], m["data"], m["produto_codigo"], m["produto_nome"], m["tipo"], m["quantidade"]),
            )

        if self.on_atualizar:
            self.on_atualizar()

    def _exp_estoque(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")],
            initialfile="relatorio_estoque.csv",
            parent=self,
        )
        if not caminho:
            return
        gerado = exportar_estoque_csv(
            caminho_arquivo=caminho,
            categoria=self.cmb_cat.get(),
            apenas_baixo_estoque=self.var_baixo.get(),
        )
        messagebox.showinfo("Exportado", f"Relatório salvo em:\n{gerado}", parent=self)

    def _exp_movs(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")],
            initialfile="historico_movimentacoes.csv",
            parent=self,
        )
        if not caminho:
            return
        gerado = exportar_movimentacoes_csv(caminho_arquivo=caminho)
        messagebox.showinfo("Exportado", f"Histórico salvo em:\n{gerado}", parent=self)
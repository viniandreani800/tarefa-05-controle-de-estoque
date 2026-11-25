import tkinter as tk
from tkinter import ttk, messagebox
from validacoes import validar_movimentacao
from produtos import listar_produtos
from movimentacoes import registrar_movimentacao, listar_movimentacoes


class TelaRegistroMovimentacao(tk.Toplevel):
    def __init__(self, master, on_atualizar=None):
        super().__init__(master)
        self.title("Entradas e Saídas de Estoque")
        self.geometry("800x480")
        self.on_atualizar = on_atualizar
        self._montar_ui()
        self._carregar_produtos()
        self._carregar_historico()

    def _montar_ui(self):
        box = ttk.LabelFrame(self, text="Registrar Movimentação", padding=10)
        box.pack(fill="x", padx=10, pady=8)

        ttk.Label(box, text="Produto:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.cmb_produto = ttk.Combobox(box, width=38, state="readonly")
        self.cmb_produto.grid(row=0, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(box, text="Tipo:").grid(row=0, column=2, sticky="w", padx=4, pady=4)
        self.cmb_tipo = ttk.Combobox(box, values=["entrada", "saida"], width=12, state="readonly")
        self.cmb_tipo.set("entrada")
        self.cmb_tipo.grid(row=0, column=3, sticky="w", padx=4, pady=4)

        ttk.Label(box, text="Quantidade:").grid(row=0, column=4, sticky="w", padx=4, pady=4)
        self.ent_qtd = ttk.Entry(box, width=10)
        self.ent_qtd.grid(row=0, column=5, sticky="w", padx=4, pady=4)

        ttk.Button(box, text="Registrar", command=self._registrar).grid(row=0, column=6, padx=8)

        colunas = ("id", "data", "codigo", "produto", "tipo", "quantidade")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings", height=14)
        titulos = {
            "id": "ID",
            "data": "Data/Hora",
            "codigo": "Código",
            "produto": "Produto",
            "tipo": "Tipo",
            "quantidade": "Quantidade",
        }
        for col in colunas:
            self.tree.heading(col, text=titulos[col])
            self.tree.column(col, width=110, anchor="center")
        self.tree.column("data", width=160)
        self.tree.column("produto", width=200, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _carregar_produtos(self):
        self._mapa_produtos = {}
        opcoes = []
        for p in listar_produtos():
            rotulo = f"{p['codigo']} - {p['nome']} (Saldo: {p['quantidade']})"
            opcoes.append(rotulo)
            self._mapa_produtos[rotulo] = p["codigo"]
        self.cmb_produto["values"] = opcoes
        if opcoes:
            self.cmb_produto.current(0)

    def _carregar_historico(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for m in listar_movimentacoes():
            self.tree.insert(
                "",
                "end",
                values=(m["id"], m["data"], m["produto_codigo"], m["produto_nome"], m["tipo"], m["quantidade"]),
            )

    def _registrar(self):
        rotulo = self.cmb_produto.get()
        codigo = self._mapa_produtos.get(rotulo, "")
        tipo = self.cmb_tipo.get()
        ok, msg, qtd = validar_movimentacao(codigo, tipo, self.ent_qtd.get())
        if not ok:
            messagebox.showwarning("Atenção", msg, parent=self)
            return

        sucesso, res_msg = registrar_movimentacao(codigo, tipo, qtd)
        if sucesso:
            messagebox.showinfo("Sucesso", res_msg, parent=self)
            self.ent_qtd.delete(0, tk.END)
            self._carregar_produtos()
            self._carregar_historico()
            if self.on_atualizar:
                self.on_atualizar()
        else:
            messagebox.showerror("Erro", res_msg, parent=self)
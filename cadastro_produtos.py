import tkinter as tk
from tkinter import ttk, messagebox
from validacoes import validar_produto
from produtos import criar_produto, atualizar_produto, excluir_produto, listar_produtos


class TelaCadastroProdutos(tk.Toplevel):
    def __init__(self, master, on_atualizar=None):
        super().__init__(master)
        self.title("Cadastro de Produtos")
        self.geometry("760x460")
        self.on_atualizar = on_atualizar
        self._montar_ui()
        self._carregar_tabela()

    def _montar_ui(self):
        form = ttk.LabelFrame(self, text="Dados do Produto", padding=10)
        form.pack(fill="x", padx=10, pady=8)

        ttk.Label(form, text="Código:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.ent_codigo = ttk.Entry(form, width=16)
        self.ent_codigo.grid(row=0, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="Nome:").grid(row=0, column=2, sticky="w", padx=4, pady=4)
        self.ent_nome = ttk.Entry(form, width=28)
        self.ent_nome.grid(row=0, column=3, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="Categoria:").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.ent_categoria = ttk.Entry(form, width=16)
        self.ent_categoria.grid(row=1, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="Preço (R$):").grid(row=1, column=2, sticky="w", padx=4, pady=4)
        self.ent_preco = ttk.Entry(form, width=14)
        self.ent_preco.grid(row=1, column=3, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="Estoque Mín.:").grid(row=1, column=4, sticky="w", padx=4, pady=4)
        self.ent_minimo = ttk.Entry(form, width=10)
        self.ent_minimo.insert(0, "5")
        self.ent_minimo.grid(row=1, column=5, sticky="w", padx=4, pady=4)

        btns = ttk.Frame(form)
        btns.grid(row=2, column=0, columnspan=6, sticky="w", pady=(8, 2))

        ttk.Button(btns, text="Salvar Novo", command=self._salvar).pack(side="left", padx=4)
        ttk.Button(btns, text="Atualizar Selecionado", command=self._atualizar).pack(side="left", padx=4)
        ttk.Button(btns, text="Excluir", command=self._excluir).pack(side="left", padx=4)
        ttk.Button(btns, text="Limpar", command=self._limpar).pack(side="left", padx=4)

        colunas = ("codigo", "nome", "categoria", "preco", "quantidade", "estoque_minimo")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings", height=12)
        titulos = {
            "codigo": "Código",
            "nome": "Nome",
            "categoria": "Categoria",
            "preco": "Preço (R$)",
            "quantidade": "Qtd",
            "estoque_minimo": "Mínimo",
        }
        for col in colunas:
            self.tree.heading(col, text=titulos[col])
            self.tree.column(col, width=110, anchor="center")
        self.tree.column("nome", width=180, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar)

    def _carregar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in listar_produtos():
            self.tree.insert(
                "",
                "end",
                values=(
                    p["codigo"],
                    p["nome"],
                    p["categoria"],
                    f"{p['preco']:.2f}",
                    p["quantidade"],
                    p["estoque_minimo"],
                ),
            )
        if self.on_atualizar:
            self.on_atualizar()

    def _ao_selecionar(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        self.ent_codigo.config(state="normal")
        self.ent_codigo.delete(0, tk.END)
        self.ent_codigo.insert(0, vals[0])
        self.ent_codigo.config(state="readonly")

        self.ent_nome.delete(0, tk.END)
        self.ent_nome.insert(0, vals[1])

        self.ent_categoria.delete(0, tk.END)
        self.ent_categoria.insert(0, vals[2])

        self.ent_preco.delete(0, tk.END)
        self.ent_preco.insert(0, vals[3])

        self.ent_minimo.delete(0, tk.END)
        self.ent_minimo.insert(0, vals[5])

    def _limpar(self):
        self.ent_codigo.config(state="normal")
        self.ent_codigo.delete(0, tk.END)
        self.ent_nome.delete(0, tk.END)
        self.ent_categoria.delete(0, tk.END)
        self.ent_preco.delete(0, tk.END)
        self.ent_minimo.delete(0, tk.END)
        self.ent_minimo.insert(0, "5")
        self.tree.selection_remove(self.tree.selection())

    def _salvar(self):
        ok, msg, dados = validar_produto(
            self.ent_codigo.get(),
            self.ent_nome.get(),
            self.ent_categoria.get(),
            self.ent_preco.get(),
            self.ent_minimo.get(),
        )
        if not ok:
            messagebox.showwarning("Atenção", msg, parent=self)
            return
        criado, res_msg = criar_produto(
            dados["codigo"], dados["nome"], dados["categoria"], dados["preco"], dados["estoque_minimo"]
        )
        if criado:
            messagebox.showinfo("Sucesso", res_msg, parent=self)
            self._limpar()
            self._carregar_tabela()
        else:
            messagebox.showerror("Erro", res_msg, parent=self)

    def _atualizar(self):
        ok, msg, dados = validar_produto(
            self.ent_codigo.get(),
            self.ent_nome.get(),
            self.ent_categoria.get(),
            self.ent_preco.get(),
            self.ent_minimo.get(),
        )
        if not ok:
            messagebox.showwarning("Atenção", msg, parent=self)
            return
        att, res_msg = atualizar_produto(
            dados["codigo"], dados["nome"], dados["categoria"], dados["preco"], dados["estoque_minimo"]
        )
        if att:
            messagebox.showinfo("Sucesso", res_msg, parent=self)
            self._limpar()
            self._carregar_tabela()
        else:
            messagebox.showerror("Erro", res_msg, parent=self)

    def _excluir(self):
        codigo = self.ent_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Atenção", "Selecione um produto para excluir.", parent=self)
            return
        if not messagebox.askyesno("Confirmar", f"Deseja excluir o produto '{codigo}'?", parent=self):
            return
        excl, res_msg = excluir_produto(codigo)
        if excl:
            messagebox.showinfo("Sucesso", res_msg, parent=self)
            self._limpar()
            self._carregar_tabela()
        else:
            messagebox.showerror("Erro", res_msg, parent=self)
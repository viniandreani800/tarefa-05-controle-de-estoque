import tkinter as tk
from tkinter import ttk
from produtos import resumo_estoque
from cadastro_produtos import TelaCadastroProdutos
from registro_movimentacao import TelaRegistroMovimentacao
from consulta_estoque import TelaConsultaEstoque
from relatorios import TelaRelatorios


class MenuPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Controle de Estoque - INE5201")
        self.geometry("660x420")
        self._montar_ui()
        self.atualizar_painel()

    def _montar_ui(self):
        cab = ttk.Frame(self, padding=14)
        cab.pack(fill="x")

        ttk.Label(
            cab,
            text="Controle de Estoque com SQLite",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            cab,
            text="Gestão de produtos, entradas/saídas, alertas de estoque baixo e relatórios",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(2, 0))

        painel = ttk.LabelFrame(self, text="Indicadores em Tempo Real", padding=12)
        painel.pack(fill="x", padx=14, pady=6)

        self.lbl_produtos = ttk.Label(painel, text="Produtos: 0", font=("Segoe UI", 10, "bold"))
        self.lbl_produtos.grid(row=0, column=0, padx=12, pady=4, sticky="w")

        self.lbl_itens = ttk.Label(painel, text="Unidades: 0", font=("Segoe UI", 10, "bold"))
        self.lbl_itens.grid(row=0, column=1, padx=12, pady=4, sticky="w")

        self.lbl_valor = ttk.Label(painel, text="Valor Total: R$ 0.00", font=("Segoe UI", 10, "bold"))
        self.lbl_valor.grid(row=1, column=0, padx=12, pady=4, sticky="w")

        self.lbl_alerta = ttk.Label(painel, text="Estoque Baixo: 0", font=("Segoe UI", 10, "bold"))
        self.lbl_alerta.grid(row=1, column=1, padx=12, pady=4, sticky="w")

        nav = ttk.LabelFrame(self, text="Navegação", padding=14)
        nav.pack(fill="both", expand=True, padx=14, pady=10)

        botoes = [
            ("1. Cadastro de Produtos", lambda: TelaCadastroProdutos(self, on_atualizar=self.atualizar_painel)),
            ("2. Registrar Entrada / Saída", lambda: TelaRegistroMovimentacao(self, on_atualizar=self.atualizar_painel)),
            ("3. Consulta de Estoque e Histórico", lambda: TelaConsultaEstoque(self, on_atualizar=self.atualizar_painel)),
            ("4. Relatórios e Alertas", lambda: TelaRelatorios(self)),
        ]

        for idx, (texto, cmd) in enumerate(botoes):
            r, c = divmod(idx, 2)
            ttk.Button(nav, text=texto, command=cmd, width=30).grid(
                row=r, column=c, padx=10, pady=10, ipady=10, sticky="nsew"
            )

        nav.columnconfigure(0, weight=1)
        nav.columnconfigure(1, weight=1)
        nav.rowconfigure(0, weight=1)
        nav.rowconfigure(1, weight=1)

    def atualizar_painel(self):
        dados = resumo_estoque()
        self.lbl_produtos.config(text=f"Produtos cadastrados: {dados['total_produtos']}")
        self.lbl_itens.config(text=f"Total de unidades: {dados['total_itens']}")
        self.lbl_valor.config(text=f"Valor total em estoque: R$ {dados['valor_total']:.2f}")
        self.lbl_alerta.config(text=f"Alertas de estoque baixo: {dados['alertas_baixo']}")
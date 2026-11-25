import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from exportacao import gerar_texto_relatorio, exportar_estoque_csv


class TelaRelatorios(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Relatórios e Alertas de Estoque")
        self.geometry("720x460")
        self._montar_ui()
        self._atualizar_texto()

    def _montar_ui(self):
        topo = ttk.Frame(self, padding=10)
        topo.pack(fill="x")

        ttk.Button(topo, text="Atualizar Relatório", command=self._atualizar_texto).pack(side="left", padx=4)
        ttk.Button(topo, text="Exportar CSV Completo", command=self._exportar_csv).pack(side="left", padx=4)

        self.txt = tk.Text(self, wrap="word", font=("Consolas", 10), padx=12, pady=12)
        self.txt.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _atualizar_texto(self):
        self.txt.config(state="normal")
        self.txt.delete("1.0", tk.END)
        self.txt.insert("1.0", gerar_texto_relatorio())
        self.txt.config(state="disabled")

    def _exportar_csv(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")],
            initialfile="relatorio_estoque.csv",
            parent=self,
        )
        if not caminho:
            return
        gerado = exportar_estoque_csv(caminho_arquivo=caminho)
        messagebox.showinfo("Exportado", f"Relatório exportado para:\n{gerado}", parent=self)
from conexao import inicializar_banco
from menu_principal import MenuPrincipal


def main():
    inicializar_banco()
    app = MenuPrincipal()
    app.mainloop()


if __name__ == "__main__":
    main()
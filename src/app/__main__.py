from src.app.view.cli import CLI


def main() -> None:
    """Punto de entrada de la aplicación."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()

try:
    from dotenv import load_dotenv
    load_dotenv('.env')
except Exception:
    pass


def main():
    from .core import start_app
    start_app()


if __name__ == "__main__":
    main()

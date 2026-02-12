from os import environ


def main() -> None:
    print(environ.get("APP_CONFIG_PATH"))


if __name__ == "__main__":
    main()

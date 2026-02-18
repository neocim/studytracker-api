from os import environ

from fastapi import FastAPI

from studytracker.bootstrap.config import load_config

def create_fastapi_app() -> FastAPI:
    app = FastAPI()

def main() -> None:
    config = load_config()


if __name__ == "__main__":
    main()

import asyncio
import textwrap
import os
from colorama import Fore, init
from hypercorn.config import Config as HyperConfig
from hypercorn.asyncio import serve
from app.main import app
from app.core.config import settings
import logging

init(autoreset=True)


def get_version_from_file():
    version_file_path = os.path.join(os.path.dirname(__file__), "VERSION")
    print(f"Looking for version file at: {version_file_path}")
    try:
        with open(version_file_path, "r") as f:
            version_str = f.read().strip()
            return version_str
    except FileNotFoundError:
        return "Unknown Version"


if __name__ == "__main__":
    settings = settings
    version = get_version_from_file()
    print(
        textwrap.dedent(
            rf"""{Fore.BLUE}
  __  __ _____  _      _____         _
 |  \/  |_   _|/ \    |_   _|__  ___| |__
 | |\/| | | | / _ \     | |/ _ \/ __| '_ \
 | |  | | | |/ ___ \    | |  __/ (__| | | |
 |_|  |_| |_/_/   \_\   |_|\___|\___|_| |_|
 version: {version}
    """
        )
    )

    config = HyperConfig()
    config.bind = [f"{settings.APP_HOST}:{settings.APP_PORT}"]
    # config.reload = True  # only use this in development
    # config.h2 = True  # Optional: HTTP/2 support
    # Optional: enable HTTP/2 if TLS certs are used
    # config.certfile = "path/to/cert.pem"
    # config.keyfile = "path/to/key.pem"
    config.alpn_protocols = ["h2", "http/1.1"]

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    try:
        asyncio.run(serve(app, config))
    except Exception as e:
        logging.error(f"Failed to start server: {e}", exc_info=True)

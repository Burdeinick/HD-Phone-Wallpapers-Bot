import json
from server_bot import app
from server_bot import receive_update
from aiohttp import web
from config import SERVER


host, port = SERVER["host"], SERVER["port"]


def main():
    app.router.add_route("POST", "/", receive_update)
    web.run_app(app, host=host, port=port) 


if __name__ == "__main__":
    main()

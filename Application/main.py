import json
from server_bot import app
from server_bot import receive_update
from aiohttp import web


def get_config():
    with open('config.json') as config:
        json_str = config.read()
        json_str = json.loads(json_str)

    host = json_str['server']['host']
    port = json_str['server']['port']
    return (host, port)


host, port = get_config()


def main():
    app.router.add_route("POST", "/", receive_update)
    web.run_app(app)


if __name__ == "__main__":
    main()

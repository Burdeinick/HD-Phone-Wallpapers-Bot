import json
from server_bot import app


def main():
    app.run(*get_config(),debug=True)

def get_config():
    with open('Application/config.json') as config:
        json_str = config.read()
        json_str = json.loads(json_str)

    host = json_str['server']['host']
    port = json_str['server']['port']
    return (host, port)


if __name__ == "__main__":
    main()

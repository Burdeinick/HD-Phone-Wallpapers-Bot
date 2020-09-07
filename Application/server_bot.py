from flask import Flask, make_response, request
from scripts.logic.logic import Telegram
from scripts.logic.logic import RequestsDb
# from scripts.logic.logic import HandlerReqDb


app = Flask(__name__)
teleg = Telegram()
request_db = RequestsDb()
# hand_req_db = HandlerReqDb()


@app.route("/", methods=["GET", "POST"])
def receive_update():
    req = request.json
    print(req)
    if request.method == "POST":
        req = request.json
        print(req)

        if req['message']['text'] == '/start':
            chat_id = req["message"]["chat"]["id"]
            user_info = request_db.get_user_info(chat_id)

            if user_info:
                teleg.send_message(chat_id, f"Такой пользователь уже есть е мае")

            else:
                resp_add_user_info = request_db.add_user_info(chat_id)
                if resp_add_user_info:
                    teleg.select_iphone(chat_id)

                else:
                    teleg.send_message(chat_id, f"Не вышло!")
        chat_id = req["message"]["chat"]["id"]
        teleg.select_iphone(chat_id)          
    return {"ok": True}

from flask import Flask, make_response, request
from scripts.logic.logic import Telegram
from scripts.logic.logic import RequestsDb
from scripts.logic.logic import HandlerReqDb


app = Flask(__name__)
teleg = Telegram()
request_db = RequestsDb()
hand_req_db = HandlerReqDb()


@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        req = request.json
        chat_id = req["message"]["chat"]["id"]
        text_message = req['message']['text']

        if text_message == '/start':
            user_exist = hand_req_db.user_exist(chat_id)
            if not user_exist:
                add_user = request_db.add_user_info(chat_id)
                if add_user:
                    teleg.select_iphone(chat_id)
            else:
                pass
        
        if text_message in hand_req_db.get_iphone_list():
            user_exist = hand_req_db.user_exist(chat_id)
            if user_exist:
                set_take_iphone = request_db.set_status_take_iphone(chat_id)
                if set_take_iphone:
                    teleg.get_picture(chat_id)



            



        # chat_id = req["message"]["chat"]["id"]
        # teleg.select_iphone(chat_id)
        # teleg.get_picture(chat_id)
       
    return {"ok": True}

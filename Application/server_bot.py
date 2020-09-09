from flask import Flask, make_response, request
from scripts.logic.logic import Telegram
from scripts.logic.logic import RequestsDb
from scripts.logic.logic import HandlerReqDb
from scripts.logic.logic import HandlerServer as hand_serv


app = Flask(__name__)
teleg = Telegram()
request_db = RequestsDb()
hand_req_db = HandlerReqDb()



@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        print(request.json)
        a = hand_serv(request.json)
        a.select_comand()

    return {"ok": True}

from flask import Flask, make_response, request
from Application.scripts.logic.logic import Telegram
from Application.scripts.logic.logic import RequestsDb


app = Flask(__name__)
teleg = Telegram()
request_db = RequestsDb()



@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        req = request.json

        if req['message']['text'] == '/start':
            chat_id = req["message"]["chat"]["id"]
            resp_add_user = request_db.add_user_id(chat_id)

            if resp_add_user:                                                   # если пользователь добавлен в бд, то можно приступить к след. шагу - д обавить в куки свои , что он прошел шаг / start внести 
                teleg.cookies[chat_id] = {'start': True, 'take_iphone': False}  # и дать ему возможоность выбрать серию своего айфона
                # здесь теперь писать метод который отобразит пользователю клавиатуру с выбором модели айфона

                teleg.send_message(chat_id, f"Все норм!")
            else:
                teleg.send_message(chat_id, f"Не вышло!")
                

            # print(request.json['message']['text'])
    
    print(teleg.cookies)
        
    return {"ok": True}


from scripts.logic.logic import Telegram
from scripts.logic.logic import RequestsDb
from scripts.logic.logic import HandlerReqDb
from scripts.logic.logic import HandlerServer as hand_serv

from TOKEN import token

import time
import asyncio

from aiohttp import web, request
import aiohttp

app = web.Application()

teleg = Telegram()
request_db = RequestsDb()
hand_req_db = HandlerReqDb()




async def receive_update(request):
    async with aiohttp.ClientSession() as session:
        print('Начал')
        start_time = time.time()
        req = await request.json()
        chat_id = req["message"]["chat"]["id"]
        text_message = req["message"]["text"] if "text" in req["message"] else ""

        if text_message == "Получить обои":

            user_exist = hand_req_db.user_exist(chat_id)
            stat_take_iphone = request_db.set_status_take_iphone(chat_id)
            if user_exist and stat_take_iphone:  # если пользователь есть в БД и он уже выбрал модель своего айфона
                await teleg.send_message(chat_id, "Секундочку, Ваши обои тоже ждут встречи с Вами \U0001f929")

                all_pix = request_db.get_pixresolution(chat_id)
                if all_pix:
                    print(all_pix)
                    ferst_pix = all_pix[0][0].split(' ')[0]
                    second_pix = all_pix[0][0].split(' ')[1]
                    method = "sendPhoto"
                    url = f"https://api.telegram.org/bot{token}/{method}"
                    async with session.get(f"https://picsum.photos/{ferst_pix}/{second_pix}") as ses_get:
                        print('sessssiiiooooo')
                        url_foto = str(ses_get.url)
                        data = {"chat_id": chat_id, "photo": url_foto}
                        await session.post(url, data=data)
                        print('POST req')

    # await session.close()



        # print('Начал')
        # start_time = time.time()
        # a = hand_serv(await request.json())
       
        # await asyncio.sleep(0.7)
        # await a.select_comand()

    print("--- %s seconds ---" % (time.time() - start_time))
    print('Закончил')
    return web.json_response({'ok': True})

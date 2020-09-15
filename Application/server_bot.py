
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


async def chec_det_wal(text_message, chat_id):
    if text_message == "Получить обои":
        user_exist = hand_req_db.user_exist(chat_id)
        stat_take_iphone = request_db.set_status_take_iphone(chat_id)
        if user_exist and stat_take_iphone:  # если пользователь есть в БД и он уже выбрал модель своего айфона
            return True
        return False 
    return False 


async def receive_update(request):
    async with aiohttp.ClientSession() as session:
        print('Начал')
        start_time = time.time()
        req = await request.json()
        a = hand_serv(req)
        chat_id = a.chat_id
        text_message = a.text_message

        if await chec_det_wal(text_message, chat_id): 
            await teleg.send_message(chat_id, "Секундочку, Ваши обои тоже ждут встречи с Вами \U0001f929")
            pix = hand_req_db.hand_get_pixresolution(chat_id)
            async with session.get(f"https://picsum.photos/{pix[0]}/{pix[1]}") as ses_get:
                url_foto = str(ses_get.url)
                method = "sendPhoto"
                data = {"chat_id": chat_id, "photo": url_foto}
                await session.post(f"https://api.telegram.org/bot{token}/{method}", data=data)

        else:
            a.select_comand()

    print("--- %s seconds ---" % (time.time() - start_time), '\n', "Закончил")
    return web.json_response({'ok': True})

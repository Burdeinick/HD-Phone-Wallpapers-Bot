from scripts.logic.logic import Telegram
from scripts.logic.logic import RequestsDb
from scripts.logic.logic import HandlerReqDb
from scripts.logic.logic import HandlerServer
from TOKEN import token
import time
import asyncio
import aiohttp
from aiohttp import web, request


app = web.Application()
teleg = Telegram()
request_db = RequestsDb()
hand_req_db = HandlerReqDb()
hand_serv = HandlerServer


async def receive_update(request):
    async with aiohttp.ClientSession() as session:
        print('Начал')
        start_time = time.time()
        req = await request.json()
        h_s = hand_serv(req)
        chat_id = h_s.chat_id
        text_message = h_s.text_message
        chec_det_wal = await h_s.chec_det_wal(text_message, chat_id)

        if chec_det_wal:
            text = "Секундочку, Ваши обои уже ждут встречи с Вами \U0001f929"
            await teleg.send_message(chat_id, text)
            pix = await hand_req_db.hand_get_pixresolution(chat_id)
            pix_1, pix_2 = pix[0], pix[1]
            
            async with session.get(f"https://picsum.photos/{pix_1}/{pix_2}") as ses_get:
                url_foto = str(ses_get.url)
                method = "sendPhoto"
                data = {"chat_id": chat_id, "photo": url_foto}
                await session.post(f"https://api.telegram.org/bot{token}/{method}", data=data)
        else:
            await h_s.select_comand()

    print("---Закончил. %s seconds ---" % (time.time() - start_time))
    return web.json_response({'ok': True})

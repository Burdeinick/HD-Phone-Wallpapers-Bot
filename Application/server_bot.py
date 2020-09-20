from scripts.logic.logic import Telegram
from scripts.logic.logic import RequestsDb
from scripts.logic.logic import HandlerReqDb
from scripts.logic.logic import HandlerServer
from scripts.logic.logic import send_error_message

from logger.log import MyLogging


from TOKEN import token, my_chat_id
import time
import asyncio
import aiohttp
from aiohttp import web, request


app = web.Application()
teleg = Telegram()
request_db = RequestsDb()
hand_req_db = HandlerReqDb()
hand_serv = HandlerServer


super_logger = MyLogging().setup_logger('server_bot',
                                        'Application/logger/logfile.log')


async def receive_update(request):
    try:
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
                width, height = pix[0], pix[1]
                
                async with session.get(f"https://picsum.photos/{width}/{height}") as ses_get:
                    url_foto = str(ses_get.url)
                    method = "sendPhoto"
                    data = {"chat_id": chat_id, "photo": url_foto}
                    await session.post(f"https://api.telegram.org/bot{token}/{method}", data=data)
            else:
                await h_s.select_comand()

        print("---Закончил. %s seconds ---" % (time.time() - start_time))
        return web.json_response({'ok': True})

    except Exception:
        super_logger.error('Error receive_update', exc_info=True)
        send_error_message()

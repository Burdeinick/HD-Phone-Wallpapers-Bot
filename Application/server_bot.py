# from flask import Flask, make_response, request
from scripts.logic.logic import Telegram
from scripts.logic.logic import RequestsDb
from scripts.logic.logic import HandlerReqDb
from scripts.logic.logic import HandlerServer as hand_serv

import time
import datetime
import asyncio

from aiohttp import web, request
import aiohttp

app = web.Application()

teleg = Telegram()
request_db = RequestsDb()
hand_req_db = HandlerReqDb()




async def receive_update(request):
    # print(await request.json())
    # print("!")

    # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # await asyncio.sleep(3)
    # time.sleep(3)
    # print('Закончил')
    # results = hand_serv(await request.json())
    # results.select_comand()
    
    async with aiohttp.ClientSession() as session:
        
        # start_time = time.time()

        # print(await request.json())
        # print('Начал')
        hand_serv(await request.json())
        # results.select_comand()
        # await asyncio.sleep(10)
        # print('Закончил')
        # print("--- %s seconds ---" % (time.time() - start_time))

        # return web.json_response({'ok': True})

    return web.json_response({'ok': True})


# @app.post("/")
# async def receive_update(json_data: Dict):
    # print(json_data)
    # results = hand_serv(json_data)
    # results.select_comand()
    # time.sleep(15)
    # print(json_data["message"]["chat"]['first_name'], 'все')

    # return {"ok": True}
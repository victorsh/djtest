# https://gist.github.com/timhughes/313c89a0d587a25506e204573c8017e4

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import aioredis
import logging
import asyncio


# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to Redis
# pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
# redis = redis.Redis(connection_pool=pool)

app = FastAPI()

# Configure CORS
# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8000"
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

@app.get('/')
async def get():
    return {'message': 'hi'}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await redis_connector(websocket)

async def redis_connector(websocket: WebSocket, redis_uri:str = "redis://localhost:6379"):
    async def consumer_handler(ws:WebSocket, r):
        try:
            while True:
                message = await ws.receive_text()
                if message:
                    await ws.send_text(message.decode("utf-8"))
        except Exception as e:
            logger.error(e)
    
    async def producer_handler(r, ws: WebSocket):
        (channel,) = await r.subscribe("chat:c")
        assert isinstance(channel, aioredis.Channel)
        try:
            while True:
                message = await channel.get()
                if message:
                    await ws.send_text(message.decode("utf-8"))
        except Exception as e:
            logger.error(e)

    redis = await aioredis.create_redis_pool(redis_uri)

    consumer_task = consumer_handler(websocket, redis)
    producer_task = producer_handler(redis, websocket)
    done, pending = await asyncio.wait(
        [consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED
    )
    logger.debug(f"Done task: {done}")
    for task in pending:
        logger.debug(f"Canceling task: {task}")
        task.cancel()
    redis.close()
    await redis.wait_closed()

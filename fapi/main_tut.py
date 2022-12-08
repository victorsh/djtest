from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from enum import Enum
from typing import List, Union, Dict, Callable
import fe
import json
import redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
async def get():
    return HTMLResponse(fe.html)

# @app.get('/')
# async def root():
#     return {"message": "Hello World"}

@app.get('/items/{item_id}')
async def read_item(item_id):
    return {"item_id": item_id}

@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {'model_name': model_name, 'message': 'Deep Learning FTW!'}

    if model_name.value == 'lenet':
        return {'model_name': model_name, 'message': 'Deep Learning FTW!'}

    return {'model_name': model_name, 'message': 'Have some risiduals'}

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def boradcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# @app.websocket('/ws/{client_id}')
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_message(f"client #{client_id} says: {data}", websocket)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")

@app.websocket('/ws/test')
async def websocket_test(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await manager.send_message('hello there', websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast('client disconnected')

@app.websocket('/v1/connect')
async def ws_connect(websocket:WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            if data['msg'] == '1':
                await manager.send_message('1', websocket)
            if data['msg'] == '2':
                await manager.send_message('2', websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast('client disconnected')

@app.websocket('/v1/game_connect/{game_id}')
async def game_connect(websocket:WebSocket, game_id:str, api_key:Union[str, None]=None, token:Union[str, None]=None):
    print(game_id)
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast('client disconnected')
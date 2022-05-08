import asyncio
from admin_panel.models import Language, Text
from flask import Flask, request
import websockets
from threading import Thread



# async def handler(websocket):
#     while True:
#         message = await websocket.recv()
#         print(message)


async def main(handler):
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()


# if __name__ == "__main__":
#     asyncio.run(main())

class Socket:
    def __init__(self):
        # for lang in Language.objects.all():
        #     for i in ['send_name_and_surname', 'send_number_register', 'send_number_register_button', 'select_filial', 'successfully_registered', 'order', 'busket', 'settings', 'our_addresses', 'my_orders', 'offers', 'questions_and_adds', 'communications', 'mainMenu', 'settings_info', 'change_name', 'change_number', 'change_language', 'back']:
        #         Text.objects.get_or_create(language=lang, name=i, data=i)
        self.client = set()
        asyncio.run(self.start_server())
    
    async def start_server(self):
        self.server = websockets.serve(self.handler, "", 8001)
        self.flask = Flask(__name__)
        self.flask.route('/act')(self.act)
        self.thread = Thread(target=self.flask.run, kwargs={'host': '164.92.173.21', 'port': 8002})
        # self.thread = Thread(target=self.flask.run, kwargs={'host': '127.0.0.1', 'port': 8002})

        self.thread.start()
        async with self.server:
            await asyncio.Future()
        self.thread.join()
    
    def act(self):
        print('xxxxx')
        data = request.get_json()
        print(request.get_json())
        order = data['order'] 
        asyncio.run(self.broadcast(str(order)))
        return "salom"
    
    async def broadcast(self, message):
        for client in self.client:
            try:
                await client.send(message)
            except:
                pass
        
    
    async def handler(self, websocket, path):
        self.client.add(websocket)
        while True:
            try:
                message = await websocket.recv()
                for client in self.client:
                    await client.send(message)
            except:
                pass
            
        self.client.remove(websocket)
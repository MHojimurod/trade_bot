import asyncio

import websockets


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
        self.client = set()
        asyncio.run(self.start_server())
    
    async def start_server(self):
        self.server = websockets.serve(self.handler, "", 8001)
        print(dir(self.server.ws_server))
        async with self.server:

            await asyncio.Future()
        
        
    
    async def handler(self, websocket, path):
        self.client.add(websocket)
        while True:
            message = await websocket.recv()
            for client in self.client:
                await client.send(message)
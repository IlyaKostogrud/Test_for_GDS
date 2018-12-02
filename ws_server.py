import asyncio
import websockets

url_list = ['https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Rfc-frame.jpg/800px-Rfc-frame.jpg',
            'https://upload.wikimedia.org/wikipedia/commons/a/ae/Rfc-frame.jpg']

print('''Hello! I'm server for URL-sending.''')

async def url_sender(websocket, path):
    
    await websocket.send(str(len(url_list)))
    
    for url in url_list:
        await websocket.send(url)

start_server = websockets.serve(url_sender, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

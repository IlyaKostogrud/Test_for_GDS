import asyncio
import websockets
import os
from tqdm import tqdm
import requests

async def url_downloader():
    async with websockets.connect('ws://localhost:8765') as websocket:
        
        i = 0
        url_list_size = int(await websocket.recv())
        
        while i < url_list_size:
            i += 1
            url = await websocket.recv()
            file_name = os.path.basename(url)
            response = requests.get(url, stream=True)        
            print('File size: ', response.headers['Content-length'], 'B')
            
            try:
                with open(file_name, "xb") as handle:
                    for data in tqdm(response.iter_content(), desc = 'Progress', unit='B'):
                        handle.write(data)
            except FileExistsError:
                print('File was previously downloaded ', os.path.abspath(file_name))

asyncio.get_event_loop().run_until_complete(url_downloader())
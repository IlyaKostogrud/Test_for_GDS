import asyncio
import websockets
import os
import errno
from tqdm import tqdm
import requests

#Get the data from the config file.
import dl_options_config as cfg
chunk_bytes = cfg.chunk_bytes 
num_threads = cfg.num_threads #понадобится для реализации многопоточного скачивания(не реализовано)
dl_directory = cfg.dl_directory

try:
    os.makedirs(dl_directory)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


def accepts_byte_ranges(url):
    """Test if the server supports multi-part file download."""
    response = requests.get(url, headers = {"Range": "bytes=0-0"})
    http_code = response.status_code
    
    if http_code == 206: # Http status code 206 means byte-ranges are accepted
        return True
    else:
        return False


def download_file(url, chunk_bytes=1):
    main_dir = os.getcwd()
    os.chdir(dl_directory)    
    file_name = os.path.basename(url)    
    response = requests.get(url, stream=True)
    
    try:
        with open(file_name, "xb") as handle:
            for data in tqdm(response.iter_content(chunk_size=chunk_bytes), desc = 'Progress'):
                handle.write(data)
    except FileExistsError:
        print('File was previously downloaded ', os.path.abspath(file_name))
        
    os.chdir(main_dir)


async def url_downloader():
    async with websockets.connect('ws://localhost:8765') as websocket:        
        
        url_list_size = int(await websocket.recv())
        
        for i in range(url_list_size):
            url = await websocket.recv()            
            download_file(url, chunk_bytes=chunk_bytes)
            

asyncio.get_event_loop().run_until_complete(url_downloader())
import asyncio
import aiohttp
import aiofiles
import random
import string
import validators

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

async def write_file(filename,content):
    try:
        async with aiofiles.open(f"{filename}", "wb") as f:
            await f.write(content)
    except Exception as e:
        print(f"Error while using aiofiles {e}")

async def download_file_and_save(link,type):
    if validators.url(link):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as response:
                    content = await response.read()
        except Exception as e:
            print(f"Error while making request {e}")
        filename = f"download_{get_random_string(6)}.{type}"
        try:
            await write_file(filename,content)
        except Exception as e:
            print(f"Error while writing the downloaded file {e}")
        print(f"{filename} downloaded successfully!")
    else:
        print("Invalid URL!")

async def main(download_links,simultaneous_downloads_limit):
    if len(download_links) <= simultaneous_downloads_limit:
        try:
            await asyncio.gather(*(download_file_and_save(link,type) for link, type in download_links.items()))
        except Exception as e:
            print(f"Error while joining async functions with gather {e}")
    else:
        print("Download limit rate was surpassed")

simultaneous_downloads_limit = 5
download_links_info = {
    "https://placekeanu.com/200/200": "svg",
    "https://placekeanu.com/400/400": "svg",
    "https://placekeanu.com/600/800": "svg",
    "https://viacep.com.br/ws/01001000/json/": "json",
    "https://viacep.com.br/ws/57304200/json/": "json",
}

asyncio.run(main(download_links_info,simultaneous_downloads_limit))
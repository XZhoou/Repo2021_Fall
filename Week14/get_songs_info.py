import aiohttp
import asyncio
import aiofiles
import async_timeout
import re
import pandas as pd
from bs4 import BeautifulSoup

song_info_list = []
playtimes_range = [10000,30000]

async def main():
    async with aiofiles.open("BUAA_21/Week14/info.csv", "r", encoding="utf-8") as fp:
        async with aiohttp.ClientSession() as session:
            async for line in fp:
                if playtimes_range[0] <=  int(line.split(',')[1]) <= playtimes_range[1]:
                    html = "https://music.163.com" + line.split(',')[2]
                    singletext = await fetch(session, html)
                    for i in re.findall(r'<a href="/song\?id=(\d+)">(.*?)</a>', singletext):
                        songtext = await fetch(session, "https://music.163.com/song?id=%s"%i[0])
                        soup = BeautifulSoup(songtext, 'html.parser')
                        album = soup.select('a[ class = "s-fc7"]')[0].get_text()
                        print([i[0], i[1], album])
                        song_info_list.append([i[0],i[1],album])
                else:
                    continue
    write_in()

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

def write_in():
    data = pd.DataFrame(song_info_list)
    data.to_csv("BUAA_21/Week14/songs_info.csv")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

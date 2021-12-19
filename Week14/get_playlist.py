import asyncio
import pandas as pd
import aiohttp
import async_timeout
import requests as rq
from bs4 import BeautifulSoup

info_list = []

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()

async def analyse_songlist():
    page_number = 38
    start_url = 'https://music.163.com/discover/playlist/?order=hot&cat=说唱'+'&limit=35'
    async with aiohttp.ClientSession() as session:
        for page in range(1,page_number+1):
            url = start_url + '&offset=' + str(35 * page)
            html = await fetch(session, url)
            soup = BeautifulSoup(html, 'html.parser')
            c = soup.find_all('li')
            for unit in c:
                try:
                    name_url = unit.find(
                        'a', {'class': "tit f-thide s-fc0"})  # m这里有URL，名字的信息
                    number = eval(unit.find('span', {'class': 'nb'}).text.replace(
                        '万', '0000'))  # 这里获取的是播放量的信息,用于初步筛选
                    list1 = [number, name_url['href']]
                    info_list.append(list1)
                    print(list1)
                except:
                    continue
    write_in()

def write_in():
    data = pd.DataFrame(info_list)
    data.to_csv("BUAA_21/Week14/info.csv")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(analyse_songlist())

import asyncio
import json
import os
import random
import time

import aiohttp
import pymongo

df = []
former_id = []
tot = 1
semaphore = asyncio.Semaphore(10)  # 限制并发量
url = 'https://s.search.bilibili.com/cate/search?'
head = [
    "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
    "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
    "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
]
header = {
    'user-agent': random.choice(head),
    'refer': 'https://www.bilibili.com/'
}


myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['Bilibili_data']
mycol = mydb["Data"]

async def get_page(url, param):
    await asyncio.sleep(2)
    async with aiohttp.ClientSession() as session:
        async with await session.get(url, headers=header, params=param) as r:
            r_text = await r.text()
            return r_text


async def parse_page(text):
    global tot
    try:
        data = json.loads(text)
        inf_list = data['result']
        temp = []
        for i in range(len(inf_list)):
            author = data['result'][i]['author']
            duration = data['result'][i]['duration']
            collection = data['result'][i]['favorites']
            aid = data['result'][i]['id']
            title = data['result'][i]['title']
            pubdate = data['result'][i]['pubdate']
            review = int(data['result'][i]['review'])
            play = int(data['result'][i]['play'])
            temp.append({'UP主': author, '视频标题': title, '发布时间': pubdate, '_id': aid, '视频时长': duration, '播放量': play,'评论数': review, '收藏数': collection, '导入时间': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
        print('爬取第%d页成功' % tot)
        tot += 1
        return temp
    except:
        print('未爬到第%d页数据'%tot)
        tot += 1
        return None

async def get_data(url, param):
    async with semaphore:
        text = await get_page(url, param)
        temp = await parse_page(text)
        await data_clean(temp)

async def data_clean(temp):
    for i in temp:
        if i['_id'] not in former_id:
            former_id.append(i['_id'])
            df.append(i)

def insert_into_database():
    df.sort(key = lambda x: x["播放量"], reverse= True)
    for i in range(len(df)):
        df[i]['排名'] = i + 1
    result = mycol.insert_many(df)
    print("插入完成,共%d条数据"%len(df))

def return_params(num):
    params = {
        'main_ver': 'v3',
        'search_type': 'video',
        'view_type': 'hot_rank',
        'order': 'click',
        'copy_right': -1,
        'cate_id': 21,
        'page': num,
        'pagesize': 100,
        'jsonp': 'jsonp',
        'time_from': 20211201,
        'time_to': 20211215
    }
    return params


def main():
    num = 140
    tasks = [asyncio.ensure_future(
        get_data(url, return_params(i))) for i in range(1, num+1)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    insert_into_database()

if __name__ == '__main__':
    start = time.time()
    main()

    end = time.time()
    print('共花费{}分钟'.format(round((end-start)/60, 2)))
    myclient.close()

    time.sleep(2)
    print('\n准备开始爬取第二周数据\n')
    os.system("python BUAA_21/Week15/latter.py")


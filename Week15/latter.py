import asyncio
import json
import random
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText

import aiohttp
import pymongo

sender = '2836072921@qq.com'  # 发送邮件的以预防
receiver = 'buaasqh@163.com'  # 接收邮件的一方
password = 'mfzmucycdhqhdeia'  # QQ邮箱的授权码
smtp_server = 'smtp.qq.com'


def send_email_func():
    msg = MIMEText('您的程序已执行完毕，请及时查看结果！\n\n这是系统自动发出邮件，请不要回复。', 'plain', 'utf-8')
    msg['From'] = u'孙小舟 <2836072921@qq.com>'
    msg['To'] = u'<buaasqh@163.com>'
    msg['Subject'] = u'您的程序已经执行完毕'
    server = smtplib.SMTP_SSL(smtp_server)
    server.set_debuglevel(1)
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()


latter_data = []
former_aid = []
new_data = []

new_data_id = []
latter_data_id = []

temp = []
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


def connect_to_database(client):
    mycol = client["Data"]
    return mycol


def select_data(col):
    global former_aid
    former_aid = [i['_id'] for i in list(col.find({}, {'_id': 1}))]


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
        for i in range(len(inf_list)):
            author = data['result'][i]['author']
            duration = data['result'][i]['duration']
            collection = data['result'][i]['favorites']
            aid = data['result'][i]['id']
            title = data['result'][i]['title']
            pubdate = data['result'][i]['pubdate']
            review = int(data['result'][i]['review'])
            play = int(data['result'][i]['play'])
            temp.append({'UP主': author, '视频标题': title, '发布时间': pubdate, '_id': aid, '视频时长': duration, '播放量': play,
                         '评论数': review, '收藏数': collection, '导入时间': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})

        print('爬取第%d页成功' % tot)
        tot += 1
        return temp
    except:
        print('未爬到第%d页数据' % tot)
        tot += 1
        return None


async def get_data(url, param):
    async with semaphore:
        text = await get_page(url, param)
        temp = await parse_page(text)
        if temp:
            await data_process(temp)
        else:
            pass


async def data_process(temp):
    for i in temp:
        if i['_id'] in new_data_id or i['_id'] in latter_data_id:
            continue
        if i['_id'] in former_aid:  # 在第一周和第二周中都出现过的视频
            i['更新时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            latter_data.append(i)
            latter_data_id.append(i['_id'])
        else:  # 第二周中新出现的视频
            new_data.append(i)
            new_data_id.append(i['_id'])


def database_operation(col):
    for i in latter_data:
        if i['_id'] in former_aid:
            former_aid.remove(i['_id'])
    add_new_column(col)
    deleted_operation(col)
    insert_operation(col)
    update_operation(col)


def add_new_column(col):
    col.update_many({"更新时间": {"$exists": False}}, {
        "$set": {"更新时间": None}})


def deleted_operation(col):
    deleted_number = 0
    for i in former_aid:
        result = col.delete_many({'_id': i})
        deleted_number += result.deleted_count
    print("%d个记录已经删除" % deleted_number)


def insert_operation(col):
    if new_data:
        result = col.insert_many(new_data)
    print("%d个记录已新创建" % len(new_data))


def update_operation(col):
    if latter_data:
        for i in latter_data:
            result = col.update_one(
                {'_id': i['_id']}, {'$set': i}, upsert=True)
    print("%d个记录已被更新" % len(latter_data))


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
        'time_from': 20211208,
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

def reorder(col):
    data = list(col.find({}))
    data.sort(key = lambda x: x["播放量"], reverse= True)
    for i in range(len(data)):
        data[i]['排名'] = i + 1
    col.delete_many({})
    col.insert_many(data)
    
if __name__ == '__main__':
    start = time.time()

    myclient1 = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient1['Bilibili_data']

    mycol = connect_to_database(mydb)

    select_data(mycol)

    main()

    database_operation(mycol)
    reorder(mycol)

    end = time.time()
    print('共花费{}分钟'.format(round((end-start)/60, 2)))
    myclient1.close()
    send_email_func()

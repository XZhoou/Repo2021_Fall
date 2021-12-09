import os
import queue
import random
import shutil
import time
from threading import Thread
from urllib import request

import pandas as pd
import requests as rq
from bs4 import BeautifulSoup

headers1 = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

count = 0
filename = "BUAA_21/Week12/info.csv"
q = queue.Queue()


def getHTMLText(url, headers):  # 通用的获取网站内容的框架
    try:
        r = rq.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "网络解析错误"


def get_url(page):  # 获取首页该分类下面的歌单url，形成url_list
    start_url = 'https://music.163.com/discover/playlist/?order=hot&cat=说唱'+'&limit=35'

    try:
        url = start_url+'&offset=' + str(35 * page)
        print("正在爬取第%d页的所有歌单id"%(page+1))
        html = getHTMLText(url, headers1)
        parse_main(html)
    except:
        print('失败')


def parse_main(html):  # 解析单个url
    soup = BeautifulSoup(html, 'html.parser')
    c = soup.find_all('li')
    for unit in c:
        try:
            name_url = unit.find(
                'a', {'class': "tit f-thide s-fc0"})  # m这里有URL，名字的信息
            number = eval(unit.find('span', {'class': 'nb'}).text.replace(
                '万', '0000'))  # 这里获取的是播放量的信息,用于初步筛选
            list1 = [name_url['title'].replace(
                u'\xa0', u' '), number, name_url['href']]

            q.put(list1[-1])
        except:
            continue


def parse_single():  # 进入歌单内部解析，获取播放量，收藏量，标签等信息
    global count
    while True:
        listid = q.get()
        # print(listid)
        if listid is None:
            break
        time.sleep(random.randint(1, 2))

        singleurl = 'https://music.163.com'+listid
        singletext = getHTMLText(singleurl, headers=headers1)
        soup = BeautifulSoup(singletext, 'html.parser')
        try:
            # 播放次数
            try:
                play_count = soup.find('strong', {'class': 's-fc6'}).text
            except:
                print("\n未查询到第%d个歌单播放次数\n"%count)
                play_count = 0
            # 收藏数量
            try:
                fav = soup.find(
                    'a', {'class': 'u-btni u-btni-fav'}).i.text.strip('(').strip(')')
                if('万') in fav:
                    fav = eval(fav.replace('万', '0000'))
            except:
                fav = 0
                print("\n未查询到第%d个歌单收藏数量\n"%count)
            # 分享次数
            try:
                share = soup.find(
                    'a', {'class': 'u-btni u-btni-share'}).i.text.strip('(').strip(')')
            except:
                share = 0
                print("\n未查询第%d个歌单分享次数\n"%count)
            # 评论数
            try:
                comment = eval(
                    soup.find('a', {'data-res-action': 'comment'}).i.span.text)
            except:
                print("\n未找到第%d个歌单评论数\n"%count)
                comment = 0
            # 歌单介绍
            try:
                introduce = soup.select(
                    'p[ class =  "intr f-brk"]')[0].get_text()
            except:
                introduce = ''
                print("\n未找到第%d个歌单介绍\n"%count)

            try:
                creater_name = soup.find('a', {'class': 's-fc7'}).text
            except:
                print("\n未找到第%d个歌单创建者昵称\n"%count)
                creater_name = 'nan'
            # 创建者id
            try:
                creater_id = soup.select('a[ class = "face"]')[
                    0].attrs['href'][14:]
            except:
                print("\n未找到第%d个歌单创建者id\n"%count)
                creater_id = 'nan'
            # 保存图片
            try:
                pic = soup.select('img[class = "j-img"]')[0].attrs['data-src']
                request.urlretrieve(
                    pic, "BUAA_21/Week12/Covers/%s.jpg" % listid[13:])

                # url = requests.get(pic)
                # image = Image.open(BytesIO(url.content))
                # image.save("BUAA_21/Week12/Covers/%s.jpg"%listid[13:])
            except:
                print("\n未找到第%d个歌单图片\n"%count)

            # 歌单长度
            try:
                length = soup.find('span', {'id': 'playlist-track-count'}).text
            except:
                length = 0
                print("\n未找到第%d个歌单长度\n"%count)
            # 创建日期
            try:

                date = soup.find('span', {'class': 'time s-fc4'}).text[:10]
            except:
                data = 'nan'
                print("\n未找到第%d个歌单创建日期\n"%count)
            # 歌单名称
            try:
                name = soup.find(
                    'h2', {"class": 'f-ff2 f-brk'}).text.replace(u'\xa0', u' ')
            except:
                name = 'nan'
                print("\n未找到第%d个歌单名称\n"%count)
            # 歌单标签
            tags = soup.find_all('a', {'class': 'u-tag'})
            p = len(tags)
            tag1 = 'nan'
            tag2 = 'nan'
            tag3 = 'nan'
            if p >= 1:
                tag1 = tags[0].text.replace(u'\xa0', u' ')
            if p >= 2:
                tag2 = tags[1].text.replace(u'\xa0', u' ')
            if p == 3:
                tag3 = tags[2].text.replace(u'\xa0', u' ')

            data = pd.DataFrame([[name, listid[13:], introduce, creater_id, creater_name,
                                  date, play_count, fav, share, comment, length, tag1, tag2, tag3]])

            data.to_csv(filename, mode='a', header=False, encoding='GBK')
            count += 1
            print('解析第{}个歌单成功'.format(count))
        except:
            count += 1
            print('解析第{}个歌单失败'.format(count))
        q.task_done()




def init():
    # 创建一个文件夹用来保存歌单封面
    if os.path.exists(filename):
        os.remove(filename)

    shutil.rmtree("BUAA_21/Week12/Covers")
    os.makedirs("BUAA_21/Week12/Covers")

    # 创建带列名称的空csv文件，方便之后进行数据写入
    title_list = ['名称', '歌单id', '歌单介绍', '创建者id', '创建者昵称', '创建日期',
                  '播放次数', '收藏量', '转发量', '评论数', '歌单长度', 'tag1', 'tag2', 'tag3']
    title_dataframe = pd.DataFrame(columns=title_list)
    title_dataframe.to_csv(filename, mode='a', encoding='GBK')


# depth就是总共爬取多少页的，打开网站可以发现每页上有30多个，总共有38页。
if __name__ == '__main__':

    init()
    pagenum = 38
    child_thread_num = 15
    clist = []
    plist = []

    for i in range(child_thread_num):
        consumer_thread = Thread(target=parse_single)
        clist.append(consumer_thread)
        # consumer_thread.start()

    for i in range(pagenum):
        producer_thread = Thread(target=get_url, args=(i,))
        plist.append(producer_thread)
    for p in plist:
        p.start()
    time.sleep(random.randint(2,4))
    print("\n----------开启%d个子线程----------"%child_thread_num)
    for c in clist:
        c.start()
    q.join()
    for _ in range(child_thread_num):
        q.put(None)
    for c in clist:
        c.join()


    print("\n----------歌单信息爬取程序运行结束-----------\n")

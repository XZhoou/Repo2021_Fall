import jieba.analyse as analyse
from wordcloud import WordCloud
import re
import numpy as np
import PIL.Image as image


def main():
    with open("C:/Users/DELL/Desktop/Code/BUAA_21/Week2/jd_comments.txt", "r", encoding="utf-8") as comments:
        jd_comments = comments.readlines()

    analyse.set_stop_words(
        "C:/Users/DELL/Desktop/Code/BUAA_21/Week2/stopwords_list.txt")

    dict = {}

    for item in jd_comments:
        cut_sentence = analyse.extract_tags(item)
        for word in cut_sentence:
            dict[word] = dict.get(word, 0) + 1

    words = list(dict.keys())

    words = " ".join(words)

    pattern = re.compile(r'[^\u4e00-\u9fa5,\u0020]')

    words = re.sub(pattern, '', words)
    # 以上两条代码用来将英文字符从文档中除去，最终筛选出所有中文词语，从而使最后得到的词云图皆为中文词语

    # 按照字典值大小降序排序
    dict = sorted(dict.items(), key=lambda item: item[1], reverse=True)

    return words, jd_comments, dict


def find_high_freq_words(dict):

    high_freq_words = []

    for i in range(4):
        high_freq_words.append(dict[i][0])

    print("高频特征词有%d个，分别为" % len(high_freq_words), high_freq_words)

    return high_freq_words


def find_matrix(jd_comments, high_freq_words):

    Matrix = []
    for item in jd_comments:
        cut_sentence = analyse.extract_tags(item)
        vector = []
        for i in range(4):
            if high_freq_words[i] in cut_sentence:
                vector.append(1)
            else:
                vector.append(0)
        # print(vector)
        # print(cut_sentence)
        Matrix.append(vector)

    print("一共有%d条文档，用特征向量表示的特征矩阵为" % len(Matrix),)

    for i in range(len(Matrix)):
        print(Matrix[i])

    return Matrix


def word_could(words):
    wordcloud = WordCloud(
        #mask=np.array(image.open("C:/Users/DELL/Desktop/Code/BUAA_21/Week2/guoguo.jpg")),# 将注释去掉，可以生成对应形状的词云图
        font_path="C:/Users/DELL/Desktop/Code/BUAA_21/Week2/msyh.ttc",
        max_words=400,  # 最大单词数
        min_font_size=4,  # 最大字号
        scale=3,  # scale越大，词云图越清晰
        random_state=12  # 随机状态数，即配色方案中有多少种颜色
    ).generate(words)
    image_produce = wordcloud.to_image()
    wordcloud.to_file("Wordcloud.jpg")
    image_produce.show()


def find_Euclidean_distance(x, y):
    # x, y are vectors
    dis = 0
    for i in range(len(x)):
        dis += pow(x[i]-y[i], 2)

    dis = pow(dis, 0.5)
    print("两个向量之间的欧氏距离是:\n",dis)
    return dis


def find_center_of_gravity(Matrix):
    center = [0 for i in range(4)]
    for i in range(len(Matrix)):
        center[0] += Matrix[i][0]
        center[1] += Matrix[i][1]
        center[2] += Matrix[i][2]
        center[3] += Matrix[i][3]
    for i in range(len(center)):
        center[i] /= float(len(Matrix))

    print("\n文档的重心是\n", center)
    return center


def find_representative_document(Matrix):
    # 找到代表性文档
    index = [i for i, x in enumerate(Matrix) if x == [1, 1, 1, 1]]

    return index


def print_representative_document(index, jd_commments):
    # 打印代表性文档
    print("正在生成代表性文档......\n")

    for i in index:
        print(jd_comments[i])


if __name__ == '__main__':
    words, jd_comments, dict = main()

    high_freq_words = find_high_freq_words(dict)

    Matrix = find_matrix(jd_comments, high_freq_words)

    center = find_center_of_gravity(Matrix)

    print("生成词云图中......\n")
    word_could(words)

    index = find_representative_document(Matrix)

    print_representative_document(index, jd_comments)

    while True:
        x,y = map(int,input("输入下标查询两个文档之间的距离（1-1003），在任意位置输入0退出程序\n").split(' '))
        if x != 0 and y != 0:
            find_Euclidean_distance(Matrix[x-1],Matrix[y-1])
        else:
            break

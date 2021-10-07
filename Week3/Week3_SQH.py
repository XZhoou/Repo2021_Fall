import jieba.analyse as analyse
import numpy as np
import jieba
import time
import re


def jieba_set_config():
    '''
    对jieba库设定参数，添加用户词典，同时设置停用词（停用词引用了上次作业中stopword_list.txt)
    '''
    print("\nSetting Jieba module config.\n")

    jieba.load_userdict(
        "C:/Users/DELL/Desktop/Code/BUAA_21/Week3/emotion_lexicon/anger.txt")
    jieba.load_userdict(
        "C:/Users/DELL/Desktop/Code/BUAA_21/Week3/emotion_lexicon/disgust.txt")
    jieba.load_userdict(
        "C:/Users/DELL/Desktop/Code/BUAA_21/Week3/emotion_lexicon/fear.txt")
    jieba.load_userdict(
        "C:/Users/DELL/Desktop/Code/BUAA_21/Week3/emotion_lexicon/joy.txt")
    jieba.load_userdict(
        "C:/Users/DELL/Desktop/Code/BUAA_21/Week3/emotion_lexicon/sadness.txt")

    analyse.set_stop_words(
        "C:/Users/DELL/Desktop/Code/BUAA_21/Week3/stopwords_list.txt")


def clear_data(file):
    '''
    进行数据清洗和整理

    去除URL，将正文内容，时间和地点分别提取出，并和微博内容组成一个维度为3的列表，最终组成一个矩阵
    '''
    with open(file, 'r', encoding='utf-8') as f:
        data = f.readlines()

    clean_data = []
    for i in data:
        vector = [0 for i in range(3)]

        pattern = re.compile(
            r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')

        i = re.sub(pattern, '', i)  # 去除微薄的URL等无关信息

        i = i.replace("转发微博", '')

        pattern = re.compile(r'(\[[^]]*)\d(?=[^\]]*\])')

        position = re.findall(pattern, i)

        position = position[-1].replace('[', '')
        # 用正则表达式选出的pattern仍有一点缺陷，所以选出的position多了一个中括号，可以继续加以改进
        # 在这里就用最基础的方法多进行一次处理
        position = list(map(float, position.split(",")))

        vector[2] = position
        # print(i)
        i = re.sub(pattern, '', i)

        i = i.rstrip()
        i = i[:-1]
        # 去掉右侧的空格，然后再去掉最后的方括号

        timestring = i[-31:]
        # timestring = timestring.replace("+0800",'')
        timestring = timestring.split("\r")[0]
        timestring = timestring.split("\t")[0]

        vector[1] = time.strptime(timestring, "%a %b %d %H:%M:%S +0800 %Y")

        vector[0] = i.replace(timestring, '')
        clean_data.append(vector)

    pattern = re.compile(r"(回复)?(//)?\s*@\S*?\s*(:| |$)")

    timeseries = []
    for i in clean_data:
        i[0] = re.sub(pattern, '', i[0])
        i[0] = analyse.extract_tags(i[0])
        # print(i)

    return clean_data


def analysis1(clean_data):
    '''
    已经完成清洗和整理的数据进行分析

    分别与五个字典进行比较，返回一个矩阵

    矩阵的五列分别对应anger,disgust,fear,joy,sadness
    '''
    def convert(lis):
        '''
        对五个字典进行处理，返回一个中文词的列表
        '''
        lis = ''.join(lis).strip("\n").splitlines()
        return lis

    with open("C:/Users/DELL/Desktop/Code/BUAA_21/Week3/emotion_lexicon/anger.txt", 'r', encoding='utf-8') as anger:
        anger_list = anger.readlines()
        anger_list = convert(anger_list)

    with open("C:/Users/DELL/Desktop/Code/BUAA_21/Week3/emotion_lexicon/disgust.txt", 'r', encoding='utf-8') as anger:
        disgust_list = anger.readlines()
        disgust_list = convert(disgust_list)

    with open("C:/Users/DELL/Desktop/Code/BUAA_21/Week3/emotion_lexicon/fear.txt", 'r', encoding='utf-8') as anger:
        fear_list = anger.readlines()
        fear_list = convert(fear_list)

    with open("C:/Users/DELL/Desktop/Code/BUAA_21/Week3/emotion_lexicon/joy.txt", 'r', encoding='utf-8') as anger:
        joy_list = anger.readlines()
        joy_list = convert(joy_list)

    with open("C:/Users/DELL/Desktop/Code/BUAA_21/Week3/emotion_lexicon/sadness.txt", 'r', encoding='utf-8') as anger:
        sadness_list = anger.readlines()
        sadness_list = convert(sadness_list)

    def judge(matrix):
        nonlocal anger_list, disgust_list, fear_list, joy_list, sadness_list, clean_data

        for comment in clean_data:
            vector = [0 for i in range(5)]
            info = []
            for word in comment[0]:
                if word in anger_list:
                    vector[0] += 1
                elif word in disgust_list:
                    vector[1] += 1
                elif word in fear_list:
                    vector[2] += 1
                elif word in joy_list:
                    vector[3] += 1
                elif word in sadness_list:
                    vector[4] += 1
            sum_num = sum(vector)
            if sum_num != 0:
                # 加入一步判断，去掉无情绪的向量
                for i in range(5):
                    vector[i] /= float(sum_num)
                info.append(vector)
                # 筛选出符合实际时间范围的数据
                info.extend(comment[1:])
                matrix.append(info)
                # print(info)
            else:
                pass

        return matrix

    return judge


def emotion_trend(Matrix, mood, mode):
    '''
    对情绪变化的趋势进行时间分析

    而通过观察时间的分布范围发现，总体的时间范围是2013-10-11 至 2013-10-13
    所以情绪的周模式，日模式和小时模式是比较有分析价值的
    如果设定为分钟模式，则显得过于细碎，不能较好的体现出情绪变化的趋势
    所以在本函数中主要选用week, day, hour模式进行分析
    '''
    def take(vector):
        return vector[1]

    Matrix.sort(key=take)  # 按照时间对矩阵中的向量进行排序
    output_matrix = []  # 输出结果的字符串矩阵

    time_range = [Matrix[0][1], Matrix[-1][1]]
    emotion_list = ['anger', 'disgust', 'fear', 'joy', 'sadness']

    if mood in emotion_list:

        index = emotion_list.index(mood)

        mode_range_min = time_range[0]
        mode_range_max = time_range[1]

        if mode == 'week':
            emotion_sum = []
            for item in Matrix:
                emotion_sum.append(item[0][index])
            output = 'From 2013-10-11 to 2013-10-13, the ' + \
                emotion_list[index] + \
                ' proportion is %.6f' % (sum(emotion_sum)/len(emotion_sum))
            output_matrix.append(output)

        elif mode == 'day':

            for i in range(int(mode_range_min.tm_mday), int(mode_range_max.tm_mday)+1):
                emotion_sum = []
                for item in Matrix:
                    if item[1].tm_mday == i:
                        emotion_sum.append(item[0][index])
                    else:
                        pass
                try:
                    output = "The 2013-10-%d\'s " % i + emotion_list[index] + ' proportion is %.6f' % (sum(
                        emotion_sum)/len(emotion_sum))
                    output_matrix.append(output)
                except:
                    break

        elif mode == 'hour':
            for i in range(int(mode_range_min.tm_mday), int(mode_range_max.tm_mday)+1):
                for j in range(0, 24):
                    emotion_sum = []
                    for item in Matrix:
                        if item[1].tm_hour == j and item[1].tm_mday == i:
                            emotion_sum.append(item[0][index])
                        else:
                            pass
                    try:
                        output = "The 2013-10-%d %d:00--%d:00\'s " % (
                            i, j, j+1)+emotion_list[index]+' proportion is %.6f' % (sum(emotion_sum)/len(emotion_sum))
                        output_matrix.append(output)
                    except:
                        break
        else:
            print("The time mode you choose is invalid")

    else:
        print("The emotion you choose is invalid.\n")

    return output_matrix


def emotion_distance(Matrix, mood, radius):
    '''
    分析情绪的空间分布

    实现一个函数可以通过参数来控制返回情绪的空间分布
    围绕某个中心点，随着半径增加，该情绪所占比例的变化(以经纬度的0.01为步长)
    而radius在输入时应该是0~0.09
    （在本方法中，中心点默认是城市的中心位置）
    '''

    position_x = []
    position_y = []

    output_matrix = []
    for i in Matrix:
        position_x.append(i[2][0])
        position_y.append(i[2][1])

    center_x = sum(position_x)/len(position_x)
    center_y = sum(position_y)/len(position_y)

    coordinates = np.array([center_x, center_y])

    for i in Matrix:
        vector = np.array(i[2])
        dis = np.linalg.norm(vector-coordinates)
        i.append(dis)

    def taken(item):
        return item[3]

    Matrix.sort(key=taken)

    emotion_list = ['anger', 'disgust', 'fear', 'joy', 'sadness']

    if mood in emotion_list:
        index = emotion_list.index(mood)
        emotion_dic = {}
        # for j in range(0.01, round(radius, 2), 0.01):
        for j in np.arange(0.01, round(radius+0.01, 2), 0.01):
            if j <= radius:
                j = round(j, 2)
                emotion_num = []
                for i in Matrix:
                    dis = i[3]
                    if j-0.01 <= dis:
                        if dis <= j:
                            emotion_num.append(i[0][index])
                        else:
                            break
                    else:
                        pass
            else:
                break

            try:
                emotion_dic[str(round(j-0.01, 2))+'~'+str(round(j, 2))
                            ] = sum(emotion_num)/len(emotion_num)
            except:
                print("Fail")

    else:
        print("The emotion you choose is invalid.\n")

    for i in emotion_dic.keys():
        output = "The proportion of %s in the %s area is %.6f." % (
            mood, i, emotion_dic[i])
        output_matrix.append(output)

    return output_matrix


if __name__ == '__main__':

    Matrix = []

    jieba_set_config()

    file = "C:/Users/DELL/Desktop/Code/BUAA_21/Week3/weibo.txt"

    clean_data = clear_data(file)

    func = analysis1(clean_data)
    Matrix = func(Matrix)

    output = emotion_trend(Matrix, 'sadness', 'day')

    output = emotion_trend(Matrix, 'joy', 'day')

    with open("C:/Users/DELL/Desktop/Code/BUAA_21/Week3/output.txt", 'a+') as f:

        output = emotion_trend(Matrix, 'sadness', 'day')

        print(*output, sep='\n', file=f)

        print('\n\n-----------------------------------------\n\n', file=f)

        output = emotion_trend(Matrix, 'joy', 'day')

        print(*output, sep='\n', file=f)

        print('\n\n-----------------------------------------\n\n', file=f)

        output = emotion_trend(Matrix, "joy", "hour")

        print(*output, sep='\n', file=f)

        print('\n\n-----------------------------------------\n\n', file=f)

        output = emotion_trend(Matrix, "joy", "week")

        print(*output, sep='\n', file=f)

        print('\n\n-----------------------------------------\n\n', file=f)

        # emotion_distance(Matrix, "joy", 0.05)

        output2 = emotion_distance(Matrix, "sadness", 0.07)

        print(*output2, sep='\n', file=f)

        print('\n\n-----------------------------------------\n\n', file=f)

        output2 = emotion_distance(Matrix, "joy", 0.05)

        print(*output2, sep='\n', file=f)

        print('\n\n-----------------------------------------\n\n', file=f)

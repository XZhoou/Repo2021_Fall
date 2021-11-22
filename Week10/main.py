# -*- coding:utf-8 -*-
import abc
import os
import random
import re

import cv2
import imageio
import jieba.analyse as analyse
import librosa
import librosa.display
import numpy
import numpy as np
import PIL.Image as image
from matplotlib import pyplot as plt
from PIL import Image
from wordcloud import WordCloud

from point import Point


class PointPlotter:
    def __init__(self, data):
        self.data = data

    def pointplot(self, *args, **kwargs):
        color = ['red', 'blue', 'green']
        tot = 0
        for i in self.data:
            plt.scatter(i.x, i.y, color=color[tot], alpha=0.7)
            tot = (tot+1) % 3
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("PointPlotter")
        plt.show()


class ArrayPlotter:
    def __init__(self, data):
        self.data = data

    def arrayplot(self, *args, **kwargs):
        length = len(self.data[0])
        x = numpy.arange(length)
        if "type" in kwargs.keys():
            if kwargs["type"].upper() == "SCATTER":
                for i in self.data:
                            # plt.plot(x,i)
                    plt.scatter(x, i)
            elif kwargs["type"].upper() == "LINE":
                for i in self.data:
                    plt.plot(x, i)
        else:
            # 如果没有指定绘图的类型，那么久默认绘制折线图
            for i in self.data:
                plt.scatter(x, i)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("ArrayPlotter")
        plt.show()


class TextPlotter:
    def __init__(self, data):
        self.data = data

    def textplot(self, *args, **kwargs):
        dict = {}
        analyse.set_stop_words("BUAA_21/Week10/txt/stopwords_list.txt")
        for item in self.data:
            cut_sentence = analyse.extract_tags(item)
            for word in cut_sentence:
                dict[word] = dict.get(word, 0) + 1
        words = list(dict.keys())
        words = " ".join(words)
        pattern = re.compile(r'[^\u4e00-\u9fa5,\u0020]')
        words = re.sub(pattern, '', words)
        wordcloud = WordCloud(
            # 将注释去掉，可以生成对应形状的词云图
            mask=np.array(image.open("BUAA_21/Week10/mask/mask.jpg")),
            font_path="BUAA_21/Week10/txt/msyh.ttc",
            max_words=400,  # 最大单词数
            min_font_size=4,  # 最大字号
            scale=3,  # scale越大，词云图越清晰
            random_state=12  # 随机状态数，即配色方案中有多少种颜色
        ).generate(words)

        image_produce = wordcloud.to_image()
        if not os.path.exists("BUAA_21/Week10/generated_wordcloud"):
            os.makedirs("BUAA_21/Week10/generated_wordcloud")
        wordcloud.to_file("BUAA_21/Week10/generated_wordcloud/Wordcloud.jpg")
        image_produce.show()


class ImagePlotter:
    def __init__(self, data):
        self.data = data

    def imageplot(self, *args, **kwargs):

        filename = []
        for root, dirs, files in os.walk(self.data):
            for file in files:
                image = Image.open(os.path.join(root, file))
                filename.append(image)
        imagenum = len(filename)
        num = 1
        for i in range(imagenum):
            # 第一行是处理前的原始图片，第二行是处理后的图片
            plt.subplot(1, imagenum, num)
            plt.imshow(filename[i])
            plt.axis("off")
            num += 1
        plt.tight_layout()  # 自动调整子图间距
        plt.show()


class GifPlotter:
    def __init__(self, data):
        self.data = data

    def gifplot(self, *args, **kwargs):
        filename = []
        for root, dirs, files in os.walk(self.data):
            for file in files:
                image_name = os.path.join(root, file)
                filename.append(image_name)

        png = []
        for i in filename:
            png.append(imageio.imread(i))
        if not os.path.exists("BUAA_21/Week10/generated_gif"):
            os.makedirs("BUAA_21/Week10/generated_gif")
        else:
            pass
        if "fps" in kwargs.keys():
            imageio.mimsave(
                "BUAA_21/Week10/generated_gif/gif.gif", png, fps=kwargs["fps"])
        else:
            imageio.mimsave(
                "BUAA_21/Week10/generated_gif/gif.gif", png, fps=12)


class MusicPlotter:
    def __init__(self, data):
        self.data = data

    def musicplot(self, *args, **kwargs):
        y, sr = librosa.load(self.data)

        # 音色谱
        chroma_stft = librosa.feature.chroma_stft(
            y=y, sr=sr, n_chroma=12, n_fft=4096)
        # 另一种常数Q音色谱
        chroma_cq = librosa.feature.chroma_cqt(y=y, sr=sr)
        # 功率归一化音色谱
        chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)
        plt.figure(figsize=(15, 15))
        plt.subplot(3, 1, 1)
        librosa.display.specshow(chroma_stft, y_axis='chroma')
        plt.title('chroma_stft')
        plt.colorbar()
        plt.subplot(3, 1, 2)
        librosa.display.specshow(chroma_cq, y_axis='chroma', x_axis='time')
        plt.title('chroma_cqt')
        plt.colorbar()
        plt.subplot(3, 1, 3)
        librosa.display.specshow(chroma_cens, y_axis='chroma', x_axis='time')
        plt.title('chroma_cens')
        plt.colorbar()
        plt.show()


class VideoPlotter:
    def __init__(self, data):
        self.data = data

    def videoplot(self, *args, **kwargs):

        # 要提取视频的文件名，隐藏后缀
        sourceFileName = self.data
        # 在这里把后缀接上
        video_path = os.path.join("", "", sourceFileName)
        times = 0
        # 提取视频的频率，每25帧提取一个
        frameFrequency = 25
        # 输出图片到当前目录vedio文件夹下
        outPutDirName = "BUAA_21/Week10/generated_frame/"
        if not os.path.exists(outPutDirName):
            # 如果文件目录不存在则创建目录
            os.makedirs(outPutDirName)
        camera = cv2.VideoCapture(video_path)
        while True:
            times += 1
            res, image = camera.read()
            if not res:
                print('not res , not image')
                break
            if times % frameFrequency == 0:
                cv2.imwrite(outPutDirName + str(times)+'.jpg', image)
                print(outPutDirName + str(times)+'.jpg')
        print('图片提取结束')
        camera.release()

        instance = GifPlotterAdapter(GifPlotter(outPutDirName))
        instance.plot()


class Plotter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def plot(data, *args, **kwargs):
        pass


class PointPlotterAdapter(Plotter):
    def __init__(self, instance):
        self.instance = instance

    def plot(self, *args, **kwargs):
        self.instance.pointplot(*args, **kwargs)


class ArrayPlotterAdapter(Plotter):
    def __init__(self, instance):
        self.instance = instance

    def plot(self, *args, **kwargs):
        self.instance.arrayplot(*args, **kwargs)


class TextPlotterAdapter(Plotter):
    def __init__(self, instance):
        self.instance = instance

    def plot(self, *args, **kwargs):
        self.instance.textplot(*args, **kwargs)


class ImagePlotterAdapter(Plotter):
    def __init__(self, instance):
        self.instance = instance

    def plot(self, *args, **kwargs):
        self.instance.imageplot(*args, **kwargs)


class GifPlotterAdapter(Plotter):
    def __init__(self, instance):
        self.instance = instance

    def plot(self, *args, **kwargs):
        self.instance.gifplot(*args, **kwargs)


class MusicPlotterAdapter(Plotter):
    def __init__(self, instance):
        self.instance = instance

    def plot(self, *args, **kwargs):
        self.instance.musicplot(*args, **kwargs)


class VideoPlotterAdapter(Plotter):
    def __init__(self, instance):
        self.instance = instance

    def plot(self, *args, **kwargs):
        self.instance.videoplot(*args, **kwargs)


def main():
    ImagePlotterdata = "BUAA_21/Week10/photos"

    PointPlotterdata = []
    for _ in range(100):
        point = Point(random.randint(1, 50), random.randint(1, 50))
        PointPlotterdata.append(point)

    GifPlotterdata = "BUAA_21/Week10/pngs_tocreate_gif"

    with open("BUAA_21/Week10/txt/data.txt", "r", encoding="utf-8") as f:
        TextPlotterdata = f.readlines()

    ArrayPlotterdata = numpy.random.randint(
        20, size=(2, 20))  # size中第一个参数决定矩阵的行，第二个参数决定矩阵的列

    MusicPlotterdata = "BUAA_21/Week10/music/testwav.wav"

    VideoPlotterdata = "BUAA_21/Week10/video/video.mp4"

    objects = []
    objects.append(PointPlotterAdapter(PointPlotter(PointPlotterdata)))
    objects.append(ArrayPlotterAdapter(ArrayPlotter(ArrayPlotterdata)))
    objects.append(TextPlotterAdapter(TextPlotter(TextPlotterdata)))
    objects.append(ImagePlotterAdapter(ImagePlotter(ImagePlotterdata)))
    objects.append(GifPlotterAdapter(GifPlotter(GifPlotterdata)))
    objects.append(MusicPlotterAdapter(MusicPlotter(MusicPlotterdata)))
    objects.append(VideoPlotterAdapter(VideoPlotter(VideoPlotterdata)))

    for obj in objects:
        # obj.plot(type = "line")
        obj.plot()
if __name__ == '__main__':
    main()

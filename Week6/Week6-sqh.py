from PIL import Image
from PIL import ImageFilter
import matplotlib.pyplot as plt
import glob
import sys
import os


class Filter(object):
    '''
    基类
    其中一个属性为待处理的图片实例，即PIL库的Image实例
    另一个属性为参数列表，用以存储可能使用参数的滤波器的参数
    包含方法属性filter()
    能够对Image实例进行特定处理
    '''

    def __init__(self, file, *args, **kwargs):
        '''
        对实例对象进行初始化
        '''

        self.Image = file
        self.args = args
        self.kwargs = kwargs

    def show_photos(self):
        '''
        展示原始的未经过处理操作的图片
        '''
        self.show()

    def filter():
        '''
        支持对实例图像进行某些操作，但不在此基类中定义
        '''

        pass


class ImageEdgeExtraction(Filter):
    '''
    实现图像锐化

    其中filter函数的参数为ImageFilter.FIND_EDGES
    '''

    def __init__(self, file, *args, **kwargs):
        super().__init__(file, *args, **kwargs)

    def filter(self):
        self.edge_extractioned_photo = self.Image.filter(
            ImageFilter.FIND_EDGES)
        # self.edge_extractioned_photo.show()
        return self.edge_extractioned_photo

    def save_extracted_photo(self):
        try:
            self.Image.save(self.kwargs['filename'])
        except:
            print(
                "Lacks argument:'filename', the image has been named as temp_extracted.png.")
            self.Image.save("BUAA_21/Week6/Temp/temp_extracted.jpg")


class ImageSharpening(Filter):
    '''
    实现图像锐化

    其中filter函数的参数为IMAGE.SHARPEN
    '''

    def __init__(self, file, *args, **kwargs):
        super().__init__(file, *args, **kwargs)

    def filter(self):
        self.sharpened_photo = self.Image.filter(ImageFilter.SHARPEN)
        # self.sharpened_photo.show()
        return self.sharpened_photo

    def save_sharpened_photo(self):
        try:
            self.Image.save(self.kwargs['filename'])
        except:
            print(
                "Lacks argument:'filename', the image has been named as temp_sharpened.png.")
            self.Image.save("BUAA_21/Week6/Temp/temp_sharpened.png")


class Imageblurring(Filter):
    '''
    实现图像模糊处理

    其中filter函数的参数为IMAGE.BLUR
    '''

    def __init__(self, file, *args, **kwargs):
        super().__init__(file, *args, **kwargs)

    def filter(self):
        self.blurred_photo = self.Image.filter(ImageFilter.BLUR)
        # self.blurred_photo.show()
        return self.blurred_photo

    def save_blurred_photo(self):
        try:
            self.Image.save(self.kwargs['filename'])
        except:
            print(
                "Lacks argument:'filename', the image has been named as temp_blurred.png.")
            self.Image.save("BUAA_21/Week6/Temp/temp_blurred.png")


class ImageResize(Filter):
    '''
    实现图像大小调整

    利用Image实例的resize方法，给定图片的长和宽;
    若实例化对象时没有传递长和宽的参数，那么默认将图片大小调整为500*300
    '''

    def __init__(self, file, *args, **kwargs):
        super().__init__(file, *args, **kwargs)

    def filter(self):
        try:
            self.resized_photo = self.Image.resize(
                (self.kwargs["length"], self.kwargs["width"]), Image.ANTIALIAS)

        except:
            try:
                self.resized_photo = self.Image.resize(
                    (self.args[0], self.args[1]), Image.ANTIALIAS)
            except:
                # 默认情况下生成500*300大小的图片
                self.resized_photo = self.Image.resize(
                    (500, 300), Image.ANTIALIAS)

        # self.resized_photo.show()
        return self.resized_photo

    def save_resized_photo(self):
        try:
            self.Image.save(self.kwargs['filename'])
        except:
            print(
                "Lacks argument:'filename', the image has been named as temp_resized.png.")
            self.Image.save("BUAA_21/Week6/Temp/temp_resized.png")


class ImageShop:

    def __init__(self, format, files, lis, operated_photo_lis):
        self.format = format
        # 如果参数files是一个文件，那么直接添加到self.files中
        # 但如果files是一个目录，那么就用glob库的glob方法找到特定格式的文件

        if self.format not in files:
            self.files = glob.glob(r"BUAA_21/Week6/*."+self.format)
            if self.files != []:
                pass
            else:
                print("The files doesn't exist.")
                sys.exit()
        else:
            self.files = [files]
        self.lis = lis
        self.operated_photo_lis = operated_photo_lis

    def load_images(self):
        '''
        加载图片，加载后应该储存在self.lis这个储存图片实例的列表中
        '''
        for i in self.files:
            photo = Image.open(i)
            self.lis.append(photo)
        self.original = self.lis[:]

    def __batch_ps(self, class_type, *args):
        '''
        内部方法，利用某个过滤器对所有图片进行处理
        '''
        args = args[0]
        for i in self.lis:
            self.operated_photo_lis.append(class_type(i, *args).filter())

        self.lis = self.operated_photo_lis[:]
        self.operated_photo_lis = []

    def batch_ps(self, *Filter):

        if isinstance(Filter[0], tuple):
            Filter = Filter[0]
        else:
            Filter = tuple(Filter)
        for i in Filter:

            if isinstance(i, str):
                # 如果只传入了操作名称
                operation = i.lower()
                args = ''

            elif isinstance(i, tuple):
                # 如果传入了操作名称和参数
                operation = i[0].lower()
                args = i[1]

            if operation in ['resize', 'resized', 'resizing']:
                self.__batch_ps(ImageResize, args)

            elif operation in ['sharpening', 'sharpen', 'sharpened', 'sharp', 'sharping']:
                self.__batch_ps(ImageSharpening, args)

            elif operation in ['blurring', 'blur', 'blurred']:
                self.__batch_ps(Imageblurring, args)

            elif operation in ["edge extraction", "edge_extraction", "edgeextraction", 'edge', 'extraction']:
                self.__batch_ps(ImageEdgeExtraction, args)

            else:
                print("The operation name doesn't exist.")
                sys.exit()

    def display(self, **args):
        '''
        实现处理后图片的显示
        '''
        imagenum = len(self.lis)
        num = 1

        for i in range(imagenum):
            # 第一行是处理前的原始图片，第二行是处理后的图片
            plt.subplot(2, imagenum, num)

            plt.imshow(self.original[i])
            plt.axis("off")

            plt.subplot(2, imagenum, num+imagenum)
            plt.imshow(self.lis[i])
            plt.axis("off")

            num += 1
        plt.tight_layout()  # 自动调整子图间距
        plt.show()

    def save(self, foldername):
        num = 1
        foldername = "BUAA_21/Week6/"+foldername
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        for i in self.lis:
            i.save(foldername + '/' + str(num) + ".jpg")
            num += 1


class TestImageShop:
    def __init__(self, content=[], image_format='jpg', operation=''):
        self.content = content
        self.operation = operation
        self.image_format = image_format

    def test(self, save=True, display=True):

        new = ImageShop(self.image_format, self.content, [], [])
        new.load_images()

        if self.operation:
            new.batch_ps(eval(self.operation))
        else:
            print("Please specify an operation name!")
            sys.exit()

        if save:
            new.save("Temp")
        else:
            pass

        if display:
            new.display()
        else:
            pass


if __name__ == '__main__':

    filename = "BUAA_21/Week6/"
    op1 = "'blurring', 'sharpening', ('resize', (500, 300))"
    # TestImageShop(content=filename, operation=op1).test()

    op2 = "'edge',('resize',(600,450))"
    # TestImageShop(content=filename, operation=op2).test()

    op3 = "'blur'"
    # TestImageShop(content=filename, operation=op3).test()

    op4 = "'sharp'"
    TestImageShop(content=filename, operation=op4).test()

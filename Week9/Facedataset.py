from PIL import Image
import numpy as np
import os

class FaceDataset:
    def __init__(self, path):
        self.start = 0
        self.path = path
        self.files = []
        # 利用os.walk方法查询文件夹下的所有文件
        for root, dirs, files in os.walk(self.path):
            for file in files:
                image = os.path.join(root, file)
                self.files.append(image)

    def load_image(self, filename):
        np_image = np.array(Image.open(filename))
        return np_image

    def __iter__(self):
        return self

    def __next__(self):
        length = len(self.files)
        while self.start < length - 1:
            x = self.load_image(self.files[self.start-1])
            print(self.start)
            self.start += 1
            return x
        else:
            return StopIteration("\nAll files have been loaded,the total amount is %d." % (self.start + 1))

def main():
    instance = FaceDataset("BUAA_21\Week9\originalPics")
    
    # try:
    #     for _ in range(100000):
    #         next(instance)
    # except StopIteration as SIError:
    #     print(SIError)

    # print(len(instance))
    # TypeError: object of type 'FaceDataset' has no len()
    # 说明FaceDataset并不是列表，而是生成了一个图片的迭代器


if __name__ == '__main__':
    main()

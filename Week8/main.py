from functools import wraps
from memory_test import Memory
from SendEmail import SendEmailClass
from PlaySound import PlaySoundClass
from tqdm import tqdm
import os


def f(x):
    if x < 0:
        return None
    if x == 1:
        return 1
    elif x == 0:
        return 1
    else:
        return f(x-1) + f(x-2)


class CheckFilePath:
    def __init__(self):
        print("CheckFilePath module is working.")

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'path' in kwargs.keys():
                # 如果函数的参数中包含path参数，进行后续的检查
                if not os.path.exists(kwargs["path"]):
                    # path指向的文件夹并不存在的话，就用mkdir方法创建一个新的文件夹，同时输出提示性信息

                    print("\nFilepath '%s' Not exists" % kwargs["path"])
                    print("\nCreated filepath '%s'\n" % kwargs['path'])
                    os.mkdir(kwargs["path"])
                else:
                    # 如果存在，就进行后续的操作即可
                    print(kwargs["path"]+" exists\n")
                return func(*args, **kwargs)
            else:
                print("Arguments 'path' doesn't exist.")
        return wrapper


@PlaySoundClass()
@SendEmailClass()
@Memory()
@CheckFilePath()
@profile  # 进行时间分析时将此行取消注释，并在命令行输入 kernprof -l -v decorater.py
# 进行装饰的时候应该是首先检查文件路径，然后再添加一个发送邮件的功能，最后在运行成功的时候播放声音
def Fibonacci_sequence(n, path):
    '''
    计算出Fibonacci数列的前n项，并保存到path路径下的ouecome.txt文件中
    '''
    with open(path+"/outcome.txt", 'w+', encoding='utf-8') as file:
        for i in tqdm(range(n)):
            print("The %d item of Fibonacci sequence is %d." %
                  (i+1, f(i)), file=file)

def main():
    Fibonacci_sequence(n=30, path='BUAA_21/Week8/Temp')


if __name__ == '__main__':
    main()

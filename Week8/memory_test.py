from memory_profiler import profile as memory_profile
from functools import wraps


class Memory:
    def __init__(self):
        pass

    def __call__(self, func):
        @wraps(func)
        @memory_profile
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper


@Memory()
def memory_rascal(x, n):
    '''生成一个字符串，长度为n*x^3'''
    number = 'a' * x * x * x * n
    return number


def main(x, n):
    memory_rascal(x, n)


if __name__ == '__main__':
    main(1024, 5)
# print(memory_rascal.__name__,'\n\n')

# outcome = memory_rascal(1024)

# cd BUAA_21/Week8
# mprof memory_test.py
# mprof plot 绘制最近的内存检测数据的图像
# mprof clean 清除所有.dat文件
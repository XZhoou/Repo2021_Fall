from functools import wraps


class Time:
    '''
    实现运行时间分析的类
    '''

    def __init__(self):
        pass

    def __call__(self, func):
        @wraps(func)
        @profile
        def wrapper(*args, **kwargs):
            # print("Time_profile decorate class is working.")
            return func(*args, **kwargs)
        return wrapper


@Time()
def time_rascal(x):
    '''
    实际上是一个运行时间很长的函数，所以不妨把它命名为time_rascal
    '''
    if x < 0:
        return None
    if x == 1:
        return 1
    elif x == 0:
        return 1
    else:
        return time_rascal(x-1) + time_rascal(x-2)


def main(x):
    outcome = time_rascal(x)


if __name__ == '__main__':
    main(35)
# 这段代码不能直接运行，会出现NameError: name 'profile' is not defined的错误
# 需要在终端输入kernprof -l -v 文件名.py

from line_profiler import LineProfiler
# 函数实现运行时间记录
def f(x):
    '''
    递归求解Fibonacci数列的第n项
    '''
    if x < 0:
        return None
    if x == 1:
        return 1
    elif x == 0:
        return 1
    else:
        return f(x-1) + f(x-2)

def main(x):
    Profiler = LineProfiler()
    func = Profiler(f)
    outcome = func(x)
    Profiler.print_stats()

if __name__ == '__main__':
    # main(30)
    main(35)

import random

def random_walk(N=10, mu=3, X0=1, sigma=1):
    '''
    迭代生成N个随机游走变量的生成器
    N为数据规模
    随机游走表现为Xt = mu + Xt-1 + Wt
    Wt是服从高斯分布的随机变量

    参数中X0为初始值
    u为随机游走的漂移量
    sigma为高斯分布的标准差，默认为1
    '''
    n = 0
    x = X0
    while (n < N):
        yield x
        x = x + mu + random.gauss(0, sigma)
        n += 1


def multidimensional_random_walk(demension=10, N=10, mu=3, X0=[0 for i in range(10)], sigma=1):
    if demension == 1:
        data = random_walk(N=N, mu=mu, X0=X0, sigma=sigma)
        return data
    elif demension >= 2:
        if isinstance(X0, list):
            if len(X0) == demension:
                pass
            elif len(X0) > demension:
                X0 = X0[:demension]
            elif len(X0) < demension:
                print("\nNot enough X0.\nSet initial value 0.\n")
                X0 = [0 for i in range(demension)]
            else:
                pass
        else:
            '''
            如果n维的随机游走序列都没有给出初始值，那么就默认初始值都为0
            '''
            print("\nNot enough X0.\nSet initial value all 0.\n")
            X0 = [0 for i in range(demension)]
        for i in range(demension):
            exec(
                "data%d=random_walk(N=N, mu=mu, X0=X0[%d], sigma=sigma)" % (i, i))
        data = zip(*list(map(eval, ["data%d" % i for i in range(demension)])))
        return data

def main():

    data = multidimensional_random_walk(demension=5, N=10, mu=5, X0=[5, 8, 9], sigma=1)
    for i in data:
        for j in i:
            print("%.2f" % j, end='\t')
        print()


if __name__ == '__main__':
    main()

import networkx as nx
import matplotlib.pyplot as plt

def plotdegree_distribution(lines, x_1, x_2):
    '''
    度在[x_1,x_2]范围内的的分布图
    输入节点文件即可

    因为不太需要节点的其他属性，
    只需要节点信息和边的信息，所以采用networkx库进行分析和可视化
    '''

    G = nx.Graph()
    edge_index = lines.index("*Edges\n")

    for i in lines[1:edge_index]:
        lis = i.split('\t')
        G.add_node(int(lis[0]))
    for i in lines[edge_index+1:]:
        lis = i.split('\t')
        G.add_edge(int(lis[0]), int(lis[1]), weight=1)
    print(nx.info(G))

    degree = nx.degree_histogram(G)  # 返回图中所有节点的度分布序列

    plt.bar([i for i in range(x_1, x_2+1)], degree[x_1:x_2+1],
            width=0.80, color='steelblue', alpha=0.9)

    plt.title("Frequency Histogram")
    plt.ylabel("Quantity")
    plt.xlabel("Degree")
    plt.show()


def draw_graph(lines):
    '''
    绘制节点文件的网络图

    因为不太需要节点的其他属性，
    只需要节点信息和边的信息，所以采用networkx库进行分析和可视化
    '''
    G = nx.Graph()
    edge_index = lines.index("*Edges\n")

    for i in lines[1:edge_index]:
        lis = i.split('\t')
        G.add_node(int(lis[0]))
    for i in lines[edge_index+1:]:

        lis = i.split('\t')
        G.add_edge(int(lis[0]), int(lis[1]), weight=1)

    # 输出无向图的信息
    # print("Info of the graph:\n",nx.info(G))
    # 绘制网络图
    nx.draw_shell(G,with_labels = True)
    # 展示图片
    plt.show()

import GraphStat.NetworkBulider.node as GsNbNode
import GraphStat.NetworkBulider.graph as GsNbGraph
import GraphStat.NetworkBulider.stat as GsNbStat
import GraphStat.Visualization.plotgraph as GsVPlot
import GraphStat.Visualization.plotnodes as GsVPlotNds


def test_node_module(lines):

    NodeInfoList = GsNbNode.init_node(lines)
    # 返回一个列表组成的矩阵

    GsNbNode.print_node(NodeInfoList[1])
    # 打印第二个节点的信息
    # *Node Infomation*
    # ID:                     1
    # Name:                   "Karen Allen"
    # Weight:                 7467
    # Node Type:              starring

    # *Other Information*:
    # American film actors
    # American stage actors
    # American video game actors
    # Bard College at Simon's Rock faculty
    # Illinois actors
    # People from Greene County, Illinois
    # Saturn Award winners

    # Adjecent Table:
    # [[1, 11814, 1], [1, 3869, 1], [1, 11348, 1], [1, 9023, 1], [1, 7353, 1], [1, 11190, 1], [1, 13214, 1], [1, 4562, 1], [1, 5465, 1], [1, 6106, 1], [1, 7922, 1], [1, 13175, 1], [1, 11814, 1]]

    degree = GsNbNode.get_degree(NodeInfoList[1])
    # The degree of the vertex is 13.
    # 但是这里仅仅统计的是从该节点出发的边，因为该图是无向图，所以真实的节点的度可能大于13
    AdjacentNodeList = GsNbNode.get_adjecent_node(NodeInfoList[1])
    # 这里也仅仅统计的是从节点1出发的边相邻的点，因为该图是无向图，所以真实的节点1相邻的节点并不止这些
    # The Adjacent node of the 1 node is:
    # 11814
    # 3869
    # 11348
    # 9023
    # 7353
    # 11190
    # 13214
    # 4562
    # 5465
    # 6106
    # 7922
    # 13175

    return NodeInfoList


def test_graph_module(lines):

    # 返回一个字典，分别存储节点信息和边信息
    # 利用邻接表结构进行无向图的存储
    Graph_list = GsNbGraph.init_graph(lines)

    # 序列化图信息
    GsNbGraph.save_graph(Graph_list)

    # 重新加载已经序列化存储的信息
    load_list = GsNbGraph.load_graph("BUAA_21/Week4/graph_info.json")

    return Graph_list
#return Graph_list


def test_stat_module(graph):

    average_degree = GsNbStat.cal_average_degree(graph)
    print("\nThe average degree of the graph is:%.2f.\n" % average_degree)
    # The average degree of the graph is: 7.16.

    # 计算网络的度分布, 返回一个字典
    degree_distribution_dict = GsNbStat.cal_degree_distribution(graph)
    # print("The degree distribution dict is:\n", degree_distribution_dict)
    # The degree distribution dict is:
    #  {'0': 6, '1': 12, '2': 13, '3': 5, '4': 0, '5': 1, '6': 4, '7': 1, '8': 0, '9': 0, '10': 1, '11': 1, '12': 1, '13': 4, '14': 1, '15': 7, '16': 0, '17': 3, '18': 1, '19': 1, '20': 10, '21': 2, '22': 3, '23': 0, '24': 14, '25': 0, '26': 0, '27': 1, '28': 4, '29': 4, '30': 0, '31': 5, '32': 0, '33': 0, '34': 21, '35': 0, '36': 24, '37': 2, '38':
    # 1, '39': 4, '40': 8, '41': 1, '42': 1, '43': 4, '44': 0, '45': 1, '46': 2, '47': 1, '48': 1, '49': 4, '50': 0, '51': 2, '52': 4, '53': 3, '54': 1, '55': 1, '56': 5, '57': 2, '58': 11, '59': 33, '60': 1, '61': 2, '62': 1, '63': 0......}

    # 根据存储的图的结构，得到每个节点的类型，返回一个字典
    type_dict = GsNbStat.get_type(graph)
    # print("The type distribution of the graph is:\n", type_dict)
    #  The type distribution of the graph is:
    #  {'0': 'starring', '1': 'starring', '2': 'writer', '3': 'director', '4': 'starring', '5': 'starring', '6': 'starring', '7': 'director', '8': 'writer', '9': 'writer', '10': 'starring', '11': 'director', '12': 'writer', '13': 'starring', '14': 'starring', '15': 'writer', '16': 'director', '17': 'writer', '18': 'starring', '19': 'starring', '20':
    # 'starring', '21': 'writer', '22': 'director', '23': 'director',...}


def test_plotgraph_module(lines):
    # 度在[x_1, x_2]范围内的的分布图
    # 输入节点文件即可
    # 生成度在1~20之间的节点的频数分布
    GsVPlot.plotdegree_distribution(lines, 1, 20)

    # 绘制节点文件的网络图
    # GsVPlot.draw_graph(lines)
    # 运行时间超过20min，还是没有生成结果


def test_plotnode_module(lines):
    # 生成所有结点的type的统计结果，并绘制柱状图
    GsVPlotNds.plot_nodes_attr(lines, 'type')


def data_clean():
    '''
    清洗数据
    去除重复的边
    '''
    with open("BUAA_21/Week4/newmovies.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
    edge_index = lines.index('*Edges\n')
    new = []
    new.extend(lines[:edge_index])

    for i in lines[edge_index+1:]:
        lis = i.split('\t')[0:2]
        lis = sorted(lis, key=int)
        if lis not in new:
            new.append(lis)
        else:
            pass
    with open("BUAA_21/Week4/newnew_movies.txt", 'w') as f:
        for i in new[:edge_index]:
            print(i, end='', file=f)
        print("*Edges\n", end='', file=f)
        for i in new[edge_index:]:
            print("%s\t%s\t1" % (i[0], i[1]), file=f)


if __name__ == '__main__':

    file = "C:/Users/DELL/Desktop/Code/BUAA_21/Week4/newnew_movies.txt"

    # data_clean()

    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open("BUAA_21/Week4/NodeInfoList.txt", "w+") as f:
        NodeInfoList = test_node_module(lines)
        print(*NodeInfoList, sep='\n', file=f)

    with open("BUAA_21/Week4/graph.txt", "w+") as f:
        graph = test_graph_module(lines)
        print(*graph, sep='\n', file=f)

    # 是个测试模块，并不需要返回结果，如果有返回变量的需要直接调用stat.py模块中的函数即可
    test_stat_module(graph)

    test_plotgraph_module(lines)

    test_plotnode_module(lines)

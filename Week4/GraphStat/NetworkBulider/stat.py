def cal_average_degree(graph):
    '''
    计算网络中的平均度
    '''

    adjacent_table = []
    sum_degree = 0
    for i in graph:
        vector = []
        vector.append(int(i['Vertex']['Id']))
        vector.append(i['AdjacentNode'])

        adjacent_table.append(vector)

        sum_degree += len(i['AdjacentNode'])
    average_degree = sum_degree*2/float(len(adjacent_table))

    return average_degree


def cal_degree_distribution(graph):
    '''
    计算网络的度分布,返回一个字典
    '''
    degree_distribution_dict = {}
    for i in graph:
        degree_distribution_dict[i['Vertex']['Id']] = len(i['AdjacentNode'])

    return degree_distribution_dict


def get_type(graph):
    '''
    根据存储的图的结构，得到每个节点的类型，返回一个字典
    '''
    type_dict = {}
    for i in graph:
        type_dict[i['Vertex']['Id']] = i['Vertex']['Type']

    return type_dict


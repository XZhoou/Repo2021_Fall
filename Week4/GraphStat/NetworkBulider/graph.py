import pickle


def init_graph(lines):
    '''

    返回一个字典，分别存储节点信息和边信息
    利用邻接表结构进行无向图的存储
    '''
    index_egde = lines.index("*Edges\n")

    # # 只保留存储节点的信息
    # # print(index_egde)
    # # 创建一个空矩阵，存储所有结点的信息
    # NodeInfoList = []
    Graph_List = []

    for line in lines[1:index_egde]:
        dic = {}
        vector = {}
        lis = line.split('\t')

        dic['Id'] = lis[0]
        dic['Name'] = lis[1]
        dic['Weight'] = lis[2]  # 因为权重信息并不用得上，所以加入字典中并不影响
        dic['Type'] = lis[3]
        dic['OtherInfo'] = lis[4].split('\n')[0].split(';')[:-1]
        # dic['EdgesTable'] = []

        vector["Vertex"] = dic
        vector["AdjacentNode"] = []
        Graph_List.append(vector)

    #     # {'Id': '34282', 'Name': '"The Lonesome Mouse"', 'Type': 'movie', 'OtherInfo': ['1943 films', 'Tom and Jerry cartoons']}
    # # 之后加入邻接表信息
    for line in lines[index_egde+1:]:
        lis = line.split('\t')
        if int(lis[1]) not in Graph_List[int(lis[0])]["AdjacentNode"]:
            Graph_List[int(lis[0])]["AdjacentNode"].append(int(lis[1]))
        else:
            pass

    return Graph_List


def save_graph(graph):
    '''
    序列化图信息
    '''
    with open("BUAA_21/Week4/graph_info.json", "wb") as f:
        pickle.dump(graph, f)


def load_graph(graph_info):
    '''
    重新加载已经序列化存储的信息
    '''
    with open(graph_info, "rb") as f:
        info = pickle.load(f)
    return info

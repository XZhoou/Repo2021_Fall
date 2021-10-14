def init_node(lines):
    '''
    返回字典dic，key为节点的属性，值为对应的属性值
    '''

    index_egde = lines.index("*Edges\n")

    # 只保留存储节点的信息
    # print(index_egde)
    # 创建一个空矩阵，存储所有结点的信息
    NodeInfoList = []

    for line in lines[1:index_egde]:
        dic = {}
        lis = line.split('\t')

        dic['Id'] = lis[0]
        dic['Name'] = lis[1]
        dic['Weight'] = lis[2]  # 因为权重信息并不用得上，所以加入字典中并不影响
        dic['Type'] = lis[3]
        dic['OtherInfo'] = lis[4].split('\n')[0].split(';')[:-1]
        dic['EdgesTable'] = []
        NodeInfoList.append(dic)
        # {'Id': '34282', 'Name': '"The Lonesome Mouse"', 'Type': 'movie', 'OtherInfo': ['1943 films', 'Tom and Jerry cartoons']}
    # 之后加入该节点相邻的边的信息
    for line in lines[index_egde+1:]:
        lis = line.split('\t')
        EdgesVector = [int(lis[0]), int(lis[1]), 1]
        if EdgesVector not in NodeInfoList[int(lis[0])]["EdgesTable"]:
            NodeInfoList[int(lis[0])]['EdgesTable'].append(EdgesVector)
        else:
            pass
        # NodeInfoList[int(lis[0])]['EdgesTable'].append(EdgesVector)

    #  {'Id': '22', 'Name': '"Bruce Malmuth"', 'Type': 'director', 'OtherInfo': ['1934 births', '2005 deaths', 'American film directors', 'Deaths from throat cancer', 'Cancer deaths in California'], 'EdgesTable': [[22, 13393, 1], [22, 837, 1], [22, 242, 1]]}
    return NodeInfoList


def get_degree(node):
    '''
    获取对应的节点的度
    '''
    degree = len(node["EdgesTable"])

    print("The degree of the vertex is %d." % degree)


def get_adjecent_node(node):
    '''
    获取该节点相邻的节点，按行打印，并返回一个列表
    '''

    AdjacentNodeList = []
    print("\nThe Adjacent node of the %s node is:" % node["Id"])
    for item in node["EdgesTable"]:
        AdjacentNodeList.append(item[1])
        print(item[1])
    return AdjacentNodeList


def print_node(node):
    '''
    显示节点全部信息（利用format函数）
    '''
    print("\n*Node Infomation*\nID:\t\t\t{:<8s}\nName:\t\t\t{:<20s}\nWeight:\t\t\t{:<10s}\nNode Type:\t\t{:<15s}\n\n*Other Information*:\n{}\n\nEdges Table:\n{}".format(
        node["Id"], node["Name"], node["Weight"], node["Type"], "\n".join(node["OtherInfo"]), node["EdgesTable"]))
    return None

import matplotlib.pyplot as plt
import collections

def plot_nodes_attr(lines, feature='type'):
    '''
    绘制图中节点属性的统计结果
    目前只有节点的type的统计绘图功能
    '''

    index_egde = lines.index("*Edges\n")

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

        vector["Vertex"] = dic
        vector["AdjacentNode"] = []
        Graph_List.append(vector)

    for line in lines[index_egde+1:]:
        lis = line.split('\t')
        if int(lis[1]) not in Graph_List[int(lis[0])]["AdjacentNode"]:
            Graph_List[int(lis[0])]["AdjacentNode"].append(int(lis[1]))
        else:
            pass

    if feature == 'type':
        type_list = []
        for i in Graph_List:
            type_list.append(i['Vertex']['Type'])

        type_dict = collections.Counter(type_list)

        plt.xlabel("Type")
        plt.ylabel("Number")
        plt.bar([1, 2, 3, 4], list(type_dict.values()),
                align='center', color=['#4E598C', '#F9C784', '#FCAF58', '#FF8C42'], width=0.5, alpha=0.7)
        plt.ylim(ymin=0, ymax=22000)
        plt.xticks([1, 2, 3, 4], list(type_dict.keys()))
        plt.title("Node Type Distribution")
        plt.show()
    else:
        print("The feature doesn't fit.\n")

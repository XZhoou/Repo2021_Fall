from Error import NotTimeDataError
from Error import NotSpatialDataError, NotTimeDataError
from pyecharts import Map, Timeline
import matplotlib.pyplot as plt
import sys

namemap = {"Beijing": "北京", "Tianjin": "天津", "Hebei": "河北", "Shanxi": "山西", "InnerMongolia": "内蒙古", "Liaoning": "辽宁", "Jilin": "吉林", "Shanghai": "上海", "Heilongjiang": "黑龙江", "Jiangsu": "江苏", "Zhejiang": "浙江", "Anhui": "安徽", "Fujian": "福建", "Jiangxi": "江西",
           "Shandong": "山东", "Henan": "河南", "Hubei": "湖北", "Hunan": "湖南", "Guangdong": "广东", "Guangxi": "广西", "Hainan": "海南", "Chongqing": "重庆", "Sichuan": "四川", "Guizhou": "贵州", "Yunnan": "云南", "Shaanxi": "陕西", "Gansu": "甘肃", "Qinghai": "青海", "Ningxia": "宁夏", "Xinjiang": "新疆"}

class Visualization(object):

    def line_graph(dic):
        '''
        根据时间分析或者空间分析后的数据绘制折线图
        '''
        x = list(dic["Value"].keys())
        y = list(dic["Value"].values())

        if "Province" in dic.keys():

            plt.plot(x, y, linewidth=2, marker='*',
                     label="The emission of CO2")
            plt.tick_params(axis='both', labelsize=6)
            plt.title("Time analysis of %s CO2 emission in %s (1997 - 2015)" %
                      (dic["Type"], dic["Province"]), fontsize=10)
            plt.legend(loc='upper left')
            plt.show()

        elif "Time" in dic.keys():
            x = x[:-2]
            y = y[:-2]
            # plt.plot(x, y, linewidth=2, marker='*', label="The emission of CO2", color="#0A2463", alpha=0.5)
            plt.bar(x, y, width=0.9, color="#0A2463", alpha=0.6)
            plt.xticks(x, x, rotation=55, fontsize=5)
            plt.yticks(fontsize=8)

            plt.title("Spatial analysis of %s CO2 emission of Year %s" %
                      (dic["Type"], dic["Time"]), fontsize=10)
            plt.show()

    def pie_graph(dic):
        '''
        根据空间分析后的数据绘制饼状图
        '''
        x = list(dic["Value"].keys())
        y = list(dic["Value"].values())
        try:
            if "Time" in dic.keys():
                x = x[:-2]
                y = y[:-2]

                colors = ("#ECCBD9", "#E1EFF6", "#97D2FB", "#83BCFF", "#80FFE8",
                          "#4B4A67", "#2364A4", "#FEC601", "#EA7317", "#AF42AE")
                plt.figure(figsize=(8, 12), dpi=80)
                patches, l_text = plt.pie(
                    y, radius=3, autopct=None, colors=colors, labels=x, labeldistance=1.03)
                for i in l_text:
                    i.set_size(6)
                plt.title("%s proportion of provinces in %s" %
                          (dic["Type"], dic["Time"]), fontsize=14)
                plt.axis("equal")
                plt.show()

            elif "Province" in dic.keys():
                raise NotSpatialDataError()
        except NotSpatialDataError as NSDE:
            print(NSDE.message)
            sys.exit(0)

    def province_distribution(dic):
        '''
        利用Pyecharts，对进行空间分析后的数据绘制地图'''
        try:
            if "Time" in dic.keys():

                if "Industry" in dic.keys():
                    temp = list(dic["Value"].keys())
                    values = list(dic["Value"].values())
                    map = Map("CO2 emission of China", "Time:%s\nType:%s\nIndustry:%s" %
                              (dic["Time"], dic["Type"], dic["Industry"]), width=1200, height=800)
                    province = []
                    for i in temp:
                        province.append(namemap[i])
                    map.add('', province, values, maptype='china',
                            visual_range=[0, max(values)], is_visualmap=True)

                    map.render(path="BUAA_21/Week7/China CO2 emission (%s-%s-%s).html" %
                               (dic["Time"], dic["Type"], dic["Industry"]))
                else:
                    temp = list(dic["Value"].keys())[:-2]
                    values = list(dic["Value"].values())[:-2]

                    map = Map("CO2 emission of China", "Time:%s\nType:%s\n" % (
                        dic["Time"], dic["Type"]), width=1200, height=800)
                    province = []
                    for i in temp:
                        province.append(namemap[i])
                    map.add('', province, values, maptype='china',
                            visual_range=[0, max(values)], is_visualmap=True)

                    map.render(path="BUAA_21/Week7/China CO2 emission (%s-%s).html" %
                               (dic["Time"], dic["Type"]))
            else:
                raise NotSpatialDataError()
        except NotSpatialDataError as NSDE:
            print(NSDE.message)
            sys.exit(0)

    def province_time_line(dic):
        '''
        利用Pyecharts对进行时间分析后的数据进行分析，绘制时间轴地图'''

        try:
            if "Province" in dic.keys():
                if "Industry" in dic.keys():
                    timedata = Timeline(
                        is_auto_play=True, timeline_bottom=0)
                    max_num = max(dic["Value"].values())
                    for year, data in dic["Value"].items():
                        map = Map("CO2 emission of China", "Province:%s\nType:%s\nIndustry:%s" %
                                  (dic["Province"], dic["Type"], dic["Industry"]), width=1200, height=800)

                        ma = map.add('', [namemap[dic["Province"]]], [
                                     data], maptype="china", visual_range=[0, max_num], is_visualmap=True)
                        timedata.add(time_point=year, chart=ma)
                    timedata.render(path="BUAA_21/Week7/1997-2015 CO2 emission (%s-%s-%s).html" %
                                    (dic["Province"], dic["Type"], dic["Industry"]))
                else:
                    timedata = Timeline(is_auto_play=True, timeline_bottom=0)
                    max_num = max(dic["Value"].values())
                    for year, data in dic["Value"].items():
                        map = Map("CO2 emission of China", "%s-%s" %
                                  (dic["Province"], dic["Type"]), width=1200, height=800)

                        ma = map.add('', [namemap[dic["Province"]]], [
                            data], maptype="china", visual_range=[0, max_num], is_visualmap=True)
                        timedata.add(time_point=year, chart=ma)
                    timedata.render(path="BUAA_21/Week7/1997-2015 CO2 emission (%s-%s).html" %
                                    (dic["Province"], dic["Type"]))
            else:
                raise NotTimeDataError

        except NotTimeDataError as NTDE:
            print(NTDE.message)
            sys.exit(0)

    def time_spatial_visualization(dic):

        time_range = list(dic["Value"].keys())
        timedata = Timeline(is_auto_play = True,timeline_bottom = 0)
        for time in time_range:
            temp = list(dic["Value"][time].keys())
            values = list(dic["Value"][time].values())
            province = []
            for i in temp:
                province.append(namemap[i])
            map = Map("CO2 emission of China", "Time: %s\nType: %s\nIndustry: %s\n"%(time,dic["Type"],dic["Industry"]),width=1200, height=800)
            ma = map.add('',province,values,maptype = "china",visual_range = [0,max(values)],is_visualmap = True)
            timedata.add(time_point=time, chart=ma)
        timedata.render(path = "BUAA_21/Week7/1997-2015 CO2 emission (China-%s-%s).html"%(dic["Type"],dic["Industry"]))

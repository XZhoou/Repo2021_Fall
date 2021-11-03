class NotNumError(ValueError):
    '''
    检测到数据表中的空值时，抛出该异常
    并保存该数据对应的年度，省份，部门，排放类型等信息
    '''
    def __init__(self, year, province, industry, type):
        self.year = year
        self.province = province
        self.industry = industry
        self.type = type
        self.message = f"Not number error: \nYear: {self.year}\nProvince: {self.province}\nIndustry:{self.industry}\nType: {self.type}\n"


class FindNoFilesError(Exception):
    '''
    没有查找到给定目录下的xlsx文件时，抛出该异常
    '''
    def __init__(self, dir):
        self.dir = dir
        self.message = f"Could not find xlsx file in current directory:{self.dir}"


class ProvinceParameterError(Exception):
    '''
    数据表中没有对应的省份名时，抛出该异常（说明省份名称输入出现错误）
    '''
    def __init__(self, province):
        self.message = f"Area parameter error: {province} doesn't exist."


class IndustryParameterError(Exception):
    '''
    数据表中没有对应的部门名时，抛出该异常（说明部门名称输入出现错误）
    '''
    def __init__(self, industry):
        self.message = f"Industry parameter error: {industry} doesn't exist"


class TypeParameterError(Exception):
    '''
    数据表中没有对应的排放类型时，抛出该异常（说明排放类型名称输入出现错误）
    '''
    def __init__(self, type):
        self.message = f"Type parameter error: {type} doesn't exist."


class TimeParameterError(Exception):
    '''
    没有对应年份的数据时，抛出该异常（说明时间的输入出现错误）
    '''
    def __init__(self, time):
        self.message = f"Time parameter error: {time} doesn't exist."


class NotSpatialDataError(Exception):
    '''
    在绘图时如果传入的数据并不是空间分析后的数据，抛出该异常
    '''
    def __init__(self):
        self.message = f"The data is not spatial data."


class NotTimeDataError(Exception):
    '''
    在绘图时如果传入的数据并不是时间分析后的数据，抛出该异常
    '''
    def __init__(self):
        self.message = f"The data is not time data."


class ZeroDivisionError(Exception):
    '''
    如果某个省市的Sum列对应的数据为0，那么在之后计算各部分的排放比例时已经会出现DivisionByZero异常，提前进行检测
    '''
    def __init__(self, province, time, type):
        self.province = province
        self.time = time
        self.type = type
        self.message = f"ZeroDivision:\n{self.type} CO2 emission of {self.province} in {self.time} is 0."

from Error import NotNumError, IndustryParameterError, FindNoFilesError, ProvinceParameterError, TimeParameterError, TypeParameterError,  ZeroDivisionError
from visualization import Visualization
import xlrd
import os
import sys


class ReadData(object):
    '''
    数据分析类，实现数据读取以及基本的时间空间分析'''

    def __init__(self):
        self.file_list = []
        self.xlsx_list = []

    def find_xlsx(self, dir):
        '''
        找到该目录下的所有xlsx文件，保存到self.file_list中去
        '''
        self.time_range = []
        file_list = []
        for root_dir, sub_dir, files in os.walk(r''+dir):
            for file in files:
                if file.endswith('.xlsx'):
                    file_list.append(os.path.join(root_dir, file))
        try:
            if file_list == []:
                raise FindNoFilesError(dir)
        except FindNoFilesError as FNFE:
            print(FNFE.message)
            sys.exit(0)

        self.file_list = file_list
        for i in self.file_list:
            self.time_range.append(i[-9:-5])

    def read(self):
        '''
        对所有xlsx进行读取，写入到列表中去
        '''

        for i in self.file_list:
            self.xlsx_list.append(xlrd.open_workbook(i))

    def time_analysis(self, province, type):
        '''
        对某个省的整个时间范围内的数据进行分析
        提取每个年份下的sum表，读取对应省份某个排放类型的数据
        '''
        self.time_analysis_dict = {}

        time_analysis_value_list = []
        for xlsx in self.xlsx_list:
            sheet1 = xlsx.sheets()[0]
            try:
                if province not in sheet1.col_values(0):
                    raise ProvinceParameterError(province)
            except ProvinceParameterError as PPE:
                print(PPE.message)
                sys.exit(0)
            finally:
                pass

            province_index = sheet1.col_values(0).index(province)

            try:
                if type not in sheet1.row_values(0):
                    raise TypeParameterError(type)
            except TypeParameterError as TPE:
                print(TPE.message)
            finally:
                pass

            type_index = sheet1.row_values(0).index(type)
            time_analysis_value_list.append(
                sheet1.cell(province_index, type_index).value)

        self.time_analysis_dict["Value"] = dict(
            zip(self.time_range, time_analysis_value_list))
        self.time_analysis_dict["Type"] = type
        self.time_analysis_dict["Province"] = province

    def spatial_analysis(self, time, type):
        '''
        对某一年的sum表进行分析
        time是输入的年份的参数
        type是列名即排放类型
        '''
        self.spatial_analysis_dict = {}
        try:
            if time not in self.time_range:
                raise TimeParameterError(time)
        except TimeParameterError as TPE:
            print(TPE.message)
            sys.exit(0)
        finally:
            pass

        time_index = self.time_range.index(time)
        xlsx = self.xlsx_list[time_index]
        sheet1 = xlsx.sheets()[0]

        try:

            if type not in sheet1.row_values(0):
                raise TypeParameterError(type)
        except TypeParameterError as TPE:
            print(TPE.message)
            sys.exit(0)

        type_index = sheet1.row_values(0).index(type)

        col_value = sheet1.col_values(type_index)[1:]
        provinces = sheet1.col_values(0)[1:]
        col_value.pop(-2)
        provinces.pop(-2)
        self.spatial_analysis_dict["Value"] = dict(zip(provinces, col_value))
        self.spatial_analysis_dict["Type"] = type
        self.spatial_analysis_dict["Time"] = time
        # print(self.spatial_analysis_dict)

    def proportion_analysis(self):
        '''
        对excel文件中名为sum的sheet进行分析

        如果一个省的Total数据为0，那么在计算分部门碳排放比例时，一定会出现Division By zero错误
        所以要对Total数据为0的数据进行记录，保存其年份，部门，省份等
        '''
        try:
            for i in self.time_range:
                self.spatial_analysis(i, "Total")
                value_dict = self.spatial_analysis_dict["Value"]
                sum_num = value_dict["Sum-CO2"]
                try:
                    for i in value_dict.keys():
                        if i != "Sum-CO2" and (value_dict[i] != 0):
                            # print(value_dict[i]/sum_num)
                            # print("The total emission of %s in %s is %.2f" % (i, self.spatial_analysis_dict["Time"], value_dict[i]))
                            pass
                        elif i == "Sum-CO2":
                            continue
                        elif value_dict[i] == 0:
                            raise ZeroDivisionError(
                                i, self.spatial_analysis_dict["Time"], self.spatial_analysis_dict["Type"])
                except ZeroDivisionError as ZDE:
                    print("\n"+ZDE.message+"\n")
        except AttributeError as AE:
            print(AE)
            sys.exit(0)

    def detailed_time_analysis(self, province, type, industry):
        '''
        详细的时间分析，不针对Sum表，而是针对更加细致的分省分部门的数据表进行分析
        对整个时间范围内，某个省某个部门的某个排放类型的排放数据进行分析
        将分析后的结果以字典形式保存在类的detailed_time_analysis_dict属性中
        '''
        self.detailed_time_analysis_dict = {}
        time_range = []
        detail_time_analysis_list = []
        year_index = 0
        for i in self.xlsx_list:
            sheet = i.sheet_by_name(province)
            try:
                if type not in sheet.row_values(0):
                    raise TypeParameterError(type)
                elif industry not in sheet.col_values(0):
                    raise IndustryParameterError(industry)

            except TypeParameterError as TPE:
                print(TPE.message)
                sys.exit(0)
            except IndustryParameterError as IPE:
                print(IPE.message)
                sys.exit(0)
            finally:
                pass

            type_index = sheet.row_values(0).index(type)
            industry_index = sheet.col_values(0).index(industry)
            cell_value = sheet.cell(industry_index, type_index).value

            try:
                if cell_value != '':
                    detail_time_analysis_list.append(cell_value)
                    time_range.append(self.time_range[year_index])
                    year_index += 1
                else:
                    year_index += 1
                    raise NotNumError(
                        year=self.time_range[year_index-1], province=province, industry=industry, type=type)
            except NotNumError as NNE:
                print(NNE.message)
            finally:
                pass

        self.detailed_time_analysis_dict["Value"] = dict(
            zip(time_range, detail_time_analysis_list))
        self.detailed_time_analysis_dict["Type"] = type
        self.detailed_time_analysis_dict["Industry"] = industry
        self.detailed_time_analysis_dict["Province"] = province

    def detailed_spatial_analysis(self, time, type, industry):
        '''
        详细的空间分析，不针对Sum表，而是针对更加细致的分省分部门的数据表进行分析
        对某一年，全国范围内某个部门的某个排放类型的排放数据进行分析
        将分析后的结果以字典形式保存在类的detailed_spatial_analysis_dict属性中
        '''
        self.detailed_spatial_analysis_dict = {}
        self.detailed_spatial_analysis_dict["Value"] = {}
        # print(self.time_range)
        time_index = self.time_range.index(str(time))
        xlsx = self.xlsx_list[time_index]
        sheet0 = xlsx.sheets()[0]

        province_lis = sheet0.col_values(0)[1:-2]

        for province in province_lis:
            sheet = xlsx.sheet_by_name(province)

            try:
                if type not in sheet.row_values(0):
                    raise TypeParameterError(type)
                elif industry not in sheet.col_values(0):
                    raise IndustryParameterError(industry)
            except TypeParameterError as TPE:
                print(TPE.message)
                sys.exit(0)
            except IndustryParameterError as IPE:
                print(IPE.message)
                sys.exit(0)
            finally:
                pass

            type_index = sheet.row_values(0).index(type)
            industry_index = sheet.col_values(0).index(industry)
            cell_value = sheet.cell(industry_index, type_index).value
            try:
                if cell_value != '':
                    self.detailed_spatial_analysis_dict["Value"][province] = cell_value
                else:
                    raise NotNumError(
                        year=time, province=province, industry=industry, type=type)
            except NotNumError as NNE:
                print(NNE.message)

        self.detailed_spatial_analysis_dict["Time"] = time
        self.detailed_spatial_analysis_dict["Type"] = type
        self.detailed_spatial_analysis_dict["Industry"] = industry

    def time_and_spatial_analysis(self, type, industry):
        '''
        整体全面的分析，对整个时间范围内，全国各个省某个部门某排放类型的数据
        将分析结果以字典形式保存在类的time_and_spatial_analysis属性中'''
        self.time_and_spatial_analysis_dic = {}
        self.time_and_spatial_analysis_dic["Value"] = {}

        province_lis = self.xlsx_list[0].sheets()[0].col_values(0)[1:-2]

        tot = 0
        for i in self.xlsx_list:
            time = self.time_range[tot]
            tot += 1
            self.time_and_spatial_analysis_dic["Value"][time] = {}
            for province in province_lis:
                sheet = i.sheet_by_name(province)
                try:
                    if type not in sheet.row_values(0):
                        raise TypeParameterError(type)
                    elif industry not in sheet.col_values(0):
                        raise IndustryParameterError(industry)
                except TypeParameterError as TPE:
                    print(TPE.message)
                    sys.exit(0)
                except IndustryParameterError as IPE:
                    print(IPE.message)
                    sys.exit(0)
                finally:
                    pass
                type_index = sheet.row_values(0).index(type)
                industry_index = sheet.col_values(0).index(industry)
                cell_value = sheet.cell(industry_index, type_index).value
                try:
                    if cell_value != '':
                        self.time_and_spatial_analysis_dic["Value"][time][province] = cell_value
                    else:
                        raise NotNumError(
                            year=time, province=province, industry=industry, type=type)
                except NotNumError as NNE:
                    print(NNE.message)

        self.time_and_spatial_analysis_dic["Type"] = type
        self.time_and_spatial_analysis_dic["Industry"] = industry


if __name__ == '__main__':

    class_read_data = ReadData()
    class_read_data.find_xlsx("BUAA_21/Week7/CO2")
    class_read_data.read()

    class_read_data.time_analysis("InnerMongolia", "Total")
    Visualization.line_graph(class_read_data.time_analysis_dict)

    class_read_data.spatial_analysis("1997", "Raw Coal")
    Visualization.line_graph(class_read_data.spatial_analysis_dict)

    Visualization.pie_graph(class_read_data.spatial_analysis_dict)

    Visualization.province_time_line(class_read_data.time_analysis_dict)

    Visualization.province_distribution(class_read_data.spatial_analysis_dict)

    class_read_data.detailed_time_analysis(province = "InnerMongolia",type = "Raw Coal", industry= "Total Consumption")
    Visualization.province_time_line(class_read_data.detailed_time_analysis_dict)

    class_read_data.detailed_spatial_analysis(time = 2001, type = "Total", industry = "Total Consumption")
    Visualization.province_distribution(class_read_data.detailed_spatial_analysis_dict)

    class_read_data.time_and_spatial_analysis(type="Total", industry="Total Consumption")
    Visualization.time_spatial_visualization(class_read_data.time_and_spatial_analysis_dic)

    class_read_data.time_and_spatial_analysis(type="Raw Coal", industry="Total Consumption")
    Visualization.time_spatial_visualization(class_read_data.time_and_spatial_analysis_dic)
    
    class_read_data.proportion_analysis()

    

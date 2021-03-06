#!/usr/bin/env python
# encoding: utf-8
# @author: liusir
# @file: excel_utils.py
# @time: 2020/7/5 8:57 上午

import os
import xlrd   #内置模块、第三方模块pip install  自定义模块
from xlutils.copy import copy
from common.localconfig_utils import local_config

class ExcelUtils():
    def __init__(self,file_path,sheet_name):
        self.file_path = file_path
        self.wb = xlrd.open_workbook(self.file_path,formatting_info=True)
        self.sheet_name = sheet_name
        self.sheet = self.get_sheet()  # 整个表格对象

    def get_sheet(self):
        sheet = self.wb.sheet_by_name(self.sheet_name)
        return sheet

    def get_row_count(self):
        row_count = self.sheet.nrows
        return row_count

    def get_col_count(self):
        col_count = self.sheet.ncols
        return col_count

    def __get_cell_value(self,row_index, col_index):
        cell_value = self.sheet.cell_value(row_index,col_index)
        return cell_value

    def get_merged_info(self):
        merged_info = self.sheet.merged_cells
        return merged_info

    def get_merged_cell_value(self,row_index, col_index):
        """既能获取普通单元格的数据又能获取合并单元格数据"""
        cell_value = None
        for (rlow, rhigh, clow, chigh) in self.get_merged_info():
            if (row_index >= rlow and row_index < rhigh):
                if (col_index >= clow and col_index < chigh):
                    cell_value = self.__get_cell_value(rlow, clow)
                    break;  # 防止循环去进行判断出现值覆盖的情况
                else:
                    cell_value = self.__get_cell_value(row_index, col_index)
            else:
                cell_value = self.__get_cell_value(row_index, col_index)
        return cell_value

    def get_sheet_data_by_dict(self):
        all_data_list = []
        first_row = self.sheet.row(0)  #获取首行数据
        for row in range(1, self.get_row_count()):
            row_dict = {}
            for col in range(0, self.get_col_count()):
                row_dict[first_row[col].value] = self.get_merged_cell_value(row, col)
            all_data_list.append(row_dict)
        return all_data_list

    def update_excel_data(self,row_id,col_id,content):
        new_wb = copy(self.wb)
        sheet = new_wb.get_sheet(self.wb.sheet_names().index(self.sheet_name))  # sheet_by_name('Sheet1')
        sheet.write(row_id, col_id, content)
        new_wb.save(self.file_path)

    def clear_excel_column(self,start_id,end_id,col_id):
        new_wb = copy(self.wb)
        sheet = new_wb.get_sheet(self.wb.sheet_names().index(self.sheet_name))  # sheet_by_name('Sheet1')
        for row_id in range(start_id,end_id):
            sheet.write(row_id,col_id,"")
        new_wb.save(self.file_path)


if __name__=='__main__':
    current_path = os.path.dirname(__file__)
    excel_path = os.path.join( current_path,'..',local_config.CASE_DATA_PATH )
    excelUtils = ExcelUtils(excel_path,"Sheet1")
    # excelUtils.update_excel_data(4,14,'xiaoliu')
    print( excelUtils.sheet.row(0) )
    print( excelUtils.sheet.row(0)[0].value)
    for i in range(len(excelUtils.sheet.row(0))):
        if excelUtils.sheet.row(0)[i].value == '测试结果':
            break
    print( i )

    # for row in excelUtils.get_sheet_data_by_dict():
    #     print(row)
    # i = 0 ;
    # for row in excelUtils.get_sheet_data_by_dict():
    #     if row['测试用例编号']=='case01' and row['测试用例步骤'] == 'step_01':
    #         break;
    #     else:
    #         i = i + 1;
    # print( i+1 )
    #
    # testdatas = excelUtils.get_sheet_data_by_dict()
    # for j in range(len(testdatas)):  # 0--4
    #     if testdatas[j]['测试用例编号'] == 'case01' and testdatas[j]['测试用例步骤'] == 'step_01':
    #         break;
    # print( j+1 )




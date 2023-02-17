# Copyright (c) 2023, ahmed and contributors
# For license information, please see license.txt

import frappe
import pandas as pd
from frappe.model.document import Document
# from frappe import _
# import csv
# # from werkzeug.wrappers import Response
import json


class TaskOneDocument(Document):
    dict_is_full = 0
    Males = {}
    Females = {}
    listofDataframes = []
    sheetnameslist = []
    sheetno_after_clear = False

    @frappe.whitelist()
    def send_file(self, csv_file_path):
        csv_file_dict = {}
        TaskOneDocument.Males.clear()
        TaskOneDocument.Females.clear()
        self.clear_data()
        self.gender = ""
        self.sheet_no = ""

        # frappe.msgprint(csv_file_path)
        csv_file = pd.read_csv(
            "/home/vboxuser/Desktop/frappe-bench/sites/dcode.com"+csv_file_path)
        # print(type(data))
        # print(len(data))
        # print(data.loc[5, 'Name'])

        self.dictionary = ""
        for row in range(len(csv_file)):
            namE = csv_file.loc[row, 'Name']

            gendeR = csv_file.loc[row, 'Gender']

            agE = int(csv_file.loc[row, 'Age'])

            csv_file_dict[namE] = [gendeR, agE]
            self.dictionary += str("{0} : {1} , {2}\n".format(
                namE, gendeR, agE))

            if gendeR == "male":
                TaskOneDocument.Males[namE] = [gendeR, agE]
            elif gendeR == "female":
                TaskOneDocument.Females[namE] = [gendeR, agE]
        # frappe.db.set_value("Task One Document", self.name,
        #                     "dictionary", self.dictionary)
        TaskOneDocument.dict_is_full = 1

        # return json.dumps(myDict)

    @frappe.whitelist()
    def send_xlsx_file(self, xlsx_file_path):
        # myDict2 = {}
        TaskOneDocument.Males.clear()
        TaskOneDocument.Females.clear()
        self.clear_data()
        self.gender = ""
        self.sheet_no = ""
        # data2 = pd.read_excel(
        #     "/home/vboxuser/Desktop/frappe-bench/sites/dcode.com"+xlsx_file_path,
        #     sheet_name=["Sheet1", "Sheet2", "Sheet3"], engine="openpyxl",
        # )

        # numberofSheets = len(data2)
        # sh1_data_frame = data2.get("Sheet1")
        # sh2_data_frame = data2.get("Sheet2")
        # sh3_data_frame = data2.get("Sheet3")
        if TaskOneDocument.dict_is_full == 1:
            frappe.throw("data will overwrite")

        ExcellFile = pd.ExcelFile(
            "/home/vboxuser/Desktop/frappe-bench/sites/dcode.com"+xlsx_file_path, engine='openpyxl',
        )
        numberofSheets = len(ExcellFile.sheet_names)
        TaskOneDocument.sheetnameslist = ExcellFile.sheet_names.copy()

        print(len(ExcellFile.sheet_names))

        for sheet in ExcellFile.sheet_names:
            TaskOneDocument.listofDataframes.append(ExcellFile.parse(sheet))

        print("\n")
        print(TaskOneDocument.listofDataframes)
        print("\n")

        # myDocument = frappe.get_doc("Task One Document", self.name)
        # myDocument.db_set("dictionary", "hello")
        # dcmnt = frappe.get_doc("Task One Document", self.name)
        # res = 0
        self.dictionary = ""
        row_count = 0
        for current_dataframe in range(0, len(TaskOneDocument.listofDataframes)):
            for dataframe_row in range(0, len(TaskOneDocument.listofDataframes[current_dataframe])):

                name = TaskOneDocument.listofDataframes[current_dataframe].loc[dataframe_row, 'Name']

                gender = TaskOneDocument.listofDataframes[current_dataframe].loc[dataframe_row, 'Gender']

                age = int(
                    TaskOneDocument.listofDataframes[current_dataframe].loc[dataframe_row, 'Age'])
                self.dictionary += str(row_count)+"  "

                self.dictionary += "{0} : {1} , {2}\n".format(
                    name, gender, age)
                # self.save()
                # myDict2[name] = [gender, age]
                if gender == "male":
                    TaskOneDocument.Males[name] = [gender, age]
                elif gender == "female":
                    TaskOneDocument.Females[name] = [gender, age]
                row_count += 1

        TaskOneDocument.dict_is_full = 1
        return int(numberofSheets)

    @ frappe.whitelist()
    def clear_data(self):
        self.dictionary = " "
        TaskOneDocument.listofDataframes.clear()
        TaskOneDocument.dict_is_full = 0
        # TaskOneDocument.sheetno_after_clear = True
        frappe.msgprint("cleared")

    @ frappe.whitelist()
    def filter_data(self, gender_type):
        if (self.file_value) and (TaskOneDocument.dict_is_full == 1):
            # self.clear_data()

            if gender_type == "Male":
                self.dictionary = ""
                for name, values in TaskOneDocument.Males.items():
                    self.dictionary += str("{0} : {1}\n".format(
                        name, TaskOneDocument.Males[name]))
                TaskOneDocument.dict_is_full = 1
                # TaskOneDocument.Males.clear()

            elif gender_type == "Female":
                self.dictionary = ""
                for name, values in TaskOneDocument.Females.items():
                    self.dictionary += str("{0} : {1}\n".format(
                        name, TaskOneDocument.Females[name]))
                TaskOneDocument.dict_is_full = 1
                # TaskOneDocument.Females.clear()
            else:
                # merging two dictionaries
                # frappe.msgprint(self.file_value)
                males_females_dictionary = {
                    **TaskOneDocument.Males, **TaskOneDocument.Females}
                self.dictionary = ""
                for name, values in males_females_dictionary.items():
                    self.dictionary += str("{0} : {1}\n".format(
                        name, males_females_dictionary[name]))
                TaskOneDocument.dict_is_full = 1

    @ frappe.whitelist()
    def display_sheet(self, current_sheet):

        if TaskOneDocument.dict_is_full == 0:
            frappe.throw("dictionary must be full")

        requested_sheet_index = int(current_sheet)-1
        requested_sheet_dataframe = TaskOneDocument.listofDataframes[requested_sheet_index]

        self.dictionary = ""

        if self.gender == "Male":
            for row in range(len(requested_sheet_dataframe)):
                gender_value = requested_sheet_dataframe.loc[row, 'Gender']

                if gender_value == "male":
                    name_value = requested_sheet_dataframe.loc[row, 'Name']
                    age_value = int(requested_sheet_dataframe.loc[row, 'Age'])
                    self.dictionary += str("{0} : {1} , {2}\n".format(
                        name_value, gender_value, age_value))
        elif self.gender == "Female":
            for row in range(len(requested_sheet_dataframe)):
                gender_value = requested_sheet_dataframe.loc[row, 'Gender']

                if gender_value == "female":
                    name_value = requested_sheet_dataframe.loc[row, 'Name']
                    age_value = int(requested_sheet_dataframe.loc[row, 'Age'])
                    self.dictionary += str("{0} : {1} , {2}\n".format(
                        name_value, gender_value, age_value))

        else:
            self.dictionary = ""
            for row in range(len(requested_sheet_dataframe)):
                name_value = requested_sheet_dataframe.loc[row, 'Name']

                gender_value = requested_sheet_dataframe.loc[row, 'Gender']

                age_value = int(requested_sheet_dataframe.loc[row, 'Age'])
                self.dictionary += str("{0} : {1} , {2}\n".format(
                    name_value, gender_value, age_value))

import pandas as pd
import numpy as np
from os import path


class Conversion:
    def get_label(self):
        """
        由用户输入标签对应关系，原标签应与列名一致。 优化可以采用三基元素字典，用户只需传入原列名（证候名就行）
        数据格式：  {原证候名：（三基元素）} 。其中，字典的值是一个元组。
        """
        user_str = input('请输入原标签及对应三基元素，如：D1-肝-血-虚--D2-心-火-旺--D3......:')
        user_list = user_str.split('--')
        for item in user_list:
            temp = item.split('-')
            self.label[temp[0]] = set(temp[1:])

    def __init__(self):
        self.label = {}
        self.new_label_set = set()
        self.file_path = input('请输入数据路径：').strip()
        try:
            self.data = pd.read_csv(self.file_path)
        except UnicodeDecodeError:
            self.data = pd.read_excel(self.file_path)
        self.get_label()
        self.add_new_label()
        self.assignment()
        self.save()

    def add_new_label(self):
        """
        遍历label字典，将本数据涉及到的三基元素组合到一个集合里面。
        遍历生成的三基元素集合，为每一个三基元素生成值为0的一列，并合并到原数据里面。
        """
        for key, value in self.label.items():
            self.new_label_set = set.union(self.new_label_set, set(value))

        for new_label in self.new_label_set:
            additional_label = pd.DataFrame({new_label: np.zeros(self.data.shape[0])})
            self.data = pd.concat([self.data, additional_label], axis=1)

    def assignment(self):
        """
        对于每一个三基元素，遍历每一个原分类对应的集合，只要存在于这个集合，就代表应该有这个三基元素的标签，因此该
        三基元素的值对应加一。
        最后的值代表标签数。=0代表没有该标签，>0代表该标签出现的次数。

        """
        for new_label in self.new_label_set:
            for key in self.label.keys():
                if new_label in self.label[key]:
                    self.data[new_label] += self.data[key]


    def save(self):
        """
        需要解决多标签的值>1的问题
        :return:
        """
        self.data.drop(self.label.keys(), axis=1, inplace=True)
        file_base_path, file_name = path.split(self.file_path)
        to_path = path.join(file_base_path, file_name+'new_label.csv')
        self.data.to_csv(to_path)



c = Conversion()
















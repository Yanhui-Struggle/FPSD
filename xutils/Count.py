# !/usr/bin/env python
# encoding: utf-8


import xml.dom.minidom as xmldom
import os


def voc_label_statistics(annotation_path):
    '''
    VOC 数据集类别统计
    :param annotation_path: voc数据集的标签文件夹
    :return: {'class1':'count',...}
    '''
    count = 0
    annotation_names = [os.path.join(annotation_path, i) for i in os.listdir(annotation_path)]

    labels = dict()
    for names in annotation_names:
        names_arr = names.split('.')
        file_type = names_arr[-1]
        if file_type != 'xml':
            continue
        file_size = os.path.getsize(names)
        if file_size == 0:
            continue

        count = count + 1
        print('process：', names)
        xmlfilepath = names
        domobj = xmldom.parse(xmlfilepath)
        # 得到元素对象
        elementobj = domobj.documentElement
        # 获得子标签
        subElementObj = elementobj.getElementsByTagName("object")
        for s in subElementObj:
            label = s.getElementsByTagName("name")[0].firstChild.data

            label_count = labels.get(label, 0)
            labels[label] = label_count + 1

    print('文件标注个数：', count)
    return labels


if __name__ == '__main__':
    annotation_path = "E:/FPSD/VOCdevkit/VOC2012/Annotations"

    label = voc_label_statistics(annotation_path)
    print(label)
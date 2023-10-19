import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import cv2
import matplotlib.pyplot as plt
from math import sqrt as sqrt
import numpy as np

if __name__ == '__main__':
    # FPSD
    # AnoRoot = 'E:\FPSD\VOCdevkit\VOC2012\Annotations'
    # fuck = ['FPSD']

    # DSSDD
    # AnoRoot = 'F:/1深度学习数据/A_Dual-polarimetric_SAR_Ship_Detection_Dataset-main/annotations/HorizontalBox/all'
    # fuck = ['DSSDD']

    # SSDD
    AnoRoot = 'F:/1深度学习数据\Official-SSDD-OPEN\VOCdevkit\VOC2012\Annotations'
    fuck = ['SSDD']

    # test
    # AnoRoot = 'F:/1深度学习数据/VOCdevkit/VOC2012/Annotations'
    # fuck = ['Test']

    # GT框宽高统计
    width = []
    height = []
    annotation_names = [os.path.join(AnoRoot, i) for i in os.listdir(AnoRoot)]

    for names in annotation_names:
        names_arr = names.split('.')
        file_type = names_arr[-1]
        if file_type != 'xml':
            continue
        file_size = os.path.getsize(names)
        if file_size == 0:
            continue
        label_file = open(names)
        tree = ET.parse(label_file)
        root = tree.getroot()
        size = root.find('size')
        img_w = int(size.find('width').text)  # 原始图片的width
        img_h = int(size.find('height').text)  # 原始图片的height
        for obj in root.iter('object'):
            xmlbox = obj.find('bndbox')
            xmin = float(xmlbox.find('xmin').text)
            ymin = float(xmlbox.find('ymin').text)
            xmax = float(xmlbox.find('xmax').text)
            ymax = float(xmlbox.find('ymax').text)
            w = xmax - xmin
            h = ymax - ymin
            # wnorm = w/ img_w
            # wnorm = w / img_w
            # w_change = (w / img_w) * input_size
            # h_change = (h / img_h) * input_size
            # s = w_change * h_change  # 得到了GT框面积
            # width.append(sqrt(s))
            # height.append(w_change / h_change)
            width.append(w)
            height.append(h)

    ass = []
    for index, w in enumerate(width):
        h = height[index]
        ass.append(w / h)

    fig = plt.figure(figsize=(6, 5), dpi=100)
    plt.hist(ass, bins=30, edgecolor='black', density=True, color='b')
    plt.title('Aspect Ratio', fontsize=13)
    plt.ylabel('Density', fontsize=13)
    plt.legend(fuck, edgecolor='black')
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # plt.xlim(0, 3.5)
    x = np.arange(0, 8, 1)
    plt.xticks(x, size=13)
    plt.yticks(size=13)
    plt.savefig('C:/Users/Lenovo/Desktop/直方图' + fuck[0] + '.png')
    plt.show()

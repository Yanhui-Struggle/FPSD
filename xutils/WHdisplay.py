import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import cv2
import matplotlib.pyplot as plt
from math import sqrt as sqrt

# 需要检查的数据
# 输入分辨率
input_size = 256

if __name__ == '__main__':
    # FPSD
    AnoRoot = 'E:\FPSD\VOCdevkit\VOC2012\Annotations'
    fuck = ['FPSD']

    # DSSDD
    # AnoRoot = 'F:/1深度学习数据/A_Dual-polarimetric_SAR_Ship_Detection_Dataset-main/annotations/HorizontalBox/all'
    # fuck = ['DSSDD']

    # SSDD
    # AnoRoot = 'F:/1深度学习数据\Official-SSDD-OPEN\VOCdevkit\VOC2012\Annotations'
    # fuck = ['SSDD']

    # test
    # AnoRoot = 'F:/1深度学习数据/VOCdevkit/VOC2012/Annotations'
    # fuck = ['Test']

    # GT框宽高统计
    width = []
    height = []
    annotation_names = [os.path.join(AnoRoot, i) for i in os.listdir(AnoRoot)]

    shipcount = 0
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
            shipcount += 1
            # wnorm = w/ img_w
            # wnorm = w / img_w
            # w_change = (w / img_w) * input_size
            # h_change = (h / img_h) * input_size
            # s = w_change * h_change  # 得到了GT框面积
            # width.append(sqrt(s))
            # height.append(w_change / h_change)
            width.append(w)
            height.append(h)

    count = 0
    for index, w in enumerate(width):
        h = height[index]
        # if w < 32 and h < 32:
        #     count += 1
        if w * h < 32**2:
            count += 1
    print('在%d艘船中，有%d艘船符合要求，占比%.5f' % (shipcount, count, count / shipcount))

    fig = plt.figure(figsize=(6, 5), dpi=100)
    plt.scatter(width, height, s=6, c='b', marker='o')
    plt.xlabel('Width', fontsize=13)
    plt.ylabel('Height', fontsize=13)
    plt.legend(fuck, edgecolor='black')
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.xticks(size=13)
    plt.yticks(size=13)
    # plt.savefig('C:/Users/Lenovo/Desktop/' + fuck[0] + '.png')
    plt.show()

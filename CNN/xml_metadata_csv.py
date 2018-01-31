#-*-coding:utf-8-*-
#-------------------------------------------------------------------------------
# Name:        
# Purpose:
#
# Author:      BQH
#
# Created:     19/09/2017
# Copyright:   (c) BQH 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import glob
import cv2
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET


def png_to_jpg(png_path):
    jpg_path = png_path.replace('.png','.jpg')
    im = cv2.imdecode(np.fromfile(png_path, dtype=np.uint8), -1)
    cv2.imencode('.jpg', im)[1].tofile(jpg_path)
    return jpg_path

def xml_to_csv(path):
    xml_list = []
    for dir in os.listdir(path):
        img_dir = os.path.join(path, dir)
        for xml_file in glob.glob(img_dir + '\*.xml'):
            tree = ET.parse(xml_file)
            root = tree.getroot()
            file_name = root.find('path').text
            file_name = file_name.replace('image_search','MechineLeaning\image_search') # 特殊本地处理
            # if file_name.find('.png') > 0:
            #     file_name = png_to_jpg(file_name)

            for member in root.findall('object'):
                value = (file_name,
                         int(root.find('size')[0].text),
                         int(root.find('size')[1].text), member[0].text,
                         int(member[4][0].text),
                         int(member[4][1].text),
                         int(member[4][2].text),
                         int(member[4][3].text)
                         )
                xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    image_path = r'E:\code\MechineLeaning\image_search\image\人物'
    xml_df = xml_to_csv(image_path)
    xml_df.to_csv('CSVMETADATAFILE.csv', index=None)
    print('successfully converted xml metadata to csv')

if __name__ == '__main__':
    main()
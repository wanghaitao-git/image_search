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

import cv2

class StructureDescriptor:
    __slot__ = ["dimension"]
    def __init__(self, dimension):
        self.dimension = dimension

    def describe(self, image):
        image = cv2.resize(image, self.dimension, interpolation=cv2.INTER_CUBIC)
        return image
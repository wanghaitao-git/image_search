# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:      BQH
#
# Created:     19/09/2017
# Copyright:   (c) BQH 2017
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import numpy as np
import cv2

from Algorithm.ColorDescriptor import ColorDescriptor
from Algorithm.StructureDescriptor import StructureDescriptor


class Searcher:
    __slot__ = ["colorIndexPath", "structureIndexPath"]

    def __init__(self, idealBins = (8, 12, 3),idealDimension = (16, 16)):
        self.color_desriptor = ColorDescriptor(idealBins)
        self.structure_descriptor = StructureDescriptor(idealDimension)

    def solve_color_distance(self, features, queryFeatures, eps=1e-5):
        distance = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for a, b in zip(features, queryFeatures)])
        return distance

    def solve_structure_distance(self, structures, queryStructures, eps=1e-5):
        distance = 0
        normalizeRatio = 5e3
        for index in range(len(queryStructures)):
            for subIndex in range(len(queryStructures[index])):
                a = structures[index][subIndex]
                b = queryStructures[index][subIndex]
                distance += (a - b) ** 2 / (a + b + eps)
        return distance / normalizeRatio

    def transform_rawQuery(self, rawQueryStructures):
        queryStructures = []
        for substructure in rawQueryStructures:
            structure = []
            for line in substructure:
                for tripleColor in line:
                    structure.append(float(tripleColor))
            queryStructures.append(structure)
        return queryStructures

    def get_distance(self, im1, im2):
        features1 = self.color_desriptor.describe(im1)
        features2 = self.color_desriptor.describe(im2)

        structures1 = self.structure_descriptor.describe(im1)
        structures2 = self.structure_descriptor.describe(im2)

        color_dis = self.solve_color_distance(features1, features2)
        structure_dis = self.solve_structure_distance(self.transform_rawQuery(structures1), self.transform_rawQuery(structures2))
        return color_dis, structure_dis


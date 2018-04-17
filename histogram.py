#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
from csv import *

def main(param):
	i = 16
	csv = Csv(param)
	datas = csv.getDatas(enum=1, feats= [i])
	titles = csv.getTitles(feats= [i])
	if datas != None:
		figure = plt.figure()
		plt.title(titles[0])
		for key, value in datas.items():
			plt.hist(value[0], color= color(key), label= key, alpha= 0.5)
		plt.legend()
		plt.show()

main("dataset_train.csv")
#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
from csv import *

def main(param):
	csv = Csv(param)
	titles = csv.getTitles(type= "number")
	datas = csv.getDatas(enum= 1, type= "number")
	i = 1
	j = 3
	if datas != None:
		figure = plt.figure()
		plt.title(titles[i])
		fig = plt.subplot(111)
		fig.set_ylabel(titles[j])
		for key, value in datas.items():
			plt.scatter(value[i], value[j], color=color(key), label= key,  marker='.', alpha= 0.5)
		plt.legend()
		plt.show()

main("dataset_train.csv")
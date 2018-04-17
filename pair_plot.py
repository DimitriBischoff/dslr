#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
from csv import *

def main(param):
	csv = Csv(param)
	datas = csv.getDatas(enum= 1, type= "number")
	titles = csv.getTitles(type= "number")
	if datas != None:
		length = len(titles)
		figure = plt.figure(figsize = (16, 9))
		figure.subplots_adjust(left = 0.05, bottom = 0.01, right = 0.99, top = 0.95, wspace = 0.1, hspace = 0.1)
		for j in range(length):
			for i in range(length):
				fig = plt.subplot(length, length, j * length + i + 1)
				fig.set_xticklabels([])
				fig.set_yticklabels([])
				if j == 0:
					plt.title(titles[i][:10])
				if i == 0:
					fig.set_ylabel(titles[j][:6], rotation = 60)
				for key, value in datas.items():
					if j == i:
						plt.hist(value[i], color=color(key), alpha= 0.5)
					else:
						plt.scatter(value[i], value[j], color=color(key), label= key,  marker='.', alpha= 0.5)
		file = param.split('.')[0] + ".png"
		plt.savefig( file, dpi=300);
		print("save " + file)


if __name__ == "__main__":
	main("dataset_train.csv")
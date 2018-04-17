#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import sys
from lib import *
from csv import *

def main(param):
	tab = ["title", "Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]
	infos = Csv(param).getInfos(type= "number")

	if infos != None:
		for title in tab:
			print("%-5s" % (title if (title != "title") else ""), end="\t")
			length = len(infos)
			for i, info in enumerate(infos):
				txt = "%14.14s" if (type(info[title]) == str) else "%14.6f"
				end = "\n" if (i == length - 1) else "\t"
				print(txt % info[title], end=end)


if __name__ == "__main__":
	argc = len(sys.argv)

	if argc >= 2:
		i = 1
		while i < argc:
			main(sys.argv[i])
			i += 1
	else:
		main("dataset_train.csv")
		# print("error params")
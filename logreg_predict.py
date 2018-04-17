#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import sys
from csv import *

def score(O, x):
	ret = 0
	for i in range(len(O)):
		if x[i]:
			ret += O[i] * x[i]
	return ret

def predict(O, x):
	return sig(score(O, x))

def whichClass(brain, feature):
	max = -1
	classe = ""
	for key, value in brain.items():
		p = predict(value, feature)
		if p > max:
			max = p
			classe = key
	return classe, max

def loadBrain(param):
	brain = {}
	with open(param, 'r') as f:
		for line in f:
			line = line[:-1].split(',')
			brain[line[0]] = []
			for poids in line[1:]:
				if isNumber(poids):
					brain[line[0]].append(float(poids))
				else:
					return None
	return brain

def featureScaling(features, infos):
	for i, elem in enumerate(features):
		if features[i]:
			features[i] = normalise(features[i], infos[i]["Min"], infos[i]["Max"])
	features = [1] + features
	return features

def main(param):
	brain = loadBrain(param[1])
	csv = Csv(param[0])
	if csv.valid and brain is not None:
		includes = [6, 8, 9, 10, 11, 12, 13, 14, 17, 18]
		infos = csv.getInfos(feats= includes)
		features = csv.getDatas(feats= includes, hole= True)
		with open("house.csv", 'w') as fileWrite:
			fileWrite.write("Index,Hogwarts House\n")
			total = 0
			for i, feature in enumerate(features):
				house, tmp = whichClass(brain, featureScaling(feature, infos))
				fileWrite.write(str(i) + "," + house + "\n")
				total += tmp
			print("accuary estimate:", total / len(features))
	elif not csv.valid:
		print("error dataset")
	elif not brain:
		print("error .lor")

if __name__ == "__main__":
	argc = len(sys.argv)

	if argc == 3:
		main(sys.argv[1:])
	else:
		# main("dataset_test.csv")
		print("error params (.csv .lor)")
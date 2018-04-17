#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import sys
from lib import *
from math import *
from csv import *
import matplotlib.pyplot as plt

def score(O, x):
	ret = 0
	for i in range(len(O)):
		ret += O[i] * x[i]
	return ret

def predict(O, x):
	return sig(score(O, x))

def cost(classe, labels, theta, features):
	m = len(features)
	total = 0
	for i in range(m):
		p = predict(theta, features[i])
		if classe == labels[i]:
			total += log10(p)
		else:
			total += log10(1 - p)
	return total / -m

def whichClass(brain, feature):
	max = -1
	classe = ""
	for key, value in brain.items():
		p = predict(value, feature)
		if p > max:
			max = p
			classe = key
	return classe

def accuary(brain, features, labels):
	ret = 0
	m = len(features)
	for i in range(m):
		classe = whichClass(brain, features[i])
		ret += labels[i] == classe
	return ret / m

def isValid(X):
	for x in X:
		if x == None or x == '':
			return False
	return True

def featureScaling(features, infos):
	j = 0
	m = len(features)
	while j < m:
		for i, elem in enumerate(features[j]):
			features[j][i] = normalise(features[j][i], infos[i]["Min"], infos[i]["Max"])
		features[j] = [1] + features[j]
		j += 1
	return features

def getGradient(theta, features, classe, labels):
	gradients = [0.0] * len(theta)
	m = len(features)
	for j in range(len(theta)):
		for i in range(m):
				y = 0 + (classe == labels[i])
				gradients[j] += (predict(theta, features[i]) - y) * features[i][j]
		gradients[j] /= m
	return gradients

def update_theta(theta, gradients, learnRate):
	for i in range(len(theta)):
		theta[i] -= gradients[i] * learnRate

def learnClasse(it, classe, labels, features):
	learnRate = 2
	theta = [0.5] * len(features[0])
	cost_history = []
	for i in range(it):
		gradients = getGradient(theta, features, classe, labels)
		update_theta(theta, gradients, learnRate)
		cost_history.append(cost(classe, labels, theta, features))
	return theta, cost_history

def showCostHistories(classes, cost_histories):
	length = len(classes)
	for i in range(length):
		plt.subplot(1, length, 1 + i)
		plt.title(classes[i])
		plt.plot(cost_histories[i])
	plt.show()

def train(infos, labels, features):
	iterations = 50
	classes = listUniq(labels)
	cost_histories = [None] * len(classes)
	brain = {}
	for i, classe in enumerate(classes):
		brain[classe], cost_histories[i] = learnClasse(iterations, classe, labels, features)
	showCostHistories(classes, cost_histories)
	return brain

def saveBrain(param, brain):
	file = param.split('.')[0] + ".lor"
	with open(file, 'w') as f:
		for key, value in brain.items():
			tmp = key
			for v in value:
				tmp += "," + str(v)
			f.write(tmp + '\n')
	print("save in", file)

def main(param):
	csv = Csv(param)
	if csv.valid:
		includes = [6, 8, 9, 10, 11, 12, 13, 14, 17, 18]
		infos = csv.getInfos(includes)

		labels, features = csv.getDatas(label=1, feats=includes)
		featureScaling(features, infos)
		
		cut = int(len(labels) * 0.7)
		labelsTrain = labels[:cut]
		featuresTrain = features[:cut]
		labelsTest = labels[cut:]
		featuresTest = features[cut:]

		print(len(labelsTrain), len(labelsTest))

		b = train(infos, labelsTrain, featuresTrain)
		print("accuary:", accuary(b, featuresTest, labelsTest))
		saveBrain(param, b)

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
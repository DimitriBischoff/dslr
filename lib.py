# -*- coding: utf-8 -*-

from math import sqrt

def transpose(matrice):
	ret = []
	for i in range(len(matrice[0])):
		tmp = []
		for j in range(len(matrice)):
			tmp.append(matrice[j][i])
		ret.append(tmp)
	return ret

def color(t):
	return ({
		"Ravenclaw"		:"#3364a6",
		"Hufflepuff"	:"#fefe00",
		"Gryffindor"	:"#cb0101",
		"Slytherin"		:"#4d9905"
	})[t]

def listUniq(liste):
	tmp = []
	for elem in liste:
		if elem not in tmp:
			tmp.append(elem)
	return tmp

def isNumber(num):
	num = str(num)
	return num.replace(".", "", 1).replace("-", "", 1).isdigit()

def sig(x):
	e = 2.718281828459045
	return 1 / (1 + e ** -x)

def abs(x):
	return x if (x >= 0) else -x

def normalise(x, m, M):
	return (x - m) / (M - m)

def standardise(x, mean, std):
	return (x - mean) / std

def scale(x, m, M):
	return x / max(abs(m), abs(M))

def mean(list):
	result = 0
	for elem in list:
		if isNumber(elem):
			result += float(elem)
	return result / len(list)

def std(list, mean):
	result = 0
	for elem in list:
		if isNumber(elem):
			tmp = float(elem) - mean
			result += tmp * tmp
	return sqrt(result / len(list))

def listMin(list):
	min = list[0]
	for elem in list:
		if isNumber(elem) and elem < min:
			min = elem
	return min

def listMax(list):
	max = list[0]
	for elem in list:
		if isNumber(elem) and elem > max:
			max = elem
	return max

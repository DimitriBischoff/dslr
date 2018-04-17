#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from lib import *

class Csv:
	def __init__(self, path):
		self.w = 0
		self.h = 0
		self.title = []
		self.infos = []
		self.content = []
		self.valid = self.readFile(path)
		if (self.valid):
			self.type = [self.typeList(self.getCol(i)) for i in range(self.w)]
			self.transNumber()
			self.initInfos()

	def __str__(self):
		if self.valid:
			return "width\t: %d height\t: %d\ntitle:\t %s\ntype\t: %s" % (self.w, self.h, ", ".join(self.title), ", ".join(self.type))
		return "Invalid Data"

	def readFile(self, path):
		with open(path, "r") as file:
			for i, line in enumerate(file):
				tmp = line.replace('\n', '').split(",")
				if i == 0:
					self.w = len(tmp)
					self.title = tmp
				else:
					self.content.append(tmp)
					self.h += 1
				if len(tmp) != self.w:
					return False
		return True

	def getCol(self, col):
		tmpCol = []
		for line in self.content:
			tmpCol.append(line[col])			
		return tmpCol

	def getCols(self, cols):
		tmp = []
		for line in self.content:
			tmpLine = []
			for col in cols:
				tmpLine.append(line[col])
			tmp.append(tmpLine)
		return tmp

	def isIndex(self, liste):
		if not isNumber(liste[0]):
			return False
		a = float(liste[0])
		i = 1
		length = len(liste)
		while i < length:
			if not isNumber(liste[i]):
				return False
			b = float(liste[i])
			if a != b -1:
				return False
			a = b
			i += 1
		return True

	def typeList(self, liste):
		tmpList = [a for a in liste if a != ""]
		tmp = listUniq(tmpList)
		if (len(tmp) < len(tmpList)):
			if len(tmp) == 2:
				return "boolean"
			if len(tmp) <= len(tmpList) * 0.5:
				return "enumerate"
		if len([a for a in tmp if not isNumber(a)]):
			return "string"
		elif self.isIndex(liste):
			return "index"
		elif not len([a for a in liste if a != ""]):
			return "undefined"
		return "number"

	def transNumber(self):
		for line in self.content:
			for i, t in enumerate(self.type):
				if t == "number" and line[i]:
					line[i] = float(line[i])

	def initInfos(self):
		self.infos = [{}] * self.w

		for i in range(self.w):
			self.infos[i] = self.getInfoCol(i, self.getCol(i))

	def getInfoCol(self, i, col):
		type = self.type[i]
		colTmp = [a for a in col if a != ""]
		if type == "number":
			m = listMin(colTmp)
			M = listMax(colTmp)
			mean_ = mean(colTmp)
			return {
				"title"	: self.title[i],
				"type"	: type,
				"Count"	: len(colTmp),
				"Mean"	: mean_,
				"Std"	: std(colTmp, mean_),
				"Min"	: m,
				"25%"	: m + (M - m) * 0.25,
				"50%"	: m + (M - m) * 0.5,
				"75%"	: m + (M - m) * 0.75,
				"Max"	: M,
			}
		return {
			"title"	: self.title[i],
			"type"	: type,
			"Count"	: len(colTmp),
			"Mean"	: 0,
			"Std"	: 0,
			"Min"	: 0,
			"25%"	: 0,
			"50%"	: 0,
			"75%"	: 0,
			"Max"	: 0,
		}

	def getLabelsFeatures(self, label, feats, hole):
		f = self.getCols(feats)
		l = self.getCol(label)
		if not hole:
			invalid = [i for i, a in enumerate(f) if len([True for b in a if b == ""])]
			for i in reversed(invalid):
				del f[i]
				del l[i]
		return l, f

	def getDatasByEnum(self, enum, feats, type, hole):
		tab = {}
		colEnum = self.getCol(enum)
		datas = self.getDatas(feats= feats, type= type, hole= True)
		width = len(datas[0])
		for i in range(len(colEnum)):
			if colEnum[i] not in tab:
				tab[colEnum[i]] = []
			invalid = len([a for a in datas[i] if a == ""])
			if not hole and invalid:
				continue
			for j in range(width):
				if j >= len(tab[colEnum[i]]):
					tab[colEnum[i]].append([])
				tab[colEnum[i]][j] += [datas[i][j]]
		return tab

	def getInfos(self, feats = None, type = None):
		if not self.valid:
			return None
		elif feats:
			return [a for i, a in enumerate(self.infos) if i in feats]
		elif type:
			return [a for a in self.infos if a["type"] == type]
		return self.infos

	def getTitles(self, feats = None, type = None):
		if not self.valid:
			return None
		elif feats:
			return [a for i, a in enumerate(self.title) if i in feats]
		elif type:
			return self.getTitles(feats= [i for i, a in enumerate(self.infos) if a["type"] == type])
		return self.title

	def getDatas(self, label= None, feats = None, type = None, enum= None, hole= False):
		if not self.valid:
			return None
		if enum:
			return self.getDatasByEnum(enum, feats, type, hole)
		if label and feats:
			return self.getLabelsFeatures(label, feats, hole)
		elif label:
			datas = self.getCol(label)
		elif feats:
			datas = self.getCols(feats)
		elif type:
			datas = self.getCols([i for i, a in enumerate(self.type) if a == type])
		else:
			datas = self.infos

		if not hole:
			invalid = [i for i, a in enumerate(datas) if len([True for b in a if b == ""])]
			for i in reversed(invalid):
				del datas[i]
		return datas


if __name__ == "__main__":
	# a = ["1", "2", "3", "", "4"]
	# b = ["1", "2", "3", "", "4", "a"]
	# c = ["1", "2", "3", "4", "1", "2", "3", "4"]
	# d = ["1", "1", "2", "2"]
	# print(Csv.typeList(Csv, a))
	# print(Csv.typeList(Csv, b))
	# print(Csv.typeList(Csv, c))
	# print(Csv.typeList(Csv, d))
	# test = [
	# 	["1", "2", "3"],
	# 	["1", "", "3"],
	# 	["1", "2", "3"],
	# 	["1", "2", ""],
	# ]

	tmp = Csv("dataset_train.csv")
	label, features = tmp.getDatas(label=1, feats=[6, 7, 8])
	# print(features)


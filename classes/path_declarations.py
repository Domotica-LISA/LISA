# -*- coding: UTF-8 -*-
import os

appPath = os.path.normpath(os.path.join(
	os.path.dirname(os.path.abspath(__file__)), 
	os.pardir))

dataPath = os.path.join(appPath, "data")
libPath = os.path.join(appPath, "classes")
modulePath = os.path.join(appPath, "modules")

configPath = appPath

def config(*fname):
	return os.path.join(appPath, *fname)

def data(*fname):
	return os.path.join(dataPath, *fname)
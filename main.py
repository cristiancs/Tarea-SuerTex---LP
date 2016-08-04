# -*- coding: utf-8 -*-
import re

# Buscar Si tiene el title
archivo = open("suertex.txt", "r")
i = 0
flags = {"separamiles": False,"ofecha": False,"error": 0}
for linea in archivo:
	result = re.search(r'\\separamiles{}',linea)
	if(result):
		if i < 2:
			flags["separamiles"] = True
		else:
			print "[ERROR][Linea: "+str(i)+"] La función "+result.group()+" ha sido declarada en un lugar incorrecto"
			flags["error"]+=1
	result = re.search(r'\\ofecha{}',linea)
	if(result):
		if i < 2:
			flags["ofecha"] = True
		else:
			print "[ERROR][Linea: "+str(i)+"] La función "+result.group()+" ha sido declarada en un lugar incorrecto"
			flags["error"]+=1
	i+=1
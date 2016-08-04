# -*- coding: utf-8 -*-
import re

def printError(funcion,linea, error):
	if(linea == -1):
		print "[ERROR] La función "+funcion+" "+error
	else:
		print "[ERROR][Linea: "+str(linea)+"] La función \""+funcion+"\" "+error
# Buscar Si tiene el title
archivo = open("suertex.txt", "r")
i = 1
flags = {"separamiles": False,"ofecha": False,"error": 0}
data = {"nproy": False}
validFunctions = {'separamiles','ofecha','fn','fc','nproy','titulo','inicio','fin','item'}
for linea in archivo:
	# Buscar  separarmiles
	result = re.search(r'\\separamiles{}',linea)
	if result:
		if i < 2:
			flags["separamiles"] = True
		else:
			printError(result.group(),i, "ha sido declarada en un lugar incorrecto")
			flags["error"]+=1
	# Buscar  ofecha
	result = re.search(r'\\ofecha{}',linea)
	if result:
		if i < 2:
			flags["ofecha"] = True
		else:
			printError(result.group(),i, "ha sido declarada en un lugar incorrecto")
			flags["error"]+=1
	# Buscar titulo de la página
	result = re.search(r'\\nproy{[a-zA-Z\s]{1,}}',linea)
	if result:
		if data["nproy"] != False:
			printError("\\nproy",i, "ha sido declarada más de una vez")
		else:
			data["nproy"] = result.group()
	# Buscar { mal usadas
	result = re.findall(r'[a-zA-Z\s]{1,}{',linea)
	for text in result:
		if text.strip("{") not in validFunctions:
			printError(text,i, "no es una función valida")
			flags["error"]+=1
	# Buscar } mal usadas
	result = re.findall(r'.{1,}}',linea)
	for text in result:
		r2 = text.split("{")
		r2 = r2[0].split("\\")
		#print r2
		if len(r2) == 1 or r2[-1] not in validFunctions:
			printError(r2[-1][:-1],i, "no es una función valida")
			flags["error"]+=1
	# Buscar \ mal usadas
	# result = re.findall(r'.{1,}\\',linea)
	# if result:
	# 	printError("/",i, " no esta permitida fuera de las variables")
		# flags["error"]+=1

	i+=1
if not data["nproy"]:
	#El titulo nunca fue declarado
	printError("\\nproy",-1, "No ha sido declarada")
	flags["error"]+=1




if flags["error"] > 0:
	# Se ha generado un error, muere el programa.
	print "No ha sido posible compilar el archivo suertex.txt, se han generado "+str(flags["error"])+" errores."
else:
	# Se genera el código
	print "Compilación generada"
	import funciones
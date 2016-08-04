# -*- coding: utf-8 -*-
import re

def printError(funcion,linea, error):
	if(linea == -1):
		print "[ERROR] La función "+funcion+" "+error
	else:
		print "[ERROR][Linea: "+str(linea)+"] La función "+funcion+" "+error
# Buscar Si tiene el title
archivo = open("suertex.txt", "r")
i = 0
flags = {"separamiles": False,"ofecha": False,"error": 0}
data = {"nproy": False}
validFunctions = {'fn','fc','nproy','titulo','inicio','fin','item'}
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
	result = re.search(r'\\nproy{[a-zA-Z\s]{1,}}',linea)
	if result:
		if data["nproy"] != False:
			printError("\\nproy",i, "ha sido declarada más de una vez")
		else:
			data["nproy"] = result.group()
	i+=1

if not data["nproy"]:
	printError("\\nproy",-1, "No ha sido declarada")
	flags["error"]+=1


if flags["error"] > 0:
	# Se ha generado un error, muere el programa.
	print "No ha sido posible compilar el archivo suertex.txt, se han generado "+str(flags["error"])+" errores."
else:
	# Se genera el código
	print "Compilación generada"
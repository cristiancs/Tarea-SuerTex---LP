# -*- coding: utf-8 -*-
import re

def printError(funcion,linea, error):
	if(linea == -1):
		print "[ERROR] La función "+funcion+" "+error
	else:
		print "[ERROR][Linea: "+str(linea)+"] \""+funcion+"\" "+error
# Buscar Si tiene el title
archivo = open("suertex.txt", "r")
i = 1
n_linea = 0
flags = {"separamiles": False,"ofecha": False,"error": 0}
list_flag = {"inicio": False, "item": False}
data = {"nproy": False}
validFunctions = {'separamiles','ofecha','fn','fc','nproy','titulo','inicio','fin','item'}
brackets = []
inicioFinList = []
for linea in archivo:
	# Buscar  separarmiles
	result = re.search(r'\\separamiles{}',linea)
	if result:
		if i < 3:
			flags["separamiles"] = True
		else:
			printError(result.group(),i, "ha sido declarada en un lugar incorrecto")
			flags["error"]+=1
	# Buscar  ofecha
	result = re.search(r'\\ofecha{}',linea)
	if result:
		if i < 3:
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
	result = re.findall(r'\\.[^\s-]{0,}',linea)
	def limpiar(string):
		return (string.split("{")[0])[1:]
	if result:
		result = map(limpiar, result)
		for funcion in result:
			if funcion not in validFunctions:
				printError("/",i, " no esta permitida fuera de las variables")
				flags["error"]+=1
	
	# Verificar que se usen bien los { }, [ ]
	result = re.findall(r'[\[\{\]\}]',linea)
	for caracter in result:
		if re.match(r'[\[\{]', caracter):
			brackets.append(caracter)
		if re.match(r'[\]\}]', caracter):
			if(len(brackets) == 0):
				printError("Hay una llave mal cerrada/abierta", i,"")
				flags["error"]+=1
			else:
				brackets.pop()
	if(len(brackets) > 0):
		printError("Hay una llave mal cerrada/abierta", i,"")
		flags["error"]+=1
	#Agregar inicio / fin a una lista
	result = re.findall(r'\\inicio{.{0,}}|\\fin{.{0,}}',linea)
	for tag in result:
		inicioFinList.append(tag)
		#Buscar que el parametro que recibe es correcto el inicio/fin
		argmt = re.search(r'{.*}', tag)
		if argmt.group()[1:-1] != 'lista_enumerada' and argmt.group()[1:-1] != 'lista_punteada':
			printError(argmt.group()[1:-1], i," no es un parametro valido para el tag \inicio o \\fin")
			flags["error"]+=1 

	# Verificar que los items esten dentro de un \inicio
	result = re.findall(r'\\item',linea)
	if result and not re.search(r'\\inicio{.{0,}}', inicioFinList[-1]):
		printError("\item", i,"se encuentra fuera de una lista")
		flags["error"]+=1 

	# Verificar items dentro de inicio
	if re.search(r'\\inicio{', linea):	# Buscar inicio de lista
		if list_flag["inicio"]:		# Si ya habia iniciado
			printError("\inicio", i, "hay un inicio dentro de otro inicio")
			flags["error"]+=1 
		else:
			list_flag["inicio"] = True
			n_linea = i
		if not re.search(r'}[\s]*$', linea):	# Incorrecto cierre de linea
			printError("\inicio", i, "hay texto fuera de un item en una lista")
			flags["error"]+=1 
	if list_flag["inicio"] and i > n_linea:
		if re.search(r'^\\item{.*}$', linea):	# Actualizar flag de item
			if not list_flag["item"]:
				list_flag["item"] = True
		elif re.search(r'\\fin{', linea):		# Buscar cierre y actualizar
			if not list_flag["item"]:
				printError("\\fin", i, "no hay items en la lista")
				flags["error"]+=1 
			list_flag["inicio"] = False
		else:
			if re.search(r'[\S]+', linea):		# Si no encontro item ni fin, buscar si hay algo demas
				printError("\inicio", i, "hay texto fuera de un item en una lista")
				flags["error"]+=1 
	i+=1
if not data["nproy"]:
	#El titulo nunca fue declarado
	printError("\\nproy",-1, "No ha sido declarada")
	flags["error"]+=1
#verificar /inicio /fin
for i in range(len(inicioFinList)/2):
	t1 = inicioFinList.pop()
	t2 = inicioFinList.pop()
	if not re.search(r'\\inicio{.{0,}}', t2) or not re.search(r'\\fin{.{0,}}', t1):
		printError("tag \inicio, \\fin",-1, "No ha sido utilizado correctamente")
		flags["error"]+=1
if flags["error"] > 0:
	# Se ha generado un error, muere el programa.
	print "No ha sido posible compilar el archivo suertex.txt, se han generado "+str(flags["error"])+" errores."
else:
	# Se genera el código
	print "Compilación generada"
	import funciones
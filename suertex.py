# -*- coding: utf-8 -*-
from funciones import *
archivo = open("suertex.txt", "r")
i = 0
i2 = 1
flags = {"separamiles": False,"ofecha": False,"error": 0}
list_flag = {"inicio": False, "item": False}
data = {"nproy": False}
validFunctions = {'separamiles','ofecha','fn','fc','nproy','titulo','inicio','fin','item'}
brackets = []
inicioFinList = []

#Compilar
for linea in archivo:
	if linea.strip():
		i+=1
	# Buscar  separarmiles
	result = re.search(r'\\separamiles{}',linea)
	if result:
		if i < 3 and flags[limpiar(result.group())] != True:
			flags["separamiles"] = True
		elif flags[limpiar(result.group())] != True:
			printError(result.group(),i2, "ha sido declarada en un lugar incorrecto")
			flags["error"]+=1
		else:
			printError(result.group(),i2, "ha sido declarada más de 1 vez")
			flags["error"]+=1

	# Buscar  ofecha
	result = re.search(r'\\ofecha{}',linea)
	if result:
		if i < 3 and flags[limpiar(result.group())] != True:
			flags["ofecha"] = True
		elif flags[limpiar(result.group())] != True:
			printError(result.group(),i2, "ha sido declarada en un lugar incorrecto")
			flags["error"]+=1
		else:
			printError(result.group(),i2, "ha sido declarada más de 1 vez")
			flags["error"]+=1

	# Buscar titulo de la página
	result = re.search(r'\\nproy{.{1,}}',linea)
	if result:
		if data["nproy"] != False:
			printError("\\nproy",i2, "ha sido declarada más de una vez")
		else:
			data["nproy"] = result.group()
	# Buscar { mal usadas
	result = re.findall(r'[a-zA-Z0-9]*{',linea)
	for text in result:
		if text.strip("{") not in validFunctions:
			printError(text,i2, "no es una función valida")
			flags["error"]+=1
	# Buscar } mal usadas
	result = re.findall(r'.*}',linea)
	for text in result:
		r2 = text.split("{")
		r2 = r2[0].split("\\")
		if len(r2) == 1 or r2[-1] not in validFunctions:
			printError(r2[-1][:-1],i2, "no es una función valida")
			flags["error"]+=1
	# Buscar \ mal usadas
	result = re.findall(r'\\.[^\s-]*',linea)
	if result:
		result = map(limpiar, result)
		if len(result) > 1 and re.search(r'(inicio|nproy|titulo|inicio|item|fin){.{0,}(\}|\s){1,} \\\w*', linea):
			printError("\\",i2, " no esta permitido el uso de 2 \  en una linea (posiblemente 2 comandos en misma linea)")
			flags["error"]+=1
		for funcion in result:
			if funcion not in validFunctions:
				printError("\\",i2, " no esta permitida fuera de las variables")
				flags["error"]+=1

	# Verificar que se usen bien los { }, [ ]
	result = re.findall(r'[\[\{\]\}]',linea)
	for caracter in result:
		if re.match(r'[\[\{]', caracter):
			brackets.append(caracter)
		if re.match(r'[\]\}]', caracter):
			if(len(brackets) == 0):
				printError("Hay una llave mal cerrada/abierta", i2,"")
				flags["error"]+=1
			else:
				brackets.pop()
	if(len(brackets) > 0):
		printError("Hay una llave mal cerrada/abierta", i2,"")
		flags["error"]+=1
	#Agregar inicio / fin a una lista
	result = re.findall(r'\\inicio{.{0,}}|\\fin{.{0,}}',linea)
	for tag in result:
		inicioFinList.append(tag)
		#Buscar que el parametro que recibe es correcto el inicio/fin
		argmt = re.search(r'{.*}', tag)
		if argmt.group()[1:-1] != 'lista_enumerada' and argmt.group()[1:-1] != 'lista_punteada':
			printError(argmt.group()[1:-1], i2," no es un parametro valido para el tag \inicio o \\fin")
			flags["error"]+=1 

	# Verificar que los items esten dentro de un \inicio
	result = re.findall(r'\\item',linea)
	if result and not re.search(r'\\inicio{.{0,}}', inicioFinList[-1]):
		printError("\item", i2,"se encuentra fuera de una lista")
		flags["error"]+=1 

	# Verificar items dentro de inicio
	result = re.search(r'\\inicio{.{0,}}', linea)
	if result:	# Buscar inicio de lista
		if list_flag["inicio"]:		# Si ya habia iniciado
			printError("\inicio", i2, "hay un inicio dentro de otro inicio")
			flags["error"]+=1 
		else:
			list_flag["inicio"] = True
	# Incorrecto cierre de linea
	elif list_flag["inicio"]:
		if not re.search(r'^\\item{.{0,}}[\s]*$|\\fin{.{0,}}',linea):
			printError("\inicio", i2, "hay texto fuera de un item en una lista")
			flags["error"]+=1 
		if re.search(r'\\item{.{0,}}', linea):	# Actualizar flag de item
			list_flag["item"] = True
		elif re.search(r'\\fin{.{0,}}', linea) and not list_flag["item"]:	# Buscar cierre y actualizar
			printError("\\fin", i2, "no hay items en la lista")
			flags["error"]+=1 
		elif re.search(r'\\fin{.{0,}}', linea):
			list_flag["inicio"] = False
	i2+=1
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
archivo.close()
if flags["error"] > 0:
	# Se ha generado un error, muere el programa.
	print "No ha sido posible compilar el archivo suertex.txt, se han generado "+str(flags["error"])+" errores."
else:
	# Se genera código
	archivo = open("suertex.txt", "r")
	salida = open("output.html", "w")

	# COMIENZO ARCHIVO HTML
	salida.write("<!DOCTYPE HTML>\n")
	p_abierto = False	# Inicializar parrafo cerrado
	linea = ""
	while not re.search(r'[\S]', linea):	# Saltar lineas vacias
		linea = archivo.readline()
	if flags["separamiles"]:	# Verificar comandos y saltar linea
		linea = archivo.readline()
	if flags["ofecha"]:
		linea = archivo.readline()
	sig = ""					# Linea auxiliar para recordar la anterior
	for sig in archivo:
		if flags["separamiles"]:	# Aplicar comando segun corresponda
			linea = separamiles(linea)
		if flags["ofecha"]:
			linea = ofecha(linea)		
		linea, p_abierto = formatPG(linea, sig, p_abierto)	# Formatear segun parrafo
		salida.write(writeLine(linea))				# Transformar a html
		linea = sig
	linea = separamiles(linea)		# Aplicar proceso a ultima linea
	linea = ofecha(linea)
	linea, p_abierto = formatPG(linea, sig, p_abierto, True)
	salida.write(writeLine(linea))
	salida.write("</body>")			# Finalizar html
	archivo.close()
	salida.close()
	print "Compilación generada"
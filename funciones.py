import re
from main import flags

# FUNCIONES TRANSFORMACION A HTML
# FUNCIONES
def separarNum(numero):
	numero = numero.group()
	separador = "."
	original = numero
	largo = len(numero)
	for i in range(-1, -largo, -1):
		if (i % -3) == 0:
			numero = separador.join([original[:i], numero[largo+i:]])
	return numero

def separamiles(linea):
	return re.sub(r'^[0-9]+(?=\s)|(?<=\s)[0-9]+(?=\s)|(?<=\s)[0-9]+$', separarNum, linea)
			
def dateReplace(fecha):
	fecha = fecha.group(0)
	return fecha[0:2]+"/"+fecha[3:5]+"/"+fecha[6:]

def ofecha(fecha):
	return re.sub(r'[\d]{2}[^\w\d\s][\d]{2}[^\w\d\s][\d]{4}', dateReplace, fecha)

# COMANDOS
def fn(texto):
	return "<strong>"+texto+"</strong>"
def fc(texto):
	return "<em>"+texto+"</em>"
def nproy(texto):
	return "<head>\n<title>"+texto+"</title>\n</head>\n<body>"
def titulo(texto):
	return "<h1>"+texto+"</h1>"
def inicio(action):
	if action == "lista_enumerada":
		return "<ol>"
	elif action == "lista_punteada":
		return "<ul>"
	else:
		return False
def fin(action):
	if action == "lista_enumerada":
		return "</ol>"
	elif action == "lista_punteada":
		return "</ul>"
	else:
		return False
def item(texto):
	return "<li>"+texto+"</li>"

# FUNCIONES ADICIONALES

def function(comando, argumento): # Comparar el string comando para verificar cual es
	if comando == "fn":
		return fn(argumento)
	elif comando == "fc":
		return fc(argumento)
	elif comando == "nproy":
		return nproy(argumento)
	elif comando == "titulo":
		return titulo(argumento)
	elif comando == "inicio":
		return inicio(argumento)
	elif comando == "fin":
		return fin(argumento)
	elif comando == "item":
		return item(argumento)
	else:
		print "No entre a ningun comando en function"

def isParagraph(linea): # 0 = No es parrafo; 1 = Es parrafo; 2 = Parrafo nuevo
	if linea == "\n":
		return False
	cmd = re.match(r'\\\w+\{', linea)
	nonParagraphs = ["nproy", "titulo", "inicio", "fin", "item", "separamiles"]
	if cmd:
		func = cmd.group()[1:-1]
		if func in nonParagraphs:
			return 0
		return 2
	return 1

def formatPG(linea, sig, p_abierto=False, end=False):
	if not p_abierto and isParagraph(linea):
		linea = "<p>" + linea
		p_abierto = True
	if p_abierto:
		pg_type = isParagraph(sig)
		if not pg_type or pg_type == 2 or end:
			linea = linea.strip("\n")+"</p>\n"
			p_abierto = False
	return linea, p_abierto

def toHtml(comando):	# Verificar funcion llamada, para trabajar con html
	comando = comando.group()
	cmd = re.match(r'(\\\w+\{)', comando)
	argmt = re.search(r'{.*}', comando)
	return function(cmd.group()[1:-1], argmt.group()[1:-1])

def writeLine(linea):
	search = re.search(r'(\\[^\\]*?})', linea)
	if search:
		linea = re.sub(r'\\[^\\]*?}', toHtml, linea)
		linea = writeLine(linea)
	return linea

archivo = open("suertex.txt", "r")
salida = open("output.html", "w")
salida.write("<!DOCTYPE HTML>")
p_abierto = False
if flags["separamiles"]:
	archivo.readline()
if flags["ofecha"]:
	archivo.readline()
linea = archivo.readline()
sig = ""
for sig in archivo:
	if flags["separamiles"]:	# Modificar segun flag \separamiles{} correspondiente
		linea = separamiles(linea)
	if flags["ofecha"]:
		linea = ofecha(linea)		
	linea, p_abierto = formatPG(linea, sig, p_abierto)
	salida.write(writeLine(linea))
	linea = sig
linea = separamiles(linea)		# Verificar ultima
linea = ofecha(linea)
linea, p_abierto = formatPG(linea, sig, p_abierto, True)
salida.write(writeLine(linea))
salida.write("</body>")
archivo.close()
salida.close()
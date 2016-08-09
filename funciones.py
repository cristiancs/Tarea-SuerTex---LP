import re

# FUNCIONES TRANSFORMACION A HTML

def fn(texto):
	return "<b>"+texto+"</b>"
def fc(texto):
	return "<i>"+texto+"</i>"
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

def isParagraph(linea):
	if linea == "\n":
		return False
	cmd = re.match(r'\\\w+\{', linea)
	nonParagraphs = ["nproy", "titulo", "inicio", "fin", "item", "separamiles"]
	if cmd:
		func = cmd.group()[1:-1]
		if func in nonParagraphs:
			return False
	return True

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
for linea in archivo:
	if isParagraph(linea) and not p_abierto:
		linea = "<p>" + linea
		p_abierto = True
	salida.write(writeLine(linea))
salida.write("\n</body>")

archivo.close()
salida.close()
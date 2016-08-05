import re
# FUNCIONES TRANSFORMACION A HTML
def fn(texto):
	return "<b>"+texto+"</b>"
def fc(texto):
	return "<i>"+texto+"</i>"
def nproy(texto):
	return "<head>\n\t<title>"+texto+"</title>\n</head>"
def titulo(texto):
	return "<h1>"+texto+"</h1>"
def inicio(action):
	if action == "lista_enumerada":
		return "<ol>\n"
	elif action == "lista_punteada":
		return "<ul>\n"
	else:
		return False
def fin(action):
	if action == "lista_enumerada":
		return "</ol>\n"
	elif action == "lista_punteada":
		return "</ul>\n"
	else:
		return False
def item(texto):
	return "<li>"+texto+"</li>\n"

# FUNCIONES ADICIONALES
def function(comando, argumento): # Comparar el string comando para verificar cual es
	comando = comando[1:]
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


def toHtml(linea):	# Verificar funcion llamada, para trabajar con html
	cmds = re.findall(r'[A-z]{1,}{[a-zA-Z\s]*.{1,}}', linea)	#[A-z]{1,}{[a-zA-Z\s]*.{1,}}
	retorno = ""
	if cmds == []:
		retorno += linea
	else:
		for comando in cmds:
			plano = False
			pos_cmd = linea.find(comando)
			retorno += linea[:pos_cmd]
			linea = linea[pos_cmd:]
			largo_actual = len(comando)
			comandos = comando.split("{")
			if len(comandos)<=2:
				retorno += function(comandos[0], comandos[1][:-1])
				linea = linea[pos_cmd+largo_actual:]
			else:
				None
	return retorno

archivo = open("suertex.txt", "r")
salida = open("output.html", "w")
for linea in archivo:
	salida.write(toHtml(linea))

archivo.close()
salida.close()
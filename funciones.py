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
def fin(texto):
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
	comando = comando[0:]
	if comando == "fn":
		fn(argumento)
	elif comando == "fc":
		fc(argumento)
	elif comando == "nproy":
		nproy(argumento)
	elif comando == "titulo":
		titulo(argumento)
	elif comando == "inicio":
		inicio(argumento)
	elif comando == "fin":
		fin(argumento)
	elif comando == "item":
		item(argumento)
	else:
		print "No entre a ningun comando en function"


def toHtml(linea):	# Verificar funcion llamada, para trabajar con html
	cmds = re.findall(r'[A-z]{1,}{[a-zA-Z\s]*.{1,}}', linea)	#[A-z]{1,}{[a-zA-Z\s]*.{1,}}
	for comando in cmds:
		comandos = comando.split(comando, "{")
		function(comandos[0], comandos[1][:-1])

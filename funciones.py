import re
from main import flags

# FUNCIONES TRANSFORMACION A HTML
# FUNCIONES

"""
separarNum(numero)
Recibiendo string de un numero los separa en sus separador
de miles correspondiente '.'
retorna string del numero formateado
"""
def separarNum(numero):
	numero = numero.group()
	separador = "."
	original = numero
	largo = len(numero)
	for i in range(-1, -largo, -1):		# Buscar de atras para adelante
		if (i % -3) == 0:				# Unir lo que se tenia con lo ya modificado
			numero = separador.join([original[:i], numero[largo+i:]])
	return numero

"""
separamiles(linea)
Hace una busqueda en un string de los numeros a formatear, esten ya sea al 
principio, al medio o al final de una linea y le agrega los '.'
segun separarNum
retorna string del numero formateado
"""
def separamiles(linea):
	return re.sub(r'^[0-9]+(?=\s)|(?<=\s)[0-9]+(?=\s)|(?<=\s)[0-9]+$', separarNum, linea)

"""
dateReplace(fecha)
Recibiendo string de una fecha, reemplaza los caracteres separadores
con el "/" correspondiente
retorna el string de la fecha formateada
"""
def dateReplace(fecha):
	fecha = fecha.group(0)
	return fecha[0:2]+"/"+fecha[3:5]+"/"+fecha[6:]

"""
ofecha(fecha)
Realiza una busqueda de las posibles fechas que se necesiten
formatear, para luego formatear segun dateReplace
retorna string de la fecha formateada
"""
def ofecha(fecha):
	return re.sub(r'[\d]{2}[^\w\d\s][\d]{2}[^\w\d\s][\d]{4}', dateReplace, fecha)

# COMANDOS
"""
fn(texto)
Transforma el texto a negrita en html
retorna string
"""
def fn(texto):
	return "<strong>"+texto+"</strong>"

"""
fc(texto)
Transforma el texto a cursiva en html
retorna string
"""
def fc(texto):
	return "<em>"+texto+"</em>"

"""
nproy(texto)
Transforma el texto a nombre de proyecto en html
retorna string
"""
def nproy(texto):
	return "<head>\n<title>"+texto+"</title>\n</head>\n<body>"

"""
titulo(texto)
Transforma el texto a titulo en html
retorna string
"""
def titulo(texto):
	return "<h1>"+texto+"</h1>"

"""
inicio(texto)
Comienza la lista requerida en html
retorna string
"""
def inicio(action):
	if action == "lista_enumerada":
		return "<ol>"
	elif action == "lista_punteada":
		return "<ul>"
	else:
		return False

"""
fin(texto)
Finaliza la lista requerida en html
retorna string
"""
def fin(action):
	if action == "lista_enumerada":
		return "</ol>"
	elif action == "lista_punteada":
		return "</ul>"
	else:
		return False

"""
item(texto)
Agrega el texto como item de lista en html
retorna string
"""
def item(texto):
	return "<li>"+texto+"</li>"

# FUNCIONES ADICIONALES

"""
function(comando, argumento)
Aplica funcion (comando) para transformar a html segun corresponda
al argumento
retorna string
"""
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

"""
isParagraph(linea)
Identifica si la linea es parrafo o no
retorna int segun el tipo del parrafo
"""
def isParagraph(linea): # 0 = No es parrafo; 1 = Es parrafo; 2 = Parrafo nuevo
	if linea == "\n":	# Ignorar lineas vacias
		return False
	cmd = re.match(r'\\\w+\{', linea)	# Verificar comandos que no van en parrafos
	nonParagraphs = ["nproy", "titulo", "inicio", "fin", "item", "separamiles"]
	if cmd:
		func = cmd.group()[1:-1]
		if func in nonParagraphs:
			return 0
		return 2
	return 1

"""
formatPG(linea, sig, p_abierto, end)
Formatea la linea segun sea parrafo o no, determinando si corresponde abrirlo, 
cerrarlo (p_abierto) o esta al final del texto (end)
retorna string, bool con el formato y el estado actual
"""
def formatPG(linea, sig, p_abierto=False, end=False):
	if not p_abierto and isParagraph(linea): # Si es parrafo y no se ha abierto
		linea = "<p>" + linea
		p_abierto = True
	if p_abierto:	# Si ya se abrio el parrafo
		pg_type = isParagraph(sig)
		if not pg_type or pg_type == 2 or end:	# Si sig no es parrafo o termina
			linea = linea.strip("\n")+"</p>\n"
			p_abierto = False
	return linea, p_abierto

"""
toHtml(comando)
Al comando ya identificado, identifica la funcion y el texto al que se le
requiere aplicar, para llamar a function sobre ellos
retorna string con la funcion realizada
"""
def toHtml(comando):	# Verificar funcion llamada, para trabajar con html
	comando = comando.group()
	cmd = re.match(r'(\\\w+\{)', comando)	# Funcion
	argmt = re.search(r'{.*}', comando)		# Texto
	return function(cmd.group()[1:-1], argmt.group()[1:-1])

"""
writeLine(linea)
Busca funciones a aplicar a la linea y luego las transforma
a html segun toHtml, luego se aplica recursivamente para
transformar funciones anidadas
retorna string de linea en html
"""
def writeLine(linea):
	search = re.search(r'(\\[^\\]*?})', linea)	# Funcion (mas interna)
	if search:
		linea = re.sub(r'\\[^\\]*?}', toHtml, linea)	# Transformar a html
		linea = writeLine(linea)	# Anidado
	return linea

archivo = open("suertex.txt", "r")
salida = open("output.html", "w")

# COMIENZO ARCHIVO HTML
salida.write("<!DOCTYPE HTML>")
p_abierto = False	# Inicializar parrafo cerrado
if flags["separamiles"]:	# Verificar comandos y saltar linea
	archivo.readline()
if flags["ofecha"]:
	archivo.readline()
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
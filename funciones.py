import re
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
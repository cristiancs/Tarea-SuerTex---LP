import re

#Obtener numero de separar miles
string = '/separamiles{25}'
result = re.split(r'/separamiles{',string)
result = re.split(r'}',result[1])[0]



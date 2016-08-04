import re

#Obtener numero de separar miles
string = 'aa /separamiles{25}'
result = re.findall(r'/separamiles{([0-9]{1,})}',string)
print result



import requests
import hashlib
import json



token = "dd3fc61ecc5857bf713f58460fb9b582f13bf28b"

urlPost = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={}".format(token)

urlGet = "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={}".format(token)


# 1ª etapa: ler o arquivo do site

response = requests.get(urlGet)
answer = response.json()


# 2ª etapa: salvar o conteúdo do site no arquivo answer.json

with open('answer.json', 'w') as outfile:
	json.dump(answer, outfile)


# 3ª etapa: decifrar a mensagem


alfabeto = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7,"i":8,"j":9,"k":10,"l":11,"m":12,"n":13,
"o":14,"p":15,"q":16,"r":17,"s":18,"t":19,"u":20,"v":21,"w":22,"x":23,"y":24,"z":25}

alfabeto2 = {-5: "v", -4: "w", -3: "x", -2: "y", -1: "z", 0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6:'g',
 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19:'t',
 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}


text = answer["cifrado"]

text2 = [] 

for ch in text:
	
	if ch.isspace():
		text2.append(" ")

	elif ch.isalpha():
		text2.append(alfabeto[ch])

	else:
		text2.append(ch) 


text3 = []

for element in text2:

	if element == " ":
		text3.append(" ")

	elif type(element) == type(0):
		indice = element - answer["numero_casas"]
		text3.append(alfabeto2[indice])

	else:
		text3.append(element) 


textDecifrada = ""

for elemento in text3:
	textDecifrada += elemento


# 4ª etapa: atualizar o answer.json no campo "decifrado"

answer["decifrado"] = textDecifrada

with open('answer.json', 'w') as outfile:
	json.dump(answer, outfile)


# 5ª etapa: criptografar a mensagem decifrada em SHA1

resumo = hashlib.sha1(textDecifrada.encode()).hexdigest() 


# 6ª etapa: atualizar o answer.json no campo "resumo_criptografico"

answer["resumo_criptografico"] = resumo
with open('answer.json', 'w') as outfile:
	json.dump(answer, outfile)


# 7ª etapa: subir o answer.json no site 
files = {'answer': open('answer.json', 'rb')}
response = requests.post(urlPost, files=files)


print(response.text)

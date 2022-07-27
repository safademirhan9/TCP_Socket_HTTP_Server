import os
import socket
import json
import re
from sympy import isprime

# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080

# Create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen(1)
print('Listening on port %s ...' % SERVER_PORT)
response = ''

while True:    
    # Wait for client connections
    client_connection, client_address = server.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()


    try:

        # Parse HTTP headers
        headers = request.split('\n')
        filename = headers[0].split()[1]
        filename = filename[filename.find('?')+1::]
        listOfParameters = filename.split('&')

        if('GET' in request):
            if('isPrime' in request):
                if('number' in request):
                    number = listOfParameters[0].split('=')[1]
                    if number.__contains__('.'):
                        response = 'HTTP/1.1 400 Bad Request\n\n '
                        dict = {"message": "Lutfen tam sayi giriniz!"}
                        data = json.dumps(dict)
                        response += data
                        client_connection.sendall(response.encode())
                    else:
                        number = int(number)
                        response = 'HTTP/1.1 200 OK\n\n OK'
                        ans = isprime(number)
                        dict = {"number": number, "isPrime": ans}
                        data = json.dumps(dict)
                        response += data
                else:
                    response = 'HTTP/1.1 400 Bad Request\n\n Bad Request'
                    client_connection.sendall(response.encode())
                    continue
            elif('download' in request):
                fileName = listOfParameters[0].split('=')[1]
                with open(fileName, 'rb') as f:
                    client_connection.sendall("HTTP/1.0 200 OK\n\n".encode())
                    while True:
                        temp = f.read(1024)
                        if not temp:
                            break
                        client_connection.send(temp)
                    f.close()
                response = 'HTTP/1.1 200 OK\n\n OK'
                client_connection.sendall(response.encode())
        elif('POST' in request):
            if('upload' in request):
                fileName = listOfParameters[0].split('=')[1]
                with open(fileName, 'wb') as f:
                    client_connection.sendall("HTTP/1.0 200 OK\n\n".encode())
                    while True:
                        temp = f.write(1024)
                        if not temp:
                            break
                        client_connection.send(temp)
                    f.close()
                response = 'HTTP/1.1 200 OK\n\n OK'
                client_connection.sendall(response.encode())
        elif('PUT' in request):
            if('rename' in request):
                for x in listOfParameters:
                    if(x.__contains__("oldFileName")):
                        oldFileName = x.split('=')[1]
                    elif(x.__contains__("newName")):
                        newName = x.split('=')[1]
                    else:
                        response = 'HTTP/1.1 400 Bad Request\n\n '
                        dict = {"message": " Yanlis veya gereksiz parametre verdiniz"}
                        data = json.dumps(dict)
                        response += data
                        client_connection.sendall(response.encode())
                        client_connection.close()
                if(oldFileName.__eq__('') or newName.__eq__('')):
                    response = 'HTTP/1.1 400 Bad Request\n\n '
                    dict = {"message": "Parametre icerigini doldurmadiniz"}
                    data = json.dumps(dict)
                    response += data
                else:
                    try:
                        os.rename(oldFileName, newName)
                        response = 'HTTP/1.1 200 OK\n\n '
                        dict = {"message": "Dosya ismi basariyla degistirilmistir"}
                        data = json.dumps(dict)
                        response += data
                    except  FileNotFoundError:
                        response = 'HTTP/1.1 200 OK\n\n '
                        dict = {"message": "Boyle bir dosya bulunmamaktadir"}
                        data = json.dumps(dict)
                        response += data
        elif('DELETE' in request):
            if('remove' in request):
                for x in listOfParameters:
                    if(x.__contains__("fileName")):
                        fileName = x.split('=')[1]
                    else:
                        response = 'HTTP/1.1 400 Bad Request\n\n '
                        dict = {"message": "Yanlis veya gereksiz parametre verdiniz"}
                        data = json.dumps(dict)
                        response += data
                        client_connection.sendall(response.encode())
                if(fileName.__eq__('')):
                    response = 'HTTP/1.1 400 Bad Request\n\n Parametre icerigini doldurmadiniz'
                    dict = {"message": "Parametre icerigini doldurmadiniz"}
                    data = json.dumps(dict)
                    response += data
                else:
                    try:
                        os.remove(fileName)
                        response = 'HTTP/1.1 200 OK\n\n '
                        dict = {"message": "Dosya basarili bir sekilde silindi"}
                        data = json.dumps(dict)
                        response += data
                    except FileNotFoundError:
                        response = 'HTTP/1.1 200 OK\n\n '
                        dict = {"message": "Dosya bulunamadi"}
                        data = json.dumps(dict)
                        response += data
    except:
        if(len(response) == 0):
            response = 'HTTP/1.1 404 NOT FOUND\n\nNot Found'
    
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server.close()


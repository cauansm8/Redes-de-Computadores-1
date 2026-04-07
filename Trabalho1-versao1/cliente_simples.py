from socket import *

# ip
nome_do_servidor = '127.0.0.1'
porta_do_servidor = 5000

# AF_INET - define a família IPv4
# SOCK_STREAM - define o tipo - TCP
cliente_Socket = socket(AF_INET, SOCK_STREAM)

# estabele conexão TCP entre servidor e cliente
# o primeiro parâmetro é o enderço do lado servidor da conexão
cliente_Socket.connect((nome_do_servidor, porta_do_servidor))

while True:

    Mensagem = input('\nDigite sua mensagem:')

    # transforma em bytes e envia
    cliente_Socket.send(Mensagem.encode('utf-8'))

    # recebe a mensagem de retorno do servidor e transforma para utf-8
    mensagemRecebida = cliente_Socket.recv(1024).decode('utf-8')

    print ('Do servidor:', mensagemRecebida)

    if mensagemRecebida == 'FIM':
        print("Conexão encerrada")
        break
  
cliente_Socket.close()

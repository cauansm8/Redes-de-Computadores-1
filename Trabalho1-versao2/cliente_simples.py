from socket import *
import threading

# thread para receber mensagem
def receber_mensagem(cliente_socket):
    while True: 
        try:

            # recebe a mensagem
            mensagem = cliente_socket.recv(1024).decode('utf-8')

            print(f"\n{mensagem}\n", end="", flush=True)

        except:
            # quando manda fim -> o socket é encerrado
            # para evitar o erro de "cliente_socket.rec(..)" 
            #  há esse except vazio para tratar esse "erro"
            pass

# ip
nome_do_servidor = '127.0.0.1'
porta_do_servidor = 5000

# AF_INET - define a família IPv4
# SOCK_STREAM - define o tipo - TCP
cliente_Socket = socket(AF_INET, SOCK_STREAM)

# estabele conexão TCP entre servidor e cliente
# o primeiro parâmetro é o enderço do lado servidor da conexão
cliente_Socket.connect((nome_do_servidor, porta_do_servidor))

nome = input('Digite seu nome: ')

cliente_Socket.send(nome.encode('utf-8'))

# thread para receber mensagem (roda em segundo plano)
# precisa da virgula nos argumentos para criar uma tupla
thread_receberMensagem = threading.Thread(target=receber_mensagem, args=(cliente_Socket,))
thread_receberMensagem.daemon = True # Faz a thread fechar se o programa principal fechar
thread_receberMensagem.start()

while True:

    # fluxo principal (envio de mensagem)
    mensagem = input('> ')

    if mensagem.upper() == 'FIM':
        cliente_Socket.send(mensagem.encode('utf-8'))
        print("Fim da conexão")
        break

    cliente_Socket.send(mensagem.encode('utf-8'))


cliente_Socket.close()

    
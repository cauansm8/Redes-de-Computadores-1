from socket import *
import threading


# verifica o tipo de mensagem
def verificarUnicast(mensagem):
    if mensagem[0] == '/' and mensagem[1] == 'p':
        return True
    else:
        return False


# código que vai rodar em paralelo
def distribuir_mensagem(conexao_socket, nome_do_cliente):
    while True: 
        try:
            # recebe a mensagem e decodifica 
            mensagem = conexao_socket.recv(1024).decode('utf-8')
            
            if mensagem.upper() == 'FIM':
                break

            print ('------')
            print(f'Mensagem recebida com sucesso do cliente {nome_do_cliente} = "{mensagem}"')
            
            # broadcast
            if verificarUnicast(mensagem) == False:
                print('Broadcast - destino: todos clientes')
                
                # percorre todas conexões
                for nome, s in clientes.items():
                    
                    # impede de enviar a mensagem para o mesmo cliente
                    if nome_do_cliente != nome:
                        s.send(f"Mensagem broadcast de {nome_do_cliente} -> {mensagem}".encode('utf-8'))
                        
                print('Mensagem enviada a todos!')


            # unicast
            else:
                # /p junior ola -> começa a separar a partir do primeiro espaço (após o '/p')
                # [1] -> junior
                # [2] -> mensagem
                divisão = mensagem.split(' ', 2)
                
                nome_destino = divisão[1]
                mensagem = divisão[2]
                print('Unicast - destino: ' + nome_destino)
                
                
                # verifica se o cliente está no dicionário
                if nome_destino in clientes:
                        s = clientes[nome_destino]
                        s.send(f"Mensagem unicast de {nome_do_cliente} -> {mensagem}".encode('utf-8'))
                        print(f'Mensagem enviada ao cliente {nome_destino}!')
                        
                else:
                    print("Cliente de destino não encontrado")
                
            print ('------\n')
        
        except:
            break

    
    # apaga o nome e o socket do cliente do dicionário
    if nome_do_cliente in clientes:
        
        del clientes[nome_do_cliente]
        
        # fecha conexão com esse cliente    
        conexao_socket.close()
        
        print(f'cliente {nome_do_cliente} saiu do chat\n')





nome_do_servidor = '127.0.0.1'
porta_do_servidor = 5000

# AF_INET - define a família IPv4
# SOCK_STREAM - define o tipo - TCP
servidor_Socket = socket(AF_INET,SOCK_STREAM)

servidor_Socket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)

# Associa o socket a um endereço IP e a uma porta específica no PC. 
servidor_Socket.bind((nome_do_servidor, porta_do_servidor))

servidor_Socket.listen(5)

# nome : socket
clientes = {}
print("Esperando conexão")

# loop infinito que apenas faz o accept
while True:

    conexao_socket, endereco = servidor_Socket.accept()

    nome = conexao_socket.recv(1024).decode('utf-8')

    # cria um hash: nome - socket
    clientes[nome] = conexao_socket

    print(f'Cliente conectado: {nome} - {conexao_socket.getpeername()}')
    
    # cria e inicia a thread
    thread = threading.Thread(target=distribuir_mensagem, args=(conexao_socket, nome))
    thread.daemon = True # Thread morre se o programa principal fechar
    thread.start()


    

from socket import *

nome_do_servidor = '127.0.0.1'
porta_do_servidor = 5000

# AF_INET - define a família IPv4
# SOCK_STREAM - define o tipo - TCP
servidor_Socket = socket(AF_INET,SOCK_STREAM)

servidor_Socket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)

# Associa o socket a um endereço IP e a uma porta específica no PC. 
servidor_Socket.bind((nome_do_servidor, porta_do_servidor))

# Coloca o servidor em modo de espera, definindo quantas conexões podem ficar na "fila"
# antes de serem atendidas. O servidor escuta as requisições de conexão TCP do cliente.
# O parâmetro especifica o número máximo de conexões em fila (pelo menos 1).
servidor_Socket.listen(2)

print ('\nO servidor está pronto para conexão!')

i = 0

while True:
    print('Aguardando conexão')

    # O servidor bloqueia (para a execução) até que um cliente tente se conectar. Quando isso acontece,
    # ele retorna um novo socket dedicado para falar com esse cliente e o endereço dele.
    # Cria uma conexão TCP entre o clientSocket (cliente) e connectionSocket (servidor).
    # Após estabelecer a conexão TCP, cliente e servidor podem enviar bytes um para o outro por ela.
    # Há garantia de que os bytes chegarão e em ordem - por causa que é com TCP
    conexao_socket, endereco = servidor_Socket.accept()
    print('cliente conectado!')

    i += 1

    while True:

        # recebe a mensagem e decodifica 
        mensagem = conexao_socket.recv(1024).decode('utf-8')

        print('Mensagem recebida com sucesso')

        # deixa em maiúsculo a sentença
        mensagem_em_maiusculo = mensagem.upper()

        # envia a sentença
        conexao_socket.send(mensagem_em_maiusculo.encode('utf-8'))
    
        # Depois de enviar a sentença modificada ao cliente, fecha-se o socket de conexão. Mas o serverSocket
        # continua aberto para outro cliente
        if mensagem_em_maiusculo == 'FIM':
            print(f'cliente número {i} desconectado -> Conexão encerrada')
            break
        
    conexao_socket.close()
    print ('-------------')
import numpy as np

redes = [''] * 4
ip_necessarios = [0] * 4
numeracao_autoridade = [0] * 4
barra = 0
mascara_de_subrede = [0] * 4
erro = False

endereco = np.zeros((4, 4),  dtype=int)
endereco_de_transmissao_broadcast = np.zeros((4, 4),  dtype=int)
endereco_da_rede = np.zeros(4, dtype=int)
qnt = 4
# intervalo de ips = broadcast - enderecogit 

# pega os conteúdos das sub-redes A, B, C, D
def inicial():
    
    # tava criando variavel local
    global numeracao_autoridade, barra, redes, ip_necessarios, erro

    # mapeia para lista automaticamente como inteiro
    numeracao_autoridade = list(map(int, input("Digite a numeracão da autoridade (sem o /CIDR!!): ").split(".")))
    barra = int(input("Digite o CIDR: "))

    if numeracao_autoridade[0] < 0 or numeracao_autoridade[0] > 255 or numeracao_autoridade[1] < 0 or numeracao_autoridade[1] > 255 or numeracao_autoridade[2] < 0 or numeracao_autoridade[2] > 255 or numeracao_autoridade[3] < 0 or numeracao_autoridade[3] > 255:
        print('ALGUM OCTETO FORA DE 0-255!')
        erro = True
        return
    

    if barra < 0 or barra > 32:
        print("CIDR fora do intervalo")
        erro = True
        return


    for i in range(4):
        nome = input(f"Nome da rede {i+1}: ")
        ips = int(input(f"Quantidade de IPs necessários para {nome}: "))
    
        if ips < 0:
            erro = True
            print("VALOR NEGATIVO PARA IP = ERRO")

        redes[i] = nome
        ip_necessarios[i] = ips


def calcularCIDR(i):
    j = 0
    
    # tem que desconsiderar os endereços de rede e de broadcast -> -2
    while (2**j - 2 < ip_necessarios[i]):
        j += 1

    cidr_resultado = 32 - j

    print(f"Prefixo CIDR /{cidr_resultado}") 

    return cidr_resultado, j





def calcularMascara(cidr, is_subRede = True):

    if cidr > 32 or cidr < 0:
        print('ERRO!')
        return
    
    mascara_temp = [0] * 32

    # preenchendo
    for i in range (0, 32):
        if cidr - i > 0:
            mascara_temp[i] = '1'
        else:
            mascara_temp[i] = '0'


    octetos = []
    # pega blocos de 8 em 8 (octetos)
    for i in range(0, 32, 8):
        bloco = mascara_temp[i:i+8]
        octetos.append(bloco)

    j = 0
    for bloco in octetos:
        # transforma cada bloco em string (de valor binário)
        valor_bin = "".join(map(str, bloco))
        
        # passa para decimal e guarda o resultado
        mascara_de_subrede[j] = int(valor_bin, 2)

        j += 1
    
    if is_subRede == True:
        print(f"Máscara de sub-rede {mascara_de_subrede[0]}.{mascara_de_subrede[1]}.{mascara_de_subrede[2]}.{mascara_de_subrede[3]}")
    else:
        print(f"Máscara de rede {mascara_de_subrede[0]}.{mascara_de_subrede[1]}.{mascara_de_subrede[2]}.{mascara_de_subrede[3]}")

    return np.array([mascara_de_subrede[0], mascara_de_subrede[1], mascara_de_subrede[2], mascara_de_subrede[3]])





def calcularEnderecoDeRede_Broadcast(j, i):
    
    # pegando o salto de quantidade de ips
    intervalo = 2 ** j

    # para o primeiro -> ele começa no primeiro endereço de autoridade indicado
    # o seu broadcast (último ip) é no final do intervalo - 1
    if i == 0:
        endereco[i, 0] = endereco_da_rede[0]
        endereco[i, 1] = endereco_da_rede[1]
        endereco[i, 2] = endereco_da_rede[2]
        endereco[i, 3] = endereco_da_rede[3]


    # para o restante -> começa no fim do anterior + 1
    # vai até o salto
    else:
        endereco[i, 0] = endereco_de_transmissao_broadcast[i-1, 0]
        endereco[i, 1] = endereco_de_transmissao_broadcast[i-1, 1]
        endereco[i, 2] = endereco_de_transmissao_broadcast[i-1, 2]
        endereco[i, 3] = endereco_de_transmissao_broadcast[i-1, 3] + 1 
        # o ultimo aumenta 1 (o anterior é o broadcast da rede anterior)



    # VERIFICAÇÃO IMPORTANTE -> carry no endereço -> se ficar 127.20.10.256 -> 127.20.11.0
    if endereco[i, 3] > 255:

        while endereco[i, 3] > 255:
            sobeIp = endereco[i, 3]- 256 

            endereco[i, 3] = sobeIp
        
            endereco[i, 2] += 1
        
    if endereco[i, 2] > 255:
        while endereco[i, 2] > 255:

            sobeIp = endereco[i, 2] - 256 

            endereco[i, 2] = sobeIp

            endereco[i, 1] += 1

    if endereco[i, 1] > 255:

        while endereco[i, 1] > 255:

            sobeIp = endereco[i, 1] - 256

            endereco[i, 1] = sobeIp
                    
            endereco[i, 0] += 1

    if endereco[i, 0] > 255:
        print('ERRO - ULTRAPASSOU O LIMITE MÁXIMO DO IPv4')
        return


    # calculamos só agora o broadcast pq é necessário corrigir o endereço 
    # (se tiver problema que resulte em carry)
    if i == 0:

        endereco_de_transmissao_broadcast[i, 0] = endereco_da_rede[0]
        endereco_de_transmissao_broadcast[i, 1] = endereco_da_rede[1]
        endereco_de_transmissao_broadcast[i, 2] = endereco_da_rede[2]
        endereco_de_transmissao_broadcast[i, 3] = endereco[i, 3] + intervalo - 1

   
    else:

        endereco_de_transmissao_broadcast[i, 0] = endereco[i, 0]
        endereco_de_transmissao_broadcast[i, 1] = endereco[i, 1]
        endereco_de_transmissao_broadcast[i, 2] = endereco[i, 2]
        endereco_de_transmissao_broadcast[i, 3] = endereco[i, 3] + intervalo - 1






    # VERIFICAÇÃO IMPORTANTE -> carry no broadcast -> se ficar 127.20.10.256 -> 127.20.11.0
    if endereco_de_transmissao_broadcast[i, 3] > 255:

        while endereco_de_transmissao_broadcast[i, 3] > 255:
            sobeIp = endereco_de_transmissao_broadcast[i, 3]- 256 

            endereco_de_transmissao_broadcast[i, 3] = sobeIp
        
            endereco_de_transmissao_broadcast[i, 2] += 1
        
    if endereco_de_transmissao_broadcast[i, 2] > 255:
        while endereco_de_transmissao_broadcast[i, 2] > 255:

            sobeIp = endereco_de_transmissao_broadcast[i, 2] - 256 

            endereco_de_transmissao_broadcast[i, 2] = sobeIp

            endereco_de_transmissao_broadcast[i, 1] += 1

    if endereco_de_transmissao_broadcast[i, 1] > 255:

        while endereco_de_transmissao_broadcast[i, 1] > 255:

            sobeIp = endereco_de_transmissao_broadcast[i, 1] - 256

            endereco_de_transmissao_broadcast[i, 1] = sobeIp
                    
            endereco_de_transmissao_broadcast[i, 0] += 1

    if endereco_de_transmissao_broadcast[i, 0] > 255:
        print('ERRO - ULTRAPASSOU O LIMITE MÁXIMO DO IPv4')
        return




    

    print(f"Endereço de rede {endereco[i, 0]}.{endereco[i, 1]}.{endereco[i, 2]}.{endereco[i, 3]}")
    print(f"Endereço de transmissão (broadcast) {endereco_de_transmissao_broadcast[i, 0]}.{endereco_de_transmissao_broadcast[i, 1]}.{endereco_de_transmissao_broadcast[i, 2]}.{endereco_de_transmissao_broadcast[i, 3]}")
    printarIpsUtilizaveis(i)


def printarIpsUtilizaveis(i):

    # o endereço inicial é um após o endereço da rede -> PRECISA FAZER VERIFICAÇÃO

    endereco_inicial_temporario = np.zeros(4, dtype=int) 
    endereco_inicial_temporario[0] = endereco[i, 0]
    endereco_inicial_temporario[1] = endereco[i, 1]
    endereco_inicial_temporario[2] = endereco[i, 2]
    endereco_inicial_temporario[3] = endereco[i, 3] + 1


    while endereco_inicial_temporario[3] > 255:

        sobeIp = endereco_inicial_temporario[3] - 256

        endereco_inicial_temporario[3] = sobeIp
                    
        endereco_inicial_temporario[2] += 1

    while endereco_inicial_temporario[2] > 255:

        sobeIp = endereco_inicial_temporario[2] - 256

        endereco_inicial_temporario[2] = sobeIp
                    
        endereco_inicial_temporario[1] += 1

    while endereco_inicial_temporario[1] > 255:

        sobeIp = endereco_inicial_temporario[1] - 256

        endereco_inicial_temporario[1] = sobeIp
                    
        endereco_inicial_temporario[0] += 1

    if endereco_inicial_temporario[0] > 255:
        print('ERRO - ULTRAPASSOU O LIMITE MÁXIMO DO IPv4')
        return


    # o endereco final é um anterior ao endereço broadcast -> PRECISA FAZER VERIFICAÇÃO
    endereco_final_temporario = np.zeros(4, dtype=int) 
    endereco_final_temporario[0] = endereco_de_transmissao_broadcast[i, 0]
    endereco_final_temporario[1] = endereco_de_transmissao_broadcast[i, 1]
    endereco_final_temporario[2] = endereco_de_transmissao_broadcast[i, 2]
    endereco_final_temporario[3] = endereco_de_transmissao_broadcast[i, 3] - 1

    while endereco_final_temporario[3] < 0:

        endereco_final_temporario[3] = 255
                    
        endereco_final_temporario[2] -= 1

    while endereco_final_temporario[2] < 0:

        endereco_final_temporario[2] = 255
                    
        endereco_final_temporario[1] -= 1

    while endereco_final_temporario[1] < 0:

        endereco_final_temporario[1] = 255
                    
        endereco_final_temporario[0] -= 1

    if endereco_final_temporario[0] < 0:
        print('ERRO - ULTRAPASSOU O LIMITE MÍNIMO DO IPv4')
        return


    print(f"Intervalo de IPs utilizáveis: {endereco_inicial_temporario[0]}.{endereco_inicial_temporario[1]}.{endereco_inicial_temporario[2]}.{endereco_inicial_temporario[3]} - {endereco_final_temporario[0]}.{endereco_final_temporario[1]}.{endereco_final_temporario[2]}.{endereco_final_temporario[3]}")


def main():
    inicial()

    if erro == True:
        print("ERRO - FINALIZANDO PROGRAMA")
        return 0


    # calculando mascara da rede e trnasformando para decimal
    mascara_da_rede = calcularMascara(barra, is_subRede = False)


    # AND em cada octeto entre numeracao_autoridade e mascara_da_rede -> No python, 
                # o AND deve ser feito entre números decimais inteiros (não bin)
    #   no slide: faz AND com binários mesmo!
    for i in range (len(mascara_da_rede)):
        endereco_da_rede[i] = numeracao_autoridade[i] & mascara_da_rede[i]
    
        

    print(f"Endereço da Rede: {endereco_da_rede[0]}.{endereco_da_rede[1]}.{endereco_da_rede[2]}.{endereco_da_rede[3]}")



    # calculando (endereço, broadcast, máscara e cidr) das sub-redes
    for i in range (0, len(redes)):
        print(f"\nRede {redes[i]}")


        # descobre o expoente do salto (para calcular a quantidade de ips e broadcast)
        n = 0
        while (2**n - 2 < ip_necessarios[i]):
            n += 1

        cidr, n = calcularCIDR(i)

        calcularMascara(cidr)

        calcularEnderecoDeRede_Broadcast(n, i)

        print('------------')

main()
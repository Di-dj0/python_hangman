import socket
import sys
import os

from sympy import false

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class main_game:

    def __init__(self, palavra): #{

        self.palavra = palavra
        self.tamanho_palavra = len(palavra)
        self.tamanho_original = len(palavra)
        self.lista_letras = list(palavra)
        self.lista_letras_usadas = []
        self.fim_do_jogo = False
        self.vidas = 10

    def verifica_letra(self, letra):

        if letra in self.lista_letras_usadas:
            print('Essa letra ja foi utilizada!')
        #Resolver problema de letras repetidas
        elif letra in self.lista_letras:
            print('Letra encontrada! \"' + letra + '\"')
            self.lista_letras_usadas.append(letra)
            counter = self.lista_letras.count(letra)
            # validado a letra, diminui a qnt de letras
            self.tamanho_palavra = self.tamanho_palavra - counter
        
        else:
            print('Letra ' + letra + ' nao esta na palavra!')
            self.lista_letras_usadas.append(letra)
            self.vidas = self.vidas - 1

    def verifica_letra_oponente(self, letra):
        if letra in self.lista_letras:
            print('Seu oponente acertou uma letra! \"' + letra + '\"')
            self.lista_letras_usadas.append(letra)
            counter = self.lista_letras.count(letra)
            # validado a letra, diminui a qnt de letras
            self.tamanho_palavra = self.tamanho_palavra - counter

        else:
            print('Seu oponente errou! A letra ' + letra + ' nao esta na palavra!')
            self.lista_letras_usadas.append(letra)
            self.vidas = self.vidas - 1

    def verifica_fim_do_jogo(self):

        if self.tamanho_palavra == 0:
            cls()
            print('Parabens!\nA palavra eh: ' + self.palavra)
            self.fim_do_jogo = True
        
        elif self.vidas == 0:
            cls()
            print('Que pena, voce perdeu :<\nA palavra era: ' + self.palavra)
            self.fim_do_jogo = True
        
        else:
            self.fim_do_jogo = False

        return self.fim_do_jogo

    def escreve_palavra(self):

        for i in range(self.tamanho_original):
            # se letra ja encontrada, printa a letra e um espaco
            if self.lista_letras[i] in self.lista_letras_usadas:
                print(self.lista_letras[i] + ' ')
            else:
                print('_ ')

    def tenta_letra(self):
        letra = input('Digite uma letra que deseja testar:')
        return letra


def main():

    socketConexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    endereco = ('127.0.0.1', 50000)
    socketConexao.bind(endereco)
    socketConexao.listen(1)

    [jogador, _] = socketConexao.accept()

    forca = main_game("BATATA")
    #Servidor tem que enviar palavra para o cliente para que o jogo inicie
    msg = 'P'.encode()
    msg += forca.tamanho_original.to_bytes(1, byteorder='big')
    msg += forca.palavra.encode()
    jogador.send(msg)

    encerrado = False

    while not encerrado:

        #Servidor começa jogando (Tentar implementar início random depois)
        forca.escreve_palavra()
        print('Vidas restantes: ' + str(forca.vidas))
        print('As letras já usadas foram' + forca.lista_letras_usadas)
        letra = forca.tenta_letra()

        while letra.isnumeric():
            print('Por favor utilize apenas letras unicas!')
            letra = forca.tenta_letra()

        forca.verifica_letra(letra)

        msg = 'L'.encode()
        msg+= letra.encode()

        jogador.send(msg)
        #Envia a letra ao oponente antes de encerrar o jogo
        encerrado = forca.verifica_fim_do_jogo()

        #Retorno já é a jogada do oponente

        if not encerrado:

            codigo = jogador.recv(1)
            if not codigo:
                sys.exit(-1)
            codigo = codigo.decode()
            if codigo == 'L':
                letra = jogador.recv(1)
                letra = letra.decode()
                forca.verifica_letra_oponente(letra)
                verificacao = forca.verifica_fim_do_jogo() #Atualizar verificação para oponente
                if verificacao == True and forca.tamanho_palavra == 0:
                    print("Você perdeu")
                    encerrado = True
                elif verificacao == True and forca.vidas == 0:
                    print("Vocês perderam! Ninguém ganhou! Todo mundo empatou!")
                    encerrado = True
                else:
                    print("Sua vez de jogar!")
            else:
                print('Erro')
                sys.exit(-2)

if __name__ == '__main__':
    main()
import socket
import sys
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class main_game:

    def __init__(self, palavra): #{

        # para testes, sobrescrevemos a palavra
        palavra = "BANANA"

        self.palavra = palavra
        self.tamanho_palavra = len(palavra)
        self.tamanho_original = len(palavra)
        self.lista_letras = list(palavra)
        self.lista_letras_usadas = []
        self.fim_do_jogo = False
        self.vidas = 10

        for i in range(self.tamanho_palavra):

            while not self.fim_do_jogo:

                self.escreve_palavra()
                print('Vidas restantes: ' + str(self.vidas))
                letra = input('Digite uma letra que deseja testar:')
                # valida se o input eh uma letra ou numero
                
                if not letra.isnumeric():
                    self.verifica_letra(letra)
                    self.verifica_fim_do_jogo()
                else:
                    print('Por favor utilize apenas letras unicas!')
    #}

    def verifica_letra(self, letra):

        if letra in self.lista_letras_usadas:
            print('Essa letra ja foi utilizada!')

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

    def escreve_palavra(self):

        for i in range(self.tamanho_original):
            # se letra ja encontrada, printa a letra e um espaco
            if self.lista_letras[i] in self.lista_letras_usadas:
                print(self.lista_letras[i] + ' ')
            else:
                print('_ ')

        
def main():

    forca = main_game("BATATA")
    encerrado = forca.fim_do_jogo

    while not encerrado:
        forca.forca()


if __name__ == '__main__':
    main()
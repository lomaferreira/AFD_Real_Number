# Disciplina: Compiladores - 2025.1 - UFMA
# Alunas: Juliana Gonçalves Câmara e Paloma Santos Ferreira
# Maio 2025
# Implementação de um Automato Finito Determinístico que Aceita Constantes Numéricas                   
from enum import Enum

class AFD:
    class Estados(Enum):
        estado_inicial = 0
        inNum = 1
        inVirgula = 2
        estado_final = 3
        inNegativo = 4

    def __init__(self, lineBuf):
        self.lineBuf = lineBuf
        self.linhaAtual = 0
        self.bufsize = len(lineBuf)
        self.EOF_flag = False

    def retrocesso(self):
        if not self.EOF_flag and self.linhaAtual > 0:
            self.linhaAtual -= 1

    def obterProximoCaracter(self):
        if self.linhaAtual >= self.bufsize:
            self.EOF_flag = True
            return None
        else:
            charAtual = self.lineBuf[self.linhaAtual]
            self.linhaAtual += 1
            return charAtual
        
    def ehDigito(self, char):
        return char.isdigit()

    def obterToken(self):
        state = self.Estados.estado_inicial
        lexema = ''

        while state != self.Estados.estado_final and not self.EOF_flag:
            token = self.obterProximoCaracter()

            if token is None:
                break

            match state:
                case self.Estados.estado_inicial:
                    if self.ehDigito(token):
                        lexema+= token
                        state = self.Estados.inNum
                    elif token == '-':
                        lexema+=token
                        state = self.Estados.inNegativo
                    else:
                        state = self.Estados.estado_inicial
                case self.Estados.inNegativo:
                    if self.ehDigito(token):
                        lexema += token
                        state = self.Estados.inNum
                    else:
                        self.retrocesso()
                        lexema=''
                        state = self.Estados.estado_inicial
                case self.Estados.inNum:
                    if self.ehDigito(token):
                        lexema += token
                    elif token == ",":
                        lexema += token
                        state = self.Estados.inVirgula
                    else:
                        state = self.Estados.estado_final
                        self.retrocesso()

                case self.Estados.inVirgula:
                    state = self.Estados.estado_inicial
                    if self.ehDigito(token):
                        lexema += token
                        state = self.Estados.inNum
                    else:
                        state = self.Estados.estado_inicial
        

        # Verificação final após sair do loop
        if lexema:
            return f"Token Aceito: {lexema}"
        else:
            return "Nenhum token foi reconhecido"
        


def main():
    while(True):
        print("Insira um lexema ou a palavra 'sair':")
        lexema=input('>>>')
        if(lexema=='sair'):
            break
        afd = AFD(lexema)
        print(afd.obterToken())


main()

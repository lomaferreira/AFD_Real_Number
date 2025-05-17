                    
from enum import Enum

class AFD:
    class Estados(Enum):
        estado_inicial = 0
        inNum = 1
        inVirgula = 2
        estado_final = 3
        inNegativo = 4
        estado_rejeitado = 5

    def __init__(self, lineBuf):
        self.lineBuf = lineBuf
        self.linhaAtual = 0
        self.bufsize = len(lineBuf)
        self.EOF_flag = False

    def retrocesso(self):
        if not self.EOF_flag and self.linhaAtual > 0:
            self.linhaAtual -= 1

    def getNextChar(self):
        if self.linhaAtual >= self.bufsize:
            self.EOF_flag = True
            return None
        else:
            charAtual = self.lineBuf[self.linhaAtual]
            self.linhaAtual += 1
            return charAtual
        
    def isDigit(self, char):
        return char.isdigit()

    def getToken(self):
        state = self.Estados.estado_inicial
        lexema = ""

        while state != self.Estados.estado_final and not self.EOF_flag:
            token = self.getNextChar()

            if token is None:
                break

            match state:
                case self.Estados.estado_inicial:
                    if self.isDigit(token):
                        lexema += token
                        state = self.Estados.inNum
                    elif token == '-':
                        lexema+=token
                        state = self.Estados.inNegativo
                    else:
                        state = self.Estados.estado_inicial
                case self.Estados.inNegativo:
                    if self.isDigit(token):
                        lexema += token
                        state = self.Estados.inNum
                    else:
                        self.retrocesso()
                        state = self.Estados.estado_final
                case self.Estados.inNum:
                    if self.isDigit(token):
                        lexema += token
                    elif token == ",":
                        lexema += token
                        state = self.Estados.inVirgula
                    else:
                        state = self.Estados.estado_final
                        self.retrocesso()

                case self.Estados.inVirgula:
                    state = self.Estados.estado_inicial
                    if self.isDigit(token):
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
        print(afd.getToken())


main()

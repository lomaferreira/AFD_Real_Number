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
        token_chars=[]
 
        while state != self.Estados.estado_final and not self.EOF_flag:
            token = self.obterProximoCaracter()
            save=True

            if token is None:
                break

            match state:
                case self.Estados.estado_inicial:
                    if self.ehDigito(token):
                        state = self.Estados.inNum
                    elif token == '-':
                        state = self.Estados.inNegativo
                    else:
                        state = self.Estados.estado_inicial
                        save=False
                case self.Estados.inNegativo:
                    if self.ehDigito(token):
                        state = self.Estados.inNum
                    else:
                        self.retrocesso()
                        token_chars=[] #esvazia a lista se tiver um menos não seguido de um digito
                        state = self.Estados.estado_inicial
                        save=False
                case self.Estados.inNum:
                    if token == ",":
                        state = self.Estados.inVirgula
                    elif not self.ehDigito(token):
                        state = self.Estados.estado_final
                        self.retrocesso()
                        save=False

                case self.Estados.inVirgula:
                    if self.ehDigito(token):
                        state = self.Estados.inNum
                    else:
                        self.retrocesso()
                        state = self.Estados.estado_final
                        save=False
        
            if save:
                token_chars.append(token)
        # Junção dos caracteres
        if token_chars:
            lexema = ''.join(token_chars)
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

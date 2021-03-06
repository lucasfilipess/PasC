import sys

from ts import TS
from tag import Tag
from token import Token

class Lexer():
   def __init__(self, input_file):
      try:
         self.input_file = open(input_file, 'rb')
         self.lookahead = 0
         self.n_line = 1
         self.n_column = 1
         self.ts = TS()
      except IOError:
         print('Erro de abertura do arquivo. Encerrando.')
         sys.exit(0)

   def closeFile(self):
      try:
         self.input_file.close()
      except IOError:
         print('Erro ao fechar arquivo. Encerrando.')
         sys.exit(0)

   def sinalizaErroLexico(self, message):
      print("[Erro Lexico]: ", message, "\n");

   def retornaPonteiro(self):
      if(self.lookahead.decode('ascii') != ''):
         self.input_file.seek(self.input_file.tell()-1)

   def printTS(self):
      self.ts.printTS()

   def proxToken(self):
      # Implementa um AFD.
      estado = 1
      lexema = ""
      c = '\u0000'

      while(True):
         self.lookahead = self.input_file.read(1)
         c = self.lookahead.decode('ascii')

         if(c == '\t'):
            self.n_column += 3
         else:
            self.n_column +=1
         if(c == '\n'):
            self.n_line += 1
            self.n_column = 1

         if(estado == 1):
            if(c == ''):
               return Token(Tag.EOF, "EOF", self.n_line, self.n_column)
            elif(c == ' ' or c == '\r'):
               estado = 1
            elif(c == '\n'):
               estado = 1
            elif(c == '='):
               estado = 2
            elif(c == '!'):
               estado = 4
            elif(c == '<'):
               estado = 6
            elif(c == '>'):
               estado = 9
            elif(c == '/'):
               estado = 16
            elif(c == '.'):
               estado = 12
            elif(c == '*'):
               estado = 21
            elif(c == '-'):
               estado = 22
            elif(c == '+'):
               estado = 23
            elif(c == '{'):
               estado = 25
            elif(c == '}'):
               estado = 26
            elif(c == '('):
               estado = 27
            elif(c == ')'):
               estado = 28
            elif(c == ','):
               estado = 29
            elif(c == ';'):
               estado = 30
            elif(c == '"'):
               estado = 31
            elif(c.isdigit()):
               lexema += c
               estado = 12
            elif(c.isalpha()):
               lexema += c
               estado = 14
            else:
               self.sinalizaErroLexico("Tabela ASCII n??o possui o caracter [" + c + "], linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               return None
         elif(estado == 2):
            if(c == '='):
               return Token(Tag.OP_EQ, "==", self.n_line, self.n_column)
            else:
               return Token(Tag.OP_ATRIB, "=", self.n_line, self.n_column)
         elif(estado == 4):
            if(c == '='):
               return Token(Tag.OP_NE, "!=", self.n_line, self.n_column)

            self.sinalizaErroLexico("Ap??s ! insira = ou um espa??o!!a linha " +
            str(self.n_line) + " e coluna " + str(self.n_column))
            return None
         elif(estado == 6):
            if(c == '='):
               return Token(Tag.OP_LE, "<=", self.n_line, self.n_column)

            return Token(Tag.OP_LT, "<", self.n_line, self.n_column)
         elif(estado == 9):
            if(c == '='):
               return Token(Tag.OP_GE, ">=", self.n_line, self.n_column)

            return Token(Tag.OP_GT, ">", self.n_line, self.n_column)
         
         elif(estado == 35):
            if(c == '/'):
               estado = 1
            else:
               estado = 34
         
         elif(estado == 34):
            if(c == '*'):
               estado = 35
            if(c == ''):
               self.sinalizaErroLexico("?? necessario fechar o comentario! linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               return None

         elif(estado == 17):
            if(c == '\n'):
               estado = 1

         elif(estado == 16):
            if(c == '/'):
               estado = 17
            elif(c == '\n'):
               estado = 1
            elif(c == '*'):
               estado = 34
            else:
               return Token(Tag.OP_DIV, "/", self.n_line, self.n_column)

         elif(estado == 21):
            return Token(Tag.OP_MUL, "*", self.n_line, self.n_column)

         elif(estado == 22):
            return Token(Tag.OP_MIN, "-", self.n_line, self.n_column)
         
         elif(estado == 23):
            return Token(Tag.OP_AD, "+", self.n_line, self.n_column)
         
         elif(estado == 25):
            return Token(Tag.SMB_OBC, "{", self.n_line, self.n_column)

         elif(estado == 26):
            return Token(Tag.SMB_CBC, "}", self.n_line, self.n_column)

         elif(estado == 27):
            return Token(Tag.SMB_OPA, "(", self.n_line, self.n_column)
         
         elif(estado == 28):
            return Token(Tag.SMB_CPA, ")", self.n_line, self.n_column)
         
         elif(estado == 29):
            return Token(Tag.SMB_COM, ",", self.n_line, self.n_column)
         
         elif(estado == 30):
            return Token(Tag.SMB_SEM, ";", self.n_line, self.n_column)
         
         elif(estado == 32):
               if(c=='\n'):
                  self.sinalizaErroLexico("Verifique as aspas! Na linha " +
                  str(self.n_line) + " e coluna " + str(self.n_column))
                  return None
               elif (c == '"'):
                  return Token(Tag.CHAR_CONST, lexema, self.n_line, self.n_column)
               elif(c.isascii()):
                  lexema += c
               else:
                  self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
                  str(self.n_line) + " e coluna " + str(self.n_column))
                  return None

         elif(estado == 31):
               if(c=='\n'):
                  self.sinalizaErroLexico("oce possui aspas sem fechamento! Na linha " +
                  str(self.n_line) + " e coluna " + str(self.n_column))
                  return None
               elif(c.isascii()):
                  estado = 32
                  lexema += c
               else:
                  self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
                  str(self.n_line) + " e coluna " + str(self.n_column))
                  return None
            
         elif(estado == 19):
            if(c.isdigit()):
               lexema += c  
            elif(c == '\n'):
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               return None
            else:
               return Token(Tag.NUM_CONST, lexema, self.n_line, self.n_column)
         
         elif(estado == 12):
            if(c.isdigit()):
               lexema += c 
            elif(c == '.'):
               estado = 19    
               lexema += c 
            else:
               return Token(Tag.NUM_CONST, lexema, self.n_line, self.n_column)

         elif(estado == 14):
            if(c.isalnum()):
               lexema += c
            else:

               self.n_column -= 1
               self.retornaPonteiro()

               estado = 1
               token = self.ts.getToken(lexema)
               if(token is None):
                  token = Token(Tag.ID, lexema, self.n_line, self.n_column)
                  self.ts.addToken(lexema, token)
                  return token
               
               token.setLinha(self.n_line)
               token.setColuna(self.n_column)
               lexema = ""
               return token
              
               


         # fim if's de estados
      # fim while

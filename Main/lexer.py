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
      isNumConst =  False
      isCharConst = ""
      estado = 1
      lexema = ""
      c = '\u0000'

      while(True):
         self.lookahead = self.input_file.read(1)
         c = self.lookahead.decode('ascii')

         if(estado == 1):
            if(c == ''):
               return Token(Tag.EOF, "EOF", self.n_line, self.n_column)
            elif(c == ' ' or c == '\t' or c == '\n' or c == '\r'):
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
               estado = 14
            elif(c.isdigit()):
               lexema += c
               estado = 12
            elif(c.isalpha()):
               lexema += c
               estado = 14
            elif(c == '/'):
               estado = 16
            else:
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               return None
         elif(estado == 2):
            if(c == '='):
               return Token(Tag.OP_EQ, "==", self.n_line, self.n_column)
            elif(c == ' '):
               return Token(Tag.OP_ATRIB, "=", self.n_line, self.n_column)
            else:   
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
            return None
         elif(estado == 4):
            if(c == '='):
               return Token(Tag.OP_NE, "!=", self.n_line, self.n_column)

            self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
            str(self.n_line) + " e coluna " + str(self.n_column))
            return None
         elif(estado == 6):
            if(c == '='):
               return Token(Tag.OP_LE, "<=", self.n_line, self.n_column)

            self.retornaPonteiro()
            return Token(Tag.OP_LT, "<", self.n_line, self.n_column)
         elif(estado == 9):
            if(c == '='):
               return Token(Tag.OP_GE, ">=", self.n_line, self.n_column)

            self.retornaPonteiro()
            return Token(Tag.OP_GT, ">", self.n_line, self.n_column)

         elif(estado == 16):
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
         
         elif(estado == 31):
            isCharConst = True

         elif(estado == 12):
            if(c.isdigit()):
               lexema += c 
            elif(c == '.'):
              isNumConst = True
              lexema += c 
            else:
               self.retornaPonteiro()
               if(isNumConst):
                  isNumConst = False
                  return Token(Tag.NUM_CONST, lexema, self.n_line, self.n_column)
               else:
                  return Token(Tag.DIGIT, lexema, self.n_line, self.n_column)

         elif(estado == 14):
            if(c.isalnum()):
               lexema += c
            else:
               self.retornaPonteiro()
               token = self.ts.getToken(lexema)
               if(token is None):
                  token = Token(Tag.ID, lexema, self.n_line, self.n_column)
                  self.ts.addToken(lexema, token)

               return token

         # fim if's de estados
      # fim while

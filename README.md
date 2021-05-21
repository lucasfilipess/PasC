Centro Universitário de Belo Horizonte – Uni-BH
Curso: Ciência da Computação
Unidade Curricular: Teoria da Computação e Compiladores
Professores: Gustavo A. Fernandes / Samara Leal

---

Trabalho Prático I – Análise Léxica e Tabela de Símbolos
Descrição do trabalho
Nesta etapa, você deverá implementar um Analisador Léxico para a linguagem PasC cuja descrição
encontra-se nas páginas 3 e 4.
Seu analisador léxico deverá ser implementado conforme visto em sala de aula, com o auxílio de
um Autômato Finito Determinístico. Ele deverá reconhecer cada lexema e retornar o token de
acordo com o lexema encontrado.
Para facilitar a implementação, uma Tabela de Símbolos (TS) deverá ser usada. Essa tabela conterá,
inicialmente, todas as palavras reservadas da linguagem. À medida que novos tokens
Identificadores)forem sendo reconhecidos, esses deverão ser consultados na TS antes de serem
cadastrados como ID. Somente palavras reservadas e identificadores serão cadastrados na TS.
Não é permitido o cadastro de um mesmo token mais de uma vez na TS.
Seu Analisador Léxico deverá imprimir a lista de todos os tokens reconhecidos, assim como
imprimir o que está cadastrado na Tabela de Símbolos, de qualquer programa escrito em PasC.
Na impressão dos tokens, deverá aparecer a tupla <nome_do_token, lexema> assim como a linha e
a coluna de cada token.
Além de reconhecer os tokens da linguagem, seu analisador léxico deverá detectar possíveis erros e
reportá-los ao usuário. O programa deverá informar o erro e o local onde ocorreu (linha e coluna).
Os erros verificados serão: i) caracteres desconhecidos (não esperados em um padrão ou inválidos),
ii) string não fechada antes de quebra de linha e iii) string não-fechada antes do fim de arquivo. Se o
analisador léxico encontrar mais do que um erro léxico, o processo de compilação deve ser
interrompido.
Espaços em branco, tabulações, quebras de linhas e comentários não são tokens, ou seja, devem ser
descartados/ignorados pelo referido analisador.
Pontos extras (3 pontos):
É possível implementar um processo de recuperação de erro, para que o analisador léxico possa
verificar a maior quantidade de código possível. Para isso o Modo Pânico deverá ser implementado
na recuperação de erros, conforme visto em sala de aula. Porém, se o número de erros léxicos
ultrapassar o limite de 3 erros, o programa deverá abortar a análise.Cronograma e Valor
O trabalho vale 30 pontos no total. Ele deverá ser entregue por etapas, pelo ulife, sendo a primeira
etapa correspondendo ao Analisador Léxico, conforme consta na tabela abaixo.
Etapa Data de entrega Valor
Analisador Léxico e Tabela de Símbolos 16/05/2021 10 pontos
Analisador Sintático A definir 10 pontos
Analisador Semântico A definir 10 pontos
O que entregar?
Você deverá entregar nesta etapa: Todos os arquivos fonte. Para avaliar a correção, o programa
deverá exibir os tokens reconhecidos e o local de sua ocorrência (linha e coluna), os tokens
armazenados na tabela de símbolos, bem como os erros léxicos, se acontecerem. O professor irá
usar programas escritos em PasC para validar o Lexer.
Regras:
• O trabalho deverá ser realizado individualmente, em dupla, ou em trio.
• Não é permitido o uso de ferramentas para geração do analisador léxico.
• A implementação deverá ser realizada, somente, em uma das linguagens: C, C++, C# (irão
apresentar para o professor), Java, Ruby, Python ou JavaScript (via Nodejs).
• Trabalhos total ou parcialmente iguais receberão avaliação nula. Cuidado com o
compartilhamento de código!
Se o analisador léxico não compilar ou apresentar erros de execução durante a fase de
testes realizada pelo professor, a avaliação será nula. O professor espera, no mínimo, um
compilador que execute, caso contrário não é possível avaliar.
Após a data definida para entrega, nenhum trabalho será recebido.
•
•
Em anexo (pasta: lexer_exemplo) segue um exemplo de uma Gramática, AFD, programas de
exemplo, e a saída dos Tokens. ATENÇÂO: a gramática do exemplo não tem relação com a
gramática do PasC.Gramática da linguagem PasC
prog
body
decl-list
decl
type
id-list → “program” “id” body “EOF”
→ decl-list “{“ stmt-list “}”
→ decl “;” decl-list | ε
→ type id-list
→ “num” | “char”
→ “id” | “id” “,” id-list
stmt-list
stmt
assign-stmt
if-stmt while-stmt
stmt-prefix
read-stmt
write-stmt → stmt “;” stmt-list | ε
→ assign-stmt | if-stmt | while-stmt | read-stmt | write-stmt
→ “id” “=” simple_expr
→ “if” “(“ expression “)” “{“ stmt-list “}” |
“if” “(“ expression “)” “{“ stmt-list “}” “else” “{“ stmt-list “}”
→ stmt-prefix “{“ stmt-list “}”
→ “while” “(“ expression “)”
→ “read” “id”
→ “write” simple-expr
expression
simple-expr
term
factor-a
factor → simple-expr | simple-expr logop simple-expr | simple-expr relop simple-expr
→ term | simple-expr addop term
→ factor-a | term mulop factor-a
→ factor | “not” factor
→ “id” | constant | “(“ expression “)”
logop
relop
addop
mulop
constant → “or” | “and”
→ “==” | “>” | “>=” | “<” | “<=” | “!=”
→ “+” | “-”
→ “_” | “/”
→ “num_const” | “char_const”
Padrões para números, caracteres, strings e identificadores do PasC
digit = [0-9]
letter
id
char_const = [A-Z | a-z]
= letter (letter | digit) _
= pelo menos um dos 256 caracteres do conjunto ASCII entre aspas duplas
num_const = digit + (“.” digit + )?Nomes para os tokens:
Operadores:
OP_EQ: ==
OP_NE: !=
OP_GT: >
OP_LT: <
Símbolos:
SMB_OBC: {
SMB_CBC: }
SMB_OPA: (
SMB_CPA: )
OP_GE: >=
OP_LE: <=
OP_AD: +
OP_MIN: -
OP_MUL: _
OP_DIV: /
OP_ATRIB: =
SMB_COM: ,
SMB_SEM: ;
Palavras-chave: KW: program, if, else, while, write, read, num, char, not, or, and
Identificadores: ID
Literal: LIT
Constantes: NUM_CONST: num_const e CHAR_CONST: char_const
Outras características de PasC
•
•
•
•
•
•
•
•
•
•
•
As palavras-chave de PasC são reservadas;
Toda variável deve ser declarada antes do seu uso (Análise Semântica);
As aspas não são tokens;
A linguagem possui comentários de mais de uma linha. Um comentário começa com “/_” e
deve terminar com “\*/”;
A linguagem possui comentários de uma linha. Um comentário começa com “//”;
A semântica das expressões é a tradicional do C;
Os tipos numeral e caractere não são compatíveis (Análise Semântica);
A linguagem não é case-sensitive;
Cada tabulação, deverá contar como 3 espaços em branco;
EOF é o código de fim de arquivo e, portanto, deve ser um token.

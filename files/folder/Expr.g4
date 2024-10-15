grammar Expr;

prog: (statement)+;

type : 'int' | 'float' | 'string' | 'bool';                                     
variable: ID                                                                         #id
        ;
literal: INT                                                                         #int
        | FLOAT                                                                      #float
        | STRING                                                                     #string            
        | BOOL                                                                       #bool
        ;

statement:
        SEMICOLON                                                                               #empty
        | type variable (',' variable)* SEMICOLON                                               #declaration
        | expression SEMICOLON                                                                  #expr
        | 'read' variable (',' variable)* SEMICOLON                                             #read
        | 'write' expression (',' expression )* SEMICOLON                                       #write
        | '{' statement* '}'                                                                    #block                              
        | 'if' '(' expression ')' statement ('else' statement)?                                 #if
        | 'while' '(' expression ')' (statement)                                                #while
        | 'for' '(' expression SEMICOLON expression SEMICOLON expression ')' (statement)        #for
        ;


expression:     
        literal                                                 #lit                                         
        | variable                                              #var                                       
        | expression AND expression                             #and
        | expression OR expression                              #or
        | expression op=(EQUAL | NOTEQUAL) expression           #equalnotequal
        | expression op=(LESSTHAN | GREATERTHAN) expression     #compare
        | expression op=(MULT | DIV | MOD) expression           #mulDiv
        | expression op=(PLUS | MINUS | '.') expression         #addSub
        | variable '=' expression                               #assignment
        | NOT expression                                        #not
        | '(' expression ')'                                    #parenthesis
        | MINUS expression                                      #unaryminus
        | expression '?' expression ':' expression              #ternary
        ;




MOD : '%';
PLUS: '+';
MINUS: '-';
MULT: '*';
DIV: '/';
EQUAL: '==';
NOTEQUAL: '!=';
LESSTHAN: '<';
GREATERTHAN: '>';
AND: '&&';
OR: '||';
NOT: '!';

SEMICOLON: ';';
COMMA: ',';

ID: [a-zA-Z] [a-zA-Z0-9]*;
INT: [0-9]+;
FLOAT: [0-9]+ '.' [0-9]+;
STRING: '"' ~'"'* '"';
BOOL: 'true' | 'false';
WS: [ \t\n\r]+ -> skip;
COMMENT: '//' ~[\r\n]* -> skip;



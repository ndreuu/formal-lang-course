grammar GraphQueryLanguage;

prog : (EOL? WS? stmt SEMI EOL?)+ EOF;

stmt : PRINT expr
     | var WS? ASSIGN WS? expr
     ;

expr : LP expr RP
     | anfunc
     | mapping
     | filtering
     | var
     | val
     | NOT expr
     | expr KLEENE
     | expr IN expr
     | expr AND expr
     | expr DOT expr
     | expr OR expr
     ;

graph : load_graph
      | cfg
      | set_start
      | set_final
      | add_start
      | add_final
      | LP graph RP
      ;

cfg : CFG ;

load_graph : LOAD (path | string);
set_start : SET START OF (graph | var) TO (vertices | var) ;
set_final : SET FINAL OF (graph | var) TO (vertices | var) ;
add_start : ADD START OF (graph | var) TO (vertices | var) ;
add_final : ADD FINAL OF (graph | var) TO (vertices | var) ;

vertices : vertex
       | vertices_range
       | vertices_set
       | select_reachable
       | select_final
       | select_start
       | select_vertices
       | LP vertices RP
       ;


vertex : INT ;

edges : edge
      | edges_set
      | select_edges ;

edge : LP vertex COMMA label COMMA vertex RP
     | LP vertex COMMA vertex RP ;

labels : label
       | labels_set
       | select_labels ;

label : string ;

anfunc : FUN variables COLON expr
       | LP anfunc RP ;

mapping : MAP anfunc expr;
filtering : FILTER anfunc expr;

select_edges : SELECT EDGES FROM (graph | var) ;
select_labels : SELECT LABELS FROM (graph | var) ;
select_reachable : SELECT REACHABLE VERTICES FROM (graph | var) ;
select_final : SELECT FINAL VERTICES FROM (graph | var) ;
select_start : SELECT START VERTICES FROM (graph | var) ;
select_vertices : SELECT VERTICES FROM (graph | var) ;
vertices_range : LCB INT DOT DOT INT RCB ;

string : STRING ;
path : PATH ;

vertices_set : LCB (INT COMMA)* (INT)? RCB
             | vertices_range ;

labels_set : LCB (STRING COMMA)* (STRING)? RCB ;

edges_set : LCB (edge COMMA)* (edge)? RCB ;
var : VAR ;

var_edge : LP var COMMA var RP
         | LP var COMMA var COMMA var RP
         | LP LP var COMMA var RP COMMA var COMMA LP var COMMA var RP RP
         ;

variables : (var COMMA)* var?
     | var_edge
     ;

val : boolean
    | graph
    | edges
    | labels
    | vertices
    ;


boolean : TRUE | FALSE;

ASSIGN : WS? '=' WS? ;
AND : WS? '&' WS?;
OR : WS? '|' WS? ;
NOT : WS? 'not' WS? ;
IN : WS? 'in' WS?;
KLEENE : WS? '*' WS?;
DOT : WS? '.' WS? ;
COMMA : WS? ',' WS?;
SEMI : ';' WS?;
LCB : WS? '{' WS?;
RCB : WS? '}' WS?;
LP : WS? '(' WS?;
RP : WS? ')' WS?;

QUOT : '"' ;
TRIPLE_QUOT : '"""' ;
COLON : WS? ':' WS?;
ARROW : '->' ;
CFG : TRIPLE_QUOT (CHAR | DIGIT | ' ' | '\n' | ARROW)* TRIPLE_QUOT ;

FUN : WS? 'fun' WS?;
LOAD : WS? 'load' WS? ;
SET : WS? 'set' WS? ;
ADD : WS? 'add' WS? ;
OF : WS? 'of' WS? ;
TO : WS? 'to' WS? ;
VERTICES : WS? 'vertices' WS? ;
LABELS : WS? 'labels' WS? ;
SELECT : WS? 'select' WS? ;
EDGES : WS? 'edges' WS? ;
REACHABLE : WS? 'reachable' WS? ;
START : WS? 'start' WS? ;
FINAL : WS? 'final' WS? ;
FROM : WS? 'from' WS? ;
FILTER : WS? 'filter' WS? ;
MAP : WS? 'map' WS? ;
PRINT : WS? 'print' WS?;
TRUE : 'true' ;
FALSE : 'false' ;

VAR : ('_' | CHAR) ID_CHAR* ;

INT : NONZERO_DIGIT DIGIT* | '0' ;
STRING : QUOT (CHAR | DIGIT | '_' | ' ')* QUOT ;
PATH : QUOT (CHAR | DIGIT | '_' | ' ' | '/' | '\\' | ':' | DOT)* QUOT ;
ID_CHAR : (CHAR | DIGIT | '_');
CHAR : [a-z] | [A-Z];
NONZERO_DIGIT : [1-9];
DIGIT : [0-9];
WS : [ \t\r]+ -> skip;
EOL : [\n]+;

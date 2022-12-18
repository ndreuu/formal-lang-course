## Описание языка запросов

```
prog = List<stmt>

stmt =
    bind of var * expr
  | print of expr

val =
    String of string
  | Int of int
  | Bool of bool
  | Graph of graph
  | Labels of labels
  | Vertices of vertices
  | Edges of edges

expr =
    Var of var                   // переменные
  | Val of val                   // константы
  | Set_start of Set<val> * expr // задать множество стартовых состояний
  | Set_final of Set<val> * expr // задать множество финальных состояний
  | Add_start of Set<val> * expr // добавить состояния в множество стартовых
  | Add_final of Set<val> * expr // добавить состояния в множество финальных
  | Get_start of expr            // получить множество стартовых состояний
  | Get_final of expr            // получить множество финальных состояний
  | Get_reachable of expr        // получить все пары достижимых вершин
  | Get_vertices of expr         // получить все вершины
  | Get_edges of expr            // получить все рёбра
  | Get_labels of expr           // получить все метки
  | Map of lambda * expr         // классический map
  | Filter of lambda * expr      // классический filter
  | Load of path                 // загрузка графа
  | Intersect of expr * expr     // пересечение языков
  | Concat of expr * expr        // конкатенация языков
  | Union of expr * expr         // объединение языков
  | Star of expr                 // замыкание языков (звезда Клини)
  | Smb of expr                  // единичный переход

lambda =
    Lambda of List<var> * expr

```
## Описание конкретного синтаксиса языка
```
prog -> (stmt SEMI EOL?)+

stmt -> PRINT expr
      | var ASSIGN expr

expr -> LP expr RP
      | anfunc
      | mapping
      | filtering
      | var
      | val
      | NOT expr
      | expr IN expr
      | expr AND expr
      | expr DOT expr
      | expr OR expr
      | expr KLEENE

graph -> load_graph
       | cfg
       | string
       | set_start
       | set_final
       | add_start
       | add_final
       | LP graph RP

load_graph -> LOAD path
set_start -> SET START OF (graph | var) TO (vertices | var)
set_final -> SET FINAL OF (graph | var) TO (vertices | var)
add_start -> ADD START OF (graph | var) TO (vertices | var)
add_final -> ADD FINAL OF (graph | var) TO (vertices | var)

vertices -> vertex
          | vertices_range
          | vertices_set
          | select_reachable
          | select_final
          | select_start
          | select_vertices
          | LP vertices RP
vertex -> INT

edges -> edge
       | edges_set
       | select_edges
edge -> LP vertex COMMA label COMMA vertex RP
      | LP vertex COMMA vertex RP

labels -> label
        | labels_set
        | select_labels
label -> string

anfunc -> FUN variables COLON expr
        | LP anfunc RP
mapping -> MAP anfunc expr
filtering -> FILTER anfunc expr
select_edges -> SELECT EDGES FROM (graph | var)
select_labels -> SELECT LABELS FROM (graph | var)
select_reachable -> SELECT REACHABLE VERTICES FROM (graph | var)
select_final -> SELECT FINAL VERTICES FROM (graph | var)
select_start -> SELECT START VERTICES FROM (graph | var)
select_vertices -> SELECT VERTICES FROM (graph | var)

vertices_range -> LCB INT DOT DOT INT RCB
cfg -> CFG
string -> STRING
path -> PATH

vertices_set -> LCB (INT COMMA)* (INT)? RCB
              | vertices_range
labels_set -> LCB (STRING COMMA)* (STRING)? RCB
edges_set -> LCB (edge COMMA)* (edge)? RCB

var -> VAR
var_edge -> LP var COMMA var RP
          | LP var COMMA var COMMA var RP
          | LP LP var COMMA var RP COMMA var COMMA LP var COMMA var RP RP
variables -> (var COMMA)* var? | var_edge

val -> boolean
     | graph
     | edges
     | labels
     | vertices

boolean -> BOOL

ASSIGN -> '='
AND -> '&'
OR -> '|'
NOT -> 'not'
IN -> 'in'
KLEENE -> '*'
DOT -> '.'
COMMA -> ','
SEMI -> ';'
LCB -> '{'
RCB -> '}'
LP -> '('
RP -> ')'
QUOT -> '"'
TRIPLE_QUOT -> '"""'
COLON -> ':'
ARROW -> '->'

FUN -> 'fun'
LOAD -> 'load'
SET -> 'set'
ADD -> 'add'
OF -> 'of'
TO -> 'to'
VERTICES -> 'vertices'
LABELS -> 'labels'
SELECT -> 'select'
EDGES -> 'edges'
REACHABLE -> 'reachable'
START -> 'start'
FINAL -> 'final'
FROM -> 'from'
FILTER -> 'filter'
MAP -> 'map'
PRINT -> 'print'
BOOL -> TRUE | FALSE
TRUE -> 'true'
FALSE -> 'false'


VAR -> ('_' | CHAR) ID_CHAR*
INT -> NONZERO_DIGIT DIGIT* | '0'
CFG -> TRIPLE_QUOT (CHAR | DIGIT | ' ' | '\n' | ARROW)* TRIPLE_QUOT
STRING -> QUOT (CHAR | DIGIT | '_' | ' ')* QUOT
PATH -> QUOT (CHAR | DIGIT | '_' | ' ' | '.' | '\' | '/')* QUOT
ID_CHAR -> (CHAR | DIGIT | '_')
CHAR -> [a-z] | [A-Z]
NONZERO_DIGIT -> [1-9]
DIGIT -> [0-9]


WS -> [ \t\r]+
EOL -> [\n]+

```


## Пример программы

Данный скрипт загружает граф "graph", задает стартовые и финальные вершины, создает запрос, выполняет пересечение и печатает результат.

```
g = load "graph";
h = set start of (set final of g to (select vertices from g)) to {1..100};
l = "l1" | "l2";
query = ("word" | l)*;
res = g & query;
print res;
```

## Правила вывода типов

Константы типизируются очевидным образом.

Тип переменной определяется типом выражения, с которым она связана.
```
[b(v)] => t
_________________
[Var (v)](b) => t
```

Загрузить можно только автомат.
```
_________________________
[Load (p)](b) => FA<int>
```

Установка финальных состояний, а так же добавление стартовых и финальных типизируется аналогично типизации установки стартовых, которая приведена ниже.
```
[s](b) => Set<t> ;  [e](b) => FA<t>
___________________________________
[Set_start (s, e)](b) => FA<t>


[s](b) => Set<t> ;  [e](b) => RSM<t>
____________________________________
[Set_start (s, e)](b) => RSM<t>

```

Получение финальных типизируется аналогично получению стартовых, правила для которого приведены ниже.
```
[e](b) => FA<t>
____________________________
[Get_start (e)](b) => Set<t>


[e](b) => RSM<t>
____________________________
[Get_start (e)](b) => Set<t>

```

```
[e](b) => FA<t>
__________________________________
[Get_reachable (e)](b) => Set<t*t>


[e](b) => RSM<t>
__________________________________
[Get_reachable (e)](b) => Set<t*t>

```

```
[e](b) => FA<t>
_______________________________
[Get_vertices (e)](b) => Set<t>


[e](b) => RSM<t>
_______________________________
[Get_vertices (e)](b) => Set<t>


[e](b) => FA<t>
______________________________________
[Get_edges (e)](b) => Set<t*string*t>


[e](b) => RSM<t>
______________________________________
[Get_edges (e)](b) => Set<t*string*t>

[e](b) => FA<t>
__________________________________
[Get_labels (e)](b) => Set<string>


[e](b) => RSM<t>
__________________________________
[Get_labels (e)](b) => Set<string>

```

Правила для ```map``` и ```filter``` традиционные.
```
[f](b) => t1 -> t2 ; [q](b) => Set<t1>
_______________________________________
[Map (f,q)](b) => Set<t2>


[f](b) => t1 -> bool ; [q](b) => Set<t1>
________________________________________
[Filter (f,q)](b) => Set<t1>
```

Пересечение для двух КС не определено.
```
[e1](b) => FA<t1> ;  [e2](b) => FA<t2>
______________________________________
[Intersect (e1, e2)](b) => FA<t1*t2>


[e1](b) => FA<t1> ;  [e2](b) => RSM<t2>
_______________________________________
[Intersect (e1, e2)](b) => RSM<t1*t2>


[e1](b) => RSM<t1> ;  [e2](b) => FA<t2>
_______________________________________
[Intersect (e1, e2)](b) => RSM<t1*t2>

```

Остальные операции над автоматами типизируются согласно формальных свойств классов языков.
```
[e1](b) => FA<t> ;  [e2](b) => FA<t>
_____________________________________
[Concat (e1, e2)](b) => FA<t>


[e1](b) => FA<t> ;  [e2](b) => RSM<t>
______________________________________
[Concat (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => FA<t>
______________________________________
[Concat (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => RSM<t>
______________________________________
[Concat (e1, e2)](b) => RSM<t>

```

```
[e1](b) => FA<t> ;  [e2](b) => FA<t>
______________________________________
[Union (e1, e2)](b) => FA<t>


[e1](b) => FA<t> ;  [e2](b) => RSM<t>
_______________________________________
[Union (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => FA<t>
_______________________________________
[Union (e1, e2)](b) => RSM<t>


[e1](b) => RSM<t> ;  [e2](b) => RSM<t>
_______________________________________
[Union (e1, e2)](b) => RSM<t>

```

```
[e](b) => FA<t>
______________________
[Star (e)](b) => FA<t>


[e](b) => RSM<t>
______________________
[Star (e)](b) => RSM<t>

```

```
[e](b) => string
________________________
[Smb (e)](b) => FA<int>

```


## Динамическая семантика языка запросов

Связывание переопределяет имя.

```
[e](b1) => x,b2
_____________________________________
[Bind (v, e)](b1) => (), (b1(v) <= x)

```

Загрузить можно только автомат и у него все вершины будут стартовыми и финальными.

```
[p](b1) => s,b2 ; read_fa_from_file s => fa
_____________________________________
[Load (p)](b1) => (fa | fa.start = fa.vertices, fa.final = fa.vertices), b1

```

# Спецификация интерпретатора

## Типизация
Типизация строгая динамическая
## Типы данных

| Type | Ops                                                |
|------|----------------------------------------------------|
| Bool | and ~ '&'<br> not ~ 'not' <br>or ~ '&#124;'  |
| Set  | intersection ~ '&'<br>is entry ~ 'in'<br>union ~ '&#124;'    |
| FA   | intersection with FA/CFG ~ '&'<br>union with FA~ '&#124;' |
| CFG  | intersection with FA ~ '&'<br>union with CFG~ '&#124;'    |
## Используемые алгоритмы
- Для выполнения теоретико-множественных операций над языками используются комбинации средств библиотеки pyformlang
- Для вычисления достижимых вершин используется класс булевых матриц, реализованный в прошлых заданиях


## Пример работы интерпретатора
`regex_intersection_or.gql`
```
regex_first = "l1" . "l2"*;
regex_second = "l1" | "l2"* | "l3";
intersection = regex_first & regex_second;
print regex_first | regex_second;
```
Запуск интерпретатора:
`python -m project.graph_query_language /tests/test_task15/example.gql`
```
(($.(("l1"|"l2").("l2")*))|($|($."l3")))
```

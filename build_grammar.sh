#!/bin/sh
cd project/graph_query_language
antlr4 -Dlanguage=Python3 -visitor GraphQueryLanguage.g4 -o generated

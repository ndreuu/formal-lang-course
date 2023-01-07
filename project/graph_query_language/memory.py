from typing import List, Dict

from project.graph_query_language.gql_exceptions import VariableNotFoundException
from project.graph_query_language.types.gql_type import GQLType


class Memory:
    def __init__(self):
        self.tables: List[Dict[str:GQLType]] = [{}]

    def new_scope(self):
        new_mem = Memory()
        new_mem.tables = self.tables.copy()
        new_mem.tables.append({})
        return new_mem

    def remove_last_scope(self):
        new_mem = Memory()
        new_mem.tables = self.tables.copy()
        new_mem.tables = new_mem.tables[:-1]
        return new_mem

    def add_variable(self, name: str, value: GQLType, level: int = -1):
        if level >= len(self.tables):
            for _ in range(level - len(self.tables) + 1):
                self.tables.append({})

        self.tables[level][name] = value

    def find_variable(self, name: str):
        scope_level = len(self.tables) - 1
        while scope_level >= 0:
            value = self.tables[scope_level].get(name)
            if value is not None:
                return value
            scope_level -= 1
        raise VariableNotFoundException(name=name)

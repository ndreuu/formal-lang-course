class RunTimeException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class NotImplementedException(RunTimeException):
    def __init__(self, instruction):
        self.msg = f"{instruction} is not implemented"


class LoadGraphException(RunTimeException):
    def __init__(self, name: str):
        self.msg = f"Wrong graph name/path ('{name}')"


class InvalidCastException(RunTimeException):
    def __init__(self, lhs: str, rhs: str):
        self.msg = f"Invalid cast for '{lhs}' and '{rhs}'"


class VariableNotFoundException(RunTimeException):
    def __init__(self, name: str):
        self.msg = f"Variable name '{name}' is not defined"


class GQLTypeError(RunTimeException):
    pass


class InvalidScriptPath(RunTimeException):
    def __init__(self, filename: str):
        self.msg = f"Could not open file {filename}"


class InvalidScriptExtension(RunTimeException):
    def __init__(self):
        self.msg = f"Expected 'gql' extension"

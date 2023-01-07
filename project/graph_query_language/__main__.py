import sys

from project.graph_query_language.gql_exceptions import RunTimeException
from project.graph_query_language.interpreter import interpreter


def main(*argv):
    try:
        interpreter(*argv)
    except RunTimeException as e:
        sys.stdout.write(f"Error: {e.msg}\n")
        exit(1)
    exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])

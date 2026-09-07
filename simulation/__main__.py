import re
from parser import Parser


def main() -> None:
    try:
        parser: Parser = Parser()
        print(parser.validate_map())
    except Exception as e:
        print(f"An error occured: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

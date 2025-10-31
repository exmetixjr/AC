# main.py - Starter template
# Created by GitHub Copilot Chat Assistant for exmetixjr/AC

def greet(name: str) -> str:
    """Return a simple greeting for the given name.

    Args:
        name: Person's name.

    Returns:
        A greeting string.
    """
    return f"Hello, {name}!"


def main() -> None:
    """Entry point: read a name from input and print a greeting.
    If no input is provided, use 'World'.
    """
    try:
        name = input("Enter your name (or press Enter for 'World'): ").strip()
    except EOFError:
        name = """"
    if not name:
        name = "World"
    print(greet(name))

if __name__ == "__main__":
    main()

from auth import login
from utils import add


def main():
    print("Welcome to Codebase Copilot")

    result = add(10, 20)
    print("Result:", result)

    login("admin", "1234")


if __name__ == "__main__":
    main()
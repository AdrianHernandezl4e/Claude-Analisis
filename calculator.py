# Basic Calculator in Python
# File: calculator.py

def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return the difference of a and b."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return the quotient of a divided by b. Raises ValueError on division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def main():
    """Interactive command-line loop for basic calculator operations."""
    operations = {
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide
    }

    print("Basic Python Calculator")
    print("Type 'exit' to quit.")

    while True:
        expr = input("Enter calculation (e.g. 2 + 3): ")
        if expr.lower() in ('exit', 'quit'):
            print("Goodbye!")
            break

        try:
            parts = expr.split()
            if len(parts) != 3:
                raise ValueError("Invalid format. Use: number operator number.")

            a_str, op, b_str = parts
            a = float(a_str)
            b = float(b_str)

            if op not in operations:
                raise ValueError(f"Unsupported operator '{op}'. Use +, -, *, /")

            result = operations[op](a, b)
            print(f"Result: {result}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()

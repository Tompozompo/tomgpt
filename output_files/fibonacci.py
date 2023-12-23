# Python program to generate Fibonacci sequence up to n

def fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        next_value = fib_sequence[-1] + fib_sequence[-2]
        fib_sequence.append(next_value)
    return fib_sequence

# Generate first 20 Fibonacci numbers
first_20_fib = fibonacci(20)
print(first_20_fib)
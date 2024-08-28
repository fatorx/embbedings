
def maior_fibonacci_abaixo_de(limite):
  """
  Determina o maior número de Fibonacci abaixo de um limite dado.

  Args:
      limite: O limite superior para o número de Fibonacci.

  Returns:
      O maior número de Fibonacci menor que o limite.
  """

  a, b = 0, 1
  while b < limite:
    a, b = b, a + b
  return a

# Encontra o maior número de Fibonacci abaixo de 1000
maior_fibonacci = maior_fibonacci_abaixo_de(1000)

print("O maior número de Fibonacci abaixo de 1000 é:", maior_fibonacci)

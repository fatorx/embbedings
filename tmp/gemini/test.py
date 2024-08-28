
def calcular_area_triangulo(base, altura):
  """Calcula a área de um triângulo.

  Args:
    base: A base do triângulo.
    altura: A altura do triângulo.

  Returns:
    A área do triângulo.
  """

  area = (base * altura) / 2
  return area

# Exemplo de uso
base = 5
altura = 10
area = calcular_area_triangulo(base, altura)
print(f"A área do triângulo é: {area}")

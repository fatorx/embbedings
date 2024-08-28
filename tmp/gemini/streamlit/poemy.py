# Importa a biblioteca "random" para gerar números aleatórios
import random

# Define uma lista de palavras para usar no poema
palavras = ["Sonho", "Esperança", "Dor", "Amor", "Luz", "Sombra", "Tempo", "Eternamente", "Infinito", "Caminho", "Destino", "Coração", "Alma"]

# Define uma lista de frases para usar no poema
frases = ["Um fio tênue que nos conecta ao universo.", "Um enigma que desvendamos a cada instante.", "Um rio que flui incessantemente.", "Um ciclo de nascer, crescer, morrer e renascer.", "Um presente que se esvai, mas nos deixa marcas."]

# Função para gerar um verso aleatório
def gerar_verso():
  """Gera um verso aleatório usando palavras e frases da lista."""
  return f"{random.choice(palavras)} {random.choice(frases)}"

# Função para gerar um poema
def gerar_poema(num_versos):
  """Gera um poema com o número de versos especificado."""
  poema = ""
  for i in range(num_versos):
    poema += gerar_verso() + "\n"
  return poema

# Gera um poema com 5 versos
poema = gerar_poema(5)

# Imprime o poema
print(poema)
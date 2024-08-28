import os
import google.generativeai as genai

class GeminiTranslator:
    def __init__(self, api_key=None):
        """
        Inicializa a classe GeminiTranslator.

        Args:
            api_key (str, optional): A chave de API do Gemini. 
                                     Se não for fornecida, será obtida da variável de ambiente GEMINI_API_KEY.
        """

        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)

        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.generation_config,
            system_instruction="Se a frase ou pergunta informada pelo usuário for em português, traduza para o Inglês",
        )

        self.chat_session = self.model.start_chat() 

    def translate_message(self, message):
        response = self.chat_session.send_message(message)
        return response.text

# Exemplo de uso
translator = GeminiTranslator()
translated_message = translator.translate_message("O que fazem em caso de incêndio em um prédio de grande porte?")
print(translated_message)

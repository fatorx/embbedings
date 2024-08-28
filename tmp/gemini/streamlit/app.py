import streamlit as st
import os

import google.generativeai as genai
from google.generativeai import GenerationConfig


# Configurar a API Key (substitua pela sua chave real quando disponível)
genai.configure(api_key='AIzaSyDyx92jDM-Et5kk4B4W0dyzes_pN3JmM4o')

api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
gen_config = GenerationConfig(**generation_config)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=gen_config,
    system_instruction="""
            Create code in Python with instructions and comments. The output must be only the code, but 
            if the script needs other files, they must be created as well, separating the files with ####
        """
)

chat_session = model.start_chat()

# Inicializar o histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []


def get_chatbot_response(prompt):
    # Enviar o prompt para a API
    print(f"Enviando prompt: {prompt}")  # Log para depuração
    response = chat_session.send_message(prompt)

    # Log do objeto de resposta completo
    print(f"Resposta completa:")
    print(response.text)

    # Verificar se houve algum bloqueio ou problema
    # if response.filters:
    #     print(f"Resposta bloqueada. Motivo: {response.filters[0]['reason']}")  # Log do motivo do bloqueio
    #     return "Desculpe, a resposta foi bloqueada ou não pôde ser gerada devido a uma restrição."

    # Acessar a resposta correta no objeto ChatResponse
    if response.text:
        print(f"Conteúdo da resposta: {response}")  # Log da mensagem retornada
        return response.text
    else:
        print("Erro: resposta inválida ou inesperada.")  # Log de erro
        return "Desculpe, houve um problema ao processar sua solicitação."


def main():
    st.title("Chatbot com Gemini (em desenvolvimento)")

    # Exibir o histórico da conversa
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Campo de texto para o usuário inserir o prompt
    if prompt := st.chat_input("Digite sua mensagem"):
        # Adicionar a mensagem do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Obter a resposta do chatbot
        try:
            response = get_chatbot_response(prompt)

            # Adicionar a resposta do chatbot ao histórico
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

        except Exception as e:
            st.error(
                f"Ocorreu um erro ao gerar a resposta. Por favor, tente novamente mais tarde. Detalhes do erro: {e}")
            print(f"Erro: {e}")  # Log do erro no console


if __name__ == "__main__":
    main()

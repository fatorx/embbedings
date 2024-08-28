from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class OpenAIUtils:
    def __init__(self, temperature=0.7, model="gpt-3.5-turbo"):
        self.llm = ChatOpenAI(temperature=temperature, model=model)
        self.prompt = ChatPromptTemplate.from_template("""
        Responda a pergunta com base no contexto abaixo. Seja breve e objetivo.
        {context}
        Pergunta: {query}
        """)

    def generate_response(self, context, query):
        prompt_value = self.prompt.format_prompt(context=context, query=query)
        response = self.llm.invoke(prompt_value.to_messages())
        return response.content

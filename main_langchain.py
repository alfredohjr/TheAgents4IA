from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

BASE_URL = 'http://127.0.0.1:1234/v1'
API_KEY = 'hello'

llm = ChatOpenAI(base_url=BASE_URL, api_key=API_KEY)

prompt = ChatPromptTemplate([
    ("system","you are a python especialist"),
    ("user","""{question}""")
])

chain = prompt | llm | StrOutputParser()

question=input("Enter your question: ")
for s in chain.stream(question):
    print(s, end="", flush=True)

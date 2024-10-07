
def basic_chat(template:list, stream=True, question:str=None):

    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    __BASE_URL = 'http://127.0.0.1:1234/v1'
    __API_KEY = 'hello'
    __MODEL = 'lmstudio-community/gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf'
    
    __llm = ChatOpenAI(base_url=__BASE_URL, api_key=__API_KEY, model=__MODEL)

    __prompt = ChatPromptTemplate(template)

    __chain = __prompt | __llm | StrOutputParser()

    __question = question
    
    if __question is None:
        __question = input("Enter the question: ")

    res = ''
    if stream:
        for s in __chain.stream(__question):
            res += s
            print(s, end="", flush=True)
    else:
        for s in __chain.stream(__question):
            res += s
    
    return res
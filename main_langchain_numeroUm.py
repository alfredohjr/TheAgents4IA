import json
import pandas as pd
from langchain_core.pydantic_v1 import Field
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.agents import Tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub

from pydantic import BaseModel

CHAT_BASE_URL = 'http://127.0.0.1:1234/v1'
CHAT_API_KEY = 'hello'

llm = ChatOpenAI(base_url=CHAT_BASE_URL, api_key=CHAT_API_KEY)

def f_procura_produtos(nome:str) -> str:

    nome = nome.lower()

    df = pd.read_csv('tmp/data/RMS00006_CadastroDeItem.csv')
    df['descricao'] = df['descricao'].str.lower()
    df = df[df['descricao'] == nome]
    if df.empty:
        return ''
    return json.dumps(df.to_dict())

class ProdutoDescricao(BaseModel):
    name:str = Field("Descrição do produto, sempre em letra minuscula.")

class ProdutoDados(BaseTool):
    name:str = 'ProdutoDados'
    description:str = """Esta ferramenta extrai os dados de um produto a partir de sua descrição. ex: 'coca-cola'"""

    def _run(self, input:str) -> str:

        parser = JsonOutputParser(pydantic_object=ProdutoDescricao)
        template = PromptTemplate(
            template="""Você deve analisar a entrada a seguir e extrair o nome do produto.
                Entrada:
                ----------------
                {input}
                ----------------
                Formato de saída:
                {formato_de_saida}""",
            input_variables=["input"],
            partial_variables={"formato_de_saida": parser.get_format_instructions()})

        cadeia = template | llm | parser
        resposta = cadeia.invoke({"input": input})
        produto = resposta["produto"]
        dados = f_procura_produtos(produto)
        return dados
    
class AgenteOpenAiFunctions:

    def __init__(self):
        dados_produto = ProdutoDados()

        self.tools = [
            Tool(name = dados_produto.name,
                 func = dados_produto.run,
                 description = dados_produto.description),
        ]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system","You need to find the product data."),
            ("placeholder", "{agent_scratchpad}"),
        ])

        self.agente = create_openai_tools_agent(llm, self.tools, prompt)
    
agente = AgenteOpenAiFunctions()
executor = AgentExecutor(
    agent = agente.agente,
    tools = agente.tools,
    verbose = True
)

pergunta = "quero os dados do produto coca-cola"

resposta = executor.invoke({"input":pergunta})
print(resposta)
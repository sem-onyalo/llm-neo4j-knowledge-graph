import os
from dotenv import load_dotenv
load_dotenv()

# tag::llm[]
# Create the LLM
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

llm = AzureChatOpenAI(
    azure_deployment=os.getenv('AZURE_OPENAI_MODEL_DEPLOYMENT_NAME'),
)
# end::llm[]

# tag::embedding[]
# Create the Embedding model
from langchain_openai import OpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv('AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME'),
)
# end::embedding[]

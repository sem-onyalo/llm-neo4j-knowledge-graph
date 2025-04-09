import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_openai import AzureChatOpenAI

load_dotenv()

llm = AzureChatOpenAI(
    azure_deployment=os.getenv('AZURE_OPENAI_MODEL_DEPLOYMENT_NAME'),
    temperature=0, # A temperature of 0 is recommended for Cypher generation.
)

graph = Neo4jGraph(
    url=os.getenv('NEO4J_URI'),
    username=os.getenv('NEO4J_USERNAME'),
    password=os.getenv('NEO4J_PASSWORD')
)

CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Only include the generated Cypher statement in your response.

Always use case insensitive search when matching strings.

Schema:
{schema}

Examples: 
# Use case insensitive matching for entity ids
MATCH (c:Chunk)-[:HAS_ENTITY]->(e)
WHERE e.id =~ '(?i)entityName'

# Find documents that reference entities
MATCH (d:Document)<-[:PART_OF]-(:Chunk)-[:HAS_ENTITY]->(e)
WHERE e.id =~ '(?i)entityName'
RETURN d

The question is:
{question}"""

cypher_generation_prompt = PromptTemplate(
    template=CYPHER_GENERATION_TEMPLATE,
    input_variables=["schema", "question"],
)

cypher_chain = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    cypher_prompt=cypher_generation_prompt,
    verbose=True,
    allow_dangerous_requests=True,
    exclude_types=["Session", "Message", "LAST_MESSAGE", "NEXT"],
)

def run_cypher(q):
    return cypher_chain.invoke({"query": q})

while (q := input("> ")) != "exit":
    print(run_cypher(q))

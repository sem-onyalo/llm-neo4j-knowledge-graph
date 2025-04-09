from dotenv import load_dotenv
load_dotenv()

from llm import llm
from graph import graph

from langchain_neo4j import GraphCypherQAChain
from langchain.prompts import PromptTemplate

# You task is to update this tool to generate and run a Cypher statement, and return the results.
    
# Create cypher_generation prompt
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

# Create the cypher_chain
cypher_chain = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    cypher_prompt=cypher_generation_prompt,
    verbose=True,
    allow_dangerous_requests=True,
    exclude_types=["Session", "Message", "LAST_MESSAGE", "NEXT"],
)

def run_cypher(q):
    # Invoke the cypher_chain
    return cypher_chain.invoke({"query": q})

# Building Knowledge Graphs with LLMs

Scripts for the [Building Knowledge Graphs with LLMs](https://graphacademy.neo4j.com/courses/llm-knowledge-graph-construction/) course.

## Environment Variables

| Name | Required |
| ---- | -------- |
| AZURE_OPENAI_API_KEY | Yes |
| AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME | Yes |
| AZURE_OPENAI_ENDPOINT | Yes |
| AZURE_OPENAI_MODEL_DEPLOYMENT_NAME | Yes |
| NEO4J_PASSWORD | Yes |
| NEO4J_URI | Yes |
| NEO4J_USERNAME | Yes |
| OPENAI_API_VERSION | Yes |

Create a `.env` file with the variables listed above. For example,

```
NEO4J_PASSWORD=
NEO4J_URI=bolt://35.170.70.188:7687
NEO4J_USERNAME=neo4j
```

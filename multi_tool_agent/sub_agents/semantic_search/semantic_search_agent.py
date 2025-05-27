from google.adk.agents import LlmAgent
from multi_tool_agent.sub_agents.semantic_search import prompt
from multi_tool_agent.tools.vector_search import search_vector_database
import os

semantic_search_agent = LlmAgent(
    name="semantic_search_agent",
    model=os.environ.get("GEMINI_MODEL",""),
    description="agent that perform vector search for context",
    instruction=prompt.SEMANTIC_SEARCH_INSTR,
    tools=[search_vector_database],
    output_key="vector_search_result"
)

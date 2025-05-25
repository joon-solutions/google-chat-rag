from google.adk.agents import LlmAgent
from multi_tool_agent.sub_agents.keyword_search import prompt


def keyword_search(query: list) -> dict:
    return {"results": "abcd"}

keyword_search_agent = LlmAgent(
    name="keyword_search_agent",
    model="gemini-2.0-flash-lite-001",
    description="agent that uses keyword search for context",
    instruction=prompt.KEYWORD_SEARCH_INSTR,
    tools=[keyword_search],
    output_key="keyword_search_result"
)

from google.adk.agents import Agent
from multi_tool_agent import prompt
from multi_tool_agent.tools.vector_search import search_vector_database







root_agent = Agent(
    name="system_activity_agent",
    model="gemini-2.0-flash-lite-001",
    description=(
        "Retrivial agent that helps user find related discussions "
        "and issues from previous incidents in their documents."
    ),
    instruction=prompt.ROOT_PROMPT,
    tools=[search_vector_database],
    )





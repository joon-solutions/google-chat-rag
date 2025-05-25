from google.adk.agents import LlmAgent
from multi_tool_agent.sub_agents.input_summarize import prompt
from multi_tool_agent.tools.memory import memorize

input_summarize_agent = LlmAgent(
    name="input_summarize_agent",
    model="gemini-2.0-flash-lite-001",
    description="agent that sanitize the user's input",
    instruction=prompt.INPUT_SUMMARIZE_INSTR,
    tools=[memorize]
)

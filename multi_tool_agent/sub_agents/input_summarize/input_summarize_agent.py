from google.adk.agents import LlmAgent
from multi_tool_agent.sub_agents.input_summarize import prompt
from multi_tool_agent.tools.memory import memorize
import os


input_summarize_agent = LlmAgent(
    name="input_summarize_agent",
    model=os.environ.get("GEMINI_MODEL",""),
    description="agent that sanitize the user's input",
    instruction=prompt.INPUT_SUMMARIZE_INSTR,
    tools=[memorize]
)

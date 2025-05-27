from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from . import prompt
from multi_tool_agent.tools.memory import memorize
import os


def exit_loop(tool_context: ToolContext):
    """tool for agent to exit the loop

    Args:
        tool_context (ToolContext): the context automatically passed by adk.

    Returns:
        empty dict
    """
    tool_context.actions.escalate = True
    return {}


evaluator_agent = LlmAgent(
    name="evaluator_agent",
    description="agent that iteratively assess the content and decide continous research",
    tools=[exit_loop, memorize],
    instruction=prompt.EVALUATOR_AGENT_INSTR,
    model=os.environ.get("GEMINI_MODEL",""),
)
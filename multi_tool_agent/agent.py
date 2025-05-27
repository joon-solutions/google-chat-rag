from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent, LoopAgent
from multi_tool_agent import prompt
from multi_tool_agent.tools.vector_search import search_vector_database
from multi_tool_agent.sub_agents import (
    input_summarize,
    keyword_search,
    semantic_search,
    evaluator,
)

from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.agent_tool import AgentTool
import os
from dotenv import load_dotenv
load_dotenv()

merger_agent = LlmAgent(
    name="SynthesisAgent",
    model="gemini-2.0-flash-lite-001",  # Or potentially a more powerful model if needed for synthesis
    instruction="""You are an AI Assistant responsible for combining findings into a structured response.

 Your primary task is to synthesize the following search results which was initiated to answer the following user question : 
 {user_message}

 **Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below. Do NOT add any external knowledge, facts, or details not present in these specific summaries.**

 **Search results:**

 *   **Vector search result:**
     {vector_search_result}

 *   **Keyword search results:**
     {keyword_search_result}

""",
    output_key="merger_agent",
)


parrallel_agent = ParallelAgent(
    name="parrallel_agent",
    sub_agents=[
        semantic_search.semantic_search_agent.semantic_search_agent,
        keyword_search.keyword_search_agent.keyword_search_agent,
    ],
)


sequential_agent = SequentialAgent(
    name="sequential_agent",
    description="Agent that helps retrieve incidents happned in the past",
    sub_agents=[
        input_summarize.input_summarize_agent.input_summarize_agent,
        parrallel_agent,
        merger_agent
    ],
)

loop_agent = LoopAgent(
    name="loop_agent",
    description="the agent that can look into previous conversations for incidents happened in the past",
    sub_agents=[sequential_agent, evaluator.evaluator_agent.evaluator_agent],
)


def set_user_question(callback_context: CallbackContext, **kwargs):
    message = callback_context.user_content
    callback_context.state["user_message"] = message
    callback_context.state["original_user_message"] = message


root_agent = LlmAgent(
    name="system_activity_agent",
    model=os.environ.get("GEMINI_MODEL",""),
    description=(
        "Onboarding assistant that helps developers with issues troubleshooting."
    ),
    instruction="Onboarding assistant that helps developers with issues troubleshooting.",
    sub_agents=[loop_agent],
    # tools=[AgentTool(sequential_agent)],
    before_agent_callback=set_user_question,
)
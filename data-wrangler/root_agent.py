from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent, LoopAgent
from . import prompt
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset,StdioServerParameters
from google.adk.tools.tool_context import ToolContext
import os
from dotenv import load_dotenv
from pathlib import Path
import tempfile
import uuid
import mimetypes
from minimal_csv_diff.eda_analyzer import analyze_multiple_files
from minimal_csv_diff.main import diff_csv
import pandas as pd
import numpy as np


load_dotenv()

current_dir = Path(__file__).resolve().parent

python_runtime = MCPToolset(
    connection_params=StdioServerParameters(
        command='uvx',
        args=[
            # "mcp-python-interpreter",
            "git+https://github.com/luutuankiet/mcp-python-interpreter.git",
            '--dir',
            str(current_dir),
            "--python-path",
            "/workspaces/EVERYTHING/joons/genai/google-chat-rag/.venv/bin/python"
        ],
        env={
            "MCP_ALLOW_SYSTEM_ACCESS": "1"
        }
    ),
        tool_filter=[
        'list_python_environment',
        'run_python_code',
    ]
)


async def process_upload(tool_ctx: ToolContext):
    return await tool_ctx.list_artifacts()




def set_user_question(callback_context: CallbackContext, **kwargs):
    message = callback_context.user_content
    callback_context.state["user_message"] = message
    callback_context.state["original_user_message"] = message

async def save_uploaded_file(callback_context: CallbackContext):
    """
    save uploaded file to local storage before passing to agent.
    """
    ctx = callback_context
    files = ctx.state['csv_raw_files'] = []
    if ctx.user_content and ctx.user_content.parts:
        temp_dir = tempfile.gettempdir()
        for part in ctx.user_content.parts:
            if part.inline_data and part.inline_data.data:
                mime_type = part.inline_data.mime_type or ''
                ext = mimetypes.guess_extension(mime_type) or '.bin'
                filename =str(uuid.uuid4()) + ext
                filepath = os.path.join(temp_dir,filename)
                await ctx.save_artifact(
                    filename,
                    part
                )
                with open(filepath, 'wb') as f:
                    f.write(part.inline_data.data)
                    files.append(filepath)
        print(f"saved artifacts: {files}.")

def inherit_docstring(from_func):
    def decorator(to_func):
        to_func.__doc__ = from_func.__doc__
        return to_func
    return decorator


@inherit_docstring(analyze_multiple_files)
def tool_analyze_multiple_files(**kwargs):
    def convert_to_native(obj):
        if isinstance(obj, dict):
            return {k: convert_to_native(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_native(i) for i in obj]
        elif isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, (np.ndarray, pd.Series)):
            return obj.tolist()
        elif pd.api.types.is_datetime64_any_dtype(type(obj)):
            return str(obj)
        else:
            return obj    
    
    try:
        analysis_result = analyze_multiple_files(**kwargs)
        clearned_analysis_result = convert_to_native(analysis_result)
        return {
            'status': 'success',
            'result': clearned_analysis_result
        }
    except Exception as e:
        return {
            'status': 'error',
            'error_message': str(e)
        }

@inherit_docstring(diff_csv)
def tool_diff_csv(**kwargs):
    try:
        results = diff_csv(**kwargs)
        return {
            'status': 'success',
            'result': results
        }
    except Exception as e:
        return {
            'status': 'error',
            'error_message': str(e)
        }    

root_agent = LlmAgent(
    name="data_diff_assistant",
    model=os.environ.get("GEMINI_MODEL",""),
    instruction=prompt.ROOT_INSTR,
    # sub_agents=[loop_agent],
    tools=[tool_analyze_multiple_files,tool_diff_csv,python_runtime],
    before_agent_callback=save_uploaded_file,
)
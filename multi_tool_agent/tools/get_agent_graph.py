from google.adk.cli.agent_graph import get_agent_graph
from multi_tool_agent.agent import root_agent
import asyncio


async def main():
    image = await get_agent_graph(root_agent, [], image=True)
    with open("graph.png", "wb") as f:
        if isinstance(image,bytes):
            f.write(image)

asyncio.run(main())
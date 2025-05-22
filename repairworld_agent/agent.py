# ./adk_agent_samples/mcp_agent/agent.py
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
import os
import logging

logging.basicConfig(level=logging.INFO)

if os.environ.get("GOOGLE_API_KEY") == "NOT_SET":
  logging.error("Please set a Google API Key using - https://aistudio.google.com/app/apikey")
  exit(1)

repairworld_api_key = os.environ.get("REPAIRWORLD_API_KEY")
repairworld_api_base = os.environ.get("REPAIRWORLD_API_BASE")

root_agent = LlmAgent(
    model=os.environ.get("GEMINI_MODEL"), # Adjust model name if needed based on availability
    name='repairworld_agent',
    instruction='Help user interact with repair-world application. If the user asks for open or close requests, use the appropriate tool and then filter the data before showing. If the user asks for any report or output in a table or email format, do provide that.',
    tools=[
      MCPToolset(connection_params=StdioServerParameters(
        command='python', # Command to run the server
        args=["-m", # Arguments for the command
              "mcp_server_repairworld",    
              "--api-key",
              repairworld_api_key,
              "--api-base",
              repairworld_api_base])
      )
    ]
)

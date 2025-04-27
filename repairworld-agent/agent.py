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



# --- Step 1: Import Tools from MCP Server ---
async def get_tools_async():
  """Gets tools from the MCP Server."""
  logging.info("Attempting to connect to the MCP server...")
  tools, exit_stack = await MCPToolset.from_server(
      # Use StdioServerParameters for local process communication
      connection_params=StdioServerParameters(
          command='python', # Command to run the server
          args=["-m", # Arguments for the command
                "mcp_server_repairworld",    
                "--api-key",
                repairworld_api_key,
                "--api-base",
                repairworld_api_base] 
      )
  )
  logging.info("MCP Toolset created successfully.")
  # MCP requires maintaining a connection to the local MCP Server.
  # exit_stack manages the cleanup of this connection.
  return tools, exit_stack

async def create_agent():
  """Gets tools from MCP Server."""
  tools, exit_stack = await get_tools_async()

  agent = LlmAgent(
      model=os.environ.get("GEMINI_MODEL"), # Adjust model name if needed based on availability
      name='repairworld_agent',
      instruction='Help user interact with repair-world application.',
      tools=tools, # Provide the MCP tools to the ADK agent
  )
  return agent, exit_stack


root_agent = create_agent()
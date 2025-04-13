# ./adk_agent_samples/mcp_agent/agent.py
import asyncio
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams, StdioServerParameters
import os

# Load environment variables from .env file in the parent directory
# Place this near the top, before using env vars like API keys
load_dotenv('./.env')

if os.environ.get("GOOGLE_API_KEY") == "NOT_SET":
  print("Please set a Google API Key using - https://aistudio.google.com/app/apikey")
  exit(1)

log_verbosity = os.environ.get("LOG_VERBOSITY")



repairworld_api_key = os.environ.get("REPAIRWORLD_API_KEY")
repairworld_api_base = os.environ.get("REPAIRWORLD_API_BASE")




# --- Step 1: Import Tools from MCP Server ---
async def get_tools_async():
  """Gets tools from the MCP Server."""
  print("Attempting to connect to the MCP server...")
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
      # For remote servers, you would use SseServerParams instead:
      # connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
  )
  print("MCP Toolset created successfully.")
  # MCP requires maintaining a connection to the local MCP Server.
  # exit_stack manages the cleanup of this connection.
  return tools, exit_stack

# --- Step 2: Agent Definition ---
async def get_agent_async():
  """Creates an ADK Agent equipped with tools from repairworld MCP Server."""
  tools, exit_stack = await get_tools_async()
  print(f"Fetched {len(tools)} tools from MCP server.")
  root_agent = LlmAgent(
      model='gemini-2.0-flash', # Adjust model name if needed based on availability
      name='repairworld_assistent',
      instruction='Help user interact with repair-world application.',
      tools=tools, # Provide the MCP tools to the ADK agent
  )
  return root_agent, exit_stack


def print_event(event):
    if log_verbosity == 0:
      print(f"Event received: {event}")
    elif log_verbosity == 1:
      print(f"Event from: {event.author}")
      if event.content and event.content.parts:
          if event.get_function_calls():
              print("  Type: Tool Call Request")
          elif event.get_function_responses():
              print("  Type: Tool Result")
          elif event.content.parts[0].text:
              if event.partial:
                  print("  Type: Streaming Text Chunk")
              else:
                  print("  Type: Complete Text Message")
              print(event.content.parts[0].text)                  
          else:
              print("  Type: Other Content (e.g., code result)")
      elif event.actions and (event.actions.state_delta or event.actions.artifact_delta):
          print("  Type: State/Artifact Update")
      else:
          print("  Type: Control Signal or Other")  
    else:
      if event.content.parts[0].text:
        print(event.content.parts[0].text)
             

# --- Step 3: Main Execution Logic ---
async def async_main():
  session_service = InMemorySessionService()
  # Artifact service might not be needed for this example
  artifacts_service = InMemoryArtifactService()

  session = session_service.create_session(
      state={}, app_name='mcp_filesystem_app', user_id='user_fs'
  )


  root_agent, exit_stack = await get_agent_async()

  runner = Runner(
      app_name='mcp_filesystem_app',
      agent=root_agent,
      artifact_service=artifacts_service, # Optional
      session_service=session_service,
  )

  # accept and run user's query
  # e.g., "list files in the 'documents' subfolder" or "read the file 'notes.txt'"
  query = ""
  while (query != "bye"):
    query = input("input >")
    #print(f"User Query: '{query}'")
    content = types.Content(role='user', parts=[types.Part(text=query)])

    print("Running agent...")
    events_async = runner.run_async(
        session_id=session.id, user_id=session.user_id, new_message=content
    )

    async for event in events_async:
      print_event(event)

  # Crucial Cleanup: Ensure the MCP server process connection is closed.
  print("Closing MCP server connection...")
  await exit_stack.aclose()
  print("Cleanup complete.")

if __name__ == '__main__':
  try:
    asyncio.run(async_main())
  except Exception as e:
    print(f"An error occurred: {e}")
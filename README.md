# google-adk-mcp

🚀 Sample project demonstrating how to build a Google ADK agent that uses an external MCP server to interact with a repair API ([repairworld application](https://github.com/nikhilpurwant/repair_world_application) - created specifically for the demo).

This agent is created to go along with the blog post and demo - [26. The simplest MCP demo (Includes Sample provider app, MCP Server and Agent 🤖 code and explanation!)](https://nikhilpurwant.com/post/tech-genai-adk-mcp/)

## 🧠 What This Project Does

This project shows how to:

1. ✅ Use **Google ADK (Agent Developer Kit)** to build an agent.
2. 🔌 Connect that agent to an existing **MCP server** that exposes functionality of the `repair_world_application` (e.g., creating and viewing repair requests).

The agent uses MCP server from the pypi repo - [mcp-server-repairworld](https://pypi.org/project/mcp-server-repairworld/).

---

## 📦 Prerequisites

- Python 3.11+
- A running [repairworld application](https://github.com/nikhilpurwant/repair_world_application).
---

## 🚀 How to Use

### 1. Clone this repo create python virtual environment

```bash
git clone https://github.com/your-username/google-adk-mcp.git
cd google-adk-mcp

# create python virtual environment
python -m venv .venv
. .venv/bin/activate # on windows do .venv\Scripts\activate

```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the agent (Agent Web Interface)

Make sure you already have the running [repairworld application](https://github.com/nikhilpurwant/repair_world_application).

Go to http://localhost:8000 to access the Agent UI

```bash
adk web
```


**OR**

### 3. Run the agent (Agent Console Interface)

Make sure you already have the running [repairworld application](https://github.com/nikhilpurwant/repair_world_application).

```bash
python agent-repairworld.py
```

The agent should now be able to invoke tools exposed by the MCP server to:

🔧 Create a repair request

📄 List all repair requests

🔍 View a repair request by ID


###  🛠 Related Projects
* [mcp-server-repairworld](https://pypi.org/project/mcp-server-repairworld/) — MCP server that exposes tools for interacting with the [repair_world_application](https://github.com/nikhilpurwant/repair_world_application).
* [repair_world_application](https://github.com/nikhilpurwant/repair_world_application) - An application allowing customers to create repair requests


# google-adk-mcp

🚀 Sample project demonstrating how to build a Google ADK agent that uses an external MCP server to interact with a repair API (`repair_world_application`).

## 🧠 What This Project Does

This project shows how to:

1. ✅ Use **Google ADK (Agent Developer Kit)** to build an agent.
2. 🔌 Connect that agent to an existing **MCP server** that exposes functionality of the `repair_world_application` (e.g., creating and viewing repair requests).

The MCP server is not implemented here — it's assumed to be already available (e.g., from [mcp-server-repairworld](https://github.com/your-org/mcp-server-repairworld)).

---

## 📦 Prerequisites

- Python 3.11+
- A running [repairworld application](https://github.com/nikhilpurwant/repair_world_application).
---

## 🚀 How to Use

### 1. Clone this repo

```bash
git clone https://github.com/your-username/google-adk-mcp.git
cd google-adk-mcp
pip install -r requirements.txt
python agent-repairworld.py
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the agent

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


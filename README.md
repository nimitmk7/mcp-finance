

## Setup your environment

### For MacOS/Linux
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### For Windows

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Make sure to restart your terminal afterwards to ensure that the uv command gets picked up.

Now, let’s create and set up our project:

```
# Initialize uv for our repo
uv init mcp_demo

# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install dependencies
uv add "mcp[cli]" httpx

# Create our server file
touch mcp_demo.py

```


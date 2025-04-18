# Introduction
This is a MCP server that helps your MCP client/LLM get access to financial data like stock price, company info, and company news. 
It is powered by the `yfinance` Python library and MarketAux API.

# Tools available:
1. Get Stock Price: Fetch the latest stock price for a symbol.
2. Get Company Info: Fetch basic company info(Name, Sector, Industry, Website, Business Summary)
3. Get Historical Data: Fetch historical data for a stock
4. Get Stock News: Fetch latest news related to a stock symbol
5. Get Market Indices: Fetch the latest data for major US market indices.


# Setup your environment

## 1. Installing uv
### For MacOS/Linux
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### For Windows

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Make sure to restart your terminal afterwards to ensure that the uv command gets picked up.

## 2. Setting up the server
Now, let’s create and set up our project:

### Cloning the repo
```
git clone git@github.com:nimitmk7/mcp-finance.git

```

### Set up environment variables:

```
# Create .env file for your API keys
cp .env.example .env

# Set API key in .env
MARKETAUX_API_KEY=your-marketaux-api-key
```

### Adding the server to Claude Client
 If you are using Claude Desktop Client, you can go to Settings -> Developer, and press on the button 'Edit Config'. It will open `claude_desktop_config.json`. Put the following configuration with your relevant details in the file:

#### For Mac Users
 ```
 {
  "mcpServers": { 
    "mcp-finance": {
      "command": "/Users/<username>/.local/bin/uv", 
      "args": [
                "--directory",
                "/Users/<username>/<path-to-dir>/mcp-finance",
                "run",
                "mcp_finance.py"
            ]
    }
  }
}
```

#### For Windows users
```
{
  "mcpServers": { 
    "mcp-finance": {
      "command": "C:\\Users\\<username>\\.local\\bin\\uv.exe", 
      "args": [
                "--directory",
                "C:\\Users\\<username>\\<path-to-dir>\\mcp-finance",
                "run",
                "mcp_finance.py"
            ]
    }
  }
}
```


If you already have some MCP servers, just add the `mcp-finance` config in the list of configs of MCP servers.
Restart the Claude Desktop client after these steps. 

## 3. Verify the setup

1. In the UI, click on the hammer icon and check whether our server tools are present in the list of available tools.

## 4. Example Usage

Try asking Claude questions like:
   - "What is the price of Nvidia stock right now"
   - "How much has the share price of Google changed over 1 month "
   - "Get me latest news for Microsoft" 



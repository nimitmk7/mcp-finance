import yfinance as yf
from mcp.server.fastmcp import FastMCP
import httpx
import os
from dotenv import load_dotenv
load_dotenv()  # This will load .env into os.environ

# Initialize MCP server
mcp = FastMCP("financial_data")
MARKETAUX_API_KEY = os.environ.get("MARKETAUX_API_KEY")

@mcp.tool()
async def get_stock_price(symbol: str) -> str:
    """Fetch the latest stock price for a symbol."""
    stock = yf.Ticker(symbol)
    data = stock.info

    if "regularMarketPrice" not in data:
        return f"No data found for symbol: {symbol}"

    return f"""
Symbol: {data['symbol']}
Name: {data.get('shortName', 'N/A')}
Price: ${data['regularMarketPrice']}
Change: {data.get('regularMarketChange', 'N/A')} ({data.get('regularMarketChangePercent', 'N/A')}%)
Market Cap: {data.get('marketCap', 'N/A')}
"""

@mcp.tool()
async def get_company_info(symbol: str) -> str:
    """Fetch basic company info."""
    stock = yf.Ticker(symbol)
    data = stock.info

    if "longBusinessSummary" not in data:
        return f"Could not find company info for {symbol}."

    return f"""
Name: {data.get("longName", "N/A")}
Sector: {data.get("sector", "N/A")}
Industry: {data.get("industry", "N/A")}
Website: {data.get("website", "N/A")}
Description: {data["longBusinessSummary"]}
"""

@mcp.tool()
async def get_historical_data(symbol: str, period: str = "5d") -> str:
    """Fetch historical stock data.

    Args:
        symbol: Stock ticker symbol
        period: Period of data (e.g., 1d, 5d, 1mo, 3mo, 1y)
    """
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)

    if hist.empty:
        return f"No historical data available for {symbol} in the given period."

    output = f"Historical prices for {symbol} ({period}):\n"
    for date, row in hist.iterrows():
        output += f"{date.date()}: Open: ${row['Open']:.2f}, Close: ${row['Close']:.2f}, Volume: {int(row['Volume'])}\n"

    return output.strip()


@mcp.tool()
async def get_stock_news(symbol: str, count: int = 5) -> str:
    """Fetch latest news using MarketAux API."""
    url = "https://api.marketaux.com/v1/news/all"
    params = {
        "countries": "us",
        "symbols": symbol,
        "filter_entities": "true",
        "language": "en",
        "limit": count,
        "api_token": MARKETAUX_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            return f"Error fetching news: {e}"

    if not data.get("data"):
        return f"No news found for {symbol}."

    output = f"🗞️ Latest news for {symbol}:\n"
    for article in data["data"]:
        output += f"\n• {article['title']} ({article['source']})\n🔗 {article['url']}\n"

    return output.strip()

@mcp.tool()
async def get_market_indices() -> str:
    """Fetch the latest data for major US market indices."""
    indices = {
        "S&P 500": "^GSPC",
        "Nasdaq": "^IXIC",
        "Dow Jones": "^DJI"
    }

    output = "📊 Major Market Indices:\n"
    for name, symbol in indices.items():
        stock = yf.Ticker(symbol)
        info = stock.info

        price = info.get("regularMarketPrice")
        change = info.get("regularMarketChange")
        percent = info.get("regularMarketChangePercent")

        if price is None:
            output += f"\n{name} ({symbol}): Data not available\n"
            continue

        output += f"\n{name} ({symbol})\n"
        output += f"Price: ${price:.2f}\n"
        output += f"Change: {change:+.2f} ({percent:+.2f}%)\n"

    return output.strip()


if __name__ == "__main__":
    mcp.run(transport="stdio")

import os
import requests
from langchain.output_parsers import JsonOutputKeyToolsParser
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.globals import set_debug
from dotenv import load_dotenv

# Enable debug mode to see intermediate chain outputs
set_debug(True)

load_dotenv()

OPENAI_CHAT_MODEL = "gpt-3.5-turbo-1106"


@tool
def repl_tool(command: str) -> str:
    """Run a Python REPL command. Return the final value set to a variable called "result" """
    exec_globals = {}
    exec(command, None, exec_globals)
    return exec_globals['result']


@tool
def stock_search(stock_tickers: list) -> list:
    """Search for multiple stocks with their ticker symbols, including the stock exchange, like AAPL:NASDAQ or GOOGL:NASDAQ, returning a list of stock summaries using the SERP API."""
    api_key = os.getenv('SERP_API_KEY')
    if not api_key:
        raise ValueError("SERP API key not found in environment variables.")

    results = []
    for stock_ticker in stock_tickers:
        print(f"Fetching stock data for {stock_ticker}")
        url = f"https://serpapi.com/search.json"
        params = {
            "engine": "google_finance",
            "q": stock_ticker,
            "api_key": api_key
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            stock_summary = data.get('summary', {})
            results.append(stock_summary['price'].replace("$", ""))
        else:
            results.append(
                f"Failed to fetch stock data for {stock_ticker}: {response.text}")

    return {"stocks": ",".join(results)}


get_stock_prices_prompt = ChatPromptTemplate.from_template(
    "Get the current stock prices for {stockA} and {stockB}, return as a comma separated list like GOOGL:NASDAQ,AAPL:NASDAQ. You can use the stock_search tool to fetch the stock prices.")

calculate_percent_difference_prompt = ChatPromptTemplate.from_template(
    "The percent difference between (comma separated stock prices) `{stocks}` current stock prices is to be calculated as Python code passed to a REPL, Round to the nearest 2 decimal places.")

model = ChatOpenAI(model=OPENAI_CHAT_MODEL, temperature=0).bind_tools(
    [repl_tool, stock_search])


chain = (
    get_stock_prices_prompt
    | model
    | JsonOutputKeyToolsParser(key_name="stock_search", first_tool_only=True, return_single=True)
    | stock_search
    | calculate_percent_difference_prompt
    | model
    | JsonOutputKeyToolsParser(key_name="repl_tool", first_tool_only=True, return_single=True)
    | repl_tool
)

result = chain.invoke({"stockA": "AAPL", "stockB": "GOOGL"})

# Returns the percent difference between the two stock prices
print(result)

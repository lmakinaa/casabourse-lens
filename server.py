"""
WafaBourse MCP Server
Exposes Casablanca Stock Exchange tools for Claude Desktop
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from trading_tools.api import WafaBourseAPI
from trading_tools.technical_analysis import TechnicalAnalysis
from trading_tools.tools import TradingTools


def build_mcp_tools(tool_defs: list) -> list[types.Tool]:
    """Convert OpenAI-format tool definitions to MCP Tool objects"""
    mcp_tools = []
    for t in tool_defs:
        fn = t["function"]
        mcp_tools.append(
            types.Tool(
                name=fn["name"],
                description=fn["description"],
                inputSchema=fn["parameters"],
            )
        )
    return mcp_tools


def main():
    wafa_api = WafaBourseAPI()
    tech_analysis = TechnicalAnalysis()
    trading_tools = TradingTools(wafa_api, tech_analysis)

    tool_defs = trading_tools.get_tool_definitions()
    mcp_tool_list = build_mcp_tools(tool_defs)

    server = Server("wafabourse")

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return mcp_tool_list

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        result = trading_tools.execute_tool(name, arguments)
        return [types.TextContent(type="text", text=result)]

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(run())


if __name__ == "__main__":
    main()

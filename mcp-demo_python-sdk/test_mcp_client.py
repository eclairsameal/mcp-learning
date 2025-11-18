import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp-demo_python-sdk/mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 列出已註冊工具
            response = await session.list_tools()
            tool_names = [tool.name for tool in response.tools]
            print("📦 可用工具:", tool_names)

            # 呼叫工具：get_weather
            weather_res = await session.call_tool(
                name="get_weather",
                arguments={"city": "東京"}
            )
            print("🌤️ 查詢結果:", weather_res.content[0].text if weather_res.content else weather_res)

            # 呼叫工具：calculate
            calc_res = await session.call_tool(
                name="calculate",
                arguments={"expression": "3*7+2"}
            )
            print("🧮 計算結果:", calc_res.content[0].text if calc_res.content else calc_res)

asyncio.run(main())

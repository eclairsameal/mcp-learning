import asyncio
import re
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

"""
自然語言解析工具名和參數
例如用正則或簡單關鍵字抓取 prompt 裡的城市或計算式。
"""


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # prompts = [
            #     "請幫我查今天東京的天氣",
            #     "幫我計算 3*7+2 的值",
            #     "請問大阪天氣如何",
            #     "計算 15/3+4"
            # ]
            prompts = [
                "Please check the weather in Tokyo today.",
                "Please calculate the value of 3*7+2.",
                "What's the weather in Osaka?",
                "Calculate 15/3+4."
            ]

            for prompt in prompts:
                print(f"\n💬 LLM Prompt: {prompt}")

                tool_name = None
                args = {}

                # ==== 自然語言解析(ch) ====
                # if "天氣" in prompt:
                # # 天氣查詢
                #     tool_name = "get_weather"
                #     city_match = re.search(r"(?:查|問|今天)?(\w+)天氣", prompt)
                #     city = city_match.group(1) if city_match else "東京"
                #     args = {"city": city}
                #
                # # 數學計算
                # elif "計算" in prompt or re.search(r"\d+[\+\-\*\/]\d+", prompt):
                #     tool_name = "calculate"
                #     expr_match = re.search(r"(\d+[\+\-\*\/]\d+(?:[\+\-\*\/]\d+)*)", prompt)
                #     expr = expr_match.group(1) if expr_match else "3*7+2"
                #     args = {"expression": expr}

                # ==== 自然語言解析（en） ====
                # Weather forecast
                if re.search(r"\bweather\b", prompt, re.I):
                    tool_name = "get_weather"
                    city_match = re.search(r"weather in (\w+)", prompt, re.I)
                    city = city_match.group(1) if city_match else "Tokyo"
                    args = {"city": city}

                # Mathematical calculation
                elif re.search(r"\bcalculate\b|\d+[\+\-\*\/]\d+", prompt, re.I):
                    tool_name = "calculate"
                    expr_match = re.search(r"(\d+[\+\-\*\/]\d+(?:[\+\-\*\/]\d+)*)", prompt)
                    expr = expr_match.group(1) if expr_match else "3*7+2"
                    args = {"expression": expr}

                if not tool_name:
                    print("⚠️ Cannot determine tool, skipping")
                    continue

                # ==== 呼叫 MCP 工具（Call MCP tool） ====
                tool_res = await session.call_tool(name=tool_name, arguments=args)
                tool_output = tool_res.content[0].text if tool_res.content else str(tool_res)
                print(f"🛠 Tool Results: {tool_output}")

                # ==== 使用 Ollama 整理回覆 （Use Ollama to organize replies） ====
                response = ollama.generate(
                    model="llama3.2:latest",
                    prompt=f"Tool Results: {tool_output}\nPlease help me organize this into a complete answer.",
                )
                llm_text = getattr(response, "response", str(response))
                print("🤖 LLM Reply:", llm_text)

asyncio.run(main())

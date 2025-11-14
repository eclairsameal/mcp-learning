import asyncio
import json
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

"""
讓 LLM 直接決定要呼叫哪個工具
可以先把可用工具列表傳給 LLM，然後問 LLM「這個 prompt 要呼叫哪個工具？」，讓 LLM 返回工具名和參數，這樣就完全不用寫死了。
"""


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            prompts = [
                "請幫我查今天東京的天氣",
                "幫我計算 3*7+2 的值",
                "請問大阪天氣如何",
                "計算 15/3+4"
            ]

            for prompt in prompts:
                print(f"\n💬 LLM Prompt: {prompt}")

                # ==== 先讓 LLM 決定工具與參數 ====
                tool_decision_prompt = f"""
                你是助手，根據下面使用者的指令選擇要呼叫的工具以及參數。
                可用工具：
                1. get_weather(city: str)
                2. calculate(expression: str)

                請以 JSON 格式回覆：
                {{
                    "tool": "工具名稱",
                    "args": {{}}
                }}

                指令: {prompt}
                """
                decision_resp = ollama.generate(
                    model="llama3.2:latest",
                    prompt=tool_decision_prompt
                )
                decision_text = getattr(decision_resp, "response", str(decision_resp))

                try:
                    decision_json = json.loads(decision_text)
                    tool_name = decision_json["tool"]
                    args = decision_json["args"]
                except Exception as e:
                    print(f"⚠️ 無法解析 LLM 決定結果: {decision_text}")
                    continue

                # ==== 呼叫 MCP 工具 ====
                tool_res = await session.call_tool(name=tool_name, arguments=args)
                tool_output = tool_res.content[0].text if tool_res.content else str(tool_res)
                print(f"🛠 工具結果: {tool_output}")

                # ==== 使用 Ollama 整理回覆 ====
                response = ollama.generate(
                    model="llama3.2:latest",
                    prompt=f"工具結果: {tool_output}\n請幫我整理成完整回答",
                )
                llm_text = getattr(response, "response", str(response))
                print("🤖 LLM 回覆:", llm_text)


asyncio.run(main())

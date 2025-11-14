import asyncio
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


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
                "幫我計算 3*7+2 的值"
            ]

            for prompt in prompts:
                print(f"\n💬 LLM Prompt: {prompt}")

                # 判斷工具()
                """
                * 它只會檢查 prompt 裡面有沒有 "天氣" 或 "計算" 這兩個關鍵字，然後直接呼叫對應的工具。
                  也就是說：
                    1.只支援固定兩種工具
                    2.呼叫的參數（city、expression）也是固定的
                * 如果你輸入其他問題，或者城市／計算式改變，這段程式碼就無法自動選擇或組裝工具參數。
                """
                if "天氣" in prompt:
                    tool_name = "get_weather"
                    args = {"city": "東京"}
                elif "計算" in prompt:
                    tool_name = "calculate"
                    args = {"expression": "3*7+2"}
                else:
                    continue

                # 呼叫 MCP 工具
                tool_res = await session.call_tool(name=tool_name, arguments=args)
                tool_output = tool_res.content[0].text if tool_res.content else str(tool_res)
                print(f"🛠 工具結果: {tool_output}")

                # 使用 Ollama generate 生成回覆
                response = ollama.generate(
                    model="llama3.2:latest",
                    prompt=f"工具結果: {tool_output}\n請幫我整理成完整回答",
                )
                llm_text = getattr(response, "response", str(response))
                print("🤖 LLM 回覆:", llm_text)

asyncio.run(main())

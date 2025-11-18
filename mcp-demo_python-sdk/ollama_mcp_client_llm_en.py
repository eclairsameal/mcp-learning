import asyncio
import json
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp-demo_python-sdk/mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            prompts = [
                "Please check the weather in Paris today.",
                "Please calculate the value of 3*7+10.",
                "What's the weather in Osaka?",
                "Calculate 15/3+4."
            ]

            for prompt in prompts:
                print(f"\n💬 LLM Prompt: {prompt}")

                # ==== 先讓 LLM 決定工具與參數 ====
                tool_decision_prompt = f"""
                You are the assistant. Select the tool and parameters to call based on the user's instructions.
                Available tools:
                1. get_weather(city: str)
                2. calculate(expression: str)

                Please reply in JSON format:
                {{
                    "tool": "Tool Name",
                    "args": {{}}
                }}

                instruction: {prompt}
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
                    print(f"⚠️ Unable to resolve LLM decision result: {decision_text}")
                    continue

                # ==== 呼叫 MCP 工具 ====
                tool_res = await session.call_tool(name=tool_name, arguments=args)
                tool_output = tool_res.content[0].text if tool_res.content else str(tool_res)
                print(f"🛠 Tool Results: {tool_output}")

                # ==== 使用 Ollama 整理回覆 ====
                response = ollama.generate(
                    model="llama3.2:latest",
                    prompt=f"Tool Results: {tool_output}\nPlease help me organize this into a complete answer.",
                )
                llm_text = getattr(response, "response", str(response))
                print("🤖 LLM Reply:", llm_text)


asyncio.run(main())

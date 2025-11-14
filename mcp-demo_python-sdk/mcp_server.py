from mcp.server.fastmcp import FastMCP
import random

# 建立 MCP Server(Create MCP Server)
app = FastMCP(name="WeatherAndMathTool")


# 註冊工具：查天氣(Registration tool: Check the weather)
@app.tool()
def get_weather(city: str) -> str:
    """Simulate weather query"""
    # weather = random.choice(["晴天", "多雲", "小雨", "暴雨", "陰天"])
    weather = random.choice(["Sunny", "Partly Cloudy", "Light Rain", "Heavy Rain", "Overcast"])
    temperature = random.randint(15, 30)
    return f"{city}: {weather}，temperature: {temperature}°C"


# 註冊工具：計算數學表達式(Registration tool: Calculate mathematical expressions)
@app.tool()
def calculate(expression: str) -> str:
    """Simple mathematical calculations"""
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Unable to calculate：{e}"


if __name__ == "__main__":
    # Run Server
    app.run()

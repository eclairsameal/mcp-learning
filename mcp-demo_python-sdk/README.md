# MCP DEMO (Python-sdk) 

[Huggingface MCP Course](https://huggingface.co/learn/mcp-course/unit1/key-concepts)

[Python-sdk](https://github.com/modelcontextprotocol/python-sdk)

[Ollama](https://ollama.com/)

## Installation

```
python3 -m venv mcp_env

source mcp_env/bin/activate

python -m pip install --upgrade pip

pip install "git+https://github.com/modelcontextprotocol/python-sdk.git"

pip install -r requirements.txt

```

You must install ollama and enable the local connection port.

```
>> ollama list

NAME                                       ID              SIZE      MODIFIED          
llama3.2:latest                            a80c4f17acd5    2.0 GB    4 months ago 

>> curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2:latest",
  "messages": [
    { "role": "user", "content": "What is 2+2?" }
  ],
  "stream": false
}'

{"model":"llama3.2:latest","created_at":"2025-11-18T06:40:37.446869Z","message":{"role":"assistant","content":"2 + 2 = 4."},"done":true,"done_reason":"stop","total_duration":4392920375,"load_duration":2960034209,"prompt_eval_count":32,"prompt_eval_duration":525777542,"eval_count":9,"eval_duration":904762166}%   
```

The mcp server is executed when the client is executed.

```
python [mcp client python script]
```

## File Description

* **mcp_server.py**

    MCP Server provides the following tools:

    1. Check the weather
    2. Calculate mathematical expressions

* **test_mcp_client.py**

    A simple test script for the MCP Server.

* **ollama_mcp_client.py**

    Let LLM organize the answers returned by the tool and send them back to the user.

* **ollama_mcp_client_regular.py**	

    Prompts use natural language parsing to determine which tools to use.

    Let LLM organize the answers returned by the tool and send them back to the user.

* **ollama_mcp_client_llm_ch.py**

    The prompts use LLM to determine which tools to use.
    
    Let LLM organize the answers returned by the tool and send them back to the user.
    
    For Chinese.

* **ollama_mcp_client_llm_en.py**

    For English.

## Results Explanation

### Prompt:

* The input format was intentionally made different for testing purposes.

* It is defined in the code.

```
 prompts = [
        "Please check the weather in Paris today.",
        "Please calculate the value of 3*7+10.",
        "What's the weather in Osaka?",
        "Calculate 15/3+4."
        ]
```

Run python script :

```
python mcp-demo_python-sdk/ollama_mcp_client_llm_en.py 
```

Results :  

💬 LLM Prompt: **Input Prompt.**

🛠 Tool Results: **The result returned by the tool.**

🤖 LLM Reply: **LLM uses the results returned by the tool to generate a response.**

```
💬 LLM Prompt: Please check the weather in Paris today.
Processing request of type CallToolRequest
Processing request of type ListToolsRequest
🛠 Tool Results: Paris: Overcast，temperature: 16°C
🤖 LLM Reply: Here's a complete answer based on the given information:

Current Weather Conditions in Paris:
- The current weather in Paris is overcast.
- The temperature is at 16°C.

Let me know if you'd like to add anything else!

💬 LLM Prompt: Please calculate the value of 3*7+10.
Processing request of type CallToolRequest
🛠 Tool Results: 3*7+10 = 31
🤖 LLM Reply: Here's the complete solution to the problem:

Problem: 3 * 7 + 10 = ?

Solution:
To solve this equation, we need to follow the order of operations (PEMDAS):
1. Multiply 3 and 7: 3 * 7 = 21
2. Add 10 to the result: 21 + 10 = 31

Therefore, the final answer is:

3 * 7 + 10 = 31

💬 LLM Prompt: What's the weather in Osaka?
Processing request of type CallToolRequest
🛠 Tool Results: Osaka: Overcast，temperature: 16°C
🤖 LLM Reply: Here is the organized information:

Weather in Osaka:
- Current weather condition: Overcast
- Temperature: 16°C

Let me know if you'd like to add anything else!

💬 LLM Prompt: Calculate 15/3+4.
Processing request of type CallToolRequest
🛠 Tool Results: 15/3+4 = 9.0
🤖 LLM Reply: Here's the completed answer:

15 / 3 + 4 = ?

First, divide 15 by 3: 15 ÷ 3 = 5

Next, add 4 to the result: 5 + 4 = 9

So, 15 / 3 + 4 = 9
```

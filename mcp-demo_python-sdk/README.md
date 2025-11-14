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
ollama list
NAME                                       ID              SIZE      MODIFIED          
llama3.2:latest                            a80c4f17acd5    2.0 GB    4 months ago     
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


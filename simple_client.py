import asyncio
import langchainhub as hub
from langchain.agents import create_agent, AgentExecutor
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_mcp_adapters.client import MultiServerMCPClient
from config import Config
base_llm = HuggingFaceEndpoint (
        repo_id=Config.MODEL_ID,
        max_new_tokens=Config.MAX_TOKENS,
        temperature=Config.TEMPERATURE,
        huggingfacehub_api_token=Config.HUGGINGFACE_TOKEN
    )
async def main():
    # 'async with' is REQUIRED to keep the stdio pipe open
    async with MultiServerMCPClient({
        "math_server": {
            "command": "python",
            "args": ["simple_server.py"],
            "transport": "stdio"
        }
    }) as client:
        
        # 1. Pull the MCP tools
        tools = await client.get_tools()
        print(tools)
        # 2. Setup LLM (Using a slightly larger model for better ReAct logic)
        
        llm = ChatHuggingFace(llm=base_llm)

        # 3. Use the standard ReAct prompt (it has the logic LLMs need for tools)
        prompt = hub.pull("hwchase17/react")

        # 4. Construct the classic Agent
        agent = create_agent(llm, tools, prompt)
        
        # 5. Create the Executor
        executor = AgentExecutor(
            agent=agent, 
            tools=tools, 
            verbose=True,
            handle_parsing_errors=True # Important for smaller models
        )

        # 6. Run it!
        response = await executor.ainvoke({"input": "What is 15 + 27?"})
        print(response["output"])

if __name__ == "__main__":
    asyncio.run(main())
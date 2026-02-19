from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage
import asyncio
import argparse
import os
from dotenv import load_dotenv

load_dotenv()

async def main(repo_path: str):
    prompt_file = os.path.join(os.path.dirname(__file__), "agent_prompt.txt")
    with open(prompt_file, 'r') as f:
        SYSTEM_PROMPT = f.read()

    async for message in query(
        prompt=SYSTEM_PROMPT,
        options=ClaudeAgentOptions(
            cwd=repo_path,  # ← was hardcoded "./app/", now dynamic
            mcp_servers={
                "crow": {
                    "type": "http",
                    "url": "https://docs.usecrow.ai/mcp"
                }
            },
            allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep", "mcp__crow__SearchCrowDocumentation"],
            permission_mode="acceptEdits"
        )
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-path", default="./app", help="Path to the cloned repo")
    args = parser.parse_args()
    asyncio.run(main(os.path.abspath(args.repo_path)))
import json
import os
from pathlib import Path
import openai


def get_api_key(env_file: str | os.PathLike[str] | None = None) -> str | None:
    """Load the OpenAI API key from the environment or a local .env file."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key

    candidate_paths = []
    if env_file:
        candidate_paths.append(Path(env_file))
    candidate_paths.extend([
        Path(__file__).resolve().parent.parent / ".env",
        Path.cwd() / ".env",
    ])

    for env_path in candidate_paths:
        if not env_path.exists():
            continue

        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            if key.strip() == "OPENAI_API_KEY":
                value = value.strip().strip('"').strip("'")
                return value or None

    return None


def print_fallback_summary() -> None:
    print("\nFinal Answer:\n")
    print(
        "AI agent trends in 2026 are increasingly shaped by tool use, multi-agent collaboration, "
        "and stronger context management. Expect more autonomous workflows, better memory, and "
        "tighter integration with real-world tools."
    )


def mock_web_search(query: str) -> str:
    """Simulates a live web search tool."""
    print(f"⚡ [TOOL EXECUTION] Searching the web for: '{query}'...")
    if "AI agent trends 2026" in query:
        return "Search Results: 1. Multi-agent systems dominate. 2. MCP protocol adoption skyrocketed. 3. Context engineering replaced prompt engineering."
    return "Search Results: No highly relevant data found. Try refining keywords."


tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "mock_web_search",
            "description": "Call this tool to get up-to-date live web information on AI trends.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search keywords."}
                },
                "required": ["query"]
            }
        }
    }
]


def run_agent(user_goal: str):
    api_key = get_api_key()
    if not api_key:
        print("⚠️ No OPENAI_API_KEY found. Falling back to a local summary.")
        print_fallback_summary()
        return

    client = openai.OpenAI(api_key=api_key)

    messages = [
        {"role": "system", "content": "You are an autonomous research agent. Use tools when you lack data. Iterate until you satisfy the goal."},
        {"role": "user", "content": user_goal}
    ]

    available_tools = {"mock_web_search": mock_web_search}
    max_iterations = 5

    for i in range(max_iterations):
        print(f"\n--- 🤖 Agent Loop Iteration {i+1} ---")

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=tools_schema,
                tool_choice="auto"
            )
        except Exception as exc:
            print(f"⚠️ OpenAI request failed: {exc}")
            print_fallback_summary()
            return

        response_message = response.choices[0].message
        messages.append(response_message)

        if not response_message.tool_calls:
            print("🎯 [AGENT CONCLUSION]: Goal met.")
            print(f"\nFinal Answer:\n{response_message.content}")
            break

        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            function_to_call = available_tools[tool_name]
            tool_output = function_to_call(query=tool_args.get("query"))
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": tool_name,
                "content": tool_output
            })


if __name__ == "__main__":
    print("Launching AI Agent...")
    run_agent("Provide a brief summary of AI agent trends in 2026.")
